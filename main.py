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
from radon.complexity import cc_visit, cc_rank

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


def calculate_parser_cc(code_string: str) -> tuple[int|None, str|None]:
    """
    Compute cyclomatic complexity and rank for the parser function.
    1. Try to find a block named 'parse' or 'parse_input'.
    2. Else try any block whose name starts with 'parse_'.
    3. Else pick the block with highest complexity.
    Returns (complexity, rank) or (None, None) on error.
    """
    if not code_string:
        return None, None

    try:
        blocks = cc_visit(code_string)
        if not blocks:
            return None, None

        # 1. exact matches
        for blk in blocks:
            if blk.name == 'parse':
                return blk.complexity, cc_rank(blk.complexity)

        # 2. prefix matches
        for blk in blocks:
            if blk.name.startswith('parse_'):
                return blk.complexity, cc_rank(blk.complexity)

        # 3. fallback: pick the block with highest complexity
        top = max(blocks, key=lambda b: b.complexity)
        return top.complexity, cc_rank(top.complexity)

    except Exception:
        return None, None


class Config:
    """Configuration settings for the script."""
    MAX_EXAMPLES = 100
    MAX_MUTATE_ATTEMPTS = 100
    MAX_INSTANCE_SEARCH = 200
    MIN_TEST_CASES = 1
    KEEP_TEST_CASES = 5
    TIMEOUT = 80
    DB_FILE = "targets9.db"
    
    # Benchmark parameters
    NUM_NONTERMINALS = range(1, 11)
    DIMS = NUM_NONTERMINALS
    NONTERMINAL_PROB = 0.5
    LOOP_PROB = 0.5
    CASES_PER_SETTING = 20

    # Default grammar generation parameters
    DEFAULT_MAX_PRODUCTIONS = 3
    DEFAULT_MAX_RHS_LENGTH = 3

    def __init__(self, args=None):
        if args:
            self.update_from_args(args)

    def update_from_args(self, args):
        """Update configuration from command-line arguments."""
        if args.max_examples is not None:
            self.MAX_EXAMPLES = args.max_examples
        if args.max_mutate_attempts is not None:
            self.MAX_MUTATE_ATTEMPTS = args.max_mutate_attempts
        if args.max_instance_search is not None:
            self.MAX_INSTANCE_SEARCH = args.max_instance_search
        if args.cases_per_setting is not None:
            self.CASES_PER_SETTING = args.cases_per_setting
        
        self.DIMS = self.NUM_NONTERMINALS
        if args.dim is not None:
            if args.dim:
                self.DIMS = args.dim
        
        if args.nonterminal_prob is not None:
            self.NONTERMINAL_PROB = args.nonterminal_prob
        if args.loop_prob is not None:
            self.LOOP_PROB = args.loop_prob
# --------------------------------------------------------------------------- #
# Core workflow
# --------------------------------------------------------------------------- #

def generate_case(num_nonterminals: int,
                  max_productions: int,
                  max_rhs_length: int,
                  nonterminal_prob: float,
                  loop_prob: float,
                  config: Config) -> dict:
    """
    Generate one (original, corrupted) parser pair and collect failing inputs.

    Returns:
        dict containing all artefacts ready to be stored in SQLite.
    """
    # 1. create a valid grammar + parser with explicit parameter names
    original_code, _, grammar, nts, terms = gen(
        num_nonterminals=num_nonterminals,
        max_productions=max_productions,
        max_rhs_length=max_rhs_length,
        max_original_examples=config.MAX_EXAMPLES,
        nonterminal_prob=nonterminal_prob,
        loop_prob=loop_prob,
    )
    # 2. corrupt the grammar and find failing inputs
    corrupted_grammar, corrupted_code, instances, nt = find_failing_mutant(
        grammar, nts, terms, original_code, config
    )
    if not instances:
        raise RuntimeError(f"Could not find at least {config.MIN_TEST_CASES} failing instances")

    # calculate cyclomatic complexity
    cc_complexity, cc_rank = calculate_parser_cc(corrupted_code)

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
        # keep only the first config.KEEP_TEST_CASES test cases in the database
        # keep test cases and store as compact JSON
        "test_cases": json.dumps(list(instances)[:config.KEEP_TEST_CASES], ensure_ascii=False),
        "cc_complexity": cc_complexity,
        "cc_rank": cc_rank,
    }

# --------------------------------------------------------------------------- #
# Parallel case generation helper
# --------------------------------------------------------------------------- #
def _generate_and_prepare_case(num_nonterminals, max_productions, max_rhs_length, nonterminal_prob, loop_prob, config):
    """Wrapper to generate a single case with retries and timeout."""
    while True:
        orig_handler = signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(config.TIMEOUT)
        try:
            artefacts = generate_case(
                num_nonterminals=num_nonterminals,
                max_productions=max_productions,
                max_rhs_length=max_rhs_length,
                nonterminal_prob=nonterminal_prob,
                loop_prob=loop_prob,
                config=config,
            )
            signal.alarm(0)
            break
        except CaseTimeout:
            print(f"[!] generate_case timed out after {config.TIMEOUT}s, regenerating grammar for "
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
# SQLite Database Manager
# --------------------------------------------------------------------------- #

class DatabaseManager:
    """Handles all database interactions."""
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = connect(self.db_file)
        self.cur = self.conn.cursor()
        self._init_db()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def _init_db(self):
        """Create table if it does not already exist, with 'num_nonterminals' column."""
        self.cur.execute(
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
                test_cases TEXT,
                cc_complexity INTEGER,
                cc_rank TEXT
            )
            """
        )
        cols = [row[1] for row in self.cur.execute("PRAGMA table_info(cases)")]
        if 'dim' in cols and 'num_nonterminals' not in cols:
            self.cur.execute("ALTER TABLE cases ADD COLUMN num_nonterminals INTEGER")
            self.cur.execute("UPDATE cases SET num_nonterminals = dim")
        if 'parser_size' not in cols:
            self.cur.execute("ALTER TABLE cases ADD COLUMN parser_size INTEGER")
            self.cur.execute("UPDATE cases SET parser_size = LENGTH(corrupted_parser)")
        if 'corrupted_symbol_count' not in cols:
            self.cur.execute("ALTER TABLE cases ADD COLUMN corrupted_symbol_count INTEGER")
        if 'cc_complexity' not in cols:
            self.cur.execute("ALTER TABLE cases ADD COLUMN cc_complexity INTEGER")
        if 'cc_rank' not in cols:
            self.cur.execute("ALTER TABLE cases ADD COLUMN cc_rank TEXT")

    def save_case(self, artefacts: dict):
        """Insert one case into the database, with fallback for oversized fields."""
        sql = (
            """
            INSERT INTO cases (
                num_nonterminals, nonterminal_prob, loop_prob, mutation_depth,
                original_grammar, original_parser,
                corrupted_grammar, corrupted_parser, corrupted_symbol_count, parser_size,
                test_cases, cc_complexity, cc_rank
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            artefacts.get("cc_complexity"),
            artefacts.get("cc_rank"),
        )
        try:
            self.cur.execute(sql, params)
        except OverflowError:
            print("[!] OverflowError saving case: one of the fields is too large for SQLite (INT_MAX)")
            for name, value in artefacts.items():
                if isinstance(value, str):
                    print(f"    {name}: {len(value)} characters")
            max_len = 10**6
            truncated = {
                name: (value[:max_len] + "... [TRUNCATED]") if isinstance(value, str) and len(value) > max_len else value
                for name, value in artefacts.items()
            }
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
                truncated.get("cc_complexity"),
                truncated.get("cc_rank"),
            )
            print(f"[!] Retrying save_case with fields truncated to {max_len} chars each.")
            self.cur.execute(sql, params_trunc)
        self.conn.commit()

    def get_existing_cases(self):
        """Count existing cases grouped by grammar parameters."""
        self.cur.execute(
            "SELECT num_nonterminals, nonterminal_prob, loop_prob, COUNT(*) FROM cases "
            "GROUP BY num_nonterminals, nonterminal_prob, loop_prob"
        )
        return {(row[0], row[1], row[2]): row[3] for row in self.cur.fetchall()}

# --------------------------------------------------------------------------- #
# CLI & main loop
# --------------------------------------------------------------------------- #
def setup_parser(config):
    """Configure and return the argument parser."""
    parser = argparse.ArgumentParser(description="Generate parser cases in parallel and store in SQLite DB")
    parser.add_argument('-w', '--workers', type=int, default=None,
                        help='Number of worker processes (default: cases per setting)')
    parser.add_argument('-c', '--cases-per-setting', type=int, default=config.CASES_PER_SETTING,
                        help=f'Number of cases to generate per setting (default: {config.CASES_PER_SETTING})')
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
    parser.add_argument('--dim', nargs='?', const='', type=_parse_int_list, default=None,
                        help=f'List of nonterminal counts to sweep (default: {config.DIMS})')
    # Search-bound overrides
    parser.add_argument('--max-examples', type=int, default=None,
                        help=f'Max examples when building a fresh parser (default: {config.MAX_EXAMPLES})')
    parser.add_argument('--max-mutate-attempts', type=int, default=None,
                        help=f'Max number of corruption attempts per case (default: {config.MAX_MUTATE_ATTEMPTS})')
    parser.add_argument('--max-instance-search', type=int, default=None,
                        help=f'Attempts to find failing inputs (default: {config.MAX_INSTANCE_SEARCH})')
    return parser


def find_failing_mutant(grammar, nts, terms, original_code, config):
    """
    Mutate a grammar and search for failing test cases.

    Returns:
        A tuple of (corrupted_grammar, corrupted_code, instances, mutated_nonterminal).
        Returns (None, None, [], None) if no failing mutant is found.
    """
    start_nt = nts[0]
    orig_parse_fn = compile_parser(original_code)
    for _ in range(config.MAX_MUTATE_ATTEMPTS):
        corrupted_grammar, new_nts, new_terms, nt, prod_idx = mutate_grammar(
            grammar, nts, terms
        )
        if len(nts) > 1 and nt == start_nt:
            continue
        corrupted_code = generate_parser_code(
            corrupted_grammar, new_nts, new_nts[0]
        )
        try:
            corr_parse_fn = compile_parser(corrupted_code)
        except Exception:
            continue
        instances = []
        for _ in range(config.MAX_INSTANCE_SEARCH):
            s = generate_biased_example_wrapper(
                grammar=grammar,
                symbol=new_nts[0],
                path=[(nt, prod_idx)],
                max_depth=get_max_depth(grammar, new_nts[0]) + 10,
            )
            if validation_check_inproc(s, orig_parse_fn) and not validation_check_inproc(s, corr_parse_fn):
                instances.append(s)
        if len(instances) >= config.MIN_TEST_CASES:
            return corrupted_grammar, corrupted_code, instances, nt
    return None, None, [], None


def run_external_grammar_mutation(args, db_manager, config):
    """Mutate a user-provided grammar from an external file."""
    print(f"[+] Starting external grammar mutation for {args.grammar_file}, cases_per_setting={config.CASES_PER_SETTING}")
    with open(args.grammar_file, encoding='utf-8') as gf:
        ext_grammar = json.load(gf)
    nonterms = list(ext_grammar.keys())
    terms = set()
    for prods in ext_grammar.values():
        for prod in prods:
            for sym in prod:
                if sym not in nonterms:
                    terms.add(sym)
    terms = list(terms)
    original_code = generate_parser_code(ext_grammar, nonterms, nonterms[0])

    for idx in range(1, config.CASES_PER_SETTING + 1):
        mutated_grammar, corrupted_code, instances, nt = find_failing_mutant(
            ext_grammar, nonterms, terms, original_code, config
        )
        if not instances:
            print(f"[!] Could not find sufficient failing instances for case {idx}, skipping")
            continue

        path = get_path(ext_grammar, nonterms[0], nt)
        mutation_depth = len(path) + 1 if path is not None else None
        nonterm_set = set(mutated_grammar.keys())
        term_set = set()
        for prods in mutated_grammar.values():
            for prod in prods:
                for sym in prod:
                    if sym not in nonterm_set:
                        term_set.add(sym)
        corrupted_symbol_count = len(nonterm_set) + len(term_set)

        cc_complexity, cc_rank = calculate_parser_cc(corrupted_code)
        artefacts = {
            "nonterminal_prob": None,
            "loop_prob": None,
            "mutation_depth": mutation_depth,
            "original_grammar": json.dumps(ext_grammar, ensure_ascii=False),
            "original_parser": original_code,
            "corrupted_grammar": json.dumps(mutated_grammar, ensure_ascii=False),
            "corrupted_parser": corrupted_code,
            "corrupted_symbol_count": corrupted_symbol_count,
            "test_cases": json.dumps(instances[:config.KEEP_TEST_CASES], ensure_ascii=False),
            "cc_complexity": cc_complexity,
            "cc_rank": cc_rank,
        }
        artefacts["num_nonterminals"] = len(nonterms)
        artefacts["max_productions"] = None
        artefacts["max_rhs_length"] = None
        artefacts["parser_size"] = len(corrupted_code)
        db_manager.save_case(artefacts)
        print(f"[+] Saved external case #{idx}/{config.CASES_PER_SETTING}")
    print(f"[✓] Done external grammar mutation. All cases stored in {config.DB_FILE}")


def run_generation_sweep(args, db_manager, config):
    """Generate new grammars based on sweep parameters and save them."""
    workers = args.workers if args.workers is not None else config.CASES_PER_SETTING
    num_nonterms = args.num_nonterminals
    max_prods = args.max_productions
    max_rhs = args.max_rhs_length
    nonterm_prob_arg = args.nonterminal_prob
    loop_prob_arg = args.loop_prob

    if num_nonterms is not None and nonterm_prob_arg is None and loop_prob_arg is None and args.dim is None:
        config.DIMS = [num_nonterms]
        num_nonterms = None

    auto_dims = False
    if args.dim is not None:
        if args.dim:
            config.DIMS = args.dim
        else:
            auto_dims = True

    existing = db_manager.get_existing_cases()
    tasks = []

    if any(param is not None for param in [num_nonterms, nonterm_prob_arg, loop_prob_arg]):
        if num_nonterms is None or nonterm_prob_arg is None or loop_prob_arg is None:
            # This should be handled by the parser setup, but as a safeguard:
            raise ValueError("Custom generation requires --num-nonterminals, --nonterminal-prob, and --loop-prob.")
        
        if max_prods is None: max_prods = num_nonterms
        if max_rhs is None: max_rhs = num_nonterms
        
        done = existing.get((num_nonterms, nonterm_prob_arg, loop_prob_arg), 0)
        remaining = max(config.CASES_PER_SETTING - done, 0)
        for _ in range(remaining):
            tasks.append((num_nonterms, max_prods, max_rhs, nonterm_prob_arg, loop_prob_arg, config))
        total = len(tasks)
        if total == 0:
            print(f"[✓] All {config.CASES_PER_SETTING} custom cases already generated. Nothing to do.")
            return
        print(f"[+] Starting custom generation of {total} cases...")
    else:
        for num_nt in config.DIMS:
            done = existing.get((num_nt, config.NONTERMINAL_PROB, config.LOOP_PROB), 0)
            remaining = max(config.CASES_PER_SETTING - done, 0)
            for _ in range(remaining):
                max_prod = num_nt if auto_dims else config.DEFAULT_MAX_PRODUCTIONS
                max_rhs_len = num_nt if auto_dims else config.DEFAULT_MAX_RHS_LENGTH
                tasks.append((num_nt, max_prod, max_rhs_len, config.NONTERMINAL_PROB, config.LOOP_PROB, config))
        total = len(tasks)
        if total == 0:
            print(f"[✓] All cases per setting already generated. Nothing to do.")
            return
        print(f"[+] Starting parallel generation of {total} cases...")

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        future_to_task = {
            executor.submit(_generate_and_prepare_case, *task): task for task in tasks
        }
        for idx, future in enumerate(concurrent.futures.as_completed(future_to_task), start=1):
            num_nonterms, max_prods, max_rhs, nonterm_prob, loop_prob, _ = future_to_task[future]
            try:
                artefacts = future.result()
            except Exception as e:
                print(f"[!] Task #{idx}/{total} for num_nonterminals={num_nonterms}, "
                      f"max_productions={max_prods}, max_rhs_length={max_rhs}, "
                      f"nonterminal_prob={nonterm_prob}, loop_prob={loop_prob} "
                      f"generated exception: {e}")
                continue
            
            cases = json.loads(artefacts['test_cases'])
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
            db_manager.save_case(artefacts)
            print(f"[+] Saved task #{idx}/{total} for num_nonterminals={num_nonterms}, "
                  f"max_productions={max_prods}, max_rhs_length={max_rhs}, "
                  f"nonterminal_prob={nonterm_prob}, loop_prob={loop_prob}")

    print(f"[✓] Done. All cases stored in {config.DB_FILE}")


def main():
    """Main entry point for the script."""
    config = Config()
    parser = setup_parser(config)
    args = parser.parse_args()
    config.update_from_args(args)

    with DatabaseManager(config.DB_FILE) as db_manager:
        if args.grammar_file:
            run_external_grammar_mutation(args, db_manager, config)
        else:
            run_generation_sweep(args, db_manager, config)

if __name__ == "__main__":
    main()
