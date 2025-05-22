#!/usr/bin/env python3
"""
merge_parser_cases.py

Merge multiple parser_cases*.db SQLite databases into a single database,
adding a column `cases` that records the number of test cases per entry.

Usage:
    python merge_parser_cases.py parser_cases4.db parser_cases5.db \
        parser_cases6.db parser_cases7.db parser_cases8.db
    # The merged output is written to parser_cases.db by default.
"""
import argparse
import json
import os
import sqlite3


def merge_dbs(input_dbs, output_db):
    # Remove existing output DB if present
    if os.path.exists(output_db):
        os.remove(output_db)
    conn_out = sqlite3.connect(output_db)
    cur_out = conn_out.cursor()
    # Create merged table with extra `cases` column
    cur_out.execute(
        '''
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
        '''
    )
    conn_out.commit()

    for db_path in input_dbs:
        conn_in = sqlite3.connect(db_path)
        cur_in = conn_in.cursor()
        for row in cur_in.execute(
            'SELECT dim, recursive_prob, loop_prob, '
            'original_grammar, original_parser, '
            'corrupted_grammar, corrupted_parser, test_cases '
            'FROM cases'
        ):
            dim, recp, loop, og, op, cg, cp, tc_json = row
            # Compute number of test cases
            try:
                cases_list = json.loads(tc_json)
                cases_count = len(cases_list)
            except Exception:
                cases_count = None
            # Insert into merged DB
            cur_out.execute(
                '''
                INSERT INTO cases (
                    dim, recursive_prob, loop_prob,
                    original_grammar, original_parser,
                    corrupted_grammar, corrupted_parser,
                    test_cases, cases
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (dim, recp, loop, og, op, cg, cp, tc_json, cases_count)
            )
        conn_out.commit()
        conn_in.close()

    conn_out.close()


def main():
    parser = argparse.ArgumentParser(
        description='Merge parser_cases databases and add a `cases` count column.'
    )
    parser.add_argument(
        'input_dbs', nargs='+',
        help='SQLite DB files to merge (e.g., parser_cases4.db parser_cases5.db ...)' 
    )
    parser.add_argument(
        '-o', '--output', default='parser_cases.db',
        help='Output SQLite DB file (default: parser_cases.db)'
    )
    args = parser.parse_args()
    merge_dbs(args.input_dbs, args.output)
    print(f"Merged {len(args.input_dbs)} databases into '{args.output}'.")


if __name__ == '__main__':
    main()