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

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('>'):
        match('>')
        match('m')
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('B'):
            match('B')
            match('-')
            parse_L()
        elif lookahead.startswith('&'):
            match('&')
            parse_A()
            match('/')
        elif lookahead.startswith('_'):
            match('_')
            match('P')
            parse_H()
            parse_A()
        elif lookahead.startswith('!'):
            match('!')
            parse_I()
            match('>')
            match(',')
        elif lookahead.startswith('^'):
            match('^')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['B', '&', '_', '!', '^']))
    elif lookahead.startswith('W'):
        match('W')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['>', 'W']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        match('*')
        match('n')
    elif lookahead.startswith('#'):
        match('#')
        match('j')
    elif lookahead.startswith('l'):
        match('l')
        parse_L()
        parse_I()
        parse_N()
    elif lookahead.startswith('}'):
        match('}')
        match('t')
    elif lookahead.startswith('t'):
        match('t')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['?', '#', 'l', '}', 't']))

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('6'):
        match('6')
    elif lookahead.startswith('4'):
        match('4')
        match('?')
        match('O')
        match('n')
    elif lookahead.startswith('%'):
        match('%')
    elif lookahead.startswith('J'):
        match('J')
        match('0')
        match('t')
        match('8')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['6', '4', '%', 'J']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('C'):
        match('C')
        match('C')
        match('>')
        parse_D()
    elif lookahead.startswith('t'):
        match('t')
    elif lookahead.startswith('c'):
        match('c')
        match('R')
    elif lookahead.startswith('^'):
        match('^')
        parse_L()
        match('e')
        match('t')
    elif lookahead.startswith('1'):
        match('1')
        match('(')
        match('k')
        match('U')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['C', 't', 'c', '^', '1']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('B'):
        match('B')
        match('-')
        parse_L()
    elif lookahead.startswith('&'):
        match('&')
        parse_A()
        match('/')
    elif lookahead.startswith('_'):
        match('_')
        match('P')
        parse_H()
        parse_A()
    elif lookahead.startswith('!'):
        match('!')
        parse_I()
        match('>')
        match(',')
    elif lookahead.startswith('^'):
        match('^')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['B', '&', '_', '!', '^']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('K'):
        match('K')
        match('w')
        match('~')
    elif lookahead.startswith('e'):
        match('e')
        match('~')
        parse_Z()
        parse_Y()
    elif lookahead.startswith("'"):
        match("'")
    elif lookahead.startswith(']'):
        match(']')
        match('R')
        match('|')
    elif lookahead.startswith('4'):
        match('4')
        match('S')
        match('~')
        match("'")
        match('Q')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['K', 'e', "'", ']', '4']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('E'):
        match('E')
        match('1')
        match('B')
        match('(')
    elif lookahead.startswith('L'):
        parse_L()
        parse_N()
        match("'")
        match('e')
        match('0')
    elif lookahead.startswith('T'):
        match('T')
        parse_L()
    elif lookahead.startswith('['):
        match('[')
        match('V')
        match('!')
    elif lookahead.startswith('d'):
        match('d')
        match('J')
        match('m')
    elif lookahead.startswith('_'):
        match('_')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['E', 'L', 'T', '[', 'd', '_']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('E'):
        match('E')
        match('w')
        match('h')
    elif lookahead.startswith('e'):
        match('e')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['E', 'e']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_I()
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