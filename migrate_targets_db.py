#!/usr/bin/env python3
"""
Migration script to add and populate mutation_depth in cases tables of target databases.
Usage:
  ./migrate_targets_db.py [db1.db db2.db ...]
If no databases are provided, it will auto-detect targets: 'targets.db' and '*_targets.db'.
"""
import os
import sys
import glob
import sqlite3
import json
from ultility import get_path

def migrate(db_file):
    print(f"Migrating {db_file}...")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    # Detect tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cases';")
    has_cases = cur.fetchone() is not None
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='repair_results';")
    has_results = cur.fetchone() is not None
    # Migrate cases table
    if has_cases:
        print(f"  Migrating 'cases' table in {db_file}")
        # Ensure mutation_depth column exists
        cols = [row[1] for row in cur.execute("PRAGMA table_info(cases)")]
        if 'mutation_depth' not in cols:
            cur.execute("ALTER TABLE cases ADD COLUMN mutation_depth INTEGER")
        # Compute and update depths (1-based BFS distance; 0 if no mutation detected)
        cur.execute("SELECT id, original_grammar, corrupted_grammar FROM cases")
        rows = cur.fetchall()
        for case_id, orig_json, corr_json in rows:
            # Default depth 0: no mutation or unrecognized mutation point
            depth = 0
            try:
                grammar = json.loads(orig_json)
                corr_grammar = json.loads(corr_json)
                # Identify mutated nonterminal by comparing grammar productions
                mutated_nt = None
                for nt, prods in grammar.items():
                    if corr_grammar.get(nt) != prods:
                        mutated_nt = nt
                        break
                if mutated_nt is not None:
                    # Compute BFS path from start nonterminal to mutated nonterminal
                    start_nt = next(iter(grammar))
                    path = get_path(grammar, start_nt, mutated_nt)
                    if path is not None:
                        # Use 1-based depth: root mutation -> depth=1, next-level->2, etc.
                        depth = len(path) + 1
            except Exception as e:
                print(f"    [!] Error in case {case_id}: {e}")
            cur.execute(
                "UPDATE cases SET mutation_depth = ? WHERE id = ?",
                (depth, case_id)
            )
        conn.commit()
        print(f"  Completed cases migration for {db_file}")
    # Migrate repair_results table
    if has_results:
        print(f"  Migrating 'repair_results' table in {db_file}")
        # Add mutation_depth column if missing
        cols = [row[1] for row in cur.execute("PRAGMA table_info(repair_results)")]
        if 'mutation_depth' not in cols:
            cur.execute("ALTER TABLE repair_results ADD COLUMN mutation_depth INTEGER")
        # Determine source DB name from file name
        base = os.path.splitext(os.path.basename(db_file))[0]
        parts = base.split('_')
        src_base = parts[-1]
        # Identify source cases DB by src_base.db (current dir or same directory as this file)
        candidate = src_base + '.db'
        if not os.path.exists(candidate):
            alt = os.path.join(os.path.dirname(db_file), candidate)
            if os.path.exists(alt):
                candidate = alt
        src_db = candidate
        if os.path.exists(src_db):
            # Attach source cases DB
            cur.execute(f"ATTACH DATABASE '{src_db}' AS cases_db")
            # Update mutation_depth by joining to cases table
            cur.execute(
                "UPDATE repair_results SET mutation_depth = ("
                "SELECT mutation_depth FROM cases_db.cases WHERE cases_db.cases.id = repair_results.case_id)"
            )
            # Commit the update before detaching to ensure no open transaction locks
            conn.commit()
            # Detach the attached database now that update is complete
            cur.execute("DETACH DATABASE cases_db")
            # Final commit to persist detach and any pending changes
            conn.commit()
            print(f"  Populated mutation_depth in repair_results from {src_db}")
        else:
            print(f"  Source DB not found for repair_results: expected {candidate}, skipping depth update.")
    if not has_cases and not has_results:
        print(f"  No 'cases' or 'repair_results' table in {db_file}, skipping migration.")
    conn.close()
    print(f"Completed migrating {db_file}\n")

def main():
    if len(sys.argv) > 1:
        db_files = sys.argv[1:]
    else:
        db_files = glob.glob("*_targets.db")
        if os.path.exists("targets.db") and "targets.db" not in db_files:
            db_files.append("targets.db")
    if not db_files:
        print("No target databases found for migration.")
        return
    for db in db_files:
        if os.path.exists(db):
            migrate(db)
        else:
            print(f"Database not found: {db}")

if __name__ == '__main__':
    main()