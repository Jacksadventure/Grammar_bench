import argparse
import json
from grammar_gen import gen,generate_example_string, generate_parser_code
# from repair import repair  # deprecated import removed to avoid unused dependency errors
from ultility import levenshtein_distance,validation_check,get_path
from localisation import localise_program_input,localise_program, refine_patch_grammar, refine_patch_logic, refine_patch_format
import sqlite3
import subprocess
import random
import os
import shutil
import uuid
# Directory for intermediate temporary cache files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)
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

def _repair_single_case(row, backend, model, results_db, run_id, sample):
    (case_id, num_nonterminals, nonterminal_prob, loop_prob, mutation_depth,
     orig_grammar, orig_parser, corr_grammar, corr_parser, failing_test_cases_json, passing_test_cases_json) = row
    # per-case DB connection for writing results
    conn = sqlite3.connect(results_db, timeout=30)
    cursor = conn.cursor()
    print(f"[Case {case_id}] ===== Case start: nonterminals={num_nonterminals}, prob={nonterminal_prob}, loop={loop_prob}, depth={mutation_depth} =====")
    # load test cases
    try:
        failing_test_cases = json.loads(failing_test_cases_json)
    except json.JSONDecodeError:
        failing_test_cases = json.loads(failing_test_cases_json.replace("'", '"'))
    try:
        passing_test_cases = json.loads(passing_test_cases_json)
    except json.JSONDecodeError:
        passing_test_cases = json.loads(passing_test_cases_json.replace("'", '"'))
    total_failing = len(failing_test_cases)
    total_passing = len(passing_test_cases)

    random_number = random.randint(0, 10000)
    corrupted_file = os.path.join(CACHE_DIR, f"case_{case_id}_corrupted_{run_id}_{sample}_{random_number}.py")
    with open(corrupted_file, 'w', encoding='utf-8') as f:
        f.write(corr_parser)

    error_examples = list(dict.fromkeys(failing_test_cases))

    # Initial patch via localization
    response = localise_program(corr_parser, error_examples, backend, model)
    print(f"[Case {case_id}] Localization response:\n{response.response_text}")
    patch_text = response.response_text
    total_prompt_tokens = getattr(response, 'prompt_tokens', 0)
    total_completion_tokens = getattr(response, 'completion_tokens', 0)
    total_tokens = getattr(response, 'total_tokens', 0)

    # Paths for patch/repaired files
    patch_file = os.path.join(CACHE_DIR, f"case_{case_id}_patch_{run_id}_{sample}_{random_number}.diff")
    repaired_file = os.path.join(CACHE_DIR, f"case_{case_id}_repaired_{run_id}_{sample}_{random_number}.py")

    success = False
    last_passed_failing = 0
    last_passed_passing = 0

    # Try initial patch + up to 10 refinements
    for refine_idx in range(0, 11):
        # Recreate repaired file from the corrupted baseline each attempt
        shutil.copy(corrupted_file, repaired_file)

        # Write current patch content
        with open(patch_file, 'w', encoding='utf-8') as f:
            f.write(patch_text)

        # Try to apply patch
        try:
            # capture outputs for error messages
            subprocess.run(['patch', '-t', repaired_file, '-i', patch_file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            err_msg = f"patch apply failed (attempt {refine_idx}): {e}"
            print(f"[Case {case_id}] {err_msg}")
            if refine_idx >= 10:
                break
            # refine patch focusing on format/line-number issues first
            resp = refine_patch_format(corr_parser, patch_text, backend, model)
            refined = resp.response_text
            total_prompt_tokens += getattr(resp, 'prompt_tokens', 0)
            total_completion_tokens += getattr(resp, 'completion_tokens', 0)
            total_tokens += getattr(resp, 'total_tokens', 0)
            patch_text = refined
            continue

        # Compile check
        comp = subprocess.run(['python3', '-m', 'py_compile', repaired_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if comp.returncode != 0:
            err_msg = comp.stderr.decode('utf-8', errors='ignore')
            print(f"[Case {case_id}] Compile failed (attempt {refine_idx}): {err_msg.strip()}")
            if refine_idx >= 10:
                break
            resp = refine_patch_grammar(corr_parser, patch_text, err_msg, backend, model)
            refined = resp.response_text
            total_prompt_tokens += getattr(resp, 'prompt_tokens', 0)
            total_completion_tokens += getattr(resp, 'completion_tokens', 0)
            total_tokens += getattr(resp, 'total_tokens', 0)
            patch_text = refined
            continue

        # Run tests (only if patch applied and compiled)
        passed_failing = 0
        for inp in failing_test_cases:
            proc = subprocess.run(['python3', repaired_file, inp], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode == 0:
                passed_failing += 1
            else:
                print(f"[Case {case_id}] Failing test failed on input={inp}, rc={proc.returncode}")
        plausible = 1 if passed_failing == total_failing else 0

        passed_passing = 0
        for inp in passing_test_cases:
            proc = subprocess.run(['python3', repaired_file, inp], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode == 0:
                passed_passing += 1
            else:
                print(f"[Case {case_id}] Passing test failed on input={inp}, rc={proc.returncode}")
        correct = 1 if plausible == 1 and passed_passing == total_passing else 0

        last_passed_failing = passed_failing
        last_passed_passing = passed_passing
        print(f"[Case {case_id}] Failing passed: {passed_failing}/{total_failing}, Passing passed: {passed_passing}/{total_passing}")

        if correct == 1:
            success = True
            break

        # Refine logic when patch applied and compiled but tests still fail
        if refine_idx >= 10:
            break
        failing_str = "\n".join(error_examples)
        resp = refine_patch_logic(corr_parser, failing_str, patch_text, backend, model)
        refined = resp.response_text
        total_prompt_tokens += getattr(resp, 'prompt_tokens', 0)
        total_completion_tokens += getattr(resp, 'completion_tokens', 0)
        total_tokens += getattr(resp, 'total_tokens', 0)
        patch_text = refined

    # Finalize and record results
    plausible = 1 if last_passed_failing == total_failing else 0
    correct = 1 if plausible == 1 and last_passed_passing == total_passing else 0

    cursor.execute(
        'REPLACE INTO repair_results(case_id,sample,puzzle_id,num_nonterminals,nonterminal_prob,loop_prob,total_failing,passed_failing,total_passing,passed_passing,plausible,correct,prompt_tokens,completion_tokens,total_tokens) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (case_id, sample, case_id, num_nonterminals, nonterminal_prob, loop_prob, total_failing, last_passed_failing, total_passing, last_passed_passing, plausible, correct, total_prompt_tokens, total_completion_tokens, total_tokens)
    )
    conn.commit()
    conn.close()
    for fname in (corrupted_file, patch_file, repaired_file):
        try:
            os.remove(fname)
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
        " corrupted_grammar, corrupted_parser, failing_test_cases, passing_test_cases"
        " FROM cases"
    )
    rows = cursor.fetchall()

    # Prepare results database
    results_conn = sqlite3.connect(results_db)
    results_cursor = results_conn.cursor()
    results_cursor.execute('''
        CREATE TABLE IF NOT EXISTS repair_results (
            case_id INTEGER,
            sample INTEGER,
            puzzle_id INTEGER,
            num_nonterminals INTEGER,
            nonterminal_prob REAL,
            loop_prob REAL,
            total_failing INTEGER,
            passed_failing INTEGER,
            total_passing INTEGER,
            passed_passing INTEGER,
            plausible INTEGER,
            correct INTEGER,
            prompt_tokens INTEGER,
            completion_tokens INTEGER,
            total_tokens INTEGER,
            PRIMARY KEY (case_id, sample)
        )
    ''')
    results_conn.commit()
    # Determine cases to (re)process
    # Determine cases and samples to (re)process
    results_cursor.execute("SELECT case_id, sample FROM repair_results")
    processed = {(case_id, sample) for case_id, sample in results_cursor.fetchall()}
    to_run = [(row, 1) for row in rows if (row[0], 1) not in processed]
    print(f"[Main] {len(to_run)} repairs to process using {workers} worker(s)")
    # dispatch either sequentially or in parallel
    if workers > 1:
        ctx = multiprocessing.get_context("spawn")
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as executor:
            futures = {executor.submit(_repair_single_case, row, backend, model, results_db, run_id, sample): row[0] for row, sample in to_run}
            for fut in concurrent.futures.as_completed(futures):
                cid = futures[fut]
                try:
                    fut.result()
                except Exception as e:
                    print(f"[Case {cid}] Worker exception: {e}")
    else:
        for row, sample in to_run:
            _repair_single_case(row, backend, model, results_db, run_id, sample)


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
if __name__ == "__main__":
    import multiprocessing as mp
    try:
        mp.set_start_method("spawn", force=True)
    except RuntimeError:
        pass
    main()
