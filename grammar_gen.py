"""
This generator (grammar_gen_lexer_loop.py) produces a random LL(1) grammar and outputs a standalone recursive descent parser 
with an integrated random lexer in generated_parser.py.

The generated grammar satisfies:
  - Each nonterminal has productions whose first symbol is a terminal.
  - For a given nonterminal, the alternatives use distinct starting terminals.
Thus, the grammar is suitable for a recursive descent parser.
Additionally, a random Lexer is generated using randomly selected token rules for each terminal.
For token patterns of the form "a+" or "b+", instead of using regular expressions the lexer uses loop-based reading.
"""

import random
import sys
from ultility import grammar_printer
# ---------------------------
# Step 1: Generate a Random Grammar for LL(1)
# ---------------------------

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
    from the start symbol (the first nonterminal).
    """
    # Limit the number of productions by the number of terminals
    max_productions = min(max_productions, num_terminals)
    
    # Ensure max_rhs_length is at least 2 if more than one nonterminal exists.
    if max_rhs_length < 2 and num_nonterminals > 1:
        raise ValueError("max_rhs_length must be at least 2 to ensure nonterminals are reachable.")
    
    # Create nonterminals (uppercase letters) and terminals (lowercase letters)
    nonterminals = [chr(i) for i in range(65, 65 + num_nonterminals)]
    terminals = [chr(i) for i in range(97, 97 + num_terminals)]
    grammar = {}
    
    # Generate productions for each nonterminal
    for nt in nonterminals:
        productions = []
        available_terminals = terminals[:]  # Copy for unique first symbol selection
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
            # Choose the rest of the production symbols from terminals ∪ nonterminals
            for _ in range(1, length):
                prod.append(random.choice(terminals + nonterminals))
            productions.append(prod)
        grammar[nt] = productions

    # Compute reachable nonterminals from the start symbol (first nonterminal)
    reachable = compute_reachable(grammar, nonterminals[0])
    unreachable = set(nonterminals) - reachable
    
    # Inject unreachable nonterminals into productions of reachable ones
    while unreachable:
        un = unreachable.pop()
        candidate = random.choice(list(reachable))
        injection_done = False
        
        # First, try appending the unreachable nonterminal to candidate's production if length allows
        for prod in grammar[candidate]:
            if len(prod) < max_rhs_length:
                prod.append(un)
                injection_done = True
                break
        
        # Otherwise, try replacing one symbol (other than the first) in candidate's production
        if not injection_done:
            for prod in grammar[candidate]:
                if len(prod) > 1:
                    index = random.randint(1, len(prod)-1)
                    prod[index] = un
                    injection_done = True
                    break
        
        # Finally, if injection was not possible, add a new production to candidate.
        if not injection_done and len(grammar[candidate]) < max_productions:
            used_firsts = {prod[0] for prod in grammar[candidate]}
            available_firsts = [t for t in terminals if t not in used_firsts]
            if not available_firsts:
                available_firsts = terminals[:]
            new_prod = [random.choice(available_firsts), un]
            grammar[candidate].append(new_prod)
            injection_done = True
        
        # Recalculate reachable set
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
# Step 3: Generate Random Token Rules for the Lexer
# ---------------------------
def generate_random_token_rules(terminals):
    """
    For each terminal, randomly choose one of two matching patterns:
    either an exact single-character match or a one-or-more repetition.
    The repetition pattern is indicated by a trailing '+' in the generated pattern.
    """
    token_rules = []
    for t in terminals:
        if random.choice([True, False]):
            # Exact match for terminal t
            pattern = t  # e.g., "a"
        else:
            # Match one or more occurrences of t (pattern represented as "a+")
            pattern = t + "+"
        token_rules.append((t, pattern))
    return token_rules

# ---------------------------
# Step 4: Generate Recursive Descent Parser Code with Integrated Loop-based Lexer
# ---------------------------
def generate_parser_code(grammar, nonterminals, terminals, start_symbol):
    """
    Generates a complete Python source code string for a recursive descent parser.
    The parser includes a random lexer that tokenizes the input based on randomly generated token rules.
    For patterns of the form "a+" or "b+", a loop-based method (instead of regex) is used to read tokens.
    """
    code_lines = []
    code_lines.append("import sys")
    code_lines.append("")
    code_lines.append("# --- Token and Lexer Classes ---")
    code_lines.append("class Token:")
    code_lines.append("    def __init__(self, token_type, value):")
    code_lines.append("        self.type = token_type")
    code_lines.append("        self.value = value")
    code_lines.append("")
    code_lines.append("    def __repr__(self):")
    code_lines.append("        return f\"Token({{self.type}}, {{self.value}})\"")
    code_lines.append("")
    code_lines.append("class Lexer:")
    code_lines.append("    def __init__(self, token_rules):")
    code_lines.append("        # token_rules is a list of tuples (token_type, pattern)")
    code_lines.append("        # If the pattern ends with '+', we treat it as a repeat-match pattern")
    code_lines.append("        self.token_rules = []")
    code_lines.append("        for token_type, pattern in token_rules:")
    code_lines.append("            if pattern.endswith('+'):")
    code_lines.append("                # For repeat-match, store the literal and mark as 'repeat'")
    code_lines.append("                self.token_rules.append((token_type, pattern[:-1], 'repeat'))")
    code_lines.append("            else:")
    code_lines.append("                # Exact match")
    code_lines.append("                self.token_rules.append((token_type, pattern, 'exact'))")
    code_lines.append("")
    code_lines.append("    def tokenize(self, text):")
    code_lines.append("        pos = 0")
    code_lines.append("        tokens = []")
    code_lines.append("        while pos < len(text):")
    code_lines.append("            # Skip whitespace")
    code_lines.append("            if text[pos].isspace():")
    code_lines.append("                pos += 1")
    code_lines.append("                continue")
    code_lines.append("")
    code_lines.append("            match_found = False")
    code_lines.append("            for token_type, literal, match_type in self.token_rules:")
    code_lines.append("                if match_type == 'exact':")
    code_lines.append("                    if text.startswith(literal, pos):")
    code_lines.append("                        tokens.append(Token(token_type, literal))")
    code_lines.append("                        pos += len(literal)")
    code_lines.append("                        match_found = True")
    code_lines.append("                        break")
    code_lines.append("                else:  # match_type == 'repeat'")
    code_lines.append("                    if text[pos] == literal:")
    code_lines.append("                        start = pos")
    code_lines.append("                        while pos < len(text) and text[pos] == literal:")
    code_lines.append("                            pos += 1")
    code_lines.append("                        tokens.append(Token(token_type, text[start:pos]))")
    code_lines.append("                        match_found = True")
    code_lines.append("                        break")
    code_lines.append("            if not match_found:")
    code_lines.append("                error(\"Lexer error: Unexpected character '{}' at position {}\".format(text[pos], pos))")
    code_lines.append("        return tokens")
    code_lines.append("")
    code_lines.append("# --- Randomly Generated Token Rules ---")
    token_rules = generate_random_token_rules(terminals)
    code_lines.append("token_rules = " + repr(token_rules))
    code_lines.append("lexer = Lexer(token_rules)")
    code_lines.append("")
    code_lines.append("# Global token list and position index")
    code_lines.append("tokens = []")
    code_lines.append("pos = 0")
    code_lines.append("")
    code_lines.append("def error(msg):")
    code_lines.append("    print('Parse error:', msg)")
    code_lines.append("    sys.exit(1)")
    code_lines.append("")
    code_lines.append("def match(expected):")
    code_lines.append("    global pos, tokens")
    code_lines.append("    if pos < len(tokens) and tokens[pos].type == expected:")
    code_lines.append("        pos += 1")
    code_lines.append("    else:")
    code_lines.append("        current = tokens[pos].value if pos < len(tokens) else 'EOF'")
    code_lines.append("        error(f\"Expected token type '{expected}', got {current}\")")
    code_lines.append("")
    # Generate parse functions for each nonterminal
    for nt in nonterminals:
        func_name = f"parse_{nt}"
        code_lines.append(f"def {func_name}():")
        code_lines.append("    global pos, tokens")
        prods = grammar[nt]
        alternatives = []
        for prod in prods:
            alternatives.append((prod[0], prod))
        code_lines.append("    if pos >= len(tokens):")
        code_lines.append(f"        error('Unexpected end of input in {nt}')")
        code_lines.append("    lookahead = tokens[pos].type")
        first_condition = True
        expected_tokens = [f"\"{alt[0]}\"" for alt in alternatives]
        for first_tok, prod in alternatives:
            cond = "if" if first_condition else "elif"
            code_lines.append(f"    {cond} lookahead == \"{first_tok}\":")
            for s in prod:
                if s in nonterminals:
                    code_lines.append(f"        parse_{s}()")
                else:
                    code_lines.append(f"        match(\"{s}\")")
            first_condition = False
        expected_tokens_str = ", ".join(expected_tokens)
        code_lines.append("    else:")
        code_lines.append(f"        error(\"Unexpected token \" + tokens[pos].value + \" in {nt}, expected one of: \" + \", \".join([{expected_tokens_str}]))")
        code_lines.append("")
    # Main parse_input function using the loop-based lexer
    code_lines.append("def parse_input(input_str):")
    code_lines.append("    global tokens, pos")
    code_lines.append("    try:")
    code_lines.append("        tokens = lexer.tokenize(input_str)")
    code_lines.append("    except Exception as e:")
    code_lines.append("        error(str(e))")
    code_lines.append("    pos = 0")
    code_lines.append(f"    parse_{start_symbol}()")
    code_lines.append("    if pos != len(tokens):")
    code_lines.append("        error('Extra tokens after parsing: ' + ' '.join(token.value for token in tokens[pos:]))")
    code_lines.append("    print('Input accepted.')")
    code_lines.append("")
    code_lines.append("def main():")
    code_lines.append("    import sys")
    code_lines.append("    if len(sys.argv) > 1:")
    code_lines.append("        input_str = sys.argv[1]")
    code_lines.append("        parse_input(input_str)")
    code_lines.append("    else:")
    code_lines.append("        print('Usage: python generated_parser.py <input_string>')")
    code_lines.append("")
    code_lines.append("if __name__ == '__main__':")
    code_lines.append("    main()")
    return "\n".join(code_lines)

# ---------------------------
# Step 5: Main Generator Routine
# ---------------------------
def gen(numterminals=10, numnonterminals=10, maxproductions=10, max_original_examples=5):
    # 1. Generate a random LL(1) grammar.
    grammar, nonterminals, terminals = generate_random_grammar(numnonterminals, numterminals, maxproductions)
    print("Generated Grammar:")
    # grammar_printer(nonterminals=nonterminals, grammar=grammar)

    start_symbol = nonterminals[0]
    
    # 2. Generate a few example derivations.
    examples = []
    for _ in range(max_original_examples):
        ex = generate_example_string(grammar, start_symbol)
        if 3 < len(ex) < 6:
            examples.append(ex)
    
    # 3. Generate the recursive descent parser code with an integrated loop-based lexer.
    parser_code = generate_parser_code(grammar, nonterminals, terminals, start_symbol)
    return parser_code, set(examples), grammar, nonterminals, terminals