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
    if lookahead == 'z':
        match('T')
    elif lookahead == 'L':
        parse_h()
        match('~')
    elif lookahead == '$':
        match('$')
    elif lookahead == '&':
        parse_h()
        parse_o()
        parse_e()
        match('e')
    elif lookahead == '.':
        match('=')
    elif lookahead == 'H':
        parse_h()
        parse_c()
        parse_p()
        match('"')
    elif lookahead == 'h':
        parse_h()
        parse_g()
        parse_j()
        parse_b()
        parse_f()
        match('f')
    elif lookahead == 'T':
        parse_o()
        match('<')
    elif lookahead == '|':
        parse_b()
        parse_g()
        match('L')
    elif lookahead == 'L':
        match('&')
    else:
        error("Unexpected token " + lookahead + " in a, expected one of: " + ", ".join(['z', 'L', '$', '&', '.', 'H', 'h', 'T', '|', 'L']))

def parse_b():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '.':
        match('.')
        match('T')

def parse_c():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in c")
    lookahead = tokens[pos]
    if lookahead == '.':
        parse_h()
        parse_h()
        match('h')
    elif lookahead == 'x':
        parse_f()
        match("'")
    elif lookahead == "'":
        parse_l()
        parse_h()
        match('&')
    elif lookahead == 'w':
        parse_h()
        match('x')
    elif lookahead == '<':
        parse_d()
        parse_l()
        match('&')
    elif lookahead == '"':
        parse_c()
        match('z')
    elif lookahead == '|':
        parse_c()
        parse_j()
        match('~')
    elif lookahead == 'z':
        match('z')
    elif lookahead == 'L':
        match('&')
    else:
        error("Unexpected token " + lookahead + " in c, expected one of: " + ", ".join(['.', 'x', "'", 'w', '<', '"', '|', 'z', 'L']))

def parse_d():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'w':
        match('w')
        match('T')
        match('.')
        parse_h()
        match('~')
        parse_j()
        parse_h()
        match('L')
        match('&')
        match('z')

def parse_e():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in e")
    lookahead = tokens[pos]
    if lookahead == 'H':
        parse_k()
        parse_j()
        match('w')
    elif lookahead == '.':
        parse_g()
        parse_c()
        match('=')
    elif lookahead == '~':
        parse_n()
        parse_p()
        parse_h()
        match('L')
    elif lookahead == '=':
        parse_l()
        parse_c()
        parse_k()
        parse_i()
        match('i')
    elif lookahead == 'T':
        match('L')
    elif lookahead == '"':
        parse_d()
        parse_p()
        parse_i()
        parse_o()
        match('"')
    elif lookahead == '<':
        parse_h()
        parse_d()
        match('d')
    elif lookahead == "'":
        match('"')
    elif lookahead == 'x':
        parse_b()
        match('&')
    elif lookahead == '|':
        parse_k()
        match('x')
    elif lookahead == 'w':
        match('w')
    elif lookahead == 'L':
        match('L')
    elif lookahead == 'h':
        parse_h()
        parse_e()
        parse_j()
        match('T')
    elif lookahead == 'z':
        match('=')
    elif lookahead == '&':
        parse_m()
        match('m')
    else:
        error("Unexpected token " + lookahead + " in e, expected one of: " + ", ".join(['H', '.', '~', '=', 'T', '"', '<', "'", 'x', '|', 'w', 'L', 'h', 'z', '&']))

def parse_f():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in f")
    lookahead = tokens[pos]
    if lookahead == 'h':
        parse_h()
        parse_p()
        parse_l()
        parse_b()
        match('b')
    elif lookahead == 'w':
        match('w')
    elif lookahead == 'z':
        parse_h()
        match('h')
    elif lookahead == '|':
        parse_h()
        parse_h()
        match('h')
    elif lookahead == 'x':
        parse_l()
        parse_e()
        parse_n()
        parse_h()
        parse_l()
        parse_h()
        match('x')
    elif lookahead == 'T':
        match('&')
    elif lookahead == 'L':
        parse_h()
        parse_a()
        parse_c()
        parse_o()
        parse_n()
        parse_h()
        match('<')
    elif lookahead == '$':
        match('$')
    elif lookahead == '=':
        match('x')
    elif lookahead == '~':
        match('~')
    elif lookahead == '<':
        parse_n()
        parse_h()
        match('=')
    else:
        error("Unexpected token " + lookahead + " in f, expected one of: " + ", ".join(['h', 'w', 'z', '|', 'x', 'T', 'L', '$', '=', '~', '<']))

def parse_g():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '=':
        match('=')

def parse_h():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in h")
    lookahead = tokens[pos]
    if lookahead == '~':
        parse_l()
        parse_h()
        match('<')
    elif lookahead == '.':
        parse_h()
        parse_l()
        parse_e()
        parse_h()
        match("'")
    elif lookahead == '&':
        parse_d()
        match('d')
    elif lookahead == '~':
        match('~')
    else:
        error("Unexpected token " + lookahead + " in h, expected one of: " + ", ".join(['~', '.', '&', '~']))

def parse_i():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in i")
    lookahead = tokens[pos]
    if lookahead == 'h':
        parse_h()
        parse_g()
        match('x')
    elif lookahead == '.':
        match('.')
    elif lookahead == "'":
        parse_h()
        parse_h()
        match('T')
    elif lookahead == '$':
        parse_b()
        parse_a()
        parse_m()
        parse_n()
        parse_h()
        match('=')
    elif lookahead == '<':
        match('L')
    elif lookahead == '=':
        parse_n()
        parse_h()
        parse_i()
        match('H')
    elif lookahead == '|':
        match('"')
    elif lookahead == 'H':
        match("'")
    elif lookahead == 'w':
        parse_c()
        parse_p()
        match('p')
    elif lookahead == 'x':
        parse_d()
        parse_h()
        match('h')
    elif lookahead == '"':
        parse_c()
        match('c')
    else:
        error("Unexpected token " + lookahead + " in i, expected one of: " + ", ".join(['h', '.', "'", '$', '<', '=', '|', 'H', 'w', 'x', '"']))

def parse_j():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '~':
        match('~')
        parse_c()

def parse_k():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'h':
        parse_h()
        match('L')
        match("'")
        parse_b()
        parse_n()
        parse_o()
        parse_h()
        parse_h()

def parse_l():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in l")
    lookahead = tokens[pos]
    if lookahead == '"':
        match('=')
    elif lookahead == '|':
        match('~')
    elif lookahead == "'":
        parse_h()
        parse_h()
        match('h')
    elif lookahead == '&':
        parse_a()
        parse_o()
        parse_g()
        parse_n()
        parse_h()
        match('h')
    elif lookahead == 'L':
        parse_a()
        parse_e()
        parse_i()
        match('i')
    elif lookahead == '<':
        parse_m()
        match('m')
    elif lookahead == 'w':
        parse_h()
        match('h')
    elif lookahead == 'T':
        parse_f()
        match('H')
    elif lookahead == '$':
        parse_c()
        match('"')
    elif lookahead == 'z':
        match('z')
    else:
        error("Unexpected token " + lookahead + " in l, expected one of: " + ", ".join(['"', '|', "'", '&', 'L', '<', 'w', 'T', '$', 'z']))

def parse_m():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == "'":
        match("'")
        match('T')
        parse_h()
        match('z')
        match('.')
        match('"')
        match('w')
        parse_j()
        match('z')

def parse_n():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in n")
    lookahead = tokens[pos]
    if lookahead == '<':
        parse_b()
        match('T')
    elif lookahead == '"':
        parse_g()
        parse_k()
        parse_a()
        match('|')
    elif lookahead == 'z':
        parse_p()
        parse_e()
        parse_k()
        parse_h()
        parse_c()
        parse_g()
        parse_e()
        match('e')
    elif lookahead == '&':
        parse_l()
        parse_g()
        parse_m()
        match('.')
    elif lookahead == 'w':
        parse_h()
        parse_m()
        parse_a()
        match('|')
    elif lookahead == '=':
        parse_n()
        parse_i()
        match('i')
    elif lookahead == '|':
        match('L')
    elif lookahead == '~':
        parse_b()
        match("'")
    elif lookahead == 'H':
        match('H')
    elif lookahead == 'T':
        parse_p()
        parse_h()
        parse_i()
        match('H')
    elif lookahead == '$':
        parse_h()
        match('h')
    elif lookahead == 'x':
        match('z')
    elif lookahead == 'h':
        parse_h()
        parse_i()
        parse_h()
        match('"')
    else:
        error("Unexpected token " + lookahead + " in n, expected one of: " + ", ".join(['<', '"', 'z', '&', 'w', '=', '|', '~', 'H', 'T', '$', 'x', 'h']))

def parse_o():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in o")
    lookahead = tokens[pos]
    if lookahead == '$':
        parse_m()
        parse_b()
        parse_c()
        match('&')
    elif lookahead == "'":
        parse_h()
        parse_a()
        parse_k()
        match('|')
    elif lookahead == 'z':
        match('z')
    elif lookahead == 'T':
        parse_p()
        match('p')
    elif lookahead == 'w':
        parse_h()
        parse_m()
        parse_l()
        parse_h()
        match('h')
    elif lookahead == '|':
        match('&')
    elif lookahead == '~':
        parse_o()
        parse_e()
        match('e')
    elif lookahead == '<':
        match('.')
    elif lookahead == '.':
        parse_i()
        match('i')
    elif lookahead == '"':
        parse_d()
        parse_i()
        match('~')
    elif lookahead == '=':
        parse_a()
        parse_c()
        parse_m()
        parse_h()
        match('h')
    else:
        error("Unexpected token " + lookahead + " in o, expected one of: " + ", ".join(['$', "'", 'z', 'T', 'w', '|', '~', '<', '.', '"', '=']))

def parse_p():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'w':
        match('w')
        parse_j()
        parse_i()
        match('L')
        match('<')

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