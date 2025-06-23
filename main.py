#!/usr/bin/env python3
"""
Generate parser grammars, purposely corrupt them, and store everything
in a SQLite database for later analysis.  No localisation, no repair.
"""

import json
import random
from datetime import datetime
from sqlite3 import connect

from grammar_gen import gen, generate_example_string, generate_parser_code
from mutation import mutate_grammar
from testies import generate_biased_example_wrapper
from ultility import (
    compile_parser,
    validation_check_inproc,
    get_max_depth,
    get_path,
    grammar_printer,
)
import signal
import concurrent.futures
import argparse

# Helpers to parse comma-separated lists from command-line arguments
def _parse_int_list(s: str) -> list[int]:
    return [int(x) for x in s.split(',') if x]

def _parse_float_list(s: str) -> list[float]:
    return [float(x) for x in s.split(',') if x]


# Exception and handler for time-limiting generate_case
class CaseTimeout(Exception):
    """Raised when generate_case exceeds the time limit."""
    pass

def _timeout_handler(signum, frame):
    raise CaseTimeout

MAX_EXAMPLES = 100          # examples when building a fresh parser
MAX_MUTATE_ATTEMPTS = 100   # how many corruption attempts per case``
MAX_INSTANCE_SEARCH = 200   # attempts to find failing inputs
MIN_TEST_CASES = 1         # minimum failing instances per case
KEEP_TEST_CASES = 5        # number of test cases to keep in DB = 20
TIMEOUT = 80             # seconds to wait for a case to be generated
# Embedded benchmark parameters
dims = range(30, 101, 5)
nonterminal_probs = [0.5]
loop_probs = [0.5]
cases_per_setting = 2

# Default parameters for grammar generation
DEFAULT_MAX_PRODUCTIONS = 5  # default max number of productions per nonterminal
DEFAULT_MAX_RHS_LENGTH = 5   # default maximum right-hand side length of productions


db_file = "targets4.db"
# --------------------------------------------------------------------------- #
# Core workflow
# --------------------------------------------------------------------------- #

def generate_case(num_nonterminals: int,
                  max_productions: int,
                  max_rhs_length: int,
                  nonterminal_prob: float,
                  loop_prob: float) -> dict:
    """
    Generate one (original, corrupted) parser pair and collect failing inputs.

    Returns:
        dict containing all artefacts ready to be stored in SQLite.
    """
    # 1. create a valid grammar + parser
    # 1. create a valid grammar + parser with explicit parameter names
    original_code, _, grammar, nts, terms = gen(
        numnonterminals=num_nonterminals,
        maxproductions=max_productions,
        max_rhs_length=max_rhs_length,
        max_original_examples=MAX_EXAMPLES,
        recursion_prob=nonterminal_prob,
        loop_prob=loop_prob,
    )
    # 2. corrupt the grammar until we get at least MIN_TEST_CASES failing inputs
    instances = []
    start_nt = nts[0]
    orig_parse_fn = compile_parser(original_code)
    for _ in range(MAX_MUTATE_ATTEMPTS):
        corrupted_grammar, new_nts, new_terms, nt, prod_idx = mutate_grammar(
            grammar, nts, terms
        )
        # Skip mutations of the start symbol when possible to force deeper changes
        if len(nts) > 1 and nt == start_nt:
            continue
        corrupted_code = generate_parser_code(
            corrupted_grammar, new_nts, new_nts[0]
        )
        corr_parse_fn = compile_parser(corrupted_code)
        # search for failing strings
        for _ in range(MAX_INSTANCE_SEARCH):
            s = generate_biased_example_wrapper(
                grammar=grammar,
                symbol=new_nts[0],
                path=[(nt, prod_idx)],
                max_depth=get_max_depth(grammar, new_nts[0]) * 2,
            )
            # Only collect strings that the original parser accepts and the corrupted parser rejects
            if validation_check_inproc(s, orig_parse_fn) and not validation_check_inproc(s, corr_parse_fn):
                instances.append(s)
        if len(instances) >= MIN_TEST_CASES:
            break

    # ensure we have enough cases
    if len(instances) < MIN_TEST_CASES:
        raise RuntimeError(f"Could not find at least {MIN_TEST_CASES} failing instances, only found {len(instances)}")

    # compute mutation depth: distance from root to mutated nonterminal
    # get_path returns a list of (parent, production_index) steps; path length = number of edges
    # use 1-based depth: root itself -> depth=1, child -> depth=2, etc.
    path = get_path(grammar, nts[0], nt)
    if path is not None:
        # len(path) is number of edges from root to nt; add 1 for root depth
        mutation_depth = len(path) + 1
    else:
        # unreachable or same as root
        mutation_depth = None

    # prepare JSON-serialisable artefacts
    # Count unique symbols in the corrupted grammar (nonterminals + terminals)
    nonterms = set(corrupted_grammar.keys())
    terms = set()
    for prods in corrupted_grammar.values():
        for prod in prods:
            for sym in prod:
                if sym not in nonterms:
                    terms.add(sym)
    corrupted_symbol_count = len(nonterms) + len(terms)
    return {
        "nonterminal_prob": nonterminal_prob,
        "loop_prob": loop_prob,
        "mutation_depth": mutation_depth,
        # store compact JSON without extra indentation to reduce size
        "original_grammar": json.dumps(grammar, ensure_ascii=False),
        "original_parser": original_code,
        # store compact JSON without extra indentation to reduce size
        "corrupted_grammar": json.dumps(corrupted_grammar, ensure_ascii=False),
        "corrupted_parser": corrupted_code,
        "corrupted_symbol_count": corrupted_symbol_count,
        # keep only the first KEEP_TEST_CASES test cases in the database
        # keep test cases and store as compact JSON
        "test_cases": json.dumps(list(instances)[:KEEP_TEST_CASES], ensure_ascii=False),
    }

# --------------------------------------------------------------------------- #
# Parallel case generation helper
# --------------------------------------------------------------------------- #
def _generate_and_prepare_case(num_nonterminals, max_productions, max_rhs_length, nonterminal_prob, loop_prob):
    """Wrapper to generate a single case with retries and timeout."""
    while True:
        orig_handler = signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(TIMEOUT)
        try:
            artefacts = generate_case(
                num_nonterminals=num_nonterminals,
                max_productions=max_productions,
                max_rhs_length=max_rhs_length,
                nonterminal_prob=nonterminal_prob,
                loop_prob=loop_prob,
            )
            signal.alarm(0)
            break
        except CaseTimeout:
            print(f"[!] generate_case timed out after {TIMEOUT}s, regenerating grammar for "
                  f"num_nonterminals={num_nonterminals}, "
                  f"nonterminal_prob={nonterminal_prob}, loop_prob={loop_prob}")
        except RuntimeError as e:
            print(f"[!] {e}, regenerating grammar for "
                  f"num_nonterminals={num_nonterminals}, "
                  f"nonterminal_prob={nonterminal_prob}, loop_prob={loop_prob}")
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, orig_handler)

    # Record number of nonterminals for DB insertion
    artefacts['num_nonterminals'] = num_nonterminals
    artefacts['max_productions'] = max_productions
    artefacts['max_rhs_length'] = max_rhs_length
    artefacts['nonterminal_prob'] = nonterminal_prob
    artefacts['loop_prob'] = loop_prob
    artefacts['parser_size'] = len(artefacts.get('corrupted_parser', ''))
    return artefacts


# --------------------------------------------------------------------------- #
# SQLite helpers
# --------------------------------------------------------------------------- #

def init_db(cursor):
    """Create table if it does not already exist, with 'num_nonterminals' column."""
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_nonterminals INTEGER,
            nonterminal_prob REAL,
            loop_prob REAL,
            mutation_depth INTEGER,
            original_grammar TEXT,
            original_parser TEXT,
            corrupted_grammar TEXT,
            corrupted_parser TEXT,
            corrupted_symbol_count INTEGER,
            parser_size INTEGER,
            test_cases TEXT
        )
        """
    )
    # Migrate old schema: if 'dim' exists without 'num_nonterminals', add and populate it
    cols = [row[1] for row in cursor.execute("PRAGMA table_info(cases)")]
    if 'dim' in cols and 'num_nonterminals' not in cols:
        cursor.execute("ALTER TABLE cases ADD COLUMN num_nonterminals INTEGER")
        cursor.execute("UPDATE cases SET num_nonterminals = dim")
    if 'parser_size' not in cols:
        cursor.execute("ALTER TABLE cases ADD COLUMN parser_size INTEGER")
        cursor.execute("UPDATE cases SET parser_size = LENGTH(corrupted_parser)")
    if 'corrupted_symbol_count' not in cols:
        cursor.execute("ALTER TABLE cases ADD COLUMN corrupted_symbol_count INTEGER")

def save_case(cursor, artefacts: dict):
    """Insert one case into the database, with fallback for oversized fields."""
    # Prepare SQL and parameters
    # Insert one case into the database
    sql = (
        """
        INSERT INTO cases (
            num_nonterminals, nonterminal_prob, loop_prob, mutation_depth,
            original_grammar, original_parser,
            corrupted_grammar, corrupted_parser, corrupted_symbol_count, parser_size,
            test_cases
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
    )
    params = (
        artefacts.get("num_nonterminals"),
        artefacts.get("nonterminal_prob"),
        artefacts.get("loop_prob"),
        artefacts.get("mutation_depth"),
        artefacts.get("original_grammar"),
        artefacts.get("original_parser"),
        artefacts.get("corrupted_grammar"),
        artefacts.get("corrupted_parser"),
        artefacts.get("corrupted_symbol_count"),
        artefacts.get("parser_size"),
        artefacts.get("test_cases"),
    )
    try:
        cursor.execute(sql, params)
    except OverflowError as e:
        # Diagnostics: report sizes of string fields
        print("[!] OverflowError saving case: one of the fields is too large for SQLite (INT_MAX)")
        for name, value in artefacts.items():
            if isinstance(value, str):
                print(f"    {name}: {len(value)} characters")
        # Fallback: truncate oversized string fields to a safe limit
        max_len = 10**6  # 1MB per field
        truncated = {}
        for name, value in artefacts.items():
            if isinstance(value, str) and len(value) > max_len:
                truncated[name] = value[:max_len] + "... [TRUNCATED]"
            else:
                truncated[name] = value
        # Retry with truncated parameters
        params_trunc = (
            truncated.get("num_nonterminals"),
            truncated.get("nonterminal_prob"),
            truncated.get("loop_prob"),
            truncated.get("mutation_depth"),
            truncated.get("original_grammar"),
            truncated.get("original_parser"),
            truncated.get("corrupted_grammar"),
            truncated.get("corrupted_parser"),
            truncated.get("corrupted_symbol_count"),
            truncated.get("parser_size"),
            truncated.get("test_cases"),
        )
        print(f"[!] Retrying save_case with fields truncated to {max_len} chars each.")
        cursor.execute(sql, params_trunc)

# --------------------------------------------------------------------------- #
# CLI & main loop
# --------------------------------------------------------------------------- #
def main():
    # Allow overriding sweep settings and search bounds
    global dims, nonterminal_probs, loop_probs
    global MAX_EXAMPLES, MAX_MUTATE_ATTEMPTS, MAX_INSTANCE_SEARCH
    parser = argparse.ArgumentParser(description="Generate parser cases in parallel and store in SQLite DB")
    parser.add_argument('-w', '--workers', type=int, default=None,
                        help='Number of worker processes (default: cases per setting)')
    parser.add_argument('-c', '--cases-per-setting', type=int, default=cases_per_setting,
                        help=f'Number of cases to generate per setting (default: {cases_per_setting})')
    # Custom grammar parameters
    parser.add_argument('--num-nonterminals', type=int, default=None,
                        help='Number of nonterminals for grammar generation')
    parser.add_argument('--max-productions', type=int, default=None,
                        help='Maximum number of productions per nonterminal')
    parser.add_argument('--max-rhs-length', type=int, default=None,
                        help='Maximum right-hand side length for productions')
    parser.add_argument('--nonterminal-prob', type=float, default=None,
                        help='Probability of nonterminal recursion in grammar generation')
    parser.add_argument('--loop-prob', type=float, default=None,
                        help='Probability of looping in grammar generation')
    # Sweep parameter overrides: comma-separated lists
    parser.add_argument('--dims', type=_parse_int_list, default=None,
                        help=f'List of nonterminal counts to sweep (default: {dims})')
    parser.add_argument('--nonterminal-probs', type=_parse_float_list, default=None,
                        help=f'List of nonterminal recursion probs (default: {nonterminal_probs})')
    parser.add_argument('--loop-probs', type=_parse_float_list, default=None,
                        help=f'List of looping probs (default: {loop_probs})')
    # Search-bound overrides
    parser.add_argument('--max-examples', type=int, default=None,
                        help=f'Max examples when building a fresh parser (default: {MAX_EXAMPLES})')
    parser.add_argument('--max-mutate-attempts', type=int, default=None,
                        help=f'Max number of corruption attempts per case (default: {MAX_MUTATE_ATTEMPTS})')
    parser.add_argument('--max-instance-search', type=int, default=None,
                        help=f'Attempts to find failing inputs (default: {MAX_INSTANCE_SEARCH})')
    args = parser.parse_args()
    cps = args.cases_per_setting
    workers = args.workers if args.workers is not None else cps
    # Extract custom parameters
    num_nonterms = args.num_nonterminals
    max_prods = args.max_productions
    max_rhs = args.max_rhs_length
    nonterm_prob_arg = args.nonterminal_prob
    loop_prob_arg = args.loop_prob
    # Override global sweep parameters if supplied
    if args.dims is not None:
        dims = args.dims
    if args.nonterminal_probs is not None:
        nonterminal_probs = args.nonterminal_probs
    if args.loop_probs is not None:
        loop_probs = args.loop_probs
    # Override search bounds if supplied
    if args.max_examples is not None:
        MAX_EXAMPLES = args.max_examples
    if args.max_mutate_attempts is not None:
        MAX_MUTATE_ATTEMPTS = args.max_mutate_attempts
    if args.max_instance_search is not None:
        MAX_INSTANCE_SEARCH = args.max_instance_search

    conn = connect(db_file)
    cur = conn.cursor()
    init_db(cur)

    # Resume capability: only generate tasks not already in DB
    # Count existing cases grouped by grammar parameters
    cur.execute(
        "SELECT num_nonterminals, nonterminal_prob, loop_prob, COUNT(*) FROM cases "
        "GROUP BY num_nonterminals, nonterminal_prob, loop_prob"
    )
    existing = {(row[0], row[1], row[2]): row[3] for row in cur.fetchall()}

    # Build task list: either custom single setting or default parameter sweep
    tasks = []
    # Custom override mode: if any custom parameter is provided
    if any(param is not None for param in [num_nonterms, max_prods, max_rhs, nonterm_prob_arg, loop_prob_arg]):
        # Require all custom parameters
        if not all(param is not None for param in [num_nonterms, max_prods, max_rhs, nonterm_prob_arg, loop_prob_arg]):
            parser.error("When specifying custom parameters, all of "
                         "--num-nonterminals, --max-productions, "
                         "--max-rhs-length, --nonterminal-prob, and --loop-prob must be provided.")
        # Resume based on num_nonterminals and nonterminal/loop probs
        done = existing.get((num_nonterms, nonterm_prob_arg, loop_prob_arg), 0)
        remaining = max(cps - done, 0)
        for _ in range(remaining):
            tasks.append((num_nonterms, max_prods, max_rhs, nonterm_prob_arg, loop_prob_arg))
        total = len(tasks)
        if total == 0:
            print(f"[✓] All {cps} custom cases already generated in {db_file}. Nothing to do.")
            conn.close()
            return
        print(f"[+] Starting custom generation of {total} cases "
              f"(num_nonterminals={num_nonterms}, max_productions={max_prods}, "
              f"max_rhs_length={max_rhs}, nonterminal_prob={nonterm_prob_arg}, "
              f"loop_prob={loop_prob_arg}, cases_per_setting={cps}, workers={workers})")
    else:
        # Default parameter sweep
        for num_nt in dims:
            for nonterm_prob in nonterminal_probs:
                for lp in loop_probs:
                    done = existing.get((num_nt, nonterm_prob, lp), 0)
                    remaining = max(cps - done, 0)
                    for _ in range(remaining):
                        tasks.append((num_nt, DEFAULT_MAX_PRODUCTIONS, DEFAULT_MAX_RHS_LENGTH, nonterm_prob, lp))
        total = len(tasks)
        if total == 0:
            print(f"[✓] All {cps} cases per setting already generated in {db_file}. Nothing to do.")
            conn.close()
            return
        print(f"[+] Starting parallel generation of {total} cases "
              f"(dims={list(dims)}, nonterminal_probs={nonterminal_probs}, loop_probs={loop_probs}, "
              f"cases_per_setting={cps}, workers={workers})")

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        future_to_task = {
            executor.submit(_generate_and_prepare_case, *task): task
            for task in tasks
        }
        for idx, future in enumerate(concurrent.futures.as_completed(future_to_task), start=1):
            num_nonterms, max_prods, max_rhs, nonterm_prob, loop_prob = future_to_task[future]
            try:
                artefacts = future.result()
            except Exception as e:
                print(f"[!] Task #{idx}/{total} for num_nonterminals={num_nonterms}, "
                      f"max_productions={max_prods}, max_rhs_length={max_rhs}, "
                      f"nonterminal_prob={nonterm_prob}, loop_prob={loop_prob} "
                      f"generated exception: {e}")
                continue
            # Validate test cases: ensure original parser accepts and corrupted parser rejects
            cases = json.loads(artefacts['test_cases'])
            # Validate test cases in-memory with compiled parsers
            orig_fn = compile_parser(artefacts['original_parser'])
            corr_fn = compile_parser(artefacts['corrupted_parser'])
            valid_cases = [
                s for s in cases
                if validation_check_inproc(s, orig_fn) and not validation_check_inproc(s, corr_fn)
            ]
            if not valid_cases:
                print(f"[!] No valid test cases for "
                      f"num_nonterminals={num_nonterms}, max_productions={max_prods}, "
                      f"max_rhs_length={max_rhs}, nonterminal_prob={nonterm_prob}, "
                      f"loop_prob={loop_prob}, skipping save.")
                continue
            artefacts['test_cases'] = json.dumps(valid_cases, ensure_ascii=False)
            save_case(cur, artefacts)
            conn.commit()
            print(f"[+] Saved task #{idx}/{total} for num_nonterminals={num_nonterms}, "
                  f"max_productions={max_prods}, max_rhs_length={max_rhs}, "
                  f"nonterminal_prob={nonterm_prob}, loop_prob={loop_prob}")

    conn.close()
    print(f"[✓] Done. All cases stored in {db_file}")

if __name__ == "__main__":
    main()