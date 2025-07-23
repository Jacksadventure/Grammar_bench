# Grammar Benchmarking and Generation Tool

This script is designed to generate and mutate parser grammars for benchmarking and analysis purposes. It supports two main modes of operation: generating new grammars based on specified parameters and mutating an existing grammar from a file.

## How to Use

### General Options

-   `-w, --workers`: Number of worker processes to use for parallel generation. Defaults to the number of cases per setting.
-   `-c, --cases-per-setting`: Number of cases to generate for each parameter setting. Default is 20.

### Mode 1: Grammar Generation and Mutation (Default)

This is the default mode. The script will generate new grammars, mutate them, find failing test cases, and store the results in a database.

**Parameters for Grammar Generation:**

-   `--dim [DIMS ...]`: A comma-separated list of nonterminal counts to sweep through (e.g., `--dim 2,4,8`). If provided without a value, it enables `auto_dims` mode where `max_productions` and `max_rhs_length` are set to the number of nonterminals.
-   `--num-nonterminals`: Specify a single number of nonterminals for generation. Requires `--nonterminal-prob` and `--loop-prob`.
-   `--max-productions`: Maximum number of productions per nonterminal.
-   `--max-rhs-length`: Maximum right-hand side length for productions.
-   `--nonterminal-prob`: Probability of nonterminal expansion.
-   `--loop-prob`: Probability of right-recursive looping.

**Example Commands:**

-   Run with default settings (generates 20 cases for 1 nonterminal):
    ```bash
    python main.py
    ```
-   Run a sweep over different numbers of nonterminals with 10 cases each:
    ```bash
    python main.py --dim 2,3,4 -c 10
    ```
-   Generate 50 cases for a custom grammar with 5 nonterminals:
    ```bash
    python main.py --num-nonterminals 5 --nonterminal-prob 0.4 --loop-prob 0.2 -c 50
    ```

### Mode 2: Mutating an External Grammar File

This mode allows you to mutate a grammar from a provided JSON file instead of generating a new one.

**Parameter:**

-   `--grammar-file <PATH>`: Path to the external grammar JSON file.

**Example Command:**

-   Mutate the grammar in `my_grammar.json` and generate 100 test cases:
    ```bash
    python main.py --grammar-file my_grammar.json -c 100
    ```

### Overriding Search Parameters

You can also override the search bounds for finding failing test cases:

-   `--max-examples`: Max examples when building a fresh parser.
-   `--max-mutate-attempts`: Max number of corruption attempts per case.
-   `--max-instance-search`: Attempts to find failing inputs.
