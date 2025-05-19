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
from ultility import validation_check

MAX_EXAMPLES = 100          # examples when building a fresh parser
MAX_MUTATE_ATTEMPTS = 100   # how many corruption attempts per case
MAX_INSTANCE_SEARCH = 200   # attempts to find failing inputs
MIN_TEST_CASES = 20         # minimum failing instances per case
KEEP_TEST_CASES = 20        # number of test cases to keep in DB

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
    instances = set()
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
                max_depth=20,
            )
            if not validation_check(s, parser_code=corrupted_code):
                instances.add(s)

        if len(instances) >= MIN_TEST_CASES:
            break  # found enough failing instances

    # ensure we have enough cases
    if len(instances) < MIN_TEST_CASES:
        raise RuntimeError(f"Could not find at least {MIN_TEST_CASES} failing instances, only found {len(instances)}")

    # prepare JSON-serialisable artefacts
    return {
        "recursive_prob": recursive_prob,
        "loop_prob": loop_prob,
        "original_grammar": json.dumps(grammar, ensure_ascii=False, indent=2),
        "original_parser": original_code,
        "corrupted_grammar": json.dumps(corrupted_grammar, ensure_ascii=False, indent=2),
        "corrupted_parser": corrupted_code,
        # keep only the first KEEP_TEST_CASES test cases in the database
        "test_cases": json.dumps(list(instances)[:KEEP_TEST_CASES], ensure_ascii=False, indent=2),
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }


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
            test_cases TEXT,
            timestamp TEXT
        )
        """
    )

def save_case(cursor, artefacts: dict):
    """Insert one case into the database."""
    cursor.execute(
        """
        INSERT INTO cases (
            dim, recursive_prob, loop_prob,
            original_grammar, original_parser,
            corrupted_grammar, corrupted_parser,
            test_cases, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            artefacts["dim"],
            artefacts["recursive_prob"],
            artefacts["loop_prob"],
            artefacts["original_grammar"],
            artefacts["original_parser"],
            artefacts["corrupted_grammar"],
            artefacts["corrupted_parser"],
            artefacts["test_cases"],
            artefacts["timestamp"],
        ),
    )

# --------------------------------------------------------------------------- #
# CLI & main loop
# --------------------------------------------------------------------------- #
def main():
    # Embedded benchmark parameters
    dims = range(10, 21)  # dimensions from 10 to 20 inclusive
    recursion_probs = [0.2, 0.4, 0.6]
    loop_probs = [0.2, 0.4, 0.6]
    cases_per_setting = 3
    db_file = "parser_cases2.db"

    conn = connect(db_file)
    cur = conn.cursor()
    init_db(cur)

    for dim in dims:
        for recursion_prob in recursion_probs:
            for loop_prob in loop_probs:
                for i in range(cases_per_setting):
                    nt_count = dim
                    nnt_count = dim
                    max_prod = dim
                    print(
                        f"[+] Generating grammar(nt={nt_count}, nnt={nnt_count}, prod={max_prod}, "
                        f"rec_prob={recursion_prob}, loop_prob={loop_prob}) "
                        f"case #{i+1}/{cases_per_setting}"
                    )
                    # attempt to generate a valid corrupted parser with sufficient failing cases
                    while True:
                        try:
                            artefacts = generate_case(
                                num_terminals=nt_count,
                                num_nonterminals=nnt_count,
                                max_productions=max_prod,
                                recursive_prob=recursion_prob,
                                loop_prob=loop_prob,
                            )
                            break
                        except RuntimeError as e:
                            print(f"[!] {e}, regenerating grammar")
                    # record parameters used for this case
                    artefacts['dim'] = dim
                    artefacts['recursive_prob'] = recursion_prob
                    artefacts['loop_prob'] = loop_prob
                    save_case(cur, artefacts)
                    conn.commit()

    conn.close()
    print(f"[✓] Done. All cases stored in {args.db}")

if __name__ == "__main__":
    main()