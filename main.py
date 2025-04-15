import argparse
import json
from grammar_gen import gen, generate_example_string, generate_parser_code
from generate_corrupt_input import mutate
from repair import repair
from ultility import levenshtein_distance, validation_check, get_path, creat_repo, grammar_printer
from localisation import localise_program_input, localise_program
from patch import replace_function_ast_in_file
from mutation import mutate_grammar
from file_diff import get_diff_function, diff
from testies import generate_biased_example_wrapper
from time import sleep
from sqlite3 import connect
import os
import uuid
from issue_maker import create_issue

MAX_EXAMPLES = 100
MAX_MUTATE_ATTEMPTS = 100

repos = [] 

def program_reapir(backend, model, dimension=5):
    """
    This function generates a parser, mutates it, and then localizes the mutation.
    It generates a parser code, mutates it, and then localizes the mutation using a given backend and model.
    It also validates the generated examples against the original and repaired parser.
    
    Returns a tuple:
      (localisation_flag, fixed, dimension, kpath)
    where:
      - localisation_flag: True if the suspicious function identified matches expected function name.
      - fixed: True if all test cases pass on the repaired code.
      - dimension: The dimension used for generation.
      - kpath: The length of the path used in repair.
    """
    # Generate a valid parser code using given dimension parameters.
    code, _, grammar, nonterminals, terminals = gen(dimension, dimension, dimension, MAX_EXAMPLES)
    # print("Generated code:")
    # print(code)
    
    # Write the original code to file.
    with open("original_generated_parser.py", "w") as f:
        f.write(code)
    
    # Introduce corruption to the generated parser.
    code = ""
    instances = set()
    for attempt in range(MAX_MUTATE_ATTEMPTS):
        corrupted_grammar, new_nonterminals, new_terminals, nt, prod_index = mutate_grammar(grammar, nonterminals, terminals)
        code = generate_parser_code(corrupted_grammar, new_nonterminals, terminals, new_nonterminals[0])
        # print("Corrupted code:")
        # print(code)
        
        # Write corrupted code to file.
        with open("corrupted_generated_parser.py", "w") as f:
            f.write(code)
        
        # Get the diff between the original and corrupted code (for logging/analysis)
        diff("original_generated_parser.py", "corrupted_generated_parser.py")
        path = get_path(grammar, new_nonterminals[0], nt)
        path = path + [(nt, prod_index)]
        kpath = len(path)
        print(f"kpath length:{kpath-1}")
        print(f"Path: {path}")
        # Generate instances that cause a validation failure
        for j in range(200):
            temp = generate_biased_example_wrapper(grammar=grammar, symbol=new_nonterminals[0], path=path, max_depth=20)
            if not validation_check(temp, "corrupted_generated_parser.py"):
                instances.add(temp)
        for index, instance in enumerate(instances):
            print(f"{index} instance: {instance}")
        if len(instances) <= 2:
            continue
        break
    
    print("Original grammar:")
    grammar_printer(nonterminals=nonterminals, grammar=grammar)
    print("Corrupted grammar:")
    grammar_printer(nonterminals=new_nonterminals, grammar=corrupted_grammar)
    print("Test cases:")
    print(instances)
    
    # Use the shortest failing instance as the primary test input.
    instance = min(instances, key=len)
    validation_set = instances - {instance}

    # Creat repo for tools on swe-bench
    repo_name = str(uuid.uuid4().hex)
    issue = create_issue(instance)
    creat_repo(repo_name=repo_name, code=code, issue=issue)
    repos.append(repo_name)
    print("Repo created")
    
    # Localise the suspicious function using the given backend and model.
    response = localise_program(code, instance, backend, model)
    print("Localisation response:")
    print(response)
    sleep(5)  # Allow time for any asynchronous processes if required
    response_json = json.loads(response)
    suspicious_function = response_json["function_name"]
    print("Suspicious function identified:")
    print(suspicious_function)
    print("Correct answer:")
    print(f"parse_{nt}")

    localisation_flag = False
    if suspicious_function == f"parse_{nt}":
        localisation_flag = True
        print("Localisation passed")
    else:
        print("Localisation failed")
    
    patch = response_json["correct_version"]
    print("Proposed patch:")
    print(patch)
    
    # Apply the patch to create a repaired version of the parser code.
    replace_function_ast_in_file("corrupted_generated_parser.py", patch, suspicious_function, "repaired_generated_parser.py")
    
    count = 0
    fixed = False
    # Check each validation input against the repaired code.
    for series, test in enumerate(validation_set):
        print(f"========Test Case {series}========")
        if validation_check(test, "repaired_generated_parser.py"):
            count += 1
            print("Validation check passed")
        else:
            print("Validation check failed")
    if count == len(validation_set):
        print("Validation check passed for all test cases")
        fixed = True
    else:
        print("Validation check failed for some test cases")
    
    return (localisation_flag, fixed, dimension, kpath)

def benchmark(backend, model, start_dimension=10, end_dimension=30, step=10, iterations=3):
    """
    Run the program repair benchmark over a range of dimensions.

    
    For each dimension in [start_dimension, end_dimension] (incremented by `step`) and for a number of iterations,
    the function calls program_reapir and records key metrics into a SQLite database.
    
    The database file 'benchmark_results.db' will contain the following columns:
      - id (auto-increment primary key)
      - dimension (the input dimension used)
      - kpath (the length of the mutation path)
      - localisation_flag (boolean, True if correct function localized)
      - fixed (boolean, True if all test cases passed on repaired code)
      - iteration (the iteration number for that dimension)
      - timestamp (when the entry was recorded)
    """
    # Connect to (or create) the SQLite database.
    conn = connect("benchmark_results.db")
    cursor = conn.cursor()
    
    # Create the results table if it doesn't already exist.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS benchmark_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            backend TEXT,
            model TEXT,
            dimension INTEGER,
            kpath INTEGER,
            localisation_flag BOOLEAN,
            fixed BOOLEAN,
            iteration INTEGER
        )
    """)
    conn.commit()

    # Iterate over dimensions and iterations.
    for dim in range(start_dimension, end_dimension + 1, step):
        for iteration in range(iterations):
            print(f"Running benchmark for dimension: {dim}, iteration: {iteration}")
            localisation_flag, fixed, used_dimension, kpath = program_reapir(backend, model, dimension=dim)
            
            # Insert the benchmark result into the database.
            cursor.execute("""
                INSERT INTO benchmark_results (backend,model,dimension, kpath, localisation_flag, fixed, iteration)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (backend, model, used_dimension, kpath, localisation_flag, fixed, iteration))
            conn.commit()
    
    conn.close()
    print("Benchmark complete. Results written to benchmark_results.db.")

def main():
    parser = argparse.ArgumentParser(description='Parser Repair Benchmark')
    parser.add_argument('--mode', type=str, default='program_repair', 
                        help='Mode to run: "program_repair" or "benchmark"')
    parser.add_argument('--backend', type=str, default='openai', 
                        help='Backend to use (e.g., openai, ollama, Claude)')
    parser.add_argument('--model', type=str, default='o1-mini-2024-09-12', 
                        help='Model name to use')
    # Benchmark-specific arguments.
    parser.add_argument('--start_dim', type=int, default=10, help='Starting dimension for benchmark')
    parser.add_argument('--end_dim', type=int, default=20, help='Ending dimension for benchmark')
    parser.add_argument('--step', type=int, default=10, help='Step increment for dimension in benchmark')
    parser.add_argument('--iterations', type=int, default=3, help='Number of iterations per dimension for benchmark')
    
    args = parser.parse_args()
    
    if args.mode == 'benchmark':
        benchmark(args.backend, args.model, args.start_dim, args.end_dim, args.step, args.iterations)
    elif args.mode == 'program_repair':
        program_reapir(args.backend, args.model)
    else:
        print("Invalid mode specified. Use 'program_repair' or 'benchmark'.")
    # # Clean up any created repositories
    # for repo in repos:
    #     os.system(f"rm -rf {repo}")
    #     print(f"Removed repository: {repo}")

if __name__ == "__main__":
    main()