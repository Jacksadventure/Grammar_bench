"""
This generator (grammar_gen.py) produces a random LL(1) grammar and a
standalone recursive descent parser.

The generation logic is now strictly forward-referencing to guarantee
no cycles between non-terminals (e.g. A -> B, B -> A) can be created.
"""

import random, string
from collections import deque
from itertools import product as cart

def _labels(alpha, k):
    out, n = [], 1
    while len(out) < k:
        for p in cart(alpha, repeat=n):
            out.append("".join(p))
            if len(out) >= k:
                break
        n += 1
    return out[:k]

def generate_random_grammar(
    num_nonterminals=10,
    nonterminal_prob=0.5,
    loop_prob=0.3,
    max_productions=5,
    max_rhs_length=5,
):
    """BFS build; every RHS NT is brand-new; guarantees *all* NTs are used."""
    # ---------- pools ----------
    NT_POOL = _labels(list(string.ascii_uppercase), num_nonterminals)
    # Terminals ≠ any NT label
    TERM_POOL = [
        ch for ch in string.ascii_letters + string.digits +
        "!#$%&()*+,-./:;<=>?@[]^_`{|}~"
        if ch not in NT_POOL
    ]
    random.shuffle(TERM_POOL)

    grammar, used_firsts = {}, set()
    queue = deque([NT_POOL.pop(0)])        # start symbol
    last_nt = None

    while queue or NT_POOL:                # keep going until NT pool drained
        # ---------------- choose LHS ----------------
        if queue:
            nt = queue.popleft()
            last_nt = nt
        else:
            # queue empty but still have unused NTs → graft onto last LHS
            nt = last_nt
        prods = grammar.setdefault(nt, [])

        # helper: fresh first terminal
        def next_first_terminal():
            if not TERM_POOL:
                raise RuntimeError("Ran out of terminals for FIRST sets")
            t = TERM_POOL.pop(0)
            used_firsts.add(t)
            return t

        # ---------- maybe self-loop ----------
        if loop_prob and random.random() < loop_prob and max_rhs_length >= 2:
            first = next_first_terminal()
            alpha = [first]
            for _ in range(random.randint(0, max_rhs_length - 2)):
                alpha.append(random.choice(TERM_POOL))
            prods += [alpha + [nt], []]

        # ---------- regular productions ----------
        n_prods = random.randint(1, max_productions)
        for _ in range(n_prods):
            first = next_first_terminal()
            rhs = [first]
            rhs_len = random.randint(1, max_rhs_length)

            for _ in range(rhs_len - 1):
                if NT_POOL and random.random() < nonterminal_prob:
                    fresh = NT_POOL.pop(0)
                    rhs.append(fresh)
                    queue.append(fresh)    # schedule for expansion
                else:
                    rhs.append(random.choice(TERM_POOL))
            prods.append(rhs)

    # ---------- decorate ----------
    decorated_nts = [f"<{n}>" for n in grammar]
    decorated = {
        f"<{lhs}>": [
            [f"<{sym}>" if sym in grammar else sym for sym in rhs]
            for rhs in rhss
        ]
        for lhs, rhss in grammar.items()
    }
    terminals_used = list(used_firsts)
    return decorated, decorated_nts, terminals_used

# ---------------------------
# Step 2: Example Generation (Unchanged)
# ---------------------------
def generate_example_string(grammar, symbol, max_depth=10):
    # ... (code is unchanged)
    if symbol not in grammar or max_depth <= 0:
        return "" if (isinstance(symbol, str) and symbol.startswith('<')) else symbol
    prods = sorted(grammar[symbol], key=len); prod = random.choice(prods[:2]); result = []
    for s in prod:
        result.append(generate_example_string(grammar, s, max_depth-1) if s in grammar else s)
    return "".join(result)

def generate_parser_code(grammar, nonterminals, start_symbol):
    """
    Build a self-contained recursive-descent parser (single Python file).

    • Detect A → α A | ε and emit a `while` loop for α*
    • After the loop, still examine any *other* productions of A
      (e.g.  l<B>  /  n e <C><D>), plus ε when allowed.
    • All remaining non-terminals are expanded in-line.
    """
    # ---------- 1. strip decorations ----------
    bare_nonterminals = [nt[1:-1] for nt in nonterminals]
    bare_start = start_symbol[1:-1]

    bare_grammar, is_nullable = {}, {}
    for dec_nt, prods in grammar.items():
        nt = dec_nt[1:-1]
        bare_grammar[nt] = []
        for p in prods:
            if not p:                         # ε
                is_nullable[nt] = True
            else:
                bare_grammar[nt].append(
                    [sym[1:-1] if sym.startswith('<') else sym for sym in p]
                )
        if is_nullable.get(nt, False) and nt not in bare_grammar:
            bare_grammar[nt] = []

    grammar = bare_grammar
    nonterminals = bare_nonterminals

    # ---------- 2. FIRST sets ----------
    EPS = object()
    first_sets = {nt: ({EPS} if is_nullable.get(nt, False) else set())
                  for nt in nonterminals}

    changed = True
    while changed:
        changed = False
        for nt, prods in grammar.items():
            for prod in prods:
                nullable_prefix = True
                for sym in prod:
                    if sym in nonterminals:
                        before = len(first_sets[nt])
                        first_sets[nt].update(x for x in first_sets[sym] if x is not EPS)
                        if len(first_sets[nt]) > before:
                            changed = True
                        if EPS not in first_sets[sym]:
                            nullable_prefix = False
                            break
                    else:                     # terminal
                        if sym not in first_sets[nt]:
                            first_sets[nt].add(sym)
                            changed = True
                        nullable_prefix = False
                        break
                if nullable_prefix and EPS not in first_sets[nt]:
                    first_sets[nt].add(EPS)
                    changed = True

    def first_seq(seq):
        """FIRST set of a sequence (ignoring EPS)."""
        look = set()
        for sym in seq:
            if sym not in nonterminals:
                look.add(sym)
                return look
            look.update(x for x in first_sets[sym] if x is not EPS)
            if EPS not in first_sets[sym]:
                return look
        return look  # seq is fully nullable

    def is_iterative(nt):
        """Return (True, alpha) if nt has rule α A | ε."""
        if not is_nullable.get(nt, False):
            return False, None
        for prod in grammar.get(nt, []):
            if prod and prod[-1] == nt:
                return True, prod[:-1]
        return False, None

    # ---------- 3. code-block generation ----------
    memo = {}
    def gen_block(nt, lvl):
        key = (nt, lvl)
        if key in memo:
            return memo[key]
        ind = '    ' * lvl
        lines = []

        iterative, alpha = is_iterative(nt)
        if iterative:
            # ----- part-1: α* -----
            lookahead = first_seq(alpha)
            conds = ' or '.join(f"tokens[pos] == {repr(t)}" for t in sorted(lookahead)) or 'False'
            lines.append(f"{ind}# Iterative rule for <{nt}> → {alpha}*")
            lines.append(f"{ind}while pos < len(tokens) and ({conds}):")
            for s in alpha:
                lines.extend(gen_sym(s, lvl + 1))

            # ----- part-2: remaining alternatives -----
            remaining = [
                p for p in grammar[nt]
                if p not in (alpha + [nt], [])            # drop loop & ε
            ]
            if remaining or is_nullable.get(nt, False):
                lines.append(f"{ind}# After loop: choose the rest of <{nt}>")
                lines.append(f"{ind}if pos < len(tokens):")
                lines.append(f"{ind}    la = tokens[pos]")
                first_branch = True
                for prod in remaining:
                    fs = first_seq(prod)
                    if not fs:
                        continue
                    kw = "if" if first_branch else "elif"
                    conds = ' or '.join(f"la == {repr(t)}" for t in sorted(fs))
                    lines.append(f"{ind}    {kw} {conds}:")
                    for s in prod:
                        lines.extend(gen_sym(s, lvl + 2))
                    first_branch = False
                if is_nullable.get(nt, False):
                    lines.append(f"{ind}    {'if' if first_branch else 'elif'} True:  # ε")
                    lines.append(f"{ind}        pass")
                else:
                    lines.append(f"{ind}    else:")
                    lines.append(f"{ind}        raise ParseError(f'Unexpected token {{la!r}} in <{nt}>')")
            # else: no remaining alts and not nullable – nothing further.
        else:
            # ---------- standard multi-branch ----------
            lines.append(f"{ind}# Standard rule set for <{nt}>")
            lines.append(f"{ind}if pos >= len(tokens):")
            if is_nullable.get(nt, False):
                lines.append(f"{ind}    pass  # nullable at EOF")
            else:
                lines.append(f"{ind}    raise ParseError('Unexpected EOF in <{nt}>')")
            lines.append(f"{ind}else:")
            lines.append(f"{ind}    la = tokens[pos]")
            first_branch = True
            for prod in grammar[nt]:
                fs = first_seq(prod)
                if not fs:
                    continue
                kw = 'if' if first_branch else 'elif'
                conds = ' or '.join(f"la == {repr(t)}" for t in sorted(fs))
                lines.append(f"{ind}    {kw} {conds}:")
                for s in prod:
                    lines.extend(gen_sym(s, lvl + 2))
                first_branch = False
            if is_nullable.get(nt, False):
                lines.append(f"{ind}    {'if' if first_branch else 'elif'} True:  # ε")
                lines.append(f"{ind}        pass")
            else:
                lines.append(f"{ind}    else:")
                lines.append(f"{ind}        raise ParseError(f'Unexpected token {{la!r}} in <{nt}>')")

        memo[key] = lines
        return lines

    def gen_sym(sym, lvl):
        ind = '    ' * lvl
        if sym in nonterminals:
            return gen_block(sym, lvl)
        return [f"{ind}match({repr(sym)})"]

    # ---------- 4. assemble source ----------
    src = [
        'import sys',
        '',
        'tokens = []',
        'pos = 0',
        '',
        'class ParseError(Exception):',
        '    pass',
        '',
        'def match(expected):',
        '    global pos',
        '    if pos < len(tokens) and tokens[pos] == expected:',
        '        pos += 1',
        '    else:',
        '        got = tokens[pos] if pos < len(tokens) else "EOF"',
        '        raise ParseError(f"Expected {expected!r}, got {got!r}")',
        '',
        'def parse(inp):',
        '    global tokens, pos',
        '    tokens = list(inp.strip())',
        '    pos = 0',
    ]
    src.extend(gen_block(bare_start, 1))
    src.extend([
        '    if pos < len(tokens):',
        '        raise ParseError(f"Extra input at end: {\'\'.join(tokens[pos:])}")',
        '    print("Input accepted.")',
        '',
        "if __name__ == '__main__':",
        '    if len(sys.argv) < 2:',
        '        print("Usage: python generated_parser.py <string>")',
        '        sys.exit(1)',
        '    try:',
        '        parse(sys.argv[1])',
        '    except ParseError as err:',
        '        print("Input rejected.")',
        '        print(err)',
    ])
    return '\n'.join(src)

def gen(
    numnonterminals, max_original_examples, nonterminal_prob,
    loop_prob=0.3, max_rhs_length=3, maxproductions=3,
):
    # ... (code is unchanged)
    grammar, nonterminals, terminals = generate_random_grammar(
        num_nonterminals=numnonterminals, nonterminal_prob=nonterminal_prob,
        loop_prob=loop_prob, max_productions=maxproductions, max_rhs_length=max_rhs_length,
    )
    if not nonterminals:
        print("Warning: Grammar generation resulted in no nonterminals.")
        return None, set(), {}, [], []
    start_symbol = nonterminals[0]
    examples = set()
    for _ in range(max_original_examples * 5):
        ex = generate_example_string(grammar, start_symbol)
        if 3 <= len(ex) < 15 and ex not in examples:
            examples.add(ex)
            if len(examples) >= max_original_examples: break
    parser_code = generate_parser_code(grammar, nonterminals, start_symbol)
    return parser_code, examples, grammar, nonterminals, terminals

if __name__ == '__main__':
    code, exs, g, nts, ts = gen(
        numnonterminals=1, max_original_examples=3, nonterminal_prob=0.1,
        loop_prob=0.3, max_rhs_length=1, maxproductions=1,
    )
    if code:
        print("--- Generated Grammar ---")
        for nt in nts:
            prods = g.get(nt, []); prod_strs = [' '.join(p) if p else 'ε' for p in prods]
            print(f"{nt.ljust(5)} -> {' | '.join(prod_strs)}")
        print("\n--- Example Derivations ---")
        print(exs if exs else "No suitable examples were generated.")
        with open("generated_parser.py", "w") as f: f.write(code)
        print("\nParser code saved to generated_parser.py")
