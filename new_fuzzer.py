#!/usr/bin/env python3
"""
Generic grammar-based fuzzer.

1.  Reads an EBNF grammar (subset) from a file or string.
2.  Converts EBNF (supports (), *, +, ?, |) to plain BNF.
3.  Randomly generates test inputs from the grammar.

Author: ChatGPT demo 2025-07-10
"""

import argparse
import itertools
import random
import re
import sys
from typing import Dict, List

###############################################################################
# 1.  Minimal tokenizer for EBNF fragments
###############################################################################

_TOKEN_RE = re.compile(r"<[^>]+>|::=|:=|[\(\)\*\+\?\|]|[^\s\(\)\*\+\?\|]+")


def tokenize(text: str) -> List[str]:
    """Return a list of tokens, preserving EBNF operators."""
    return [t for t in _TOKEN_RE.findall(text) if t.strip()]


###############################################################################
# 2.  EBNF ➜ BNF converter (creates fresh non-terminals <N1>, <N2> ... )
###############################################################################

def convert_ebnf(ebnf: str) -> Dict[str, List[List[str]]]:
    grammar: Dict[str, List[List[str]]] = {}
    nt_counter = itertools.count(1)

    # ---------- helper functions defined BEFORE first use ----------
    def fresh_nt() -> str:
        return f"<N{next(nt_counter)}>"

    def add_production(lhs: str, prod: List[str]) -> None:
        grammar.setdefault(lhs, []).append(prod)

    def expand_rhs(lhs: str, rhs: str) -> None:
        """Expand one RHS EBNF expression into BNF and add to grammar."""
        prods: List[List[str]] = [[]]          # stack of current alternatives
        paren_stack: List[int] = []

        tokens = tokenize(rhs)
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            # --- grouping ---
            if tok == "(":
                paren_stack.append(len(prods))
                prods.append([])
            elif tok == ")":
                if not paren_stack:
                    raise SyntaxError("Unmatched ')'")
                group = prods.pop()
                paren_stack.pop()
                mod = tokens[i + 1] if i + 1 < len(tokens) and tokens[i + 1] in "*+?" else None
                if mod:
                    i += 1
                g_nt = fresh_nt()
                add_production(g_nt, group)
                if mod in ("*", "?"):
                    add_production(g_nt, [])
                if mod in ("*", "+"):
                    add_production(g_nt, group + [g_nt])
                prods[-1].append(g_nt)
            # --- choice ---
            elif tok == "|":
                prods.append([])
            # --- modifiers * + ? ---
            elif tok in "*+?":
                if not prods[-1]:
                    raise SyntaxError(f"Modifier '{tok}' without target")
                prev = prods[-1].pop()
                rep_nt = fresh_nt()
                add_production(rep_nt, [prev])
                if tok in ("*", "?"):
                    add_production(rep_nt, [])
                if tok in ("*", "+"):
                    add_production(rep_nt, [prev, rep_nt])
                prods[-1].append(rep_nt)
            # --- terminal / non-terminal ---
            else:
                prods[-1].append(tok)
            i += 1

        for p in prods:
            add_production(lhs, p)

    # ---------- main scan ----------
    current_lhs: str | None = None
    pending_rhs: List[str] = []

    for raw in map(str.strip, ebnf.splitlines()):
        if not raw or raw.startswith("#"):
            continue
        if ":=" in raw or "::=" in raw:
            if pending_rhs and current_lhs:
                for alt in pending_rhs:
                    expand_rhs(current_lhs, alt)
            lhs, rhs_part = map(str.strip, re.split(r":=|::=", raw, 1))
            current_lhs = lhs if lhs.startswith("<") else f"<{lhs}>"
            pending_rhs = [rhs_part]
        elif raw.startswith("|"):
            pending_rhs.append(raw.lstrip("|").strip())
        else:
            raise SyntaxError(f"Unrecognized line: {raw}")

    if pending_rhs and current_lhs:
        for alt in pending_rhs:
            expand_rhs(current_lhs, alt)

    # deduplicate
    for nt, alts in grammar.items():
        uniq = []
        for p in alts:
            if p not in uniq:
                uniq.append(p)
        grammar[nt] = uniq

    return grammar


###############################################################################
# 3.  Simple grammar-based fuzzer
###############################################################################

class GrammarFuzzer:
    def __init__(self, grammar: Dict[str, List[List[str]]], start: str = "<S>", max_depth: int = 12):
        self.grammar = grammar
        self.start = start
        self.max_depth = max_depth

    def _expand(self, symbol: str, depth: int) -> str:
        # terminal token
        if symbol not in self.grammar or depth >= self.max_depth:
            return symbol
        production = random.choice(self.grammar[symbol])
        return "".join(self._expand(tok, depth + 1) for tok in production)

    def fuzz(self) -> str:
        return self._expand(self.start, 0)


###############################################################################
# 4.  CLI driver
###############################################################################

DEFAULT_EBNF = """
<S> := s
     | (a <A> | b <B>)*
<A> := a <A>
<B> := b <B>
"""

def main() -> None:
    parser = argparse.ArgumentParser(description="Grammar-based fuzzer for EBNF grammars.")
    parser.add_argument("-g", "--grammar", metavar="FILE", help="EBNF grammar file (default: built-in sample)")
    parser.add_argument("-n", "--num", type=int, default=10, help="Number of samples to generate (default: 10)")
    parser.add_argument("--seed", type=int, help="Random seed")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    if args.grammar:
        try:
            with open(args.grammar, "r", encoding="utf-8") as fp:
                ebnf_text = fp.read()
        except OSError as exc:
            sys.exit(f"Failed to read grammar file: {exc}")
    else:
        ebnf_text = DEFAULT_EBNF

    grammar = convert_ebnf(ebnf_text)
    fuzzer = GrammarFuzzer(grammar)

    for _ in range(args.num):
        print(fuzzer.fuzz())


if __name__ == "__main__":
    main()