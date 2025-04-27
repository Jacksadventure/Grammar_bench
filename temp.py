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
    elif lookahead == "i":
        match("i")
    elif lookahead == "e":
        match("e")
        parse_C()
        match("f")
    elif lookahead == "b":
        match("b")
    elif lookahead == "g":
        match("g")
    elif lookahead == "c":
        match("c")
        match("f")
    elif lookahead == "a":
        match("a")
    elif lookahead == "h":
        match("h")
        match("a")
        parse_J()
    elif lookahead == "j":
        match("j")
        match("i")
        match("g")
    elif lookahead == "f":
        match("f")
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(["d", "i", "e", "b", "g", "c", "a", "h", "j", "f"]))

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == "j":
        match("j")

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == "a":
        match("a")
        match("c")

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
        match("h")
        parse_G()
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(["i"]))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead == "c":
        match("c")
        parse_A()
        parse_E()
    elif lookahead == "b":
        match("b")
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(["c", "b"]))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead == "f":
        match("f")
        parse_I()
    elif lookahead == "a":
        match("a")
    elif lookahead == "j":
        match("j")
        match("a")
        match("a")
    elif lookahead == "e":
        match("e")
    elif lookahead == "h":
        match("h")
        match("g")
    elif lookahead == "b":
        match("b")
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(["f", "a", "j", "e", "h", "b"]))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead == "a":
        match("a")
    elif lookahead == "d":
        match("d")
        match("g")
        parse_J()
    elif lookahead == "g":
        match("g")
        match("a")
        parse_D()
    elif lookahead == "c":
        match("c")
        parse_H()
    elif lookahead == "b":
        match("b")
        match("j")
    elif lookahead == "h":
        match("h")
    elif lookahead == "j":
        match("j")
        match("j")
    elif lookahead == "e":
        match("e")
        parse_F()
        parse_H()
    elif lookahead == "i":
        match("i")
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(["a", "d", "g", "c", "b", "h", "j", "e", "i"]))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead == "h":
        match("h")
        parse_E()
        match("i")
    elif lookahead == "f":
        match("f")
    elif lookahead == "a":
        match("a")
        match("c")
    elif lookahead == "j":
        match("j")
        match("d")
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(["h", "f", "a", "j"]))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead == "j":
        match("j")
        parse_C()
    elif lookahead == "a":
        match("a")
    elif lookahead == "f":
        match("f")
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(["j", "a", "f"]))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead == "g":
        match("g")
        match("i")
    elif lookahead == "f":
        match("f")
        match("c")
    elif lookahead == "e":
        match("e")
        match("d")
        parse_C()
    elif lookahead == "d":
        match("d")
        match("d")
    elif lookahead == "b":
        match("b")
        match("e")
    elif lookahead == "i":
        match("i")
    elif lookahead == "a":
        match("a")
    elif lookahead == "c":
        match("c")
    elif lookahead == "h":
        match("h")
        match("h")
    elif lookahead == "j":
        match("j")
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(["g", "f", "e", "d", "b", "i", "a", "c", "h", "j"]))

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