#!/usr/bin/env python3
"""
Generate parser grammars, purposely corrupt them, and store everything
in a SQLite database for later analysis.  No localisation, no repair.
"""

import json
import random
from datetime import datetime
from sqlite3 import connect

from new_grammar_gen import generate_grammar, grammar_to_ebnf
from new_fuzzer import convert_ebnf
from new_codegen import read_grammar, generate_parser
from mutation import mutate_grammar
from testies import generate_biased_example_wrapper
from ultility import (
    compile_parser,
    validation_check_inproc,
    get_max_depth,
    get_path,
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
num_nonterminals = range(1,11)
dims = num_nonterminals
nonterminal_probs = [0.1]
loop_probs = [0.6]
cases_per_setting = 10

# Default parameters for grammar generation
DEFAULT_MAX_PRODUCTIONS = 5  # default max number of productions per nonterminal
DEFAULT_MAX_RHS_LENGTH = 5   # default maximum right-hand side length of productions


db_file = "targets7.db"
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
    # 1. generate random EBNF grammar and compile original parser
    ebnf_text = generate_grammar(num_nonterminals)
    grammar = convert_ebnf(ebnf_text)
    nts = list(grammar.keys())
    nonterms = set(nts)
    terms = [sym for prods in grammar.values() for prod in prods for sym in prod if sym not in nonterms]
    import tempfile
    tmp = tempfile.NamedTemporaryFile('w+', delete=False, suffix='.ebnf')
    tmp.write(ebnf_text); tmp.flush(); tmp.close()
    rules = read_grammar(tmp.name)
    original_code = generate_parser(rules)

    # 2. corrupt grammar until a failing example is found
    instances = []
    start_nt = nts[0]
    orig_parse_fn = compile_parser(original_code)
    for _ in range(MAX_MUTATE_ATTEMPTS):
        corrupted, new_nts, new_terms, nt, prod_idx = mutate_grammar(grammar, nts, terms)
        if len(nts) > 1 and nt == start_nt:
            continue
        corr_ebnf = grammar_to_ebnf(corrupted, new_nts)
        tmp2 = tempfile.NamedTemporaryFile('w+', delete=False, suffix='.ebnf')
        tmp2.write(corr_ebnf); tmp2.flush(); tmp2.close()
        corr_rules = read_grammar(tmp2.name)
        corrupted_code = generate_parser(corr_rules)
        corr_parse_fn = compile_parser(corrupted_code)
        for _ in range(MAX_INSTANCE_SEARCH):
            s = generate_biased_example_wrapper(
                grammar=grammar,
                symbol=new_nts[0],
                path=[(nt, prod_idx)],
                max_depth=get_max_depth(grammar, new_nts[0]) + 10,
            )
            if validation_check_inproc(s, orig_parse_fn) and not validation_check_inproc(s, corr_parse_fn):
                instances.append(s)
        if instances:
            break

    if not instances:
        raise RuntimeError(f"Could not find failing example; only found {len(instances)}")

    path0 = get_path(grammar, nts[0], nt)
    mutation_depth = (len(path0) + 1) if path0 is not None else None

    nonterms_c = set(corrupted.keys())
    terms_c = {sym for prods in corrupted.values() for prod in prods for sym in prod if sym not in nonterms_c}
    corrupted_symbol_count = len(nonterms_c) + len(terms_c)
    return {
        'nonterminal_prob': nonterminal_prob,
        'loop_prob': loop_prob,
        'mutation_depth': mutation_depth,
        'original_grammar': ebnf_text,
        'original_parser': original_code,
        'corrupted_grammar': grammar_to_ebnf(corrupted, new_nts),
        'corrupted_parser': corrupted_code,
        'corrupted_symbol_count': corrupted_symbol_count,
        'parser_size': len(corrupted_code),
        'test_cases': json.dumps(instances[:KEEP_TEST_CASES], ensure_ascii=False),
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
    parser.add_argument('--grammar-file', type=str, default=None,
                        help='Path to external grammar JSON file for mutation (bypass grammar generation)')
    # Custom grammar parameters
    parser.add_argument('--num-nonterminals', type=int, default=None,
                        help='Number of nonterminals for grammar generation')
    parser.add_argument('--max-productions', type=int, default=None,
                        help='Maximum number of productions per nonterminal')
    parser.add_argument('--max-rhs-length', type=int, default=None,
                        help='Maximum right-hand side length for productions')
    parser.add_argument('--nonterminal-prob', type=float, default=None,
                        help='Probability of nonterminal expansion in grammar generation (nonterminal-prob + loop-prob <1)')
    parser.add_argument('--loop-prob', type=float, default=None,
                        help='Probability of right-recursive looping in grammar generation (nonterminal-prob + loop-prob <1)')
    # Sweep parameter overrides: comma-separated lists
    parser.add_argument('--dims', nargs='?', const='', type=_parse_int_list, default=None,
                        help=f'List of nonterminal counts to sweep (default: {dims})')
    parser.add_argument('--nonterminal-probs', type=_parse_float_list, default=None,
                        help=f'List of nonterminal recursion probs; paired with --loop-probs by position (default: {nonterminal_probs})')
    parser.add_argument('--loop-probs', type=_parse_float_list, default=None,
                        help=f'List of looping probs; paired with --nonterminal-probs by position (default: {loop_probs})')
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
    # Handle case where only --num-nonterminals is supplied: treat as dims override
    if num_nonterms is not None and nonterm_prob_arg is None and loop_prob_arg is None and args.dims is None:
        dims = [num_nonterms]
        args.dims = dims
        num_nonterms = None
    # Override global sweep parameters if supplied
    auto_dims = False
    if args.dims is not None:
        if args.dims:
            dims = args.dims
        else:
            # flag provided without values: auto adjust defaults to follow nonterminal counts
            auto_dims = True
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

    # External grammar mutation mode: load and mutate a user-provided EBNF grammar
    if args.grammar_file:
        print(f"[+] Starting external grammar mutation for {args.grammar_file}, cases_per_setting={cps}")
        # load EBNF from file and compile original parser
        ebnf_text = open(args.grammar_file, encoding='utf-8').read()
        grammar = convert_ebnf(ebnf_text)
        nts = list(grammar.keys())
        terms = [sym for prods in grammar.values() for prod in prods for sym in prod if sym not in nts]
        rules = read_grammar(args.grammar_file)
        original_code = generate_parser(rules)
        orig_fn = compile_parser(original_code)
        # mutate and extract failing instances
        import tempfile
        for idx in range(1, cps + 1):
            instances = []
            for _ in range(MAX_MUTATE_ATTEMPTS):
                mutated, new_nts, new_terms, nt, prod_idx = mutate_grammar(grammar, nts, terms)
                if len(nts) > 1 and nt == nts[0]:
                    continue
                corr_ebnf = grammar_to_ebnf(mutated, new_nts)
                tmp2 = tempfile.NamedTemporaryFile('w+', delete=False, suffix='.ebnf')
                tmp2.write(corr_ebnf); tmp2.flush(); tmp2.close()
                corr_rules = read_grammar(tmp2.name)
                corrupted_code = generate_parser(corr_rules)
                corr_fn = compile_parser(corrupted_code)
                for _ in range(MAX_INSTANCE_SEARCH):
                    s = generate_biased_example_wrapper(
                        grammar=grammar,
                        symbol=new_nts[0],
                        path=[(nt, prod_idx)],
                        max_depth=get_max_depth(grammar, new_nts[0]) + 10,
                    )
                    if validation_check_inproc(s, orig_fn) and not validation_check_inproc(s, corr_fn):
                        instances.append(s)
                if instances:
                    break
            if not instances:
                print(f"[!] Could not find sufficient failing instances for case {idx}, skipping")
                continue
            path0 = get_path(grammar, nts[0], nt)
            mutation_depth = (len(path0) + 1) if path0 is not None else None
            nonterms_c = set(mutated.keys())
            terms_c = {sym for prods in mutated.values() for prod in prods for sym in prod if sym not in nonterms_c}
            corrupted_symbol_count = len(nonterms_c) + len(terms_c)
            artefacts = {
                'nonterminal_prob': None,
                'loop_prob': None,
                'mutation_depth': mutation_depth,
                'original_grammar': ebnf_text,
                'original_parser': original_code,
                'corrupted_grammar': grammar_to_ebnf(mutated, new_nts),
                'corrupted_parser': corrupted_code,
                'corrupted_symbol_count': corrupted_symbol_count,
                'test_cases': json.dumps(instances[:KEEP_TEST_CASES], ensure_ascii=False),
                'num_nonterminals': len(nts),
                'max_productions': None,
                'max_rhs_length': None,
                'parser_size': len(corrupted_code),
            }
            save_case(cur, artefacts)
            conn.commit()
            print(f"[+] Saved external case #{idx}/{cps}")
        conn.close()
        print(f"[✓] Done external grammar mutation. All cases stored in {db_file}")
        return

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
    # Custom override mode: if any core custom parameter is provided
    if any(param is not None for param in [num_nonterms, nonterm_prob_arg, loop_prob_arg]):
        # Require mandatory custom parameters: num-nonterminals, nonterminal-prob, loop-prob
        if num_nonterms is None or nonterm_prob_arg is None or loop_prob_arg is None:
            parser.error("When specifying custom parameters, "
                         "--num-nonterminals, --nonterminal-prob, and --loop-prob must be provided.")
        # Set max-productions and max-rhs-length to follow num-nonterminals if not explicitly provided
        if max_prods is None:
            max_prods = num_nonterms
        if max_rhs is None:
            max_rhs = num_nonterms
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
        # Default parameter sweep: paired nonterminal and loop probabilities (sum must be <1)
        for num_nt in dims:
            for nonterm_prob, lp in zip(nonterminal_probs, loop_probs):
                if nonterm_prob + lp >= 1:
                    continue
                done = existing.get((num_nt, nonterm_prob, lp), 0)
                remaining = max(cps - done, 0)
                for _ in range(remaining):
                    if auto_dims:
                        max_prod = num_nt
                        max_rhs_len = num_nt
                    else:
                        max_prod = DEFAULT_MAX_PRODUCTIONS
                        max_rhs_len = DEFAULT_MAX_RHS_LENGTH
                    tasks.append((num_nt, max_prod, max_rhs_len, nonterm_prob, lp))
        total = len(tasks)
        if total == 0:
            print(f"[✓] All {cps} cases per setting already generated in {db_file}. Nothing to do.")
            conn.close()
            return
        print(f"[+] Starting parallel generation of {total} cases "
              f"(dims={list(dims)}, paired (nonterminal_prob, loop_prob) sum<1, "
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
