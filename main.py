#!/usr/bin/env python3
"""
Generate parser grammars, purposely corrupt them, and store everything
in a SQLite database for later analysis.  No localisation, no repair.
"""

import argparse
import json
import os
import random
import uuid
from datetime import datetime
from sqlite3 import connect

from grammar_gen import gen, generate_example_string, generate_parser_code
from mutation import mutate_grammar
from testies import generate_biased_example_wrapper
from ultility import validation_check, grammar_printer

MAX_EXAMPLES = 100          # examples when building a fresh parser
MAX_MUTATE_ATTEMPTS = 100   # how many corruption attempts per case
MAX_INSTANCE_SEARCH = 200   # attempts to find failing inputs

# --------------------------------------------------------------------------- #
# Core workflow
# --------------------------------------------------------------------------- #

def generate_case(dim: int,
                  recursive_prob: float,
                  loop_prob: float) -> dict:
    """
    Generate one (original, corrupted) parser pair and collect failing inputs.

    Returns:
        dict containing all artefacts ready to be stored in SQLite.
    """
    # 1. create a valid grammar + parser
    original_code, _, grammar, nts, terms = gen(
        dim, dim, dim, MAX_EXAMPLES, recursive_prob, loop_prob
    )

    # 2. corrupt the grammar until we get at least two failing inputs
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

        if len(instances) >= 20:
            break  # success

    if not instances:
        raise RuntimeError("Could not find any failing instances")

    # prepare JSON-serialisable artefacts
    return {
        "dim": dim,
        "recursive_prob": recursive_prob,
        "loop_prob": loop_prob,
        "original_grammar": json.dumps(grammar, ensure_ascii=False, indent=2),
        "original_parser": original_code,
        "corrupted_grammar": json.dumps(corrupted_grammar, ensure_ascii=False, indent=2),
        "corrupted_parser": corrupted_code,
        "test_cases": json.dumps(list(instances), ensure_ascii=False, indent=2),
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
    p = argparse.ArgumentParser(description="Generate corrupted parser cases.")
    p.add_argument("--cases", type=int, default=10,
                   help="Number of cases to generate **per dimension**")

    grp = p.add_mutually_exclusive_group(required=False)
    grp.add_argument("--dim", type=int,
                     help="Generate only this dimension (old behaviour)")
    grp.add_argument("--dim_range", nargs=2, type=int, metavar=("MIN", "MAX"),
                     help="Generate every dimension in [MIN, MAX] (inclusive)")

    p.add_argument("--recursive_prob", type=float, default=0.5)
    p.add_argument("--loop_prob", type=float, default=0.5)
    p.add_argument("--db", type=str, default="parser_cases.db",
                   help="SQLite file name")
    args = p.parse_args()

    # build the list of dimensions to iterate over
    if args.dim_range:
        d_min, d_max = args.dim_range
        if d_min <= 0 or d_max < d_min:
            p.error("Invalid --dim_range (must satisfy 0 < MIN ≤ MAX)")
        dims = list(range(d_min, d_max + 1))
    else:
        dims = [args.dim or 5]       # default fixed dimension 5

    conn = connect(args.db)
    cur = conn.cursor()
    init_db(cur)

    for dim in dims:
        for i in range(args.cases):
            print(f"[+] Generating dim={dim}  case #{i+1}/{args.cases}")
            artefacts = generate_case(
                dim=dim,
                recursive_prob=args.recursive_prob,
                loop_prob=args.loop_prob,
            )
            save_case(cur, artefacts)
            conn.commit()

    conn.close()
    print(f"[✓] Done. All cases stored in {args.db}")

if __name__ == "__main__":
    main()