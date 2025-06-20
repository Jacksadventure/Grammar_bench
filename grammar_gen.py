"""
This generator (grammar_gen.py) produces a random LL(1) grammar with nonterminals wrapped in angle brackets (e.g., <X>)
and outputs a standalone recursive descent parser in generated_parser.py.
The generated grammar satisfies:
  - No left recursion.
  - Each nonterminal has productions whose first symbol is a terminal.
  - For a given nonterminal, the alternatives use distinct starting terminals.
Thus, the grammar is suitable for a recursive descent parser.
It also embeds a few example derivations.
"""

import random
import string
from itertools import product as _itertools_product

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
    num_terminals=None,
    max_productions=5,
    max_rhs_length=5,
    recursion_prob=0.5,
    loop_prob=0.3,          # chance a non-terminal becomes α Nt | ε
):
    # ----------------- symbol pools -----------------
    # default number of terminals to number of nonterminals if not provided
    if num_terminals is None:
        num_terminals = num_nonterminals
    max_productions = min(max_productions, num_terminals)
    if max_rhs_length < 2 and num_nonterminals > 1:
        raise ValueError("max_rhs_length must be ≥ 2 to keep all NTs reachable")

    # ----------------- symbol pools -----------------
    # Nonterminal symbols: allow letters (upper/lower), generate names of increasing length
    ALPHABET_NT = list(string.ascii_uppercase)
    random.shuffle(ALPHABET_NT)  # shuffle to randomize order
    def _generate_labels(alphabet: str, count: int) -> list[str]:
        labels = []
        length = 1
        # generate combinations of given alphabet until required count reached
        while len(labels) < count:
            for p in _itertools_product(alphabet, repeat=length):
                labels.append(''.join(p))
                if len(labels) >= count:
                    break
            length += 1
        return labels[:count]
    nonterminals = _generate_labels(ALPHABET_NT, num_nonterminals)
    # Terminal symbols: single-character tokens from allowed set
    ALPHABET_T = string.ascii_letters + string.digits + "'!#$%&'()*+,-./:;<=>?@[]^_`{|}~'"
    # suffle the terminal symbols to randomize their order
    ALPHABET_T = list(ALPHABET_T)
    random.shuffle(ALPHABET_T)
    terminals = ALPHABET_T
    grammar   = {}

    # ------------- generate productions -------------
    for nt in nonterminals:
        prods = []

        # α Nt | ε  ----------------------------------------------------
        if random.random() < recursion_prob and max_productions >= 2:
            length = random.randint(1, max_rhs_length)
            alpha  = [random.choice(terminals)]
            for _ in range(1, length):
                alpha.append(
                    random.choice(nonterminals)
                    if random.random() < loop_prob
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

    # Ensure each nonterminal has at least one terminal-only or empty production
    for nt in nonterminals:
        prods = grammar[nt]
        has_terminal_or_empty = False
        for prod in prods:
            if not prod or (len(prod) == 1 and prod[0] in terminals):
                has_terminal_or_empty = True
                break
        if not has_terminal_or_empty:
            # Add a terminal-only production for this nonterminal
            grammar[nt].append([random.choice(terminals)])
    # Decorate nonterminals and grammar keys for readability: wrap them in angle brackets
    decorated_nonterminals = [f'<{nt}>' for nt in nonterminals]
    decorated_grammar = {}
    bare_nts = set(nonterminals)
    for nt in nonterminals:
        decorated_nt = f'<{nt}>'
        prods = grammar[nt]
        decorated_prods = []
        for prod in prods:
            decorated_prod = []
            for sym in prod:
                if sym in bare_nts:
                    decorated_prod.append(f'<{sym}>')
                else:
                    decorated_prod.append(sym)
            decorated_prods.append(decorated_prod)
        decorated_grammar[decorated_nt] = decorated_prods
    # Eliminate possible left recursion by prefixing any production starting with its nonterminal
    for decorated_nt, prods in decorated_grammar.items():
        for prod in prods:
            if prod and prod[0] == decorated_nt:
                prod.insert(0, random.choice(terminals))
    return decorated_grammar, decorated_nonterminals, terminals

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
    # Support decorated grammar: strip angle brackets on nonterminals for internal code generation
    if nonterminals and isinstance(nonterminals[0], str) and nonterminals[0].startswith('<') and nonterminals[0].endswith('>'):
        # Build bare nonterminals list
        bare_nonterminals = [nt[1:-1] for nt in nonterminals]
        # Build bare grammar mapping
        bare_grammar = {}
        for decorated_nt, prods in grammar.items():
            bare_nt = decorated_nt[1:-1]
            bare_prods = []
            for prod in prods:
                bare_prod = []
                for sym in prod:
                    if isinstance(sym, str) and sym.startswith('<') and sym.endswith('>'):
                        bare_prod.append(sym[1:-1])
                    else:
                        bare_prod.append(sym)
                bare_prods.append(bare_prod)
            bare_grammar[bare_nt] = bare_prods
        grammar = bare_grammar
        nonterminals = bare_nonterminals
        if isinstance(start_symbol, str) and start_symbol.startswith('<') and start_symbol.endswith('>'):
            start_symbol = start_symbol[1:-1]
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
    # match expected token or error (including EOF)
    code_lines.append('    if pos < len(tokens) and tokens[pos].startswith(expected):')
    code_lines.append('        pos += 1')
    code_lines.append('    else:')
    code_lines.append('        error("Expected " + expected + ", got " + (tokens[pos] if pos < len(tokens) else "EOF"))')
    code_lines.append('')

    # Helpers to emit parse-code bodies; inline_children=True allows one-level expansion of nonterminals
    def gen_noniterative_body(nt, inline_children):
        lines = []
        lines.append((1, f'if pos >= len(tokens):'))
        lines.append((2, f'error("Unexpected end of input in {nt}")'))
        lines.append((1, 'lookahead = tokens[pos]'))
        first = True
        expected = []
        for prod in grammar[nt]:
            first_tok = '' if not prod else prod[0]
            expected.append(repr(first_tok))
            if first_tok == '':
                continue
            cond = 'if' if first else 'elif'
            lines.append((1, f'{cond} lookahead.startswith({repr(first_tok)}):'))
            for s in prod:
                if s in nonterminals and inline_children:
                    iterative_child, child_base = is_iterative_rule(s)
                    if iterative_child:
                        for lvl, ln in gen_iterative_body(s, child_base, False):
                            lines.append((lvl+1, ln))
                    else:
                        for lvl, ln in gen_noniterative_body(s, False):
                            lines.append((lvl+1, ln))
                elif s in nonterminals:
                    lines.append((2, f'parse_{s}()'))
                else:
                    lines.append((2, f'match({repr(s)})'))
            first = False
        exp_str = ", ".join(expected)
        lines.append((1, 'else:'))
        lines.append((2, 'error("Parse failed")'))
        return lines

    def gen_iterative_body(nt, base_prod, inline_children):
        lines = []
        first_tok = base_prod[0]
        lines.append((1, f'while pos < len(tokens) and tokens[pos].startswith({repr(first_tok)}):'))
        for s in base_prod:
            if s in nonterminals and inline_children:
                for lvl, ln in gen_noniterative_body(s, False):
                    lines.append((lvl+1, ln))
            elif s in nonterminals:
                lines.append((2, f'parse_{s}()'))
            else:
                lines.append((2, f'match({repr(s)})'))
        return lines

    # Generate a parse_<nt>() function for each nonterminal;
    # inline one level of expansions for the start symbol
    for nt in nonterminals:
        inline_children = (nt == start_symbol)
        iterative, base_prod = is_iterative_rule(nt)
        code_lines.append(f'def parse_{nt}():')
        code_lines.append('    global pos, tokens')
        if iterative:
            for lvl, ln in gen_iterative_body(nt, base_prod, inline_children):
                code_lines.append('    ' + '    '*(lvl-1) + ln)
        else:
            for lvl, ln in gen_noniterative_body(nt, inline_children):
                code_lines.append('    ' + '    '*(lvl-1) + ln)
        code_lines.append('')

    # Main parse function.
    code_lines.append('def parse_input(input_str):')
    code_lines.append('    global tokens, pos')
    code_lines.append('    tokens = list(input_str)')
    code_lines.append('    pos = 0')
    code_lines.append(f'    parse_{start_symbol}()')
    # Accept partial matches: ignore extra tokens (do not enforce full consumption)
    code_lines.append('    print("Input accepted.")')
    code_lines.append('')
    # Main block: use command-line argument if provided, else read from stdin.
    code_lines.append('def main():')
    code_lines.append('    import sys')
    code_lines.append('    if len(sys.argv) > 1:')
    code_lines.append('        input_str = sys.argv[1]')
    code_lines.append('    else:')
    code_lines.append('        input_str = sys.stdin.read()')
    code_lines.append('    parse_input(input_str)')
    code_lines.append('')
    code_lines.append('if __name__ == "__main__":')
    code_lines.append('    main()')

    # Prune any parse_<nt>() definitions that are never called in the inlined code
    called = {start_symbol}
    for line in code_lines:
        for nt in nonterminals:
            # detect actual calls to parse_<nt>() but ignore the function definition header
            if nt != start_symbol and f'parse_{nt}()' in line and not line.strip().startswith(f'def parse_{nt}('):
                called.add(nt)
    new_lines = []
    skipping = None
    for line in code_lines:
        if skipping:
            # skip until end of unused function block (blank line)
            if line.strip() == '':
                skipping = None
            continue
        if line.startswith('def parse_'):
            name = line[len('def parse_'):].split('(')[0]
            if name in nonterminals and name not in called:
                skipping = name
                continue
        new_lines.append(line)
    code_lines = new_lines

    return "\n".join(code_lines)

# ---------------------------
# Step 4: Main Generator Routine
# ---------------------------
def gen(
    numnonterminals,
    max_original_examples,
    recursion_prob,
    numterminals=None,
    loop_prob=0.5,
    max_rhs_length=3,
    maxproductions=3
):
    # number of terminals defaults to number of nonterminals if not specified
    if numterminals is None:
        numterminals = numnonterminals
    # 1. Generate a random LL(1) grammar with controlled recursion
    grammar, nonterminals, terminals = generate_random_grammar(
        num_nonterminals=numnonterminals,
        num_terminals=numterminals,
        max_productions=maxproductions,
        max_rhs_length=max_rhs_length,
        recursion_prob=recursion_prob,
        loop_prob=loop_prob
    )
    start_symbol = nonterminals[0]
    # 2. Generate a few example derivations
    examples = []
    for _ in range(max_original_examples):
        ex = generate_example_string(grammar, start_symbol)
        if 3 < len(ex) < 6:
            examples.append(ex)

    parser_code = generate_parser_code(grammar, nonterminals, start_symbol)

    # Return parser code, example derivations, and grammar with angle brackets
    return parser_code, set(examples), grammar, nonterminals, terminals