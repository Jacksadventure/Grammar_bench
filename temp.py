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
    if lookahead == "l":
        match("l")
    elif lookahead == "p":
        match("p")
        parse_N()
    elif lookahead == "h":
        match("h")
        match("r")
    elif lookahead == "q":
        match("q")
    elif lookahead == "t":
        match("t")
        parse_P()
        parse_D()
    elif lookahead == "j":
        match("j")
        parse_N()
        match("d")
    elif lookahead == "r":
        match("r")
        parse_C()
    elif lookahead == "e":
        match("e")
        parse_J()
        match("g")
    elif lookahead == "i":
        match("i")
        match("h")
        parse_N()
    elif lookahead == "o":
        match("o")
        match("q")
    elif lookahead == "s":
        match("s")
        parse_N()
    elif lookahead == "g":
        match("g")
        match("o")
    elif lookahead == "n":
        match("n")
        parse_S()
        match("k")
    elif lookahead == "d":
        match("d")
        parse_D()
    elif lookahead == "b":
        match("b")
        match("m")
        parse_D()
    elif lookahead == "k":
        match("k")
        match("p")
        parse_N()
    elif lookahead == "f":
        match("f")
    elif lookahead == "a":
        match("a")
    elif lookahead == "m":
        match("m")
        parse_I()
        match("f")
    elif lookahead == "c":
        match("c")
        parse_G()
        parse_H()
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(["l", "p", "h", "q", "t", "j", "r", "e", "i", "o", "s", "g", "n", "d", "b", "k", "f", "a", "m", "c"]))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead == "p":
        match("p")
        match("p")
        parse_M()
    elif lookahead == "i":
        match("i")
        parse_R()
        parse_D()
    elif lookahead == "l":
        match("l")
        match("o")
    elif lookahead == "c":
        match("c")
        match("s")
        parse_G()
    elif lookahead == "b":
        match("b")
        match("r")
        match("m")
    elif lookahead == "h":
        match("h")
        parse_R()
    elif lookahead == "q":
        match("q")
        match("j")
        match("h")
    elif lookahead == "a":
        match("a")
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(["p", "i", "l", "c", "b", "h", "q", "a"]))

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == "h":
        match("h")
        match("b")
        parse_O()

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead == "a":
        match("a")
        match("t")
    elif lookahead == "d":
        match("d")
        match("t")
        parse_J()
    elif lookahead == "l":
        match("l")
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(["a", "d", "l"]))

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == "r":
        match("r")

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == "g":
        match("g")

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead == "h":
        match("h")
        match("c")
    elif lookahead == "q":
        match("q")
        match("o")
        parse_R()
    elif lookahead == "g":
        match("g")
    elif lookahead == "s":
        match("s")
    elif lookahead == "t":
        match("t")
        match("l")
    elif lookahead == "e":
        match("e")
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(["h", "q", "g", "s", "t", "e"]))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == "p":
        match("p")
        parse_T()

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead == "i":
        match("i")
        parse_K()
    elif lookahead == "b":
        match("b")
    elif lookahead == "p":
        match("p")
    elif lookahead == "a":
        match("a")
    elif lookahead == "m":
        match("m")
        parse_E()
        parse_I()
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(["i", "b", "p", "a", "m"]))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead == "b":
        match("b")
    elif lookahead == "e":
        match("e")
        match("n")
        match("k")
    elif lookahead == "l":
        match("l")
        parse_Q()
        match("a")
    elif lookahead == "d":
        match("d")
        match("a")
    elif lookahead == "o":
        match("o")
        match("r")
        parse_L()
    elif lookahead == "q":
        match("q")
        parse_G()
        match("j")
    elif lookahead == "c":
        match("c")
        parse_T()
    elif lookahead == "s":
        match("s")
    elif lookahead == "m":
        match("m")
    elif lookahead == "t":
        match("t")
        parse_I()
        parse_R()
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(["b", "e", "l", "d", "o", "q", "c", "s", "m", "t"]))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead == "h":
        match("h")
    elif lookahead == "t":
        match("t")
        match("p")
    elif lookahead == "m":
        match("m")
        match("i")
        parse_K()
    elif lookahead == "e":
        match("e")
        parse_I()
    elif lookahead == "l":
        match("l")
        match("m")
        parse_G()
    elif lookahead == "g":
        match("g")
        parse_C()
    elif lookahead == "p":
        match("p")
        match("k")
    elif lookahead == "a":
        match("a")
        parse_G()
        parse_L()
    elif lookahead == "r":
        match("r")
        parse_S()
        match("q")
    elif lookahead == "s":
        match("s")
        parse_I()
    elif lookahead == "f":
        match("f")
        match("e")
    elif lookahead == "d":
        match("d")
        parse_C()
        match("j")
    elif lookahead == "b":
        match("b")
        parse_P()
    elif lookahead == "i":
        match("i")
        match("a")
    elif lookahead == "o":
        match("o")
    elif lookahead == "n":
        match("n")
        match("f")
        match("q")
    elif lookahead == "c":
        match("c")
    elif lookahead == "k":
        match("k")
        match("t")
        parse_A()
    elif lookahead == "j":
        match("j")
    elif lookahead == "q":
        match("q")
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(["h", "t", "m", "e", "l", "g", "p", "a", "r", "s", "f", "d", "b", "i", "o", "n", "c", "k", "j", "q"]))

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == "j":
        match("j")
        parse_A()

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead == "o":
        match("o")
        parse_C()
    elif lookahead == "l":
        match("l")
    elif lookahead == "m":
        match("m")
    elif lookahead == "j":
        match("j")
    elif lookahead == "q":
        match("q")
    elif lookahead == "k":
        match("k")
        parse_I()
        match("q")
    elif lookahead == "s":
        match("s")
        match("k")
        match("o")
    elif lookahead == "d":
        match("d")
    elif lookahead == "p":
        match("p")
        parse_S()
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(["o", "l", "m", "j", "q", "k", "s", "d", "p"]))

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == "a":
        match("a")
        match("i")
        parse_K()

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead == "o":
        match("o")
        match("s")
    elif lookahead == "i":
        match("i")
    elif lookahead == "p":
        match("p")
    elif lookahead == "a":
        match("a")
    elif lookahead == "m":
        match("m")
        match("t")
    elif lookahead == "h":
        match("h")
    elif lookahead == "e":
        match("e")
        parse_F()
    elif lookahead == "b":
        match("b")
    elif lookahead == "f":
        match("f")
        parse_T()
    elif lookahead == "s":
        match("s")
        match("m")
    elif lookahead == "g":
        match("g")
        parse_F()
    elif lookahead == "l":
        match("l")
        parse_P()
        match("o")
    elif lookahead == "q":
        match("q")
        parse_E()
    elif lookahead == "c":
        match("c")
    elif lookahead == "j":
        match("j")
        match("d")
    elif lookahead == "t":
        match("t")
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(["o", "i", "p", "a", "m", "h", "e", "b", "f", "s", "g", "l", "q", "c", "j", "t"]))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead == "d":
        match("d")
        match("c")
        parse_T()
        parse_Q()
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(["d", ""]))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead == "r":
        match("r")
    elif lookahead == "m":
        match("m")
        parse_I()
    elif lookahead == "b":
        match("b")
    elif lookahead == "e":
        match("e")
    elif lookahead == "k":
        match("k")
        match("o")
        parse_J()
    elif lookahead == "g":
        match("g")
        parse_L()
    elif lookahead == "f":
        match("f")
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(["r", "m", "b", "e", "k", "g", "f"]))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead == "t":
        match("t")
    elif lookahead == "h":
        match("h")
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(["t", "h"]))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead == "h":
        match("h")
    elif lookahead == "k":
        match("k")
        match("t")
        parse_N()
    elif lookahead == "b":
        match("b")
    elif lookahead == "o":
        match("o")
    elif lookahead == "a":
        match("a")
        match("h")
    elif lookahead == "i":
        match("i")
        parse_K()
        parse_E()
    elif lookahead == "c":
        match("c")
        match("n")
    elif lookahead == "g":
        match("g")
    elif lookahead == "r":
        match("r")
        match("c")
        parse_T()
    elif lookahead == "t":
        match("t")
        match("b")
        match("p")
    elif lookahead == "m":
        match("m")
        parse_B()
    elif lookahead == "s":
        match("s")
        parse_O()
    elif lookahead == "l":
        match("l")
        match("m")
        match("q")
    elif lookahead == "q":
        match("q")
        match("t")
        parse_N()
    elif lookahead == "n":
        match("n")
    elif lookahead == "j":
        match("j")
    elif lookahead == "f":
        match("f")
        match("d")
    elif lookahead == "p":
        match("p")
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(["h", "k", "b", "o", "a", "i", "c", "g", "r", "t", "m", "s", "l", "q", "n", "j", "f", "p"]))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead == "a":
        match("a")
        parse_D()
    elif lookahead == "b":
        match("b")
        match("t")
        parse_R()
    elif lookahead == "n":
        match("n")
        match("p")
    elif lookahead == "q":
        match("q")
    elif lookahead == "j":
        match("j")
    elif lookahead == "g":
        match("g")
    elif lookahead == "c":
        match("c")
        parse_F()
    elif lookahead == "h":
        match("h")
        match("i")
        parse_T()
    elif lookahead == "i":
        match("i")
        parse_P()
    elif lookahead == "l":
        match("l")
        parse_A()
        parse_Q()
    elif lookahead == "k":
        match("k")
        match("f")
        parse_C()
    elif lookahead == "p":
        match("p")
        parse_O()
    elif lookahead == "e":
        match("e")
        parse_C()
        parse_N()
    elif lookahead == "s":
        match("s")
        parse_C()
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(["a", "b", "n", "q", "j", "g", "c", "h", "i", "l", "k", "p", "e", "s"]))

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