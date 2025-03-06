#!/usr/bin/env python3
"""
This generator (grammar_gen.py) produces a random LL(1) grammar 
and outputs a standalone recursive descent parser in generated_parser.py.

The generated grammar satisfies:
  - Each nonterminal has productions whose first symbol is a terminal.
  - For a given nonterminal, the alternatives use distinct starting terminals.
Thus, the grammar is suitable for a recursive descent parser.
It also embeds a few example derivations.
"""

import random

# ---------------------------
# Step 1: Generate a Random Grammar for LL(1)
# ---------------------------
def generate_random_grammar(num_nonterminals=10, num_terminals=10, max_productions=10, max_rhs_length=3):
    """
    Generates a random grammar with:
      - Nonterminals: Uppercase letters (e.g. A, B, C, …)
      - Terminals: Lowercase letters (e.g. a, b, c, …)
    For each nonterminal:
      - The number of productions is between 1 and max_productions (ensuring max_productions <= num_terminals).
      - Each production's first symbol is chosen from the terminal set without repetition,
        ensuring unique FIRST tokens for alternatives.
      - The remaining symbols (if any) are randomly chosen from the union of terminals and nonterminals.
    Returns: (grammar, nonterminals, terminals)
      where grammar is a dict mapping nonterminal -> list of productions (each production is a list of symbols).
    """
    # Ensure we can assign distinct starting terminals
    max_productions = min(max_productions, num_terminals)
    
    nonterminals = [chr(i) for i in range(65, 65 + num_nonterminals)]
    terminals = [chr(i) for i in range(97, 97 + num_terminals)]
    grammar = {}
    
    for nt in nonterminals:
        productions = []
        available_terminals = terminals[:]  # copy for selecting first symbol uniquely
        num_prods = random.randint(1, max_productions)
        for _ in range(num_prods):
            length = random.randint(1, max_rhs_length)
            prod = []
            # For LL(1), ensure the first symbol is a terminal.
            if available_terminals:
                first = random.choice(available_terminals)
                available_terminals.remove(first)
            else:
                first = random.choice(terminals)
            prod.append(first)
            # For subsequent symbols, randomly choose from terminals ∪ nonterminals.
            for _ in range(1, length):
                prod.append(random.choice(terminals + nonterminals))
            productions.append(prod)
        grammar[nt] = productions
    return grammar, nonterminals, terminals

# ---------------------------
# Step 2: Generate Example Derivations from the Grammar
# ---------------------------
def generate_example_string(grammar, symbol, max_depth=10):
    """
    Recursively generate a derivation string from the given nonterminal symbol.
    Terminals are returned as is.
    """
    if symbol not in grammar or max_depth <= 0:
        return symbol
    prod = random.choice(grammar[symbol])
    result = []
    for s in prod:
        if s in grammar:
            result.append(generate_example_string(grammar, s, max_depth-1))
        else:
            result.append(s)
    return "".join(result)

# ---------------------------
# Step 3: Generate Recursive Descent Parser Code
# ---------------------------
def generate_parser_code(grammar, nonterminals, start_symbol):
    """
    Generate a complete Python source code string for a recursive descent parser.
    Each nonterminal gets its own function (e.g. parse_A for nonterminal A).
    The parser expects a list of tokens and uses a global index 'pos'.
    """
    code_lines = []
    code_lines.append('import sys')
    code_lines.append('')
    code_lines.append('tokens = []')
    code_lines.append('pos = 0')
    code_lines.append('')
    code_lines.append('def error(msg):')
    code_lines.append('    print("Parse error:", msg)')
    code_lines.append('    sys.exit(1)')
    code_lines.append('')
    code_lines.append('def match(expected):')
    code_lines.append('    global pos, tokens')
    code_lines.append('    if pos < len(tokens) and tokens[pos] == expected:')
    code_lines.append('        pos += 1')
    code_lines.append('    else:')
    code_lines.append('        error("Expected " + expected + ", got " + (tokens[pos] if pos < len(tokens) else "EOF"))')
    code_lines.append('')
    
    # For each nonterminal, generate a function parse_<nonterminal>()
    for nt in nonterminals:
        func_name = f'parse_{nt}'
        code_lines.append(f'def {func_name}():')
        code_lines.append('    global pos, tokens')
        prods = grammar[nt]
        alternatives = []
        for prod in prods:
            first_tok = prod[0]
            alternatives.append((first_tok, prod))
        code_lines.append('    if pos >= len(tokens):')
        code_lines.append(f'        error("Unexpected end of input in {nt}")')
        code_lines.append('    lookahead = tokens[pos]')
        first_condition = True
        # Prepare a list of expected tokens as literal strings
        expected_tokens = [f'"{alt[0]}"' for alt in alternatives]
        for first_tok, prod in alternatives:
            cond = 'if' if first_condition else 'elif'
            code_lines.append(f'    {cond} lookahead == "{first_tok}":')
            for s in prod:
                if s in nonterminals:
                    code_lines.append(f'        parse_{s}()')
                else:
                    code_lines.append(f'        match("{s}")')
            first_condition = False
        # Instead of using an f-string that causes nesting issues, we build the error line manually.
        expected_tokens_str = ", ".join(expected_tokens)
        error_line = ('    else:\n'
                      '        error("Unexpected token " + lookahead + " in ' + nt +
                      ', expected one of: " + ", ".join([' + expected_tokens_str + ']))')
        code_lines.append(error_line)
        code_lines.append('')
    
    # Main parse function.
    code_lines.append('def parse_input(input_str):')
    code_lines.append('    global tokens, pos')
    code_lines.append('    tokens = list(input_str)')
    code_lines.append('    pos = 0')
    code_lines.append(f'    parse_{start_symbol}()')
    code_lines.append('    if pos != len(tokens):')
    code_lines.append('        error("Extra tokens after parsing: " + " ".join(tokens[pos:]))')
    code_lines.append('    print("Input accepted.")')
    code_lines.append('')
    # Main block: if a command-line argument is provided, use it; otherwise, run examples.
    code_lines.append('def main():')
    code_lines.append('    import sys')
    code_lines.append('    if len(sys.argv) > 1:')
    code_lines.append('        input_str = sys.argv[1]')
    code_lines.append('        parse_input(input_str)')
    # code_lines.append('    else:')
    # code_lines.append('        examples = [')
    # for ex in examples:
    #     code_lines.append(f'            "{ex}",')
    # code_lines.append('        ]')
    # code_lines.append('        for ex in examples:')
    # code_lines.append('            print("Testing input:", ex)')
    # code_lines.append('            parse_input(ex)')
    # code_lines.append('            print()')
    code_lines.append('')
    code_lines.append('if __name__ == "__main__":')
    code_lines.append('    main()')
    return "\n".join(code_lines)

# ---------------------------
# Step 4: Main Generator Routine
# ---------------------------
def gen(numterminals,numnonterminals,maxproductions,max_original_examples):
    # 1. Generate a random LL(1) grammar.
    grammar, nonterminals, terminals = generate_random_grammar()
    print("Generated Grammar:")
    for nt in nonterminals:
        for prod in grammar[nt]:
            print(f"  {nt} -> {' '.join(prod)}")
    start_symbol = nonterminals[0]
    
    # 2. Generate a few example derivations.
    examples = []
    for _ in range(max_original_examples):
        ex = generate_example_string(grammar, start_symbol)
        if len(ex)>3 and len(ex)<6:
            examples.append(ex)

    # print("\nExample input strings:")
    # for ex in examples:
    #     print("  " + ex)
    
    # 3. Generate the recursive descent parser code.
    parser_code = generate_parser_code(grammar, nonterminals, start_symbol)

    return (parser_code, set(examples),grammar,nonterminals, terminals)
# if __name__ == "__main__":
#     main()