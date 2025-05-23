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
from ultility import validation_check, get_max_depth
import signal
import concurrent.futures
import argparse

# Exception and handler for time-limiting generate_case
class CaseTimeout(Exception):
    """Raised when generate_case exceeds the time limit."""
    pass

def _timeout_handler(signum, frame):
    raise CaseTimeout

MAX_EXAMPLES = 100          # examples when building a fresh parser
MAX_MUTATE_ATTEMPTS = 100   # how many corruption attempts per case``
MAX_INSTANCE_SEARCH = 200   # attempts to find failing inputs
MIN_TEST_CASES = 5         # minimum failing instances per case
KEEP_TEST_CASES = 5        # number of test cases to keep in DB = 20
TIMEOUT = 80             # seconds to wait for a case to be generated
# Embedded benchmark parameters
dims = range(1, 41)  
recursion_probs = [0.1, 0.2,0.3,0.4,0.5]
loop_probs = [0.1, 0.2,0.3,0.4,0.5]
cases_per_setting = 1


db_file = "parser_cases3.db"
# --------------------------------------------------------------------------- #
# Core workflow
# --------------------------------------------------------------------------- #

def generate_case(num_terminals: int,
                  num_nonterminals: int,
                  max_productions: int,
                  recursive_prob: float,
                  loop_prob: float) -> dict:
    """
    Generate one (original, corrupted) parser pair and collect failing inputs.

    Returns:
        dict containing all artefacts ready to be stored in SQLite.
    """
    # 1. create a valid grammar + parser
    # 1. create a valid grammar + parser with explicit parameter names
    original_code, _, grammar, nts, terms = gen(
        numterminals=num_terminals,
        numnonterminals=num_nonterminals,
        maxproductions=max_productions,
        max_original_examples=MAX_EXAMPLES,
        recursion_prob=recursive_prob,
        loop_prob=loop_prob,
    )
    # 2. corrupt the grammar until we get at least MIN_TEST_CASES failing inputs
    instances = []
    for _ in range(MAX_MUTATE_ATTEMPTS):
        corrupted_grammar, new_nts, new_terms, nt, prod_idx = mutate_grammar(
            grammar, nts, terms
        )
        corrupted_code = generate_parser_code(
            corrupted_grammar, new_nts, new_nts[0]
        )
        # search for failing strings
        for _ in range(MAX_INSTANCE_SEARCH):
            s = generate_biased_example_wrapper(
                grammar=grammar,
                symbol=new_nts[0],
                path=[(nt, prod_idx)],  # bias toward the mutated rule
                max_depth=get_max_depth(grammar, new_nts[0])*5,
            )
            if not validation_check(s, parser_code=corrupted_code):
                instances.append(s)

        if len(instances) >= MIN_TEST_CASES:
            break  # found enough failing instances

    # ensure we have enough cases
    if len(instances) < MIN_TEST_CASES:
        raise RuntimeError(f"Could not find at least {MIN_TEST_CASES} failing instances, only found {len(instances)}")

    # prepare JSON-serialisable artefacts
    return {
        "recursive_prob": recursive_prob,
        "loop_prob": loop_prob,
        # store compact JSON without extra indentation to reduce size
        "original_grammar": json.dumps(grammar, ensure_ascii=False),
        "original_parser": original_code,
        # store compact JSON without extra indentation to reduce size
        "corrupted_grammar": json.dumps(corrupted_grammar, ensure_ascii=False),
        "corrupted_parser": corrupted_code,
        # keep only the first KEEP_TEST_CASES test cases in the database
        # keep test cases and store as compact JSON
        "test_cases": json.dumps(list(instances)[:KEEP_TEST_CASES], ensure_ascii=False),
    }

# --------------------------------------------------------------------------- #
# Parallel case generation helper
# --------------------------------------------------------------------------- #
def _generate_and_prepare_case(dim, recursive_prob, loop_prob):
    """Wrapper to generate a single case with retries and timeout."""
    nt_count = dim
    nnt_count = dim
    max_prod = dim
    while True:
        orig_handler = signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(TIMEOUT)
        try:
            artefacts = generate_case(
                num_terminals=nt_count,
                num_nonterminals=nnt_count,
                max_productions=max_prod,
                recursive_prob=recursive_prob,
                loop_prob=loop_prob,
            )
            signal.alarm(0)
            break
        except CaseTimeout:
            print(f"[!] generate_case timed out after {TIMEOUT}s, regenerating grammar for dim={dim}, rec_prob={recursive_prob}, loop_prob={loop_prob}")
        except RuntimeError as e:
            print(f"[!] {e}, regenerating grammar for dim={dim}, rec_prob={recursive_prob}, loop_prob={loop_prob}")
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, orig_handler)
    artefacts['dim'] = dim
    artefacts['recursive_prob'] = recursive_prob
    artefacts['loop_prob'] = loop_prob
    return artefacts


# --------------------------------------------------------------------------- #
# SQLite helpers
# --------------------------------------------------------------------------- #

def init_db(cursor):
    """Create table if it does not already exist."""
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dim INTEGER,
            recursive_prob REAL,
            loop_prob REAL,
            original_grammar TEXT,
            original_parser TEXT,
            corrupted_grammar TEXT,
            corrupted_parser TEXT,
            test_cases TEXT
        )
        """
    )

def save_case(cursor, artefacts: dict):
    """Insert one case into the database, with fallback for oversized fields."""
    # Prepare SQL and parameters
    sql = (
        """
        INSERT INTO cases (
            dim, recursive_prob, loop_prob,
            original_grammar, original_parser,
            corrupted_grammar, corrupted_parser,
            test_cases
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
    )
    params = (
        artefacts.get("dim"),
        artefacts.get("recursive_prob"),
        artefacts.get("loop_prob"),
        artefacts.get("original_grammar"),
        artefacts.get("original_parser"),
        artefacts.get("corrupted_grammar"),
        artefacts.get("corrupted_parser"),
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
            truncated.get("dim"),
            truncated.get("recursive_prob"),
            truncated.get("loop_prob"),
            truncated.get("original_grammar"),
            truncated.get("original_parser"),
            truncated.get("corrupted_grammar"),
            truncated.get("corrupted_parser"),
            truncated.get("test_cases"),
        )
        print(f"[!] Retrying save_case with fields truncated to {max_len} chars each.")
        cursor.execute(sql, params_trunc)

# --------------------------------------------------------------------------- #
# CLI & main loop
# --------------------------------------------------------------------------- #
def main():
    parser = argparse.ArgumentParser(description="Generate parser cases in parallel and store in SQLite DB")
    parser.add_argument('-w', '--workers', type=int, default=None,
                        help='Number of worker processes (default: cases per setting)')
    parser.add_argument('-c', '--cases-per-setting', type=int, default=cases_per_setting,
                        help=f'Number of cases to generate per setting (default: {cases_per_setting})')
    args = parser.parse_args()
    cps = args.cases_per_setting
    workers = args.workers if args.workers is not None else cps

    conn = connect(db_file)
    cur = conn.cursor()
    init_db(cur)

    tasks = [(dim, rec_prob, loop_prob)
             for dim in dims
             for rec_prob in recursion_probs
             for loop_prob in loop_probs
             for _ in range(cps)]
    total = len(tasks)
    print(f"[+] Starting parallel generation of {total} cases "
          f"(dims={list(dims)}, rec_probs={recursion_probs}, loop_probs={loop_probs}, "
          f"cases_per_setting={cps}, workers={workers})")

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        future_to_task = {
            executor.submit(_generate_and_prepare_case, dim, rec_prob, loop_prob): (dim, rec_prob, loop_prob)
            for dim, rec_prob, loop_prob in tasks
        }
        for idx, future in enumerate(concurrent.futures.as_completed(future_to_task), start=1):
            dim, rec_prob, loop_prob = future_to_task[future]
            try:
                artefacts = future.result()
            except Exception as e:
                print(f"[!] Task #{idx}/{total} for dim={dim}, rec_prob={rec_prob}, loop_prob={loop_prob} "
                      f"generated exception: {e}")
                continue
            save_case(cur, artefacts)
            conn.commit()
            print(f"[+] Saved task #{idx}/{total} for dim={dim}, rec_prob={rec_prob}, loop_prob={loop_prob}")

    conn.close()
    print(f"[✓] Done. All cases stored in {db_file}")

if __name__ == "__main__":
    main()