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
    if lookahead == "j":
        match("j")
    elif lookahead == "h":
        match("h")
    elif lookahead == "a":
        match("a")
        parse_B()
        parse_I()
    elif lookahead == "d":
        match("d")
        parse_D()
        parse_A()
    elif lookahead == "e":
        match("e")
        parse_D()
    elif lookahead == "b":
        match("b")
    elif lookahead == "g":
        match("g")
        match("i")
        match("h")
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(["j", "h", "a", "d", "e", "b", "g"]))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
        match("a")
    elif lookahead == "g":
        match("g")
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(["i", "g"]))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead == "c":
        match("c")
    elif lookahead == "b":
        match("b")
    elif lookahead == "g":
        match("g")
        match("b")
        match("j")
    elif lookahead == "i":
        match("i")
    elif lookahead == "f":
        match("f")
        match("j")
        match("c")
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(["c", "b", "g", "i", "f"]))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead == "h":
        match("h")
        match("j")
        parse_A()
    elif lookahead == "a":
        match("a")
        parse_J()
    elif lookahead == "g":
        match("g")
        parse_F()
    elif lookahead == "d":
        match("d")
        parse_D()
        parse_C()
    elif lookahead == "i":
        match("i")
        parse_B()
        match("c")
    elif lookahead == "c":
        match("c")
    elif lookahead == "e":
        match("e")
    elif lookahead == "b":
        match("b")
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(["h", "a", "g", "d", "i", "c", "e", "b"]))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead == "g":
        match("g")
        parse_I()
        parse_B()
    elif lookahead == "b":
        match("b")
    elif lookahead == "f":
        match("f")
        parse_G()
        parse_D()
    elif lookahead == "a":
        match("a")
        match("i")
        match("c")
    elif lookahead == "c":
        match("c")
        match("i")
        match("b")
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(["g", "b", "f", "a", "c"]))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead == "j":
        match("j")
        match("h")
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(["j"]))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead == "c":
        match("c")
        parse_E()
    elif lookahead == "e":
        match("e")
        parse_D()
        parse_A()
    elif lookahead == "b":
        match("b")
        parse_A()
    elif lookahead == "h":
        match("h")
        match("h")
    elif lookahead == "f":
        match("f")
        parse_D()
        match("f")
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(["c", "e", "b", "h", "f"]))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead == "a":
        match("a")
        match("j")
    elif lookahead == "b":
        match("b")
        match("b")
        parse_F()
    elif lookahead == "g":
        match("g")
    elif lookahead == "h":
        match("h")
        match("j")
    elif lookahead == "j":
        match("j")
    elif lookahead == "e":
        match("e")
        match("g")
        parse_I()
    elif lookahead == "i":
        match("i")
    elif lookahead == "f":
        match("f")
        match("h")
    elif lookahead == "c":
        match("c")
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(["a", "b", "g", "h", "j", "e", "i", "f", "c"]))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead == "j":
        match("j")
        parse_G()
        parse_H()
    elif lookahead == "e":
        match("e")
    elif lookahead == "f":
        match("f")
        match("f")
        parse_D()
    elif lookahead == "i":
        match("i")
        match("e")
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(["j", "e", "f", "i"]))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
    elif lookahead == "j":
        match("j")
        match("c")
        parse_F()
    elif lookahead == "h":
        match("h")
        parse_E()
        match("e")
    elif lookahead == "a":
        match("a")
        parse_C()
        parse_E()
    elif lookahead == "g":
        match("g")
        match("h")
    elif lookahead == "c":
        match("c")
    elif lookahead == "d":
        match("d")
        parse_E()
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(["i", "j", "h", "a", "g", "c", "d"]))

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