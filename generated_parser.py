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
        parse_E()
        match("c")
    elif lookahead == "e":
        match("e")
    elif lookahead == "c":
        match("c")
        match("a")
        parse_F()
    elif lookahead == "i":
        match("i")
        match("i")
        parse_I()
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(["d", "e", "c", "i"]))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead == "f":
        match("f")
        match("c")
    elif lookahead == "d":
        match("d")
    elif lookahead == "g":
        match("g")
        parse_G()
    elif lookahead == "c":
        match("c")
    elif lookahead == "b":
        match("b")
    elif lookahead == "h":
        match("h")
        match("g")
        parse_D()
    elif lookahead == "a":
        match("a")
        match("h")
        parse_I()
    elif lookahead == "j":
        match("j")
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(["f", "d", "g", "c", "b", "h", "a", "j"]))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead == "j":
        match("j")
    elif lookahead == "b":
        match("b")
        parse_D()
    elif lookahead == "a":
        match("a")
        match("j")
        match("f")
    elif lookahead == "h":
        match("h")
        parse_D()
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(["j", "b", "a", "h"]))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead == "h":
        match("h")
        match("a")
        match("b")
    elif lookahead == "j":
        match("j")
        match("b")
    elif lookahead == "i":
        match("i")
        match("b")
        match("b")
    elif lookahead == "d":
        match("d")
        match("e")
    elif lookahead == "c":
        match("c")
        match("b")
        parse_H()
    elif lookahead == "b":
        match("b")
        match("h")
    elif lookahead == "g":
        match("g")
        parse_H()
    elif lookahead == "e":
        match("e")
    elif lookahead == "f":
        match("f")
        parse_C()
        match("f")
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(["h", "j", "i", "d", "c", "b", "g", "e", "f"]))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
    elif lookahead == "e":
        match("e")
        parse_J()
        match("f")
    elif lookahead == "b":
        match("b")
        parse_H()
        parse_C()
    elif lookahead == "h":
        match("h")
    elif lookahead == "c":
        match("c")
        parse_J()
        parse_C()
    elif lookahead == "j":
        match("j")
    elif lookahead == "g":
        match("g")
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(["i", "e", "b", "h", "c", "j", "g"]))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead == "a":
        match("a")
    elif lookahead == "i":
        match("i")
        parse_B()
        match("j")
    elif lookahead == "f":
        match("f")
        match("a")
    elif lookahead == "e":
        match("e")
    elif lookahead == "b":
        match("b")
        match("g")
    elif lookahead == "j":
        match("j")
        parse_E()
        match("j")
    elif lookahead == "c":
        match("c")
        match("a")
        match("d")
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(["a", "i", "f", "e", "b", "j", "c"]))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead == "e":
        match("e")
        parse_D()
        parse_D()
    elif lookahead == "i":
        match("i")
        parse_B()
    elif lookahead == "g":
        match("g")
        match("f")
        parse_I()
    elif lookahead == "c":
        match("c")
        parse_F()
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(["e", "i", "g", "c"]))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead == "d":
        match("d")
        match("j")
        parse_H()
    elif lookahead == "g":
        match("g")
    elif lookahead == "h":
        match("h")
    elif lookahead == "j":
        match("j")
    elif lookahead == "i":
        match("i")
    elif lookahead == "b":
        match("b")
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(["d", "g", "h", "j", "i", "b"]))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead == "d":
        match("d")
        match("a")
        parse_C()
    elif lookahead == "c":
        match("c")
        parse_C()
        parse_E()
    elif lookahead == "e":
        match("e")
    elif lookahead == "i":
        match("i")
        match("b")
        parse_I()
    elif lookahead == "g":
        match("g")
    elif lookahead == "b":
        match("b")
    elif lookahead == "f":
        match("f")
        match("h")
        match("a")
    elif lookahead == "j":
        match("j")
    elif lookahead == "h":
        match("h")
    elif lookahead == "a":
        match("a")
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(["d", "c", "e", "i", "g", "b", "f", "j", "h", "a"]))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
    elif lookahead == "c":
        match("c")
        parse_G()
        match("c")
    elif lookahead == "e":
        match("e")
    elif lookahead == "b":
        match("b")
        match("b")
    elif lookahead == "j":
        match("j")
        parse_J()
        match("a")
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(["i", "c", "e", "b", "j"]))

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