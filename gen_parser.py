#!/usr/bin/env python3
"""
Generate a recursive descent parser from a JSON BNF grammar file.
"""
import json
import sys
from grammar_gen import generate_parser_code

grammar = json.load(open('grammar.json', encoding='utf-8'))
nonterminals = list(grammar.keys())
start = nonterminals[0]
parser_code = generate_parser_code(grammar, nonterminals, start)
sys.stdout.write(parser_code)