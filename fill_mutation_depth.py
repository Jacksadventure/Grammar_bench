#!/usr/bin/env python3
"""
fill_mutation_depth.py

Fills the mutation_depth column in repair_results databases by copying values
from a source cases database.

Usage:
    fill_mutation_depth.py --source-db cases.db result1.db [result2.db ...]

Output:
    Prints progress and summary for each result database.
"""
import argparse
import sqlite3
import sys

def fill_from_source(source_db, result_db):
    """Update mutation_depth in result_db from source_db."""
    try:
        src_conn = sqlite3.connect(source_db)
        src_cur = src_conn.cursor()
    except sqlite3.Error as e:
        print(f"Error opening source DB '{source_db}': {e}", file=sys.stderr)
        return
    try:
        res_conn = sqlite3.connect(result_db)
        res_cur = res_conn.cursor()
    except sqlite3.Error as e:
        print(f"Error opening result DB '{result_db}': {e}", file=sys.stderr)
        src_conn.close()
        return

    # Check that mutation_depth column exists
    res_cur.execute("PRAGMA table_info(repair_results)")
    cols = [row[1] for row in res_cur.fetchall()]
    if 'mutation_depth' not in cols:
        print(f"Result DB '{result_db}' missing 'mutation_depth' column; skipping.", file=sys.stderr)
        res_conn.close()
        src_conn.close()
        return

    # Extract all case_ids from results
    res_cur.execute("SELECT case_id FROM repair_results")
    case_ids = [r[0] for r in res_cur.fetchall()]
    print(f"Updating {len(case_ids)} cases in '{result_db}'...")
    updated = 0
    for cid in case_ids:
        # Fetch mutation_depth from source cases table
        try:
            src_cur.execute("SELECT mutation_depth FROM cases WHERE id=?", (cid,))
            row = src_cur.fetchone()
        except sqlite3.Error as e:
            print(f"Error querying source DB for case_id={cid}: {e}", file=sys.stderr)
            continue
        if row is None:
            print(f"Source DB '{source_db}' has no entry for case_id={cid}", file=sys.stderr)
            continue
        md = row[0]
        # Update result
        try:
            res_cur.execute(
                "UPDATE repair_results SET mutation_depth=? WHERE case_id=?", (md, cid)
            )
            updated += 1
        except sqlite3.Error as e:
            print(f"Error updating result DB for case_id={cid}: {e}", file=sys.stderr)
    res_conn.commit()
    print(f"Completed '{result_db}': updated {updated}/{len(case_ids)} rows.")
    res_conn.close()
    src_conn.close()

def main():
    parser = argparse.ArgumentParser(
        description="Fill mutation_depth in repair_results DBs from source cases DB."
    )
    parser.add_argument(
        '--source-db', '-s', required=True,
        help='Path to source cases database containing mutation_depth in table cases.'
    )
    parser.add_argument(
        'result_dbs', nargs='+',
        help='Paths to repair_results databases to update.'
    )
    args = parser.parse_args()

    for rdb in args.result_dbs:
        fill_from_source(args.source_db, rdb)

if __name__ == '__main__':
    main()