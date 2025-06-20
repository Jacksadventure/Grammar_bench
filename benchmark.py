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
import shutil
import uuid
from mutation import mutate_grammar
from file_diff import get_diff_function
from testies import generate_biased_example_wrapper
from time import sleep
from file_diff import diff

MAX_TESTS = 1
MAX_EXAMPLES = 100
MAX_MUTATE_ATTEMPTS = 100

import concurrent.futures
import multiprocessing

def _repair_single_case(row, backend, model, results_db, run_id):
    (case_id, num_nonterminals, nonterminal_prob, loop_prob, mutation_depth,
     orig_grammar, orig_parser, corr_grammar, corr_parser, test_cases_json) = row
    # per-case DB connection for writing results
    conn = sqlite3.connect(results_db, timeout=30)
    cursor = conn.cursor()
    print(f"[Case {case_id}] ===== Case start: nonterminals={num_nonterminals}, prob={nonterminal_prob}, loop={loop_prob}, depth={mutation_depth} =====")
    # load test cases
    try:
        test_cases = json.loads(test_cases_json)
    except json.JSONDecodeError:
        test_cases = json.loads(test_cases_json.replace("'", '"'))
    total_tests = len(test_cases)
    print(f"[Case {case_id}] Total tests: {total_tests}")
    # write corrupted parser to file and collect failing test examples
    corrupted_file = f"case_{case_id}_corrupted_{run_id}.py"
    with open(corrupted_file, 'w', encoding='utf-8') as f:
        f.write(corr_parser)
    error_examples = []
    for inp in test_cases:
        proc = subprocess.run(['python3', corrupted_file, inp], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            error_examples.append(inp)
    # deduplicate preserving order
    error_examples = list(dict.fromkeys(error_examples))
    print(f"[Case {case_id}] Collected {len(error_examples)} unique error examples")
    # generate patch via localization using failing examples
    response = localise_program(corr_parser, error_examples, backend, model)
    print(f"[Case {case_id}] Localization response:\n{response.response_text}")
    patch_text = response.response_text
    prompt_tokens = response.prompt_tokens
    completion_tokens = response.completion_tokens
    total_tokens = response.total_tokens
    patch_file = f"case_{case_id}_patch_{run_id}.diff"
    with open(patch_file, 'w', encoding='utf-8') as f:
        f.write(patch_text)
    repaired_file = f"case_{case_id}_repaired_{run_id}.py"
    shutil.copy(corrupted_file, repaired_file)
    # apply patch quietly
    try:
        subprocess.run(
            ['patch', '-t', '-s', repaired_file, '-i', patch_file], check=True
        )
    except Exception as e:
        # first: naive line-level replacement
        try:
            diff_lines = patch_text.splitlines()
            removals = [l[1:] for l in diff_lines if l.startswith('-') and not l.startswith('---')]
            additions = [l[1:] for l in diff_lines if l.startswith('+') and not l.startswith('+++')]
            if len(removals) != len(additions):
                raise ValueError("Mismatched removal/addition lines")
            with open(repaired_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for old, new in zip(removals, additions):
                replaced = False
                for idx, ln in enumerate(lines):
                    if ln.rstrip('\n') == old:
                        lines[idx] = new + '\n'
                        replaced = True
                        break
                if not replaced:
                    raise ValueError(f"Line to replace not found: {old}")
            with open(repaired_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        except Exception:
            # fallback: AST per-function aggregated hunks
            try:
                from patch import replace_function_ast_in_file
                func_hunks = {}
                for ln in patch_text.splitlines():
                    if ln.startswith('@@'):
                        parts = ln.split('@@')
                        sig = parts[-1].strip()
                        fname = sig.split()[1].split('(')[0]
                        func_hunks.setdefault(fname, {'sig': sig, 'lines': []})
                    elif ln.startswith('+') and not ln.startswith('+++'):
                        func_hunks[fname]['lines'].append(ln[1:])
                if not func_hunks:
                    raise ValueError("No function signature in diff")
                for fname, info in func_hunks.items():
                    code = info['sig'] + '\n' + '\n'.join(info['lines'])
                    replace_function_ast_in_file(repaired_file, code, fname, repaired_file)
            except Exception:
                print(f"[Case {case_id}] Repair failed: {e}")
                passed_tests = 0
                fix = 0
                cursor.execute(
                    'REPLACE INTO repair_results(case_id,puzzle_id,num_nonterminals,nonterminal_prob,loop_prob,total_tests,passed_tests,fix,prompt_tokens,completion_tokens,total_tokens) VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                    (case_id, case_id, num_nonterminals, nonterminal_prob, loop_prob, total_tests, passed_tests, fix, prompt_tokens, completion_tokens, total_tokens)
                )
                conn.commit()
                conn.close()
                return
    # run tests
    passed_tests = 0
    for inp in test_cases:
        proc = subprocess.run(['python3', repaired_file, inp], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode == 0:
            passed_tests += 1
        else:
            print(f"[Case {case_id}] Test failed on input={inp}, rc={proc.returncode}")
    print(f"[Case {case_id}] Result: {passed_tests}/{total_tests}")
    fix = 1 if passed_tests == total_tests else 0
    # write result
    cursor.execute(
        'REPLACE INTO repair_results(case_id,puzzle_id,num_nonterminals,nonterminal_prob,loop_prob,total_tests,passed_tests,fix,prompt_tokens,completion_tokens,total_tokens) VALUES(?,?,?,?,?,?,?,?,?,?,?)',
        (case_id, case_id, num_nonterminals, nonterminal_prob, loop_prob, total_tests, passed_tests, fix, prompt_tokens, completion_tokens, total_tokens)
    )
    conn.commit()
    conn.close()
    # cleanup
    try:
        os.remove(repaired_file)
    except OSError:
        pass

def program_reapir(backend, model, db_path='parser_cases.db', results_db='repair_results.db', workers=1):
    """
    Read parser cases from a SQLite database and perform localization for each case.
    Supports parallel execution with `workers` processes.
    """
    # generate a unique run identifier to avoid filename collisions
    run_id = uuid.uuid4().hex
    # read source cases
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
            puzzle_id INTEGER,
            num_nonterminals INTEGER,
            nonterminal_prob REAL,
            loop_prob REAL,
            total_tests INTEGER,
            passed_tests INTEGER,
            fix INTEGER,
            prompt_tokens INTEGER,
            completion_tokens INTEGER,
            total_tokens INTEGER
        )
    ''')
    results_conn.commit()
    # Determine cases to (re)process
    results_cursor.execute("SELECT case_id FROM repair_results")
    processed_cases = {r[0] for r in results_cursor.fetchall()}
    to_run = [row for row in rows if row[0] not in processed_cases]
    print(f"[Main] {len(to_run)} cases to process using {workers} worker(s)")
    # dispatch either sequentially or in parallel
    if workers > 1:
        ctx = multiprocessing.get_context("spawn")
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as executor:
            futures = {executor.submit(_repair_single_case, row, backend, model, results_db, run_id): row[0] for row in to_run}
            for fut in concurrent.futures.as_completed(futures):
                cid = futures[fut]
                try:
                    fut.result()
                except Exception as e:
                    print(f"[Case {cid}] Worker exception: {e}")
    else:
        for row in to_run:
            _repair_single_case(row, backend, model, results_db, run_id)

def main():
    parser = argparse.ArgumentParser(description='Sample Parser')
    # parser.add_argument('--mode', type=str, default='input_repair', help='mode: input_repair or program_repair')
    parser.add_argument('--backend', type=str, default='openai', help='backend: openai / ollama / Claude')
    parser.add_argument('--model', type=str, default='o1-mini-2024-09-12', help='model: model name')
    parser.add_argument('--db-path', type=str, default='parser_cases.db', help='Path to the parser_cases SQLite database')
    parser.add_argument('--results-db', type=str, default='repair_results.db', help='Path to output results SQLite database')
    parser.add_argument('--workers', type=int, default=1, help='number of parallel workers')
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
    program_reapir(args.backend, args.model, args.db_path, results_db_name, args.workers)
    # Clean up repaired files after run
    for fname in os.listdir('.'):
        if fname.startswith('case_') and '_repaired_' in fname:
            try:
                os.remove(fname)
            except OSError:
                pass
            
if __name__ == "__main__":
    import multiprocessing as mp
    try:
        mp.set_start_method("spawn", force=True)
    except RuntimeError:
        pass
    main()