import argparse
import json
from grammar_gen import gen,generate_example_string, generate_parser_code
# from repair import repair  # deprecated import removed to avoid unused dependency errors
from ultility import levenshtein_distance,validation_check,get_path
from localisation import localise_program_input,localise_program
import sqlite3
import subprocess
import random
import os
import uuid
from mutation import mutate_grammar
from file_diff import get_diff_function
from testies import generate_biased_example_wrapper
from time import sleep
from file_diff import diff

MAX_TESTS = 1
MAX_EXAMPLES = 100
MAX_MUTATE_ATTEMPTS = 100

def program_reapir(backend, model, db_path='parser_cases.db', results_db='repair_results.db'):
    """
    Read parser cases from a SQLite database and perform localization for each case.
    """
    # generate a unique run identifier to avoid filename collisions
    run_id = uuid.uuid4().hex
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, num_nonterminals, nonterminal_prob, loop_prob, mutation_depth, original_grammar, original_parser,"
        " corrupted_grammar, corrupted_parser, test_cases"
        " FROM cases"
    )
    rows = cursor.fetchall()

    # Prepare results database
    results_conn = sqlite3.connect(results_db)
    results_cursor = results_conn.cursor()
    results_cursor.execute('''
        CREATE TABLE IF NOT EXISTS repair_results (
            case_id INTEGER PRIMARY KEY,
            num_nonterminals INTEGER,
            nonterminal_prob REAL,
            loop_prob REAL,
            total_tests INTEGER,
            passed_tests INTEGER,
            fix INTEGER
        )
    ''')
    results_conn.commit()
    # Check for previously processed cases to allow resuming
    results_cursor.execute("SELECT case_id FROM repair_results")
    processed_cases = {r[0] for r in results_cursor.fetchall()}
    for row in rows:
        # Unpack query results including mutation_depth
        case_id, num_nonterminals, nonterminal_prob, loop_prob, mutation_depth, orig_grammar, orig_parser, corr_grammar, corr_parser, test_cases_json = row
        # Skip cases already recorded in results DB
        if case_id in processed_cases:
            print(f"Skipping case {case_id}: already processed")
            continue
        print(f"========Case {case_id}========")
        print(f"num_nonterminals: {dim}, nonterminal_prob: {nonterminal_prob}, loop_prob: {loop_prob}, mutation_depth: {mutation_depth}")

        # Load test cases
        try:
            test_cases = json.loads(test_cases_json)
        except json.JSONDecodeError:
            test_cases = json.loads(test_cases_json.replace("'", '"'))
        total_tests = len(test_cases)
        print(f"Total test cases: {total_tests}")
        # # devide test cases into two parts
        # trigger_inputs = test_cases[:total_tests//2]
        # validation_test_cases = test_cases[total_tests//2:]

        response = localise_program(corr_parser, orig_grammar, backend, model)
        print("Localization response:")
        print(response)
        # The response is a unified diff patch; apply it to the corrupted parser
        patch_text = response
        corrupted_file = f"case_{case_id}_corrupted_{run_id}.py"
        with open(corrupted_file, 'w', encoding='utf-8') as f:
            f.write(corr_parser)
        patch_file = f"case_{case_id}_patch_{run_id}.diff"
        with open(patch_file, 'w', encoding='utf-8') as f:
            f.write(patch_text)
        repaired_file = f"case_{case_id}_repaired_{run_id}.py"
        try:
            subprocess.run(
                ['patch', corrupted_file, patch_file, '-o', repaired_file],
                check=True
            )
        except Exception as e:
            print(f"Repair failed for case {case_id}: {e}")
            passed_tests = 0
            fix = 0
            results_cursor.execute(
                'INSERT OR REPLACE INTO repair_results(case_id, num_nonterminals, nonterminal_prob, loop_prob, total_tests, passed_tests, fix) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (case_id, num_nonterminals, nonterminal_prob, loop_prob, total_tests, passed_tests, fix)
            )
            results_conn.commit()
            continue

        # Run all test cases on repaired parser, record 0 passed if program fails to run
        passed_tests = 0
        try:
            for test_input in test_cases:
                proc = subprocess.run(
                    ['python3', repaired_file, test_input],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                if proc.returncode == 0:
                    passed_tests += 1
                else:
                    print(f"Test failed on input: {test_input}, return code: {proc.returncode}")
        except Exception as e:
            print(f"Error running repaired program for case {case_id}: {e}")
            passed_tests = 0

        print(f"Case {case_id}: {passed_tests}/{total_tests} tests passed after repair.")
        fix = 1 if passed_tests == total_tests else 0
        results_cursor.execute(
            'INSERT OR REPLACE INTO repair_results(case_id, num_nonterminals, nonterminal_prob, loop_prob, total_tests, passed_tests, fix) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (case_id, num_nonterminals, nonterminal_prob, loop_prob, total_tests, passed_tests, fix)
        )
        results_conn.commit()
        # Delete repaired parser file for this case
        try:
            os.remove(repaired_file)
        except OSError:
            pass

def main():
    parser = argparse.ArgumentParser(description='Sample Parser')
    # parser.add_argument('--mode', type=str, default='input_repair', help='mode: input_repair or program_repair')
    parser.add_argument('--backend', type=str, default='openai', help='backend: openai / ollama / Claude')
    parser.add_argument('--model', type=str, default='o1-mini-2024-09-12', help='model: model name')
    parser.add_argument('--db-path', type=str, default='parser_cases.db', help='Path to the parser_cases SQLite database')
    parser.add_argument('--results-db', type=str, default='repair_results.db', help='Path to output results SQLite database')
    args = parser.parse_args()
    # if args.mode == 'input_repair':
    #     program_input_reapir(args.backend,args.model)
    # elif args.mode == 'program_repair':
    #     program_reapir(args.backend,args.model)
    # else:
    #     print("Invalid mode")
    # Determine results database name; include source DB, backend, and model to enable resuming
    default_arg = 'repair_results.db'
    if args.results_db == default_arg:
        src_base = os.path.splitext(os.path.basename(args.db_path))[0]
        results_db_name = f"repair_results_{args.backend}_{args.model}_{src_base}.db"
    else:
        results_db_name = args.results_db
    print(f"Using results database: {results_db_name}")
    program_reapir(args.backend, args.model, args.db_path, results_db_name)
    # Clean up repaired files after run
    for fname in os.listdir('.'):
        if fname.startswith('case_') and '_repaired_' in fname:
            try:
                os.remove(fname)
            except OSError:
                pass
            
if __name__ == "__main__":
    main()