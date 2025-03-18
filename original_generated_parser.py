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
    if lookahead == "c":
        match("c")
        parse_D()
    elif lookahead == "b":
        match("b")
        match("f")
    elif lookahead == "g":
        match("g")
        match("a")
        match("d")
    elif lookahead == "j":
        match("j")
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(["c", "b", "g", "j"]))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead == "h":
        match("h")
        parse_E()
    elif lookahead == "g":
        match("g")
        parse_B()
    elif lookahead == "i":
        match("i")
        match("e")
    elif lookahead == "f":
        match("f")
        parse_C()
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(["h", "g", "i", "f"]))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead == "e":
        match("e")
    elif lookahead == "f":
        match("f")
    elif lookahead == "h":
        match("h")
        match("g")
        match("g")
    elif lookahead == "c":
        match("c")
    elif lookahead == "i":
        match("i")
    elif lookahead == "g":
        match("g")
        parse_G()
    elif lookahead == "d":
        match("d")
        parse_E()
    elif lookahead == "b":
        match("b")
        match("h")
        parse_I()
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(["e", "f", "h", "c", "i", "g", "d", "b"]))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
        parse_A()
        parse_F()
    elif lookahead == "c":
        match("c")
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(["i", "c"]))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead == "j":
        match("j")
    elif lookahead == "a":
        match("a")
        parse_B()
    elif lookahead == "d":
        match("d")
    elif lookahead == "i":
        match("i")
        parse_C()
    elif lookahead == "f":
        match("f")
    elif lookahead == "b":
        match("b")
    elif lookahead == "h":
        match("h")
    elif lookahead == "e":
        match("e")
        match("c")
    elif lookahead == "g":
        match("g")
        match("f")
    elif lookahead == "c":
        match("c")
        parse_F()
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(["j", "a", "d", "i", "f", "b", "h", "e", "g", "c"]))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead == "c":
        match("c")
        parse_B()
    elif lookahead == "h":
        match("h")
    elif lookahead == "f":
        match("f")
        match("h")
        parse_F()
    elif lookahead == "b":
        match("b")
    elif lookahead == "j":
        match("j")
        parse_I()
        match("i")
    elif lookahead == "d":
        match("d")
    elif lookahead == "e":
        match("e")
        parse_D()
        parse_J()
    elif lookahead == "i":
        match("i")
        parse_H()
    elif lookahead == "a":
        match("a")
        parse_D()
        parse_F()
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(["c", "h", "f", "b", "j", "d", "e", "i", "a"]))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead == "h":
        match("h")
        parse_E()
    elif lookahead == "j":
        match("j")
    elif lookahead == "i":
        match("i")
        match("d")
        match("d")
    elif lookahead == "b":
        match("b")
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(["h", "j", "i", "b"]))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
        match("j")
        parse_I()
    elif lookahead == "h":
        match("h")
        parse_J()
        parse_G()
    elif lookahead == "e":
        match("e")
    elif lookahead == "g":
        match("g")
        parse_H()
        parse_D()
    elif lookahead == "a":
        match("a")
        parse_B()
    elif lookahead == "j":
        match("j")
        parse_J()
        match("h")
    elif lookahead == "b":
        match("b")
    elif lookahead == "c":
        match("c")
        match("e")
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(["i", "h", "e", "g", "a", "j", "b", "c"]))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead == "d":
        match("d")
        parse_H()
        match("g")
    elif lookahead == "j":
        match("j")
        parse_D()
        match("j")
    elif lookahead == "a":
        match("a")
        match("c")
        match("f")
    elif lookahead == "g":
        match("g")
        match("b")
    elif lookahead == "c":
        match("c")
    elif lookahead == "h":
        match("h")
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(["d", "j", "a", "g", "c", "h"]))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead == "f":
        match("f")
        parse_C()
    elif lookahead == "c":
        match("c")
        match("d")
        parse_E()
    elif lookahead == "e":
        match("e")
        parse_D()
    elif lookahead == "j":
        match("j")
    elif lookahead == "a":
        match("a")
        match("c")
        parse_J()
    elif lookahead == "h":
        match("h")
        match("j")
        match("a")
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(["f", "c", "e", "j", "a", "h"]))

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