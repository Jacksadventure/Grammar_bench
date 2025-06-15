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

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('S'):
        match('S')
        match('i')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('+'):
            match('+')
            match('f')
            match('~')
        elif lookahead.startswith('E'):
            match('E')
        elif lookahead.startswith('_'):
            match('_')
            match('r')
            match(':')
            match("'")
        elif lookahead.startswith('j'):
            match('j')
            parse_A()
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['+', 'E', '_', 'j']))
        while pos < len(tokens) and tokens[pos].startswith('d'):
            match('d')
            parse_H()
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('Q'):
            match('Q')
            parse_Y()
            match('m')
        elif lookahead.startswith('.'):
            match('.')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['Q', '.']))
    elif lookahead.startswith('4'):
        match('4')
        match('-')
    elif lookahead.startswith('%'):
        match('%')
        match('o')
    elif lookahead.startswith('c'):
        match('c')
        match('/')
    elif lookahead.startswith('v'):
        match('v')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['S', '4', '%', 'c', 'v']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('I'):
        match('I')
        match('^')
        match('(')
        parse_M()
    elif lookahead.startswith('6'):
        match('6')
        match("'")
        match('$')
    elif lookahead.startswith('E'):
        match('E')
        parse_D()
        match('s')
    elif lookahead.startswith('@'):
        match('@')
        parse_H()
        parse_Y()
        parse_D()
    elif lookahead.startswith('&'):
        match('&')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['I', '6', 'E', '@', '&']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
        match('f')
        match('~')
    elif lookahead.startswith('E'):
        match('E')
    elif lookahead.startswith('_'):
        match('_')
        match('r')
        match(':')
        match("'")
    elif lookahead.startswith('j'):
        match('j')
        parse_A()
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['+', 'E', '_', 'j']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('I'):
        match('I')
        match('*')
    elif lookahead.startswith('u'):
        match('u')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['I', 'u']))

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('!'):
        match('!')
        match('c')
        parse_L()

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('p'):
        match('p')
        parse_H()
        match('!')
        match('a')
    elif lookahead.startswith('E'):
        match('E')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['p', 'E']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('T'):
        match('T')
        match('~')
        match('I')
        parse_C()
        match('-')
    elif lookahead.startswith('*'):
        match('*')
        parse_P()
        parse_L()
    elif lookahead.startswith('Z'):
        match('Z')
        parse_A()
        match('T')
        match("'")
    elif lookahead.startswith('?'):
        match('?')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['T', '*', 'Z', '?']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('5'):
        match('5')
        parse_P()
        match('w')
        parse_Y()
    elif lookahead.startswith('<'):
        match('<')
        match("'")
        match('a')
        parse_L()
    elif lookahead.startswith('p'):
        match('p')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['5', '<', 'p']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_D()
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