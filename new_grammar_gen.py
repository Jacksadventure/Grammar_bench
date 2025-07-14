#!/usr/bin/env python3
"""
Random EBNF grammar generator
─────────────────────────────
• Produces a self-contained EBNF grammar string on stdout.
• Guarantees every non-terminal can eventually derive only terminals (adds ε if needed).
• Uses *, +, ?, concatenation, and choice (|) at random.
"""

from __future__ import annotations
import argparse, random, string, itertools

# ------------------------- configurable params ------------------------- #
DEFAULT_TERMINALS = list(string.ascii_lowercase)         # a … z
MIN_PRODS_PER_NT   = 1
MAX_PRODS_PER_NT   = 3
MAX_SEQ_LEN        = 4                                   # tokens in one sequence
STAR_PROB, PLUS_PROB, OPT_PROB = 0.15, 0.15, 0.10        # chance to wrap ()*  ()+  ()?
REC_SYMBOL_PROB = 0.30                                   # chance to include *this* NT
# ---------------------------------------------------------------------- #


def random_nt(idx: int) -> str:
    return f"<N{idx}>" if idx else "<S>"                # <S> is start symbol


def choose_terminal() -> str:
    return random.choice(DEFAULT_TERMINALS)


def gen_sequence(nt_index: int, nts: list[str]) -> list[str]:
    """Return a random list of tokens (terminals / non-terminals)."""
    seq = []
    length = random.randint(1, MAX_SEQ_LEN)
    for _ in range(length):
        if random.random() < 0.5:                       # terminal
            seq.append(choose_terminal())
        else:                                           # some non-terminal
            # 30% chance to choose this non-terminal (left recursion), otherwise select a random other one
            if random.random() < REC_SYMBOL_PROB:
                seq.append(random_nt(nt_index))
            else:
                seq.append(random.choice(nts))
    return seq


def wrap_ebnf(seq: list[str]) -> list[str]:
    """Randomly wrap sequence in (), then apply *, + or ?."""
    # do not wrap empty productions
    if not seq:
        return seq
    if random.random() < (STAR_PROB + PLUS_PROB + OPT_PROB):
        mod = random.choices(["*", "+", "?"], [STAR_PROB, PLUS_PROB, OPT_PROB])[0]
        return ["("] + seq + [")", mod]
    return seq


def ensure_generating(grammar: dict[str, list[list[str]]], nts: list[str]) -> None:
    """Add ε to purely left-recursive or non-generating NTs."""
    generating = set()           # NTs known to derive terminals
    changed = True
    while changed:
        changed = False
        for nt, alts in grammar.items():
            if nt in generating:
                continue
            for prod in alts:
                if all(tok not in grammar or tok in generating for tok in prod):
                    generating.add(nt)
                    changed = True
                    break

    for nt in nts:
        if nt not in generating:
            grammar[nt].append([])   # add empty production

def ensure_reachable(grammar: dict[str, list[list[str]]], nts: list[str]) -> None:
    """Add productions to start symbol so every non-terminal is reachable from <S>."""
    start = nts[0]
    reachable = {start}
    stack = [start]
    while stack:
        nt = stack.pop()
        for prod in grammar.get(nt, []):
            for tok in prod:
                if tok in grammar and tok not in reachable:
                    reachable.add(tok)
                    stack.append(tok)
    for nt in nts:
        if nt not in reachable:
            grammar[start].append([nt])


def grammar_to_ebnf(grammar: dict[str, list[list[str]]], nts: list[str]) -> str:
    lines = []
    for nt in nts:
        rhs_parts = []
        for prod in grammar[nt]:
            if not prod:
                rhs_parts.append("ε")                    # display ε explicitly
            else:
                rhs_parts.append(" ".join(prod))
        lines.append(f"{nt} := " + " | ".join(rhs_parts))
    return "\n".join(lines)

def remove_left_recursion(grammar: dict[str, list[list[str]]],
                          nts: list[str]) -> tuple[dict[str, list[list[str]]], list[str]]:
    """Eliminate left recursion (direct and indirect) from the grammar."""
    new_grammar: dict[str, list[list[str]]] = {}
    new_nts: list[str] = []
    for Ai in nts:
        # replace indirect left recursion for previous nonterminals
        prods = grammar[Ai]
        updated: list[list[str]] = []
        for prod in prods:
            if prod and prod[0] in new_nts:
                Aj = prod[0]
                rest = prod[1:]
                for delta in new_grammar[Aj]:
                    updated.append(delta + rest)
            else:
                updated.append(prod)
        # separate direct left recursion
        alpha: list[list[str]] = []
        beta: list[list[str]] = []
        for prod in updated:
            if prod and prod[0] == Ai:
                alpha.append(prod[1:])
            else:
                beta.append(prod)
        if alpha:
            # direct left recursion exists: introduce a fresh non-terminal for recursion
            base_name = Ai.strip("<>")
            Ai_p = f"<{base_name}_prime>"
            # if no non-left-recursive alternatives, add ε to beta so A -> A'
            if not beta:
                beta.append([])
            new_nts.append(Ai)
            new_nts.append(Ai_p)
            new_grammar[Ai] = []
            new_grammar[Ai_p] = []
            for b in beta:
                new_grammar[Ai].append(b + [Ai_p])
            for a in alpha:
                new_grammar[Ai_p].append(a + [Ai_p])
            new_grammar[Ai_p].append([])  # ε
        else:
            new_nts.append(Ai)
            new_grammar[Ai] = beta
    return new_grammar, new_nts


def generate_grammar(n_nonterms: int) -> str:
    nts = [random_nt(i) for i in range(n_nonterms)]
    grammar: dict[str, list[list[str]]] = {nt: [] for nt in nts}

    # create random productions (raw, without EBNF quantifiers)
    for idx, nt in enumerate(nts):
        n_prods = random.randint(MIN_PRODS_PER_NT, MAX_PRODS_PER_NT)
        for _ in range(n_prods):
            seq = gen_sequence(idx, nts)
            grammar[nt].append(seq)

    # safety pass: guarantee termination
    ensure_generating(grammar, nts)
    # ensure every non-terminal is reachable from the start symbol
    ensure_reachable(grammar, nts)
    # eliminate left recursion and ensure new symbols generate
    grammar, nts = remove_left_recursion(grammar, nts)
    ensure_generating(grammar, nts)
    ensure_reachable(grammar, nts)
    # apply random EBNF wrapping (*, +, ?) after eliminating left recursion
    for nt in nts:
        grammar[nt] = [wrap_ebnf(prod) for prod in grammar[nt]]
    # ensure each production alternative starts with a terminal
    for nt in nts:
        for i, prod in enumerate(grammar[nt]):
            # if the first symbol is not one of the defined terminals, prefix a terminal
            if prod and prod[0] not in DEFAULT_TERMINALS:
                grammar[nt][i] = [choose_terminal()] + prod
    return grammar_to_ebnf(grammar, nts)


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate random terminating EBNF grammar.")
    ap.add_argument("-n", "--nonterm", type=int, default=4,
                    help="number of non-terminals (default: 4 incl. <S>)")
    ap.add_argument("-s", "--seed", type=int, help="random seed")
    args = ap.parse_args()
    if args.seed is not None:
        random.seed(args.seed)

    print(generate_grammar(max(2, args.nonterm)))       # minimum 2 NTs


if __name__ == "__main__":
    main()
