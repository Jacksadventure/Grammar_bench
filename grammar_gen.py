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
import random

def compute_reachable(grammar, start):
    """
    Compute the set of nonterminals that are reachable from the start symbol.
    Since the first symbol of each production is a terminal (for LL(1) reasons),
    we only traverse symbols from the production starting at the second symbol.
    """
    reachable = set()
    queue = [start]
    while queue:
        nt = queue.pop(0)
        if nt in reachable:
            continue
        reachable.add(nt)
        for prod in grammar[nt]:
            # Check symbols in the production starting from the second position
            for symbol in prod[1:]:
                if symbol in grammar and symbol not in reachable:
                    queue.append(symbol)
    return reachable

def generate_random_grammar(num_nonterminals=10, num_terminals=10, max_productions=10, max_rhs_length=3):
    """
    Generates a random LL(1) grammar while ensuring that all nonterminals are reachable
    from the start symbol (the first nonterminal). Note: if max_rhs_length < 2 and there
    are more than one nonterminal, it's impossible to inject unreachable nonterminals.
    """
    # Ensure the number of productions for each nonterminal does not exceed the number of terminals
    max_productions = min(max_productions, num_terminals)
    
    # If max_rhs_length is less than 2, it's impossible to add nonterminals beyond the first symbol.
    if max_rhs_length < 2 and num_nonterminals > 1:
        raise ValueError("max_rhs_length must be at least 2 to ensure all nonterminals are reachable.")
    
    # Create nonterminals (uppercase letters) and terminals (lowercase letters)
    nonterminals = [chr(i) for i in range(65, 65 + num_nonterminals)]
    terminals = [chr(i) for i in range(97, 97 + num_terminals)]
    grammar = {}
    
    # Generate productions for each nonterminal
    for nt in nonterminals:
        productions = []
        available_terminals = terminals[:]  # Copy of terminals for unique first symbol selection
        num_prods = random.randint(1, max_productions)
        for _ in range(num_prods):
            length = random.randint(1, max_rhs_length)
            prod = []
            # The first symbol must be a terminal
            if available_terminals:
                first = random.choice(available_terminals)
                available_terminals.remove(first)
            else:
                first = random.choice(terminals)
            prod.append(first)
            # For the remaining positions, choose randomly from terminals ∪ nonterminals
            for _ in range(1, length):
                prod.append(random.choice(terminals + nonterminals))
            productions.append(prod)
        grammar[nt] = productions

    # Compute the set of nonterminals reachable from the start symbol (first nonterminal)
    reachable = compute_reachable(grammar, nonterminals[0])
    unreachable = set(nonterminals) - reachable
    
    # For each unreachable nonterminal, inject it into a production of a reachable nonterminal.
    while unreachable:
        un = unreachable.pop()  # Get an unreachable nonterminal
        candidate = random.choice(list(reachable))  # Randomly choose a reachable nonterminal as a candidate
        injection_done = False
        
        # First, try appending the unreachable nonterminal to one of candidate's productions if length allows
        for prod in grammar[candidate]:
            if len(prod) < max_rhs_length:
                prod.append(un)
                injection_done = True
                break
        
        # If not possible, try replacing a symbol (other than the first) in one of candidate's productions
        if not injection_done:
            for prod in grammar[candidate]:
                if len(prod) > 1:
                    index = random.randint(1, len(prod) - 1)
                    prod[index] = un
                    injection_done = True
                    break
        
        # Finally, if no injection was possible and candidate can accept more productions,
        # add a new production that starts with a unique terminal and then the unreachable nonterminal.
        if not injection_done and len(grammar[candidate]) < max_productions:
            used_firsts = {prod[0] for prod in grammar[candidate]}
            available_firsts = [t for t in terminals if t not in used_firsts]
            if not available_firsts:
                available_firsts = terminals[:]
            new_prod = [random.choice(available_firsts), un]
            grammar[candidate].append(new_prod)
            injection_done = True
        
        # Recalculate reachable set after injection until all nonterminals are reachable
        reachable = compute_reachable(grammar, nonterminals[0])
        unreachable = set(nonterminals) - reachable
    
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

    parser_code = generate_parser_code(grammar, nonterminals, start_symbol)

    return (parser_code, set(examples),grammar,nonterminals, terminals)