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
        parse_A()
        parse_B()
    elif lookahead == "h":
        match("h")
        parse_A()
    elif lookahead == "b":
        match("b")
    elif lookahead == "g":
        match("g")
        match("d")
    elif lookahead == "e":
        match("e")
    elif lookahead == "f":
        match("f")
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(["d", "h", "b", "g", "e", "f"]))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
        parse_H()
        parse_E()
    elif lookahead == "h":
        match("h")
        match("e")
    elif lookahead == "g":
        match("g")
        parse_A()
        match("d")
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(["i", "h", "g"]))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead == "g":
        match("g")
    elif lookahead == "d":
        match("d")
    elif lookahead == "i":
        match("i")
        match("h")
        match("a")
    elif lookahead == "j":
        match("j")
        match("b")
    elif lookahead == "e":
        match("e")
        parse_J()
    elif lookahead == "a":
        match("a")
    elif lookahead == "h":
        match("h")
        parse_C()
        match("g")
    elif lookahead == "c":
        match("c")
    elif lookahead == "b":
        match("b")
        parse_H()
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(["g", "d", "i", "j", "e", "a", "h", "c", "b"]))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead == "f":
        match("f")
    elif lookahead == "i":
        match("i")
        match("h")
        parse_C()
    elif lookahead == "g":
        match("g")
    elif lookahead == "b":
        match("b")
        parse_A()
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(["f", "i", "g", "b"]))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead == "a":
        match("a")
        match("f")
    elif lookahead == "h":
        match("h")
        parse_H()
    elif lookahead == "j":
        match("j")
        match("a")
    elif lookahead == "e":
        match("e")
        match("j")
        parse_D()
    elif lookahead == "g":
        match("g")
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(["a", "h", "j", "e", "g"]))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead == "d":
        match("d")
        parse_I()
    elif lookahead == "b":
        match("b")
        parse_H()
    elif lookahead == "j":
        match("j")
        parse_I()
    elif lookahead == "c":
        match("c")
        parse_G()
        match("g")
    elif lookahead == "g":
        match("g")
        match("i")
    elif lookahead == "f":
        match("f")
        match("i")
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(["d", "b", "j", "c", "g", "f"]))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead == "c":
        match("c")
        match("g")
    elif lookahead == "j":
        match("j")
    elif lookahead == "e":
        match("e")
        parse_E()
    elif lookahead == "a":
        match("a")
        parse_A()
        parse_F()
    elif lookahead == "f":
        match("f")
        parse_E()
        match("c")
    elif lookahead == "d":
        match("d")
    elif lookahead == "i":
        match("i")
        parse_A()
        parse_H()
    elif lookahead == "h":
        match("h")
    elif lookahead == "g":
        match("g")
        match("a")
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(["c", "j", "e", "a", "f", "d", "i", "h", "g"]))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead == "d":
        match("d")
        match("d")
        parse_F()
    elif lookahead == "f":
        match("f")
        parse_I()
        parse_J()
    elif lookahead == "h":
        match("h")
        match("e")
        parse_B()
    elif lookahead == "b":
        match("b")
        parse_G()
        parse_I()
    elif lookahead == "e":
        match("e")
    elif lookahead == "a":
        match("a")
        match("i")
        match("d")
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(["d", "f", "h", "b", "e", "a"]))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead == "b":
        match("b")
        parse_J()
    elif lookahead == "a":
        match("a")
    elif lookahead == "e":
        match("e")
    elif lookahead == "i":
        match("i")
        parse_F()
        match("c")
    elif lookahead == "h":
        match("h")
    elif lookahead == "f":
        match("f")
        parse_E()
    elif lookahead == "g":
        match("g")
        match("f")
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(["b", "a", "e", "i", "h", "f", "g"]))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead == "a":
        match("a")
        match("j")
    elif lookahead == "c":
        match("c")
        parse_B()
        match("a")
    elif lookahead == "g":
        match("g")
        parse_I()
    elif lookahead == "d":
        match("d")
        parse_C()
        match("b")
    elif lookahead == "f":
        match("f")
        match("f")
    elif lookahead == "b":
        match("b")
        match("i")
    elif lookahead == "h":
        match("h")
        match("b")
        match("i")
    elif lookahead == "j":
        match("j")
        parse_E()
    elif lookahead == "e":
        match("e")
        match("h")
        match("c")
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(["a", "c", "g", "d", "f", "b", "h", "j", "e"]))

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