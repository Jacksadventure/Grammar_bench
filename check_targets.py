#!/usr/bin/env python3
"""
Script to verify that testcases in targets.db can be successfully parsed by the original parser.
If the parser code is not provided, it generates a parser from the original grammar.
Temporary parser files are named randomly to avoid conflicts.
Unparsable testcases are reported.
"""
import os
import sys
import sqlite3
import json
import subprocess
import tempfile

# Ensure grammar_gen module can be imported when script is run from its own directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
import grammar_gen

def generate_parser_code_from_grammar(grammar):
    nonterminals = list(grammar.keys())
    if not nonterminals:
        raise ValueError("Empty grammar")
    start_symbol = nonterminals[0]
    return grammar_gen.generate_parser_code(grammar, nonterminals, start_symbol)

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Check that testcases in targets.db are parseable by the original parser"
    )
    parser.add_argument(
        '--db', type=str, default='targets.db',
        help='Path to the targets.db SQLite database'
    )
    parser.add_argument(
        '--python', type=str, default=sys.executable,
        help='Python interpreter to execute parser scripts'
    )
    args = parser.parse_args()

    db_path = args.db
    if not os.path.isfile(db_path):
        print(f"Error: database file '{db_path}' not found", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, original_parser, original_grammar, test_cases FROM cases"
    )
    rows = cursor.fetchall()
    conn.close()

    any_failures = False

    for case_id, orig_parser, orig_grammar, test_cases_json in rows:
        # Load test cases array
        try:
            test_cases = json.loads(test_cases_json)
        except json.JSONDecodeError:
            try:
                test_cases = json.loads(test_cases_json.replace("'", '"'))
            except json.JSONDecodeError:
                print(f"Case {case_id}: invalid test_cases JSON, skipping", file=sys.stderr)
                continue

        # Determine parser code
        if orig_parser and orig_parser.strip():
            parser_code = orig_parser
        elif orig_grammar and orig_grammar.strip():
            try:
                grammar = json.loads(orig_grammar)
            except json.JSONDecodeError:
                print(f"Case {case_id}: invalid original_grammar JSON, skipping", file=sys.stderr)
                continue
            try:
                parser_code = generate_parser_code_from_grammar(grammar)
            except Exception as e:
                print(f"Case {case_id}: error generating parser from grammar: {e}", file=sys.stderr)
                continue
        else:
            print(f"Case {case_id}: no parser or grammar available, skipping", file=sys.stderr)
            continue

        # Write parser code to a temporary file with random name
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', suffix='.py', delete=False
        ) as tmpf:
            parser_filename = tmpf.name
            tmpf.write(parser_code)

        # Test each testcase
        failing = []
        for tc in test_cases:
            try:
                proc = subprocess.run(
                    [args.python, parser_filename, tc],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except Exception:
                failing.append(tc)
                continue
            if proc.returncode != 0:
                failing.append(tc)

        # Clean up temporary parser file
        try:
            os.remove(parser_filename)
        except OSError:
            pass

        # Report failures
        if failing:
            any_failures = True
            print(f"Case {case_id} failed parsing {len(failing)}/{len(test_cases)} testcases:")
            for tc in failing:
                print(tc)

    if not any_failures:
        print("All testcases parsed successfully.")

if __name__ == '__main__':
    main()