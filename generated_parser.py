#!/usr/bin/env python3
"""
Generated Recursive Descent Parser

This parser was automatically generated from a random LL(1) grammar.
Example derivations:
#   i f j j
#   a
#   h h b a d h g
#   i g f j
"""

import sys

tokens = []
pos = 0

def error(msg):
    print("Parse error:", msg)
    sys.exit(1)

def match(expected):
    global pos, tokens
    if pos < len(tokens) and tokens[pos] == expected:
        pos += 1
    else:
        error("Expected " + expected + ", got " + (tokens[pos] if pos < len(tokens) else "EOF"))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead == "b":
        match("b")
        match("d")
        parse_B()
    elif lookahead == "c":
        match("c")
        match("j")
        parse_E()
    elif lookahead == "f":
        match("f")
        parse_B()
    elif lookahead == "j":
        match("j")
        parse_I()
    elif lookahead == "d":
        match("d")
        match("c")
    elif lookahead == "h":
        match("h")
        match("h")
        parse_H()
    elif lookahead == "a":
        match("a")
    elif lookahead == "i":
        match("i")
        parse_G()
        match("j")
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(["b", "c", "f", "j", "d", "h", "a", "i"]))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead == "h":
        match("h")
    elif lookahead == "g":
        match("g")
        match("h")
    elif lookahead == "c":
        match("c")
        parse_H()
    elif lookahead == "b":
        match("b")
        parse_F()
    elif lookahead == "a":
        match("a")
        match("e")
    elif lookahead == "i":
        match("i")
    elif lookahead == "f":
        match("f")
        match("h")
        parse_A()
    elif lookahead == "d":
        match("d")
        match("h")
        parse_C()
    elif lookahead == "j":
        match("j")
        parse_D()
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(["h", "g", "c", "b", "a", "i", "f", "d", "j"]))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead == "d":
        match("d")
        parse_E()
    elif lookahead == "h":
        match("h")
        match("a")
    elif lookahead == "g":
        match("g")
    elif lookahead == "e":
        match("e")
    elif lookahead == "j":
        match("j")
        parse_I()
        match("b")
    elif lookahead == "b":
        match("b")
        parse_G()
    elif lookahead == "c":
        match("c")
        parse_J()
        match("h")
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(["d", "h", "g", "e", "j", "b", "c"]))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead == "g":
        match("g")
    elif lookahead == "i":
        match("i")
        parse_J()
        match("a")
    elif lookahead == "e":
        match("e")
    elif lookahead == "b":
        match("b")
    elif lookahead == "j":
        match("j")
        parse_J()
        parse_B()
    elif lookahead == "d":
        match("d")
        parse_F()
        parse_B()
    elif lookahead == "a":
        match("a")
        parse_A()
    elif lookahead == "c":
        match("c")
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(["g", "i", "e", "b", "j", "d", "a", "c"]))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead == "f":
        match("f")
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(["f"]))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead == "c":
        match("c")
        match("b")
    elif lookahead == "j":
        match("j")
    elif lookahead == "a":
        match("a")
        parse_A()
        match("g")
    elif lookahead == "e":
        match("e")
        match("c")
        match("d")
    elif lookahead == "i":
        match("i")
        match("h")
        parse_F()
    elif lookahead == "b":
        match("b")
        parse_G()
    elif lookahead == "h":
        match("h")
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(["c", "j", "a", "e", "i", "b", "h"]))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead == "g":
        match("g")
        parse_E()
    elif lookahead == "b":
        match("b")
    elif lookahead == "f":
        match("f")
        match("j")
    elif lookahead == "j":
        match("j")
        parse_F()
        match("a")
    elif lookahead == "a":
        match("a")
        parse_I()
        match("e")
    elif lookahead == "c":
        match("c")
        match("g")
    elif lookahead == "i":
        match("i")
        match("h")
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(["g", "b", "f", "j", "a", "c", "i"]))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead == "f":
        match("f")
        match("f")
        match("f")
    elif lookahead == "i":
        match("i")
        match("c")
    elif lookahead == "g":
        match("g")
    elif lookahead == "j":
        match("j")
    elif lookahead == "b":
        match("b")
        match("a")
        parse_B()
    elif lookahead == "h":
        match("h")
        match("c")
    elif lookahead == "c":
        match("c")
    elif lookahead == "d":
        match("d")
        parse_F()
        parse_C()
    elif lookahead == "e":
        match("e")
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(["f", "i", "g", "j", "b", "h", "c", "d", "e"]))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead == "h":
        match("h")
    elif lookahead == "b":
        match("b")
        parse_F()
    elif lookahead == "j":
        match("j")
        parse_F()
    elif lookahead == "f":
        match("f")
    elif lookahead == "g":
        match("g")
        parse_B()
        parse_I()
    elif lookahead == "c":
        match("c")
        match("g")
    elif lookahead == "e":
        match("e")
        parse_E()
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(["h", "b", "j", "f", "g", "c", "e"]))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead == "h":
        match("h")
    elif lookahead == "d":
        match("d")
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(["h", "d"]))

def parse_input(input_str):
    global tokens, pos
    tokens = input_str.strip().split()
    pos = 0
    parse_A()
    if pos != len(tokens):
        error("Extra tokens after parsing: " + " ".join(tokens[pos:]))
    print("Input accepted.")

def main():
    import sys
    if len(sys.argv) > 1:
        input_str = sys.argv[1]
        parse_input(input_str)
    else:
        examples = [
            "ifjj",
            "a",
            "hhbadhg",
            "igfj",
        ]
        for ex in examples:
            print("Testing input:", ex)
            parse_input(ex)
            print()

if __name__ == "__main__":
    main()