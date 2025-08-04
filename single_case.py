#!/usr/bin/env python3
"""
Generate a single parser case and print its artefacts as JSON to stdout.
Usage: python single_case.py --num-nonterminals M --max-productions P --max-rhs-length L --nonterminal-prob R --loop-prob L
"""
import json
import argparse

from main import generate_case
from ultility import grammar_printer, compile_parser, validation_check_inproc

class Config:
    """Configuration settings for the script."""
    MAX_EXAMPLES = 100
    MAX_MUTATE_ATTEMPTS = 100
    MAX_INSTANCE_SEARCH = 200
    MIN_TEST_CASES = 1
    KEEP_TEST_CASES = 5
    TIMEOUT = 80
    DB_FILE = "targets11.db"
    
    # Benchmark parameters
    NUM_NONTERMINALS = range(10,11)
    DIMS = NUM_NONTERMINALS
    NONTERMINAL_PROB = 0.5
    LOOP_PROB = 0.3
    CASES_PER_SETTING = 1

    # Default grammar generation parameters
    DEFAULT_MAX_PRODUCTIONS = 5
    DEFAULT_MAX_RHS_LENGTH = 5
    def __init__(self, args=None):
        if args:
            self.update_from_args(args)

    def update_from_args(self, args):
        """Update configuration from command-line arguments."""
        if args.max_examples is not None:
            self.MAX_EXAMPLES = args.max_examples
        if args.max_mutate_attempts is not None:
            self.MAX_MUTATE_ATTEMPTS = args.max_mutate_attempts
        if args.max_instance_search is not None:
            self.MAX_INSTANCE_SEARCH = args.max_instance_search
        if args.cases_per_setting is not None:
            self.CASES_PER_SETTING = args.cases_per_setting
        
        self.DIMS = self.NUM_NONTERMINALS
        if args.dim is not None:
            if args.dim:
                self.DIMS = args.dim
        
        if args.nonterminal_prob is not None:
            self.NONTERMINAL_PROB = args.nonterminal_prob
        if args.loop_prob is not None:
            self.LOOP_PROB = args.loop_prob

def main():
    parser = argparse.ArgumentParser(description="Generate a single parser case and output as JSON")
    parser.add_argument('--num-nonterminals', '-n', type=int, default=2,
                        help='Number of nonterminals for grammar generation (default: %(default)s)')
    parser.add_argument('--max-productions', '-p', type=int, default=Config.DEFAULT_MAX_PRODUCTIONS,
                        help='Max productions per nonterminal (default: %(default)s)')
    parser.add_argument('--max-rhs-length', '-r', type=int, default=Config.DEFAULT_MAX_RHS_LENGTH,
                        help='Max right-hand side length of productions (default: %(default)s)')
    parser.add_argument('--nonterminal-prob', type=float, default=Config.NONTERMINAL_PROB,
                        help='Probability of nonterminal recursion in grammar generation (default: %(default)s)')
    parser.add_argument('--loop-prob', type=float, default=Config.LOOP_PROB,
                        help='Probability of looping in grammar generation (default: %(default)s)')
    args = parser.parse_args()

    # Generate one parser case using the core API
    try:
        artefacts = generate_case(
            num_nonterminals=args.num_nonterminals,
            max_productions=args.max_productions,
            max_rhs_length=args.max_rhs_length,
            nonterminal_prob=args.nonterminal_prob,
            loop_prob=args.loop_prob,
            config=Config()
        )
    except Exception as e:
        parser.error(f"Error generating case: {e}")

    print("Generated grammar:")
    print(artefacts['original_grammar'])
    print("Original code:")
    print(artefacts['original_parser'])
    print("Corrupted grammar:")
    print(artefacts['corrupted_grammar'])
    print("Corrupted code:")
    print(artefacts['corrupted_parser'])
    print("Test cases:")
    # artefacts['test_cases'] is stored as a JSON-encoded string by generate_case;
    # decode it first so we iterate over complete test-case strings, not characters.
    raw_cases = (
        json.loads(artefacts['test_cases'])
        if isinstance(artefacts['test_cases'], str)
        else artefacts['test_cases']
    )

    # Keep only those strings accepted by the original parser
    # but rejected by the corrupted parser, just to be safe.
    orig_parse_fn = compile_parser(artefacts['original_parser'])
    corr_parse_fn = compile_parser(artefacts['corrupted_parser'])
    test_cases = [
        s for s in raw_cases
        if validation_check_inproc(s, orig_parse_fn) and not validation_check_inproc(s, corr_parse_fn)
    ]

    if not test_cases:
        print("[!] Warning: no valid failing test cases found after validation.")

    for i, test_case in enumerate(test_cases):
        print(f"Test case {i + 1}:")
        print(test_case)

if __name__ == '__main__':
    main()
