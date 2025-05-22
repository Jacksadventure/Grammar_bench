#!/usr/bin/env python3
"""
Extract a limited number of test case records per unique (dim, loop_prob, recursive_prob) triple
from parser_cases.db and save into lite.db.
"""
import sqlite3
import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--db-path', default='parser_cases.db',
        help='Path to input SQLite DB file (default: parser_cases.db)'
    )
    parser.add_argument(
        '--output-db', default='lite.db',
        help='Path to output SQLite DB file (default: lite.db)'
    )
    parser.add_argument(
        '--num', type=int, default=2,
        help='Number of records per (dim, loop_prob, recursive_prob) group to keep (default: 2)'
    )
    args = parser.parse_args()

    if not os.path.exists(args.db_path):
        print(f"Error: input DB '{args.db_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    if os.path.exists(args.output_db):
        os.remove(args.output_db)

    conn_in = sqlite3.connect(args.db_path)
    cur_in = conn_in.cursor()

    # fetch unique (dim, loop_prob, recursive_prob) groups in sorted order
    cur_in.execute(
        "SELECT DISTINCT dim, loop_prob, recursive_prob FROM cases"
        " ORDER BY dim, recursive_prob, loop_prob"
    )
    groups = cur_in.fetchall()

    conn_out = sqlite3.connect(args.output_db)
    cur_out = conn_out.cursor()
    cur_out.execute(
        """
        CREATE TABLE cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dim INTEGER,
            recursive_prob REAL,
            loop_prob REAL,
            original_grammar TEXT,
            original_parser TEXT,
            corrupted_grammar TEXT,
            corrupted_parser TEXT,
            test_cases TEXT,
            cases INTEGER
        )
        """
    )
    conn_out.commit()

    total_inserted = 0
    for dim, lp, rp in groups:
        cur_in.execute(
            """
            SELECT dim, recursive_prob, loop_prob,
                   original_grammar, original_parser,
                   corrupted_grammar, corrupted_parser,
                   test_cases, cases
            FROM cases
            WHERE dim = ? AND loop_prob = ? AND recursive_prob = ?
            ORDER BY id
            LIMIT ?
            """,
            (dim, lp, rp, args.num)
        )
        rows = cur_in.fetchall()
        for row in rows:
            cur_out.execute(
                """
                INSERT INTO cases (
                    dim, recursive_prob, loop_prob,
                    original_grammar, original_parser,
                    corrupted_grammar, corrupted_parser,
                    test_cases, cases
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                row
            )
            total_inserted += 1
    conn_out.commit()
    conn_in.close()
    conn_out.close()

    print(
        f"Created '{args.output_db}' with {total_inserted} records "
        f"({args.num} per {len(groups)} groups)."
    )

if __name__ == '__main__':
    main()