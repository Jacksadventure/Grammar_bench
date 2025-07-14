#!/usr/bin/env python3
"""
make_interpreter.py  —  generate a recursive-descent parser *with*
 • `if/elif` for `|`   (alternatives)
 • `while` / `if` for `* + ?` (repetition / option)

Only Python stdlib required.  Supports EBNF subset: (), *, +, ?, |, <non-terminal>.
"""

from __future__ import annotations
import argparse, itertools, re, textwrap, pathlib
from typing import Dict, List

###############################################################################
# 1.  Tokenizer
###############################################################################
TOK = re.compile(r"<[^>]+>|::=|:=|[\(\)\*\+\?\|]|[^\s\(\)\*\+\?\|]+")


def tk(line: str) -> List[str]:
    return [t for t in TOK.findall(line) if t.strip()]


###############################################################################
# 2. Tiny EBNF AST  (so we can emit loops & if/else directly)
###############################################################################
class Node: pass
class Seq(Node):
    def __init__(self, parts: List[Node]): self.parts = parts
class Alt(Node):
    def __init__(self, choices: List[Node]): self.choices = choices
class Rep(Node):               # *, +
    def __init__(self, expr: Node, at_least1: bool): self.expr, self.at_least1 = expr, at_least1
class Opt(Node):               # ?
    def __init__(self, expr: Node): self.expr = expr
class Term(Node):              # terminal or non-terminal
    def __init__(self, text: str): self.text = text             # e.g. 'a'  or  <A>


###############################################################################
# 3. Parse RHS into AST
###############################################################################
def parse_rhs(tokens: List[str]) -> Node:
    """EBNF → AST (recursive-descent on tokens list)"""
    pos = 0

    def parse_alt() -> Node:
        nonlocal pos
        seqs = [parse_seq()]
        while pos < len(tokens) and tokens[pos] == "|":
            pos += 1
            seqs.append(parse_seq())
        return seqs[0] if len(seqs) == 1 else Alt(seqs)

    def parse_seq() -> Node:
        nonlocal pos
        parts: List[Node] = []
        while pos < len(tokens) and tokens[pos] not in [")", "|"]:
            parts.append(parse_item())
        return parts[0] if len(parts) == 1 else Seq(parts)

    def parse_item() -> Node:
        nonlocal pos
        tok = tokens[pos]
        if tok == "(":
            pos += 1
            inner = parse_alt()
            if pos >= len(tokens) or tokens[pos] != ")":
                raise SyntaxError("')' expected")
            pos += 1
            base: Node = inner
        else:
            base = Term(tok)
            pos += 1

        if pos < len(tokens) and tokens[pos] in ["*", "+", "?"]:
            op = tokens[pos]; pos += 1
            if op == "*":   return Rep(base, at_least1=False)
            if op == "+":   return Rep(base, at_least1=True)
            if op == "?":   return Opt(base)
        return base

    tree = parse_alt()
    if pos != len(tokens):
        raise SyntaxError("extra tokens in RHS")
    return tree


###############################################################################
# 4. Read EBNF file → dict[NT] = AST
###############################################################################
def read_grammar(path: str) -> Dict[str, Node]:
    text = pathlib.Path(path).read_text(encoding="utf-8")
    rules: Dict[str, Node] = {}
    cur_lhs, rhs_buffer = None, []

    def flush():
        nonlocal rhs_buffer
        if cur_lhs and rhs_buffer:
            rhs_ast = parse_rhs(tk(" ".join(rhs_buffer)))
            rules[cur_lhs] = rhs_ast
        rhs_buffer = []

    for raw in map(str.strip, text.splitlines()):
        if not raw or raw.startswith("#"):
            continue
        if ":=" in raw or "::=" in raw:
            flush()
            cur_lhs, rhs0 = map(str.strip, re.split(r":=|::=", raw, 1))
            cur_lhs = cur_lhs if cur_lhs.startswith("<") else f"<{cur_lhs}>"
            rhs_buffer = [rhs0]
        elif raw.startswith("|"):
            rhs_buffer.append(raw[1:].strip())
        else:
            raise SyntaxError(f"bad line: {raw}")
    flush()
    return rules


###############################################################################
# 5. Emit Python parse functions (loops / if-else)
###############################################################################
FUNC_TMPL = textwrap.dedent("""
def parse_{name}(s: str, pos: int):
    \"\"\"parse {nt}\"\"\"
{body}
""")

def emit_expr(node: Node, nt_map: Dict[str, str], indent: str, var: str, out: List[str]):
    """Append Python code parsing `node`, update `pos` to var, collect nodes into list `nodes`."""
    new_indent = indent + "    "

    if isinstance(node, Term):
        if node.text.startswith("<"):                     # non-terminal
            fn = nt_map[node.text]
            out.append(f"{indent}try:")
            out.append(f"{new_indent}child, {var} = {fn}(s, {var})")
            out.append(f"{new_indent}nodes.append(child)")
            out.append(f"{indent}except SyntaxError:")
            out.append(f"{new_indent}raise")
        else:                                             # literal terminal (single char / token)
            lit = node.text
            out.append(f"{indent}if {var} < len(s) and s[{var}] == {lit!r}:")
            out.append(f"{new_indent}nodes.append({lit!r})")
            out.append(f"{new_indent}{var} += 1")
            out.append(f"{indent}else:")
            out.append(f"{new_indent}raise SyntaxError('expected {lit}')")

    elif isinstance(node, Seq):
        for part in node.parts:
            emit_expr(part, nt_map, indent, var, out)

    elif isinstance(node, Alt):
        out.append(f"{indent}# alternation with backup rollback")
        out.append(f"{indent}backup = {var}")
        for i, choice in enumerate(node.choices):
            prefix = "if" if i == 0 else "elif"
            out.append(f"{indent}{prefix} True:")
            emit_expr(choice, nt_map, indent + "    ", var, out)
        out.append(f"{indent}else:")
        out.append(f"{indent}    {var} = backup")
        out.append(f"{indent}if {var} == backup:")
        out.append(f"{indent}    raise SyntaxError('no alternative matched')")

    elif isinstance(node, Rep):
        out.append(f"{indent}# repetition {'+' if node.at_least1 else '*'}")
        out.append(f"{indent}{var}_count = 0")
        out.append(f"{indent}while True:")
        out.append(f"{indent}    try:")
        emit_expr(node.expr, nt_map, indent + "        ", var, out)
        out.append(f"{indent}        {var}_count += 1")
        out.append(f"{indent}        continue")
        out.append(f"{indent}    except SyntaxError:")
        out.append(f"{indent}        break")
        if node.at_least1:
            out.append(f"{indent}if {var}_count == 0:")
            out.append(f"{indent}    raise SyntaxError('expected at least one')")
    elif isinstance(node, Opt):
        out.append(f"{indent}try:")
        emit_expr(node.expr, nt_map, new_indent, var, out)
        out.append(f"{indent}except SyntaxError:")
        out.append(f"{new_indent}pass")
    else:
        raise TypeError(node)


def generate_parser(rules: Dict[str, Node]) -> str:
    nt_map = {nt: f"parse_{nt.strip('<>')}" for nt in rules}
    funcs_src: List[str] = []
    for nt, ast in rules.items():
        name = nt.strip("<>")
        lines: List[str] = []
        body_indent = "    "
        # function body prologue
        lines.append(f"{body_indent}nodes: list = []")
        lines.append(f"{body_indent}pos0 = pos")
        # emit parsing code with correct indentation
        emit_expr(ast, nt_map, body_indent, "pos", lines)
        lines.append(f"{body_indent}return ({repr(nt)} , nodes), pos")
        body = "\n".join(lines)
        funcs_src.append(FUNC_TMPL.format(name=name, nt=nt, body=body))
    top = textwrap.dedent("""\
    \"\"\"Auto-generated parser (if/else + loops) — DO NOT EDIT.\"\"\"
    from typing import Tuple
    """)
    top += "\n".join(funcs_src)
    top += textwrap.dedent("""
    def parse_input(source: str):
        node, pos = parse_S(source, 0)
        if pos != len(source):
            raise SyntaxError(f'extra input at {pos}')
        return node

    # alias for end-to-end tests
    def parse(source: str):
        return parse_input(source)
    """)
    return top


###############################################################################
# 6. CLI
###############################################################################
def main():
    pa = argparse.ArgumentParser(description="Generate loop/if-else parser from EBNF.")
    pa.add_argument("-g", "--grammar", required=True)
    pa.add_argument("-o", "--output", required=True)
    args = pa.parse_args()

    rules = read_grammar(args.grammar)
    src = generate_parser(rules)
    pathlib.Path(args.output).write_text(src, encoding="utf-8")
    print(f"Parser written to {args.output}.")

if __name__ == "__main__":
    main()
