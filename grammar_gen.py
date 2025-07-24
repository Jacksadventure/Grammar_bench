import random
import string
import sys
import textwrap
from collections import deque
from itertools import product as cart

# ───────────────────────── helper: label factory ────────────────────────────
def _labels(alpha, k: int):
    out, n = [], 1
    while len(out) < k:
        for p in cart(alpha, repeat=n):
            out.append("".join(p))
            if len(out) >= k:
                break
        n += 1
    return out[:k]

# ───────────────────────── grammar generator (safe) ─────────────────────────
def generate_random_grammar(
    num_nonterminals=10,
    nonterminal_prob=0.5,
    loop_prob=0.3,
    max_productions=5,
    max_rhs_length=5,
):
    """
    Build an LL(1) grammar that fulfils:
      • forward-referencing only;
      • each NT expanded once;
      • optional single tail-recursion (α A | ε);
      • every requested NT is used at least once.
    """
    NT_POOL = _labels(list(string.ascii_uppercase), num_nonterminals)
    TERM_POOL = [
        ch for ch in (
            string.ascii_letters + string.digits +
            "!#$%&()*+,-./:;<=>?@[]^_`{|}~"
        ) if ch not in NT_POOL
    ]
    random.shuffle(TERM_POOL)

    grammar, used_firsts = {}, set()
    start_symbol = NT_POOL.pop(0)
    queue = deque([start_symbol])
    expanded = set()

    while queue:
        nt = queue.popleft()
        if nt in expanded:
            continue
        expanded.add(nt)

        prods = grammar.setdefault(nt, [])

        # helper: distinct leading terminal for FIRST disambiguation
        def next_first_terminal():
            if not TERM_POOL:
                raise RuntimeError("Ran out of terminals")
            t = TERM_POOL.pop(0)
            used_firsts.add(t)
            return t

        # ─── ① optional tail-recursion pair  α A | ε ───────────────────────
        if loop_prob and random.random() < loop_prob and max_rhs_length >= 2:
            first = next_first_terminal()
            alpha = [first] + [
                random.choice(TERM_POOL)
                for _ in range(random.randint(0, max_rhs_length - 2))
            ]
            prods += [alpha + [nt], []]      # αA  and  ε

        # ─── ② ordinary productions – consume remaining NT_POOL ────────────
        n_prods = random.randint(1, max_productions)
        for p_i in range(n_prods):
            first = next_first_terminal()
            rhs = [first]

            rhs_len = random.randint(1, max_rhs_length)
            need_new_nt = bool(NT_POOL)          # force at least one fresh NT if any left

            for _ in range(rhs_len - 1):
                if NT_POOL and (need_new_nt or random.random() < nonterminal_prob):
                    fresh = NT_POOL.pop(0)
                    rhs.append(fresh)
                    queue.append(fresh)
                    need_new_nt = False
                else:
                    rhs.append(random.choice(TERM_POOL))

            if need_new_nt and NT_POOL:
                fresh = NT_POOL.pop(0)
                rhs.append(fresh)
                queue.append(fresh)

            prods.append(rhs)

    # decorate with angle brackets for parser readability
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

# ───────────────────────── derive example strings ───────────────────────────
def generate_example_string(grammar, symbol, max_depth=10):
    if symbol not in grammar or max_depth <= 0:
        return "" if (isinstance(symbol, str) and symbol.startswith("<")) else symbol
    prods = sorted(grammar[symbol], key=len)
    prod = random.choice(prods[:2])
    return "".join(
        generate_example_string(grammar, s, max_depth - 1) if s in grammar else s
        for s in prod
    )

# ───────────────────────── parser code generator (memoised) ────────────────
def generate_parser_code(grammar, nonterminals, start_symbol):
    bare_nonterminals = [nt[1:-1] for nt in nonterminals]
    bare_start = start_symbol[1:-1]

    bare_grammar, is_nullable = {}, {}
    for dec_nt, prods in grammar.items():
        nt = dec_nt[1:-1]
        bare_grammar[nt] = []
        for p in prods:
            if not p:
                is_nullable[nt] = True
            else:
                bare_grammar[nt].append(
                    [sym[1:-1] if sym.startswith("<") else sym for sym in p]
                )
        if is_nullable.get(nt, False) and nt not in bare_grammar:
            bare_grammar[nt] = []
    grammar = bare_grammar
    nonterminals = bare_nonterminals

    EPS = object()
    first_sets = {
        nt: ({EPS} if is_nullable.get(nt, False) else set()) for nt in nonterminals
    }
    changed = True
    while changed:
        changed = False
        for nt, prods in grammar.items():
            for prod in prods:
                nullable_prefix = True
                for sym in prod:
                    if sym in nonterminals:
                        before = len(first_sets[nt])
                        first_sets[nt].update(
                            x for x in first_sets[sym] if x is not EPS
                        )
                        changed |= len(first_sets[nt]) > before
                        if EPS not in first_sets[sym]:
                            nullable_prefix = False
                            break
                    else:
                        if sym not in first_sets[nt]:
                            first_sets[nt].add(sym)
                            changed = True
                        nullable_prefix = False
                        break
                if nullable_prefix and EPS not in first_sets[nt]:
                    first_sets[nt].add(EPS)
                    changed = True

    def first_seq(seq):
        look = set()
        for sym in seq:
            if sym not in nonterminals:
                look.add(sym)
                return look
            look.update(x for x in first_sets[sym] if x is not EPS)
            if EPS not in first_sets[sym]:
                return look
        return look

    def is_iterative(nt):
        if not is_nullable.get(nt, False):
            return False, None
        for prod in grammar.get(nt, []):
            if prod and prod[-1] == nt:
                return True, prod[:-1]
        return False, None

    memo = {}
    INDENT = "    "

    def gen_block(nt, lvl):
        if nt in memo:
            return textwrap.indent(memo[nt], INDENT * lvl).splitlines()

        ind = INDENT * lvl
        lines = []
        iterative, alpha = is_iterative(nt)

        if iterative:
            lookahead = first_seq(alpha)
            conds = " or ".join(f"tokens[pos] == {repr(t)}" for t in sorted(lookahead)) or "False"
            lines += [
                f"{ind}# α* loop for <{nt}>",
                f"{ind}while pos < len(tokens) and ({conds}):",
            ]
            for s in alpha:
                lines.extend(gen_sym(s, lvl + 1))

            remaining = [p for p in grammar[nt] if p not in (alpha + [nt], [])]
            if remaining or is_nullable.get(nt, False):
                lines += [
                    f"{ind}# other alts of <{nt}>",
                    f"{ind}if pos < len(tokens):",
                    f"{ind}{INDENT}la = tokens[pos]",
                ]
                first_branch = True
                for prod in remaining:
                    fs = first_seq(prod)
                    if not fs:
                        continue
                    kw = "if" if first_branch else "elif"
                    conds = " or ".join(f"la == {repr(t)}" for t in sorted(fs))
                    lines.append(f"{ind}{INDENT}{kw} {conds}:")
                    for s in prod:
                        lines.extend(gen_sym(s, lvl + 2))
                    first_branch = False
                if is_nullable.get(nt, False):
                    lines += [
                        f"{ind}{INDENT}{'if' if first_branch else 'elif'} True:  # ε",
                        f"{ind}{INDENT * 2}pass",
                    ]
                else:
                    lines += [
                        f"{ind}{INDENT}else:",
                        f"{ind}{INDENT * 2}raise ParseError(f'Unexpected token {{la!r}} in <{nt}>')",
                    ]
        else:
            lines += [
                f"{ind}# standard alts for <{nt}>",
                f"{ind}if pos >= len(tokens):",
            ]
            if is_nullable.get(nt, False):
                lines.append(f"{ind}{INDENT}pass  # nullable at EOF")
            else:
                lines.append(f"{ind}{INDENT}raise ParseError('Unexpected EOF in <{nt}>')")
            lines += [f"{ind}else:", f"{ind}{INDENT}la = tokens[pos]"]
            first_branch = True
            for prod in grammar[nt]:
                fs = first_seq(prod)
                if not fs:
                    continue
                kw = "if" if first_branch else "elif"
                conds = " or ".join(f"la == {repr(t)}" for t in sorted(fs))
                lines.append(f"{ind}{INDENT}{kw} {conds}:")
                for s in prod:
                    lines.extend(gen_sym(s, lvl + 2))
                first_branch = False
            if is_nullable.get(nt, False):
                lines += [
                    f"{ind}{INDENT}{'if' if first_branch else 'elif'} True:  # ε",
                    f"{ind}{INDENT * 2}pass",
                ]
            else:
                lines += [
                    f"{ind}{INDENT}else:",
                    f"{ind}{INDENT * 2}raise ParseError(f'Unexpected token {{la!r}} in <{nt}>')",
                ]

        memo[nt] = "\n".join(lines)
        return lines

    def gen_sym(sym, lvl):
        if sym in nonterminals:
            return gen_block(sym, lvl)
        return [f"{INDENT * lvl}match({repr(sym)})"]

    src = [
        "import sys",
        "",
        "tokens = []",
        "pos = 0",
        "",
        "class ParseError(Exception):",
        "    pass",
        "",
        "def match(expected):",
        "    global pos",
        "    if pos < len(tokens) and tokens[pos] == expected:",
        "        pos += 1",
        "    else:",
        "        got = tokens[pos] if pos < len(tokens) else 'EOF'",
        "        raise ParseError(f'Expected {expected!r}, got {got!r}')",
        "",
        "def parse(inp):",
        "    global tokens, pos",
        "    tokens = list(inp.strip())",
        "    pos = 0",
    ]
    src.extend(gen_block(bare_start, 1))
    src.extend(
        [
            "    if pos < len(tokens):",
            "        raise ParseError(f'Extra input at end: {\"\".join(tokens[pos:])}')",
            '    print("Input accepted.")',
            "",
            "if __name__ == '__main__':",
            "    if len(sys.argv) < 2:",
            '        print(\"Usage: python generated_parser.py <string>\")',
            "        sys.exit(1)",
            "    try:",
            "        parse(sys.argv[1])",
            "    except ParseError as err:",
            '        print(\"Input rejected.\")',
            "        print(err)",
        ]
    )
    return "\n".join(src)

# ───────────────────────── public façade ────────────────────────────────────
def gen(
    num_nonterminals=10,
    max_original_examples=5,
    nonterminal_prob=0.5,
    loop_prob=0.3,
    max_rhs_length=3,
    max_productions=3,
):
    grammar, nts, ts = generate_random_grammar(
        num_nonterminals=num_nonterminals,
        nonterminal_prob=nonterminal_prob,
        loop_prob=loop_prob,
        max_productions=max_productions,
        max_rhs_length=max_rhs_length,
    )
    start_symbol = nts[0]
    examples = set()
    for _ in range(max_original_examples * 5):
        ex = generate_example_string(grammar, start_symbol)
        examples.add(ex)
        if len(examples) >= max_original_examples:
            break
    parser_code = generate_parser_code(grammar, nts, start_symbol)
    return parser_code, examples, grammar, nts, ts

# ───────────────────────── self-test / CLI ─────────────────────────────────
if __name__ == "__main__":
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 5000))

    code, exs, g, nts, ts = gen(
        num_nonterminals=1,
        max_original_examples=3,
        nonterminal_prob=0.5,
        loop_prob=0.5,
        max_rhs_length=3,
        max_productions=3,
    )
    print("--- Generated Grammar ---")
    for nt in nts:
        prods = g[nt]
        print(nt.ljust(5), "->", " | ".join(" ".join(p) if p else "ε" for p in prods))
    print("\n--- Example Strings ---")
    print(", ".join(sorted(exs)) if exs else "(none)")
    with open("generated_parser.py", "w") as f:
        f.write(code)
    print("\nParser code saved to generated_parser.py")
