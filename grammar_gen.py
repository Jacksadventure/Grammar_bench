import random
import string
import sys
import textwrap
from collections import deque
from itertools import product as cart

from ultility import grammar_printer

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

        # ─── ① optional tail-recursion pair A -> α b A | ε ───────────────────────
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
        TERM_POOL = [
            ch for ch in (
                string.ascii_letters + string.digits +
                "!#$%&()*+,-./:;<=>?@[]^_`{|}~"
            ) if ch not in NT_POOL
        ]
        random.shuffle(TERM_POOL)
    # Ensure the grammar is complete and contains the requested number of nonterminals.
    # If not, the generation process has failed, and we rely on the caller's
    # retry logic to try again.
    if len(grammar) != num_nonterminals:
        raise RuntimeError(
            f"Generated grammar has {len(grammar)} nonterminals, but "
            f"{num_nonterminals} were requested. This may be due to exhausting "
            f"the terminal pool or a generation logic error."
        )

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
    import textwrap

    # -------------------------------------------------------------
    # Step 1: Normalize grammar symbols (remove angle brackets <>)
    # -------------------------------------------------------------
    bare_nonterminals = [nt[1:-1] for nt in nonterminals]
    bare_start = start_symbol[1:-1]

    bare_grammar, is_nullable = {}, {}
    for dec_nt, prods in grammar.items():
        nt = dec_nt[1:-1]
        lst = []
        for p in prods:
            if not p:
                # Empty production → nullable nonterminal
                is_nullable[nt] = True
                lst.append([])  # Represent epsilon (ε) as an empty list
            else:
                # Remove <> from nonterminals, leave terminals as is
                lst.append([sym[1:-1] if sym.startswith("<") else sym for sym in p])
        bare_grammar[nt] = lst

    grammar = bare_grammar
    nonterminals = set(bare_nonterminals)

    # -------------------------------------------------------------
    # Step 2: Compute FIRST sets for each nonterminal (with ε)
    # -------------------------------------------------------------
    EPS = object()  # Unique marker for epsilon
    first_sets = {nt: (set([EPS]) if is_nullable.get(nt, False) else set())
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
                        # Add all FIRST(sym) except ε
                        first_sets[nt].update(x for x in first_sets[sym] if x is not EPS)
                        if len(first_sets[nt]) > before:
                            changed = True
                        # If sym cannot be empty, stop
                        if EPS not in first_sets[sym]:
                            nullable_prefix = False
                            break
                    else:
                        # Terminal: add it and stop
                        if sym not in first_sets[nt]:
                            first_sets[nt].add(sym)
                            changed = True
                        nullable_prefix = False
                        break
                if nullable_prefix and EPS not in first_sets[nt]:
                    first_sets[nt].add(EPS)
                    changed = True

    # Helper: compute FIRST set of a single production
    def first_of_prod(prod):
        s = set()
        for sym in prod:
            if sym in nonterminals:
                s.update(x for x in first_sets[sym] if x is not EPS)
                if EPS not in first_sets[sym]:
                    return s, False
            else:
                s.add(sym)
                return s, False
        return s, True  # Entire production can be empty

    # -------------------------------------------------------------
    # Step 3: Build predictive parsing decisions (lookahead table)
    # -------------------------------------------------------------
    decisions = {}
    for nt, prods in grammar.items():
        cases = []
        epsilon_added = False
        for prod in prods:
            look, nullable = first_of_prod(prod)
            if look:
                cases.append((sorted(look), prod))
            if nullable and not epsilon_added:
                # Special marker for epsilon production
                cases.append(('__EPS__', []))
                epsilon_added = True
        decisions[nt] = cases

    # Collect all terminals (for debugging / error messages)
    terminals = set()
    for nt, prods in grammar.items():
        for prod in prods:
            for sym in prod:
                if sym not in nonterminals:
                    terminals.add(sym)

    # -------------------------------------------------------------
    # Step 4: Convert decision table into a Python parser (iterative)
    # -------------------------------------------------------------
    IND = " " * 4

    def dumps_cases():
        """Convert decision table into Python code literal."""
        def dump_prod(prod):
            return "[" + ", ".join(repr(x) for x in prod) + "]"

        lines = []
        lines.append("{")
        for nt, cases in decisions.items():
            lines.append(f"{IND}{repr(nt)}: [")
            for look, prod in cases:
                if look == '__EPS__':
                    lines.append(f"{IND*2}({{'__EPS__'}}, {dump_prod(prod)}),")
                else:
                    lines.append(f"{IND*2}({{{', '.join(repr(x) for x in look)}}}, {dump_prod(prod)}),")
            lines.append(f"{IND}],")
        lines.append("}")
        return "\n".join(lines)

    src = [
        "import sys",
        "",
        f"NONTERMINALS = {sorted(nonterminals)!r}",
        f"TERMINALS = {sorted(terminals)!r}",
        f"START = {bare_start!r}",
        "",
        "# DECISIONS: for each nonterminal, a list of (lookahead set, production).",
        "# Special lookahead {'__EPS__'} means epsilon (empty production).",
        f"DECISIONS = {dumps_cases()}",
        "",
        "class ParseError(Exception):",
        "    pass",
        "",
        "def parse(inp):",
        "    tokens = list(inp.strip())",  # Input as a list of tokens (characters here)
        "    pos = 0",                      # Current position in tokens
        "    stack = [START]",              # Explicit stack for iterative parsing",
        "",
        "    def peek_la():",
        "        return tokens[pos] if pos < len(tokens) else None",
        "",
        "    while stack:",
        "        top = stack.pop()",        # Take top of stack
        "        la = peek_la()",           # Lookahead symbol
        "",
        "        if top not in NONTERMINALS:",
        "            # Terminal: must match exactly",
        "            if la == top:",
        "                pos += 1",
        "            else:",
        "                got = la if la is not None else 'EOF'",
        "                raise ParseError(f\"Expected {top!r}, got {got!r}\")",
        "            continue",
        "",
        "        # Nonterminal: choose a production based on lookahead",
        "        chosen = None",
        "        cases = DECISIONS.get(top, [])",
        "        for look, prod in cases:",
        "            if '__EPS__' in look:",
        "                if chosen is None:",
        "                    chosen = prod  # Save epsilon as fallback",
        "                continue",
        "            if la in look:",
        "                chosen = prod",
        "                break",
        "",
        "        if chosen is None:",
        "            got = la if la is not None else 'EOF'",
        "            raise ParseError(f\"Unexpected token {got!r} in <{top}>\")",
        "",
        "        # Push production symbols in reverse order (so first symbol is on top)",
        "        for sym in reversed(chosen):",
        "            stack.append(sym)",
        "",
        "    # If parsing finishes but tokens remain, it's an error",
        "    if pos < len(tokens):",
        "        tail = ''.join(tokens[pos:])",
        "        raise ParseError(f\"Extra input at end: {tail}\")",
        '    print(\"Input accepted.\")',
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
    # grammar_printer(nts, grammar)
    start_symbol = nts[0]
    examples = set()
    # for _ in range(max_original_examples * 5):
    #     ex = generate_example_string(grammar, start_symbol)
    #     examples.add(ex)
    #     if len(examples) >= max_original_examples:
    #         break
    parser_code = generate_parser_code(grammar, nts, start_symbol)
    return parser_code, examples, grammar, nts, ts

# ───────────────────────── self-test / CLI ─────────────────────────────────
if __name__ == "__main__":
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 5000))

    code, exs, g, nts, ts = gen(
        num_nonterminals=40,
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