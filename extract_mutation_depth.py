#!/usr/bin/env python3
"""
extract_mutation_depth.py

Extracts the mutation_depth values from the repair_results table in one or more
SQLite databases and outputs them as CSV to stdout.

Usage:
    extract_mutation_depth.py path/to/db1.db path/to/db2.db ... > mutation_depths.csv

Output Columns:
    db_file, case_id, mutation_depth
"""
import argparse
import sqlite3
import csv
import sys

def extract_from_db(db_path, writer):
    """Extracts case_id and mutation_depth from the given SQLite DB and writes to CSV writer."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT case_id, mutation_depth FROM repair_results")
    except sqlite3.Error as e:
        sys.stderr.write(f"Error accessing database '{db_path}': {e}\n")
        return
    rows = cursor.fetchall()
    for case_id, mutation_depth in rows:
        writer.writerow([db_path, case_id, mutation_depth])
    conn.close()

def main():
    parser = argparse.ArgumentParser(
        description='Extract mutation_depth from repair_results tables.')
    parser.add_argument(
        'db_paths', nargs='+', help='Paths to SQLite databases')
    args = parser.parse_args()

    csv_writer = csv.writer(sys.stdout)
    # write header
    csv_writer.writerow(['db_file', 'case_id', 'mutation_depth'])
    for db_path in args.db_paths:
        extract_from_db(db_path, csv_writer)

if __name__ == '__main__':
    main()