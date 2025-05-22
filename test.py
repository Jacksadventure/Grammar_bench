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
    if lookahead == 'E':
        match('/')
    elif lookahead == 'P':
        match('E')
    elif lookahead == 'k':
        match('P')
    elif lookahead == '/':
        match(']')
    elif lookahead == 'o':
        match('k')
    elif lookahead == '_':
        match('_')
    elif lookahead == '*':
        parse_f()
        parse_b()
        match('k')
    else:
        error("Unexpected token " + lookahead + " in a, expected one of: " + ", ".join(['E', 'P', 'k', '/', 'o', '_', '*']))

def parse_b():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in b")
    lookahead = tokens[pos]
    if lookahead == 'm':
        match('P')
    elif lookahead == 'k':
        parse_h()
        match('k')
    else:
        error("Unexpected token " + lookahead + " in b, expected one of: " + ", ".join(['m', 'k']))

def parse_c():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in c")
    lookahead = tokens[pos]
    if lookahead == 'E':
        match('*')
    elif lookahead == 'o':
        match(']')
    elif lookahead == '4':
        match('k')
    elif lookahead == '_':
        match(']')
    elif lookahead == '*':
        match('4')
    elif lookahead == 'k':
        match('4')
    elif lookahead == ']':
        match('m')
    elif lookahead == 'm':
        match('m')
    elif lookahead == 'P':
        match(']')
    elif lookahead == '/':
        match('4')
    else:
        error("Unexpected token " + lookahead + " in c, expected one of: " + ", ".join(['E', 'o', '4', '_', '*', 'k', ']', 'm', 'P', '/']))

def parse_d():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in d")
    lookahead = tokens[pos]
    if lookahead == '_':
        match('4')
    elif lookahead == '4':
        match('k')
    elif lookahead == '*':
        parse_b()
        parse_h()
        match('_')
    else:
        error("Unexpected token " + lookahead + " in d, expected one of: " + ", ".join(['_', '4', '*']))

def parse_e():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in e")
    lookahead = tokens[pos]
    if lookahead == 'P':
        parse_f()
        match('_')
    elif lookahead == 'm':
        match('P')
    elif lookahead == 'k':
        parse_j()
        parse_g()
        match('/')
    elif lookahead == '4':
        match('4')
    elif lookahead == '_':
        parse_b()
        match('b')
    elif lookahead == 'o':
        parse_f()
        parse_a()
        match('a')
    elif lookahead == '/':
        match('4')
    elif lookahead == '*':
        parse_a()
        match(']')
    elif lookahead == 'E':
        parse_c()
        match('/')
    elif lookahead == ']':
        parse_a()
        match('k')
    else:
        error("Unexpected token " + lookahead + " in e, expected one of: " + ", ".join(['P', 'm', 'k', '4', '_', 'o', '/', '*', 'E', ']']))

def parse_f():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in f")
    lookahead = tokens[pos]
    if lookahead == '4':
        parse_g()
        parse_a()
        match('k')
    elif lookahead == 'E':
        parse_c()
        match('c')
    elif lookahead == 'k':
        match('_')
    elif lookahead == '/':
        parse_d()
        match('E')
    elif lookahead == 'm':
        match('*')
    elif lookahead == '*':
        match('k')
    elif lookahead == 'P':
        match('4')
    else:
        error("Unexpected token " + lookahead + " in f, expected one of: " + ", ".join(['4', 'E', 'k', '/', 'm', '*', 'P']))

def parse_g():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '4':
        match('4')
        match('m')
        match('o')
        parse_h()
        match('E')
        match('E')

def parse_h():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in h")
    lookahead = tokens[pos]
    if lookahead == 'E':
        parse_a()
        match('m')
    elif lookahead == 'P':
        parse_j()
        match('j')
    elif lookahead == '_':
        match('*')
    elif lookahead == '/':
        match('4')
    elif lookahead == 'o':
        match('P')
    else:
        error("Unexpected token " + lookahead + " in h, expected one of: " + ", ".join(['E', 'P', '_', '/', 'o']))

def parse_i():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in i")
    lookahead = tokens[pos]
    if lookahead == 'o':
        parse_j()
        match('/')
    elif lookahead == '4':
        match('m')
    elif lookahead == '_':
        match('m')
    elif lookahead == '/':
        match('m')
    elif lookahead == 'm':
        match('E')
    elif lookahead == ']':
        parse_d()
        match('4')
    elif lookahead == '*':
        match('*')
    elif lookahead == 'k':
        match('k')
    elif lookahead == 'P':
        match('_')
    elif lookahead == 'E':
        match('*')
    else:
        error("Unexpected token " + lookahead + " in i, expected one of: " + ", ".join(['o', '4', '_', '/', 'm', ']', '*', 'k', 'P', 'E']))

def parse_j():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in j")
    lookahead = tokens[pos]
    if lookahead == 'o':
        match('k')
    elif lookahead == '4':
        match('o')
    elif lookahead == 'm':
        parse_i()
        match('m')
    elif lookahead == '/':
        match(']')
    elif lookahead == 'E':
        parse_j()
        match('o')
    elif lookahead == 'k':
        match('4')
    else:
        error("Unexpected token " + lookahead + " in j, expected one of: " + ", ".join(['o', '4', 'm', '/', 'E', 'k']))

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