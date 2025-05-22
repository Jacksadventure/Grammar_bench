#!/usr/bin/env python3
"""
Filter test cases in parser_cases.db to ensure they are accepted
by the original parser and rejected by the corrupted parser.
Usage:
    python filter_parser_cases.py [--db-path parser_cases.db]
"""
import argparse
import sqlite3
import json
import subprocess
import tempfile
import os
import sys


def run_parser(parser_path: str, sample: str) -> bool:
    """Return True if `python parser_path` reading sample from stdin exits with code 0."""
    # Feed sample via stdin to avoid argument-length limits
    proc = subprocess.run(
        [sys.executable, parser_path],
        input=sample,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc.returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Filter parser_cases.db test cases"
    )
    parser.add_argument(
        "--db-path", default="parser_cases.db",
        help="Path to the parser_cases SQLite database"
    )
    parser.add_argument(
        "--output-db", default=None,
        help="If set, write filtered cases to this new DB instead of modifying in-place"
    )
    args = parser.parse_args()

    db_path = args.db_path
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' not found.", file=sys.stderr)
        sys.exit(1)

    conn_in = sqlite3.connect(db_path)
    cur_in = conn_in.cursor()
    # ensure the DB has the expected 'cases' table
    cur_in.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='cases';"
    )
    if not cur_in.fetchone():
        cur_in.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [r[0] for r in cur_in.fetchall()]
        print(
            f"Error: database '{db_path}' does not contain table 'cases'.\n"
            f"Available tables: {', '.join(tables)}",
            file=sys.stderr
        )
        sys.exit(1)

    out_db = args.output_db
    # If output DB specified, write filtered rows to new DB
    if out_db:
        if os.path.exists(out_db):
            os.remove(out_db)
        conn_out = sqlite3.connect(out_db)
        cur_out = conn_out.cursor()
        # Create output table (same schema)
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

        rows = cur_in.execute(
            '''
            SELECT id, dim, recursive_prob, loop_prob,
                   original_grammar, original_parser,
                   corrupted_grammar, corrupted_parser, test_cases
            FROM cases
            '''
        ).fetchall()
        total_rows = len(rows)
        inserted = 0
        dropped = 0
        with tempfile.TemporaryDirectory() as tmpdir:
            for db_id, dim, recp, loopp, og, op, cg, cp, tc_json in rows:
                try:
                    test_cases = json.loads(tc_json)
                except json.JSONDecodeError:
                    continue
                # write parsers
                orig_file = os.path.join(tmpdir, f"orig_{db_id}.py")
                corr_file = os.path.join(tmpdir, f"corr_{db_id}.py")
                with open(orig_file, 'w') as f:
                    f.write(op)
                with open(corr_file, 'w') as f:
                    f.write(cp)
                # filter cases
                new_cases = []
                for sample in test_cases:
                    if run_parser(orig_file, sample) and not run_parser(corr_file, sample):
                        new_cases.append(sample)
                if new_cases:
                    cur_out.execute(
                        '''
                        INSERT INTO cases (
                          id, dim, recursive_prob, loop_prob,
                          original_grammar, original_parser,
                          corrupted_grammar, corrupted_parser,
                          test_cases, cases
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''',
                        (db_id, dim, recp, loopp,
                         og, op, cg, cp,
                         json.dumps(new_cases), len(new_cases))
                    )
                    inserted += 1
                else:
                    dropped += 1
        conn_out.commit()
        conn_out.close()
        conn_in.close()
        print(f"Processed {total_rows} rows; inserted {inserted}; dropped {dropped} into '{out_db}'.")
        sys.exit(0)

    # In-place update (default if no --output-db)
    conn = conn_in
    cur = cur_in
    rows = cur.execute(
        "SELECT id, original_parser, corrupted_parser, test_cases FROM cases"
    ).fetchall()
    total_rows = len(rows)
    total_filtered = 0
    total_dropped = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        for db_id, op, cp, tc_json in rows:
            try:
                test_cases = json.loads(tc_json)
            except json.JSONDecodeError:
                continue
            orig_file = os.path.join(tmpdir, f"orig_{db_id}.py")
            corr_file = os.path.join(tmpdir, f"corr_{db_id}.py")
            with open(orig_file, 'w') as f:
                f.write(op)
            with open(corr_file, 'w') as f:
                f.write(cp)
            new_cases = []
            for sample in test_cases:
                if run_parser(orig_file, sample) and not run_parser(corr_file, sample):
                    new_cases.append(sample)
            if new_cases:
                if len(new_cases) != len(test_cases):
                    removed = len(test_cases) - len(new_cases)
                    print(f"[id {db_id}] removed {removed} / {len(test_cases)} cases")
                    cur.execute(
                        "UPDATE cases SET test_cases = ?, cases = ? WHERE id = ?",
                        (json.dumps(new_cases), len(new_cases), db_id)
                    )
                    total_filtered += 1
            else:
                print(f"[id {db_id}] dropped (0 remaining cases)")
                cur.execute("DELETE FROM cases WHERE id = ?", (db_id,))
                total_dropped += 1
    conn.commit()
    conn.close()
    print(
        f"Processed {total_rows} rows; "
        f"updated {total_filtered} rows; "
        f"dropped {total_dropped} rows."
    )


if __name__ == '__main__':
    main()