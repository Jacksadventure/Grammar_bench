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

def parse_a():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in a")
    lookahead = tokens[pos]
    if lookahead == '~':
        parse_f()
        parse_a()
        parse_f()
        match('f')
    elif lookahead == 'f':
        parse_f()
        parse_c()
        parse_f()
        parse_e()
        parse_g()
        match('r')
    elif lookahead == 'Q':
        parse_g()
        parse_g()
        match('g')
    elif lookahead == '|':
        parse_g()
        parse_g()
        parse_g()
        match('g')
    elif lookahead == '5':
        match('r')
    elif lookahead == '3':
        parse_g()
        match('5')
    elif lookahead == 'r':
        parse_d()
        parse_g()
        parse_f()
        parse_j()
        match('j')
    else:
        error("Unexpected token " + lookahead + " in a, expected one of: " + ", ".join(['~', 'f', 'Q', '|', '5', '3', 'r']))

def parse_b():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == ']':
        match(']')
        parse_f()
        parse_a()

def parse_c():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in c")
    lookahead = tokens[pos]
    if lookahead == ']':
        parse_g()
        parse_f()
        match('3')
    elif lookahead == '5':
        parse_b()
        parse_g()
        parse_j()
        parse_i()
        parse_g()
        match('g')
    elif lookahead == '~':
        parse_d()
        match('5')
    elif lookahead == '3':
        parse_g()
        parse_g()
        parse_e()
        match('Q')
    else:
        error("Unexpected token " + lookahead + " in c, expected one of: " + ", ".join([']', '5', '~', '3']))

def parse_d():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in d")
    lookahead = tokens[pos]
    if lookahead == 'l':
        parse_h()
        match('r')
    elif lookahead == '~':
        parse_g()
        parse_h()
        match('5')
    elif lookahead == 'g':
        parse_g()
        parse_e()
        parse_g()
        parse_c()
        parse_f()
        match('l')
    elif lookahead == 'r':
        match('l')
    elif lookahead == 'f':
        parse_f()
        match(']')
    elif lookahead == 'Q':
        parse_c()
        match(']')
    elif lookahead == '5':
        parse_g()
        match(']')
    else:
        error("Unexpected token " + lookahead + " in d, expected one of: " + ", ".join(['l', '~', 'g', 'r', 'f', 'Q', '5']))

def parse_e():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'g':
        parse_g()
        match('Q')
        parse_a()
        match('|')
        match('~')
        parse_i()
        parse_i()
        parse_f()
        match(']')

def parse_f():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'g':
        parse_g()
        match('r')
        match('r')
        match('3')
        match('~')
        match('|')
        match('l')

def parse_g():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in g")
    lookahead = tokens[pos]
    if lookahead == 'f':
        parse_f()
        parse_b()
        parse_c()
        match('|')
    elif lookahead == '~':
        parse_f()
        parse_d()
        match('~')
    elif lookahead == '5':
        match('|')
    elif lookahead == 'Q':
        match('Q')
    else:
        error("Unexpected token " + lookahead + " in g, expected one of: " + ", ".join(['f', '~', '5', 'Q']))

def parse_h():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'l':
        match('l')
        match('r')
        parse_i()
        match(']')
        parse_d()
        match(']')
        parse_f()
        parse_g()

def parse_i():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in i")
    lookahead = tokens[pos]
    if lookahead == ']':
        parse_f()
        parse_b()
        parse_b()
        parse_g()
        match('3')
    elif lookahead == 'g':
        parse_g()
        parse_f()
        match(']')
    elif lookahead == '3':
        parse_h()
        match('Q')
    elif lookahead == '~':
        parse_i()
        parse_j()
        match('j')
    elif lookahead == 'l':
        parse_j()
        parse_f()
        match('5')
    elif lookahead == 'f':
        parse_f()
        match('f')
    elif lookahead == '|':
        parse_c()
        parse_h()
        match('h')
    elif lookahead == 'r':
        match('5')
    else:
        error("Unexpected token " + lookahead + " in i, expected one of: " + ", ".join([']', 'g', '3', '~', 'l', 'f', '|', 'r']))

def parse_j():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in j")
    lookahead = tokens[pos]
    if lookahead == 'g':
        parse_g()
        match('|')
    elif lookahead == ']':
        parse_g()
        match('g')
    elif lookahead == 'r':
        parse_f()
        parse_i()
        parse_f()
        match('l')
    elif lookahead == 'Q':
        parse_a()
        match('a')
    elif lookahead == 'f':
        parse_f()
        parse_c()
        parse_f()
        match('f')
    elif lookahead == '|':
        parse_c()
        parse_f()
        match('f')
    elif lookahead == '~':
        match('~')
    elif lookahead == '5':
        parse_f()
        parse_f()
        parse_f()
        match('f')
    elif lookahead == 'l':
        parse_d()
        parse_i()
        match(']')
    elif lookahead == '3':
        parse_a()
        parse_a()
        match('a')
    else:
        error("Unexpected token " + lookahead + " in j, expected one of: " + ", ".join(['g', ']', 'r', 'Q', 'f', '|', '~', '5', 'l', '3']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_a()
    if pos != len(tokens):
        error("Extra tokens after parsing: " + " ".join(tokens[pos:]))
    print("Input accepted.")

def main():
    import sys
    if len(sys.argv) > 1:
        input_str = sys.argv[1]
    else:
        input_str = sys.stdin.read()
    parse_input(input_str)

if __name__ == "__main__":
    main()