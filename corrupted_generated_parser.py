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
        parse_F()
        match("i")
    elif lookahead == "i":
        match("i")
        match("i")
        parse_I()
    elif lookahead == "c":
        match("c")
    elif lookahead == "j":
        match("j")
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(["d", "i", "c", "j"]))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead == "a":
        match("a")
    elif lookahead == "e":
        match("e")
        match("c")
        match("h")
    elif lookahead == "d":
        match("d")
        match("g")
        parse_B()
    elif lookahead == "j":
        match("j")
        parse_H()
        parse_B()
    elif lookahead == "i":
        match("i")
    elif lookahead == "g":
        match("g")
    elif lookahead == "h":
        match("h")
    elif lookahead == "b":
        match("b")
        match("i")
        parse_G()
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(["a", "e", "d", "j", "i", "g", "h", "b"]))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead == "e":
        match("e")
        match("g")
    elif lookahead == "d":
        match("d")
        parse_J()
        parse_H()
    elif lookahead == "g":
        match("g")
        match("h")
    elif lookahead == "b":
        match("b")
        parse_H()
        match("i")
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(["e", "d", "g", "b"]))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead == "e":
        match("e")
    elif lookahead == "g":
        match("g")
        match("g")
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(["e", "g"]))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead == "j":
        match("j")
        parse_J()
    elif lookahead == "a":
        match("a")
        match("d")
        match("c")
    elif lookahead == "g":
        match("g")
    elif lookahead == "i":
        match("i")
        parse_C()
        parse_B()
    elif lookahead == "e":
        match("e")
        parse_C()
        match("d")
    elif lookahead == "b":
        match("b")
        match("d")
        parse_I()
    elif lookahead == "d":
        match("d")
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(["j", "a", "g", "i", "e", "b", "d"]))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead == "e":
        match("e")
        match("b")
        match("i")
    elif lookahead == "f":
        match("f")
        match("g")
        parse_B()
    elif lookahead == "g":
        match("g")
    elif lookahead == "i":
        match("i")
    elif lookahead == "c":
        match("c")
    elif lookahead == "h":
        match("h")
    elif lookahead == "d":
        match("d")
        match("a")
        match("a")
    elif lookahead == "j":
        match("j")
        match("i")
        parse_A()
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(["e", "f", "g", "i", "c", "h", "d", "j"]))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
    elif lookahead == "g":
        match("g")
        parse_H()
    elif lookahead == "c":
        match("c")
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(["i", "g", "c"]))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
        match("i")
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(["i"]))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead == "g":
        match("g")
        match("f")
        match("f")
    elif lookahead == "h":
        match("h")
    elif lookahead == "i":
        match("i")
        parse_F()
        match("b")
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(["g", "h", "i"]))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead == "h":
        match("h")
        match("e")
    elif lookahead == "i":
        match("i")
    elif lookahead == "b":
        match("b")
        match("h")
    elif lookahead == "e":
        match("e")
    elif lookahead == "g":
        match("g")
        parse_A()
    elif lookahead == "c":
        match("c")
        match("g")
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(["h", "i", "b", "e", "g", "c"]))

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