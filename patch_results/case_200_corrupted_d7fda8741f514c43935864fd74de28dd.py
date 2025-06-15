import sys

tokens = []
pos = 0

def error(msg):
    print("Parse error:", msg)
    sys.exit(1)

def match(expected):
    global pos, tokens
    if pos < len(tokens) and tokens[pos].startswith(expected):
        pos += 1
    else:
        error("Expected " + expected + ", got " + (tokens[pos] if pos < len(tokens) else "EOF"))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('s'):
        match('s')
        match('=')
        match('K')
        match('/')
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('e'):
            match('e')
            parse_Y()
            match('s')
            match('j')
            match('K')
        elif lookahead.startswith('E'):
            match('E')
            parse_C()
        elif lookahead.startswith('O'):
            match('O')
            match('Q')
            match(']')
            parse_G()
        elif lookahead.startswith('C'):
            parse_C()
            parse_L()
        elif lookahead.startswith('#'):
            match('#')
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['e', 'E', 'O', 'C', '#']))
    elif lookahead.startswith("'"):
        match("'")
        match('4')
    elif lookahead.startswith('x'):
        match('x')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['s', "'", 'x']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('['):
        match('[')
        match('y')
        parse_L()
        match('P')
        match('s')
    elif lookahead.startswith('U'):
        match('U')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['[', 'U']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('e'):
        match('e')
        parse_Y()
        match('s')
        match('j')
        match('K')
    elif lookahead.startswith('E'):
        match('E')
        parse_C()
    elif lookahead.startswith('O'):
        match('O')
        match('Q')
        match(']')
        parse_G()
    elif lookahead.startswith('C'):
        parse_C()
        parse_L()
    elif lookahead.startswith('#'):
        match('#')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['e', 'E', 'O', 'C', '#']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('s'):
        match('s')
        match('s')
        match('b')
    elif lookahead.startswith('%'):
        match('%')
        match('D')
    elif lookahead.startswith('/'):
        match('/')
        parse_T()
        parse_T()
    elif lookahead.startswith('&'):
        match('&')
        match('x')
        match('8')
        match('.')
        match('w')
    elif lookahead.startswith('W'):
        match('W')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['s', '%', '/', '&', 'W']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('R'):
        match('R')
        parse_X()
    elif lookahead.startswith('O'):
        match('O')
        match('i')
        match('o')
        match('9')
    elif lookahead.startswith('E'):
        match('E')
        parse_L()
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['R', 'O', 'E']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('k'):
        match('k')
        parse_S()
        match('i')
        match('c')
        parse_Y()
    elif lookahead.startswith('V'):
        match('V')
        match('U')
        match('K')
    elif lookahead.startswith('o'):
        match('o')
        match('b')
    elif lookahead.startswith('A'):
        match('A')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['k', 'V', 'o', 'A']))

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('a'):
        match('a')
        match("'")

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        match('q')
        parse_L()
    elif lookahead.startswith('-'):
        match('-')
        match('+')
        match('?')
    elif lookahead.startswith('i'):
        match('i')
    elif lookahead.startswith('k'):
        match('k')
        parse_T()
        match('~')
        parse_M()
        match('(')
    elif lookahead.startswith('l'):
        match('l')
        match('1')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['o', '-', 'i', 'k', 'l']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_X()
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