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
    if lookahead == "h":
        match("h")
        match("a")
    elif lookahead == "c":
        match("c")
    elif lookahead == "e":
        match("e")
        match("j")
        match("h")
    elif lookahead == "g":
        match("g")
        parse_F()
    elif lookahead == "b":
        match("b")
        parse_D()
    elif lookahead == "a":
        match("a")
        parse_B()
        parse_D()
    elif lookahead == "f":
        match("f")
    elif lookahead == "d":
        match("d")
        parse_J()
        parse_B()
    elif lookahead == "i":
        match("i")
        parse_C()
        parse_I()
    elif lookahead == "j":
        match("j")
        parse_E()
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(["h", "c", "e", "g", "b", "a", "f", "d", "i", "j"]))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead == "d":
        match("d")
    elif lookahead == "j":
        match("j")
        parse_H()
        match("i")
    elif lookahead == "i":
        match("i")
        match("a")
        parse_C()
    elif lookahead == "f":
        match("f")
    elif lookahead == "e":
        match("e")
        parse_G()
    elif lookahead == "b":
        match("b")
    elif lookahead == "a":
        match("a")
        parse_A()
        parse_F()
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(["d", "j", "i", "f", "e", "b", "a"]))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead == "j":
        match("j")
    elif lookahead == "f":
        match("f")
    elif lookahead == "d":
        match("d")
    elif lookahead == "g":
        match("g")
    elif lookahead == "h":
        match("h")
        match("d")
    elif lookahead == "e":
        match("e")
        parse_G()
    elif lookahead == "i":
        match("i")
        parse_G()
    elif lookahead == "c":
        match("c")
    elif lookahead == "b":
        match("b")
    elif lookahead == "a":
        match("a")
        match("j")
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(["j", "f", "d", "g", "h", "e", "i", "c", "b", "a"]))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead == "j":
        match("j")
    elif lookahead == "h":
        match("h")
        match("i")
    elif lookahead == "c":
        match("c")
    elif lookahead == "i":
        match("i")
        match("b")
    elif lookahead == "g":
        match("g")
    elif lookahead == "a":
        match("a")
    elif lookahead == "e":
        match("e")
        match("b")
    elif lookahead == "d":
        match("d")
        match("i")
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(["j", "h", "c", "i", "g", "a", "e", "d"]))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead == "d":
        match("d")
    elif lookahead == "a":
        match("a")
        match("c")
        parse_B()
    elif lookahead == "c":
        match("c")
        parse_E()
        match("h")
    elif lookahead == "b":
        match("b")
        match("b")
        match("f")
    elif lookahead == "i":
        match("i")
    elif lookahead == "g":
        match("g")
        match("b")
        match("d")
    elif lookahead == "e":
        match("e")
        parse_C()
        parse_J()
    elif lookahead == "j":
        match("j")
    elif lookahead == "h":
        match("h")
        parse_F()
        parse_D()
    elif lookahead == "f":
        match("f")
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(["d", "a", "c", "b", "i", "g", "e", "j", "h", "f"]))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead == "d":
        match("d")
    elif lookahead == "g":
        match("g")
        match("b")
        parse_F()
    elif lookahead == "h":
        match("h")
    elif lookahead == "i":
        match("i")
        parse_D()
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(["d", "g", "h", "i"]))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
        parse_F()
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(["i"]))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead == "g":
        match("g")
    elif lookahead == "b":
        match("b")
    elif lookahead == "f":
        match("f")
    elif lookahead == "h":
        match("h")
    elif lookahead == "f":
        match("f")
        parse_E()
    elif lookahead == "e":
        match("e")
        match("f")
    elif lookahead == "i":
        match("i")
        match("h")
        match("e")
    elif lookahead == "d":
        match("d")
        match("i")
    elif lookahead == "j":
        match("j")
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(["g", "b", "f", "h", "f", "e", "i", "d", "j"]))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead == "h":
        match("h")
        parse_G()
        parse_G()
    elif lookahead == "b":
        match("b")
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(["h", "b"]))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead == "e":
        match("e")
    elif lookahead == "f":
        match("f")
        match("b")
        match("d")
    elif lookahead == "j":
        match("j")
        parse_A()
        parse_I()
    elif lookahead == "c":
        match("c")
        match("h")
    elif lookahead == "d":
        match("d")
    elif lookahead == "a":
        match("a")
        parse_J()
    elif lookahead == "b":
        match("b")
        match("i")
    elif lookahead == "i":
        match("i")
        match("e")
    elif lookahead == "h":
        match("h")
        match("b")
        parse_C()
    elif lookahead == "g":
        match("g")
        match("d")
        parse_A()
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(["e", "f", "j", "c", "d", "a", "b", "i", "h", "g"]))

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