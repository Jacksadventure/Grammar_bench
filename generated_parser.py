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
    if lookahead == "d":
        match("d")
    elif lookahead == "a":
        match("a")
        parse_I()
        parse_F()
    elif lookahead == "c":
        match("c")
        parse_H()
    elif lookahead == "h":
        match("h")
    elif lookahead == "i":
        match("i")
    elif lookahead == "e":
        match("e")
        parse_C()
        match("e")
    elif lookahead == "j":
        match("j")
        parse_F()
        parse_D()
    elif lookahead == "b":
        match("b")
        parse_H()
    elif lookahead == "f":
        match("f")
    elif lookahead == "g":
        match("g")
        match("d")
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(["d", "a", "c", "h", "i", "e", "j", "b", "f", "g"]))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead == "g":
        match("g")
        parse_H()
    elif lookahead == "b":
        match("b")
        parse_A()
    elif lookahead == "c":
        match("c")
        parse_C()
        match("i")
    elif lookahead == "d":
        match("d")
        match("e")
    elif lookahead == "h":
        match("h")
        parse_I()
    elif lookahead == "i":
        match("i")
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(["g", "b", "c", "d", "h", "i"]))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead == "d":
        match("d")
    elif lookahead == "e":
        match("e")
        parse_J()
    elif lookahead == "g":
        match("g")
        parse_H()
    elif lookahead == "i":
        match("i")
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(["d", "e", "g", "i"]))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead == "f":
        match("f")
    elif lookahead == "a":
        match("a")
        parse_H()
    elif lookahead == "d":
        match("d")
    elif lookahead == "i":
        match("i")
        parse_I()
        match("c")
    elif lookahead == "g":
        match("g")
    elif lookahead == "e":
        match("e")
        match("j")
    elif lookahead == "h":
        match("h")
        match("j")
    elif lookahead == "j":
        match("j")
        parse_C()
        match("d")
    elif lookahead == "c":
        match("c")
    elif lookahead == "b":
        match("b")
        parse_F()
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(["f", "a", "d", "i", "g", "e", "h", "j", "c", "b"]))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead == "d":
        match("d")
        parse_B()
        match("f")
    elif lookahead == "h":
        match("h")
        parse_D()
        parse_D()
    elif lookahead == "e":
        match("e")
        match("i")
    elif lookahead == "g":
        match("g")
        match("a")
    elif lookahead == "f":
        match("f")
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(["d", "h", "e", "g", "f"]))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead == "h":
        match("h")
    elif lookahead == "e":
        match("e")
        parse_J()
        parse_E()
    elif lookahead == "d":
        match("d")
        match("i")
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(["h", "e", "d"]))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead == "g":
        match("g")
    elif lookahead == "d":
        match("d")
        parse_B()
    elif lookahead == "f":
        match("f")
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(["g", "d", "f"]))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead == "g":
        match("g")
        parse_I()
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(["g"]))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead == "j":
        match("j")
        match("h")
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(["j"]))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
        parse_E()
        match("f")
    elif lookahead == "b":
        match("b")
        match("d")
        match("g")
    elif lookahead == "f":
        match("f")
    elif lookahead == "g":
        match("g")
    elif lookahead == "d":
        match("d")
        parse_B()
    elif lookahead == "h":
        match("h")
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(["i", "b", "f", "g", "d", "h"]))

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