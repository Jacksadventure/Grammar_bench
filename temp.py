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
    elif lookahead == "a":
        match("a")
    elif lookahead == "f":
        match("f")
        parse_H()
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(["j", "a", "f"]))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
        parse_C()
    elif lookahead == "g":
        match("g")
    elif lookahead == "f":
        match("f")
    elif lookahead == "e":
        match("e")
        match("h")
        parse_G()
    elif lookahead == "b":
        match("b")
        match("e")
        parse_D()
    elif lookahead == "d":
        match("d")
    elif lookahead == "j":
        match("j")
    elif lookahead == "a":
        match("a")
        match("h")
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(["i", "g", "f", "e", "b", "d", "j", "a"]))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead == "d":
        match("d")
        match("f")
        parse_E()
    elif lookahead == "i":
        match("i")
        match("g")
    elif lookahead == "e":
        match("e")
        parse_E()
        match("e")
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(["d", "i", "e"]))

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == "h":
        match("h")
        parse_B()

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == "g":
        match("g")
        match("e")

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead == "d":
        match("d")
        match("j")
        match("g")
    elif lookahead == "a":
        match("a")
        match("a")
    elif lookahead == "e":
        match("e")
        match("e")
    elif lookahead == "j":
        match("j")
        parse_I()
        match("f")
    elif lookahead == "j":
        match("j")
        parse_G()
    elif lookahead == "i":
        match("i")
        match("a")
    elif lookahead == "c":
        match("c")
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(["d", "a", "e", "j", "j", "i", "c"]))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead == "j":
        match("j")
    elif lookahead == "c":
        match("c")
        parse_F()
        match("i")
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(["j", "c"]))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == "g":
        match("g")
        parse_D()
        match("j")

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == "d":
        match("d")

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead == "g":
        match("g")
        match("a")
    elif lookahead == "i":
        match("i")
        match("a")
        parse_I()
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(["g", "i"]))

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