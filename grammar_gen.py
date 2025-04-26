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
            for symbol in prod[1:]:
                if symbol in grammar and symbol not in reachable:
                    queue.append(symbol)
    return reachable


def generate_random_grammar(
    num_nonterminals=10,
    num_terminals=10,
    max_productions=10,
    max_rhs_length=3,
    recursion_prob=0.5,
    loop_prob=0.3,          # chance a non‑terminal becomes α Nt | ε
):
    # ----------------- symbol pools -----------------
    max_productions = min(max_productions, num_terminals)
    if max_rhs_length < 2 and num_nonterminals > 1:
        raise ValueError("max_rhs_length must be ≥ 2 to keep all NTs reachable")

    nonterminals = [chr(65 + i) for i in range(num_nonterminals)]
    terminals    = [chr(97 + i) for i in range(num_terminals)]
    grammar      = {}

    # ------------- generate productions -------------
    for nt in nonterminals:
        prods = []

        # α Nt | ε  ----------------------------------------------------
        if random.random() < loop_prob and max_productions >= 2:
            length = random.randint(1, max_rhs_length)
            alpha  = [random.choice(terminals)]
            for _ in range(1, length):
                alpha.append(
                    random.choice(nonterminals)
                    if random.random() < recursion_prob
                    else random.choice(terminals)
                )
            alpha.append(nt)      # right‑recursive tail
            prods.extend([alpha, []])   # ε is an empty list
            grammar[nt] = prods
            continue              # no further productions for this NT
        # --------------------------------------------------------------

        # regular productions
        avail_terms = terminals[:]
        n_prods     = random.randint(1, max_productions)
        for _ in range(n_prods):
            first = random.choice(avail_terms)
            avail_terms.remove(first) if first in avail_terms else None

            rhs = [first]
            for _ in range(1, random.randint(1, max_rhs_length)):
                rhs.append(
                    random.choice(nonterminals)
                    if random.random() < recursion_prob
                    else random.choice(terminals)
                )
            prods.append(rhs)

        grammar[nt] = prods

    # --------------- reachability repair -------------
    start       = nonterminals[0]
    reachable   = compute_reachable(grammar, start)
    unreachable = set(nonterminals) - reachable

    while unreachable:
        un  = unreachable.pop()
        src = random.choice(list(reachable))
        injected = False

        def safe(prod, nt=src):
            """do not alter ε or right‑recursive prod (... nt)"""
            return prod and prod[-1] != nt

        # append un
        for prod in grammar[src]:
            if safe(prod) and len(prod) < max_rhs_length:
                prod.append(un)
                injected = True
                break

        # replace inside prod
        if not injected:
            for prod in grammar[src]:
                if safe(prod) and len(prod) > 1:
                    idx = random.randint(1, len(prod) - 1)
                    prod[idx] = un
                    injected = True
                    break

        # new production if still not reachable
        if not injected and len(grammar[src]) < max_productions:
            used  = {p[0] for p in grammar[src] if p}
            first = random.choice([t for t in terminals if t not in used] or terminals)
            grammar[src].append([first, un])

        reachable   = compute_reachable(grammar, start)
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
    If a nonterminal has productions like:
         <Xs> → <X><Xs> | ε
    (with ε represented as an empty production []),
    then the parser code for that nonterminal is generated using an iterative
    while loop rather than explicit recursion.
    """
    def is_iterative_rule(nt):
        """
        Check if nonterminal nt defines a repetition.
        We expect two alternatives:
          - One alternative is the recursive alternative where the last symbol is nt.
          - One alternative is epsilon (empty production, represented as []).
        If so, return (True, base_prod) where base_prod is the recursive alternative with
        its final self-reference removed.
        Otherwise, return (False, None).
        """
        recursive_prod = None
        epsilon_found = False
        for prod in grammar[nt]:
            if prod == []:
                epsilon_found = True
            elif prod[-1] == nt:
                # Save the production without the recursive call.
                recursive_prod = prod[:-1]
        return (epsilon_found and (recursive_prod is not None)), recursive_prod

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

    # For each nonterminal, generate a parse function.
    for nt in nonterminals:
        func_name = f'parse_{nt}'
        iterative, base_prod = is_iterative_rule(nt)
        code_lines.append(f'def {func_name}():')
        code_lines.append('    global pos, tokens')
        if iterative:
            # Generate iterative (while loop) code.
            # Assume that the base alternative (from <X><Xs>) starts with a terminal,
            # which we use for the while loop test.
            first_tok = base_prod[0]
            code_lines.append(f'    while pos < len(tokens) and tokens[pos] == "{first_tok}":')
            # Generate code for the symbols in the base production.
            for s in base_prod:
                if s in nonterminals:
                    code_lines.append(f'        parse_{s}()')
                else:
                    code_lines.append(f'        match("{s}")')
        else:
            # Use the original recursive descent code generation.
            prods = grammar[nt]
            alternatives = []
            for prod in prods:
                first_tok = "" if not prod else prod[0]
                alternatives.append((first_tok, prod))
            code_lines.append('    if pos >= len(tokens):')
            code_lines.append(f'        error("Unexpected end of input in {nt}")')
            code_lines.append('    lookahead = tokens[pos]')
            first_condition = True
            # Create a list of expected tokens for error reporting.
            expected_tokens = [f'"{alt[0]}"' for alt in alternatives]
            for first_tok, prod in alternatives:
                if first_tok == "":
                    continue
                cond = 'if' if first_condition else 'elif'
                code_lines.append(f'    {cond} lookahead == "{first_tok}":')
                for s in prod:
                    if s in nonterminals:
                        code_lines.append(f'        parse_{s}()')
                    else:
                        code_lines.append(f'        match("{s}")')
                first_condition = False
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
    # Main block: use command-line argument if provided.
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
def gen(
    numterminals,
    numnonterminals,
    maxproductions,
    max_original_examples,
    recursion_prob=0.5,
    loop_prob=0.5,
):
    # 1. Generate a random LL(1) grammar with controlled recursion
    grammar, nonterminals, terminals = generate_random_grammar(
        num_nonterminals=numnonterminals,
        num_terminals=numterminals,
        max_productions=maxproductions,
        recursion_prob=recursion_prob
    )
    start_symbol = nonterminals[0]

    # 2. Generate a few example derivations
    examples = []
    for _ in range(max_original_examples):
        ex = generate_example_string(grammar, start_symbol)
        if 3 < len(ex) < 6:
            examples.append(ex)

    parser_code = generate_parser_code(grammar, nonterminals, start_symbol)
    return parser_code, set(examples), grammar, nonterminals, terminals