#!/usr/bin/env python3
"""
Generate a single parser case and print its artefacts as JSON to stdout.
Usage: python single_case.py --num-nonterminals M --max-productions P --max-rhs-length L --nonterminal-prob R --loop-prob L
"""
import json
import argparse

from main import generate_case

def main():
    parser = argparse.ArgumentParser(description="Generate a single parser case and output as JSON")
    parser.add_argument('--num-nonterminals', '-n', type=int, required=True,
                        help='Number of nonterminals for grammar generation')
    parser.add_argument('--max-productions', '-p', type=int, required=True,
                        help='Max productions per nonterminal')
    parser.add_argument('--max-rhs-length', '-r', type=int, required=True,
                        help='Max right-hand side length of productions')
    parser.add_argument('--nonterminal-prob', type=float, required=True,
                        help='Probability of nonterminal recursion in grammar generation')
    parser.add_argument('--loop-prob', type=float, required=True,
                        help='Probability of looping in grammar generation')
    args = parser.parse_args()

    # Generate one parser case using the core API
    try:
        artefacts = generate_case(
            num_nonterminals=args.num_nonterminals,
            max_productions=args.max_productions,
            max_rhs_length=args.max_rhs_length,
            nonterminal_prob=args.nonterminal_prob,
            loop_prob=args.loop_prob,
        )
    except Exception as e:
        parser.error(f"Error generating case: {e}")
    # Print artefacts as pretty JSON
    print(json.dumps(artefacts, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()