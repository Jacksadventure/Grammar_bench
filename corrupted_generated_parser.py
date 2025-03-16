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
    if lookahead == "a":
        match("a")
    elif lookahead == "f":
        match("f")
        match("e")
    elif lookahead == "c":
        match("c")
        match("j")
    elif lookahead == "g":
        match("g")
        parse_C()
        parse_B()
    elif lookahead == "d":
        match("d")
        match("e")
        parse_F()
    elif lookahead == "b":
        match("b")
    elif lookahead == "i":
        match("i")
        parse_E()
        parse_J()
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(["a", "f", "c", "g", "d", "b", "i"]))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead == "j":
        match("j")
        match("i")
    elif lookahead == "f":
        match("f")
        parse_D()
        match("j")
    elif lookahead == "d":
        match("d")
        match("c")
    elif lookahead == "g":
        match("g")
        match("e")
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(["j", "f", "d", "g"]))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead == "f":
        match("f")
        parse_J()
        match("j")
    elif lookahead == "a":
        match("a")
        parse_A()
    elif lookahead == "e":
        match("e")
        parse_C()
    elif lookahead == "j":
        match("j")
        parse_A()
        parse_C()
    elif lookahead == "h":
        match("h")
        parse_D()
        parse_C()
    elif lookahead == "c":
        match("c")
        parse_G()
        parse_H()
    elif lookahead == "i":
        match("i")
        match("i")
        match("c")
    elif lookahead == "g":
        match("g")
        match("d")
    elif lookahead == "b":
        match("b")
    elif lookahead == "d":
        match("d")
        match("c")
        parse_C()
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(["f", "a", "e", "j", "h", "c", "i", "g", "b", "d"]))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
        parse_B()
    elif lookahead == "j":
        match("j")
    elif lookahead == "b":
        match("b")
        match("f")
    elif lookahead == "g":
        match("g")
        match("j")
    elif lookahead == "a":
        match("a")
    elif lookahead == "d":
        match("d")
    elif lookahead == "f":
        match("f")
        parse_D()
        match("g")
    elif lookahead == "c":
        match("c")
        parse_I()
    elif lookahead == "h":
        match("h")
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(["i", "j", "b", "g", "a", "d", "f", "c", "h"]))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
    elif lookahead == "b":
        match("b")
    elif lookahead == "e":
        match("e")
        match("c")
        match("g")
    elif lookahead == "d":
        match("d")
        parse_I()
        match("f")
    elif lookahead == "j":
        match("j")
        parse_B()
        match("h")
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(["i", "b", "e", "d", "j"]))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead == "d":
        match("d")
        parse_G()
    elif lookahead == "a":
        match("a")
        match("f")
    elif lookahead == "j":
        match("j")
        parse_G()
        match("d")
    elif lookahead == "b":
        match("b")
        parse_F()
    elif lookahead == "e":
        match("e")
        match("f")
        match("a")
    elif lookahead == "h":
        match("h")
        parse_H()
    elif lookahead == "c":
        match("c")
        match("f")
        parse_C()
    elif lookahead == "f":
        match("f")
        parse_A()
        match("d")
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(["d", "a", "j", "b", "e", "h", "c", "f"]))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead == "f":
        match("f")
        match("g")
    elif lookahead == "j":
        match("j")
        match("e")
        match("b")
    elif lookahead == "i":
        match("i")
        parse_E()
    elif lookahead == "a":
        match("a")
    elif lookahead == "h":
        match("h")
    elif lookahead == "b":
        match("b")
        match("c")
        match("d")
    elif lookahead == "d":
        match("d")
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(["f", "j", "i", "a", "h", "b", "d"]))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead == "a":
        match("a")
        match("j")
        parse_H()
    elif lookahead == "c":
        match("c")
    elif lookahead == "d":
        match("d")
        match("i")
    elif lookahead == "d":
        match("d")
        parse_B()
        parse_H()
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(["a", "c", "d", "d"]))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead == "e":
        match("e")
        match("b")
    elif lookahead == "f":
        match("f")
        parse_H()
    elif lookahead == "b":
        match("b")
        parse_F()
    elif lookahead == "c":
        match("c")
    elif lookahead == "i":
        match("i")
    elif lookahead == "h":
        match("h")
    elif lookahead == "j":
        match("j")
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(["e", "f", "b", "c", "i", "h", "j"]))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead == "c":
        match("c")
    elif lookahead == "g":
        match("g")
        parse_H()
        parse_H()
    elif lookahead == "d":
        match("d")
    elif lookahead == "e":
        match("e")
        match("c")
        match("f")
    elif lookahead == "i":
        match("i")
    elif lookahead == "h":
        match("h")
        parse_I()
    elif lookahead == "b":
        match("b")
        match("j")
    elif lookahead == "f":
        match("f")
    elif lookahead == "a":
        match("a")
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(["c", "g", "d", "e", "i", "h", "b", "f", "a"]))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
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

if __name__ == "__main__":
    main()