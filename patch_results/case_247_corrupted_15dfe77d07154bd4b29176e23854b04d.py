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
    if lookahead.startswith('['):
        match('[')
        match('1')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('d'):
            match('d')
            parse_S()
            parse_S()
            parse_K()
        elif lookahead.startswith('*'):
            match('*')
        elif lookahead.startswith('_'):
            match('_')
            match('<')
            match('<')
            match(',')
        elif lookahead.startswith('K'):
            parse_K()
            match('y')
            parse_X()
            match('c')
            match('y')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['d', '*', '_', 'K']))
    elif lookahead.startswith('N'):
        match('N')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['[', 'N']))

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(')'):
        match(')')
        parse_E()
        match('g')

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('@'):
        match('@')
        match('h')
    elif lookahead.startswith('J'):
        match('J')
        match('`')
        parse_L()
        match('&')
    elif lookahead.startswith('m'):
        match('m')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['@', 'J', 'm']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith(':'):
        match(':')
        match('P')
        parse_I()
        match('?')
        match('i')
    elif lookahead.startswith('|'):
        match('|')
        match('O')
        parse_X()
        match('=')
    elif lookahead.startswith('f'):
        match('f')
        parse_I()
        parse_G()
    elif lookahead.startswith('&'):
        match('&')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join([':', '|', 'f', '&']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('T'):
        match('T')
        match('{')
        match('>')
        match('f')
        parse_L()
    elif lookahead.startswith('W'):
        match('W')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['T', 'W']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('H'):
        match('H')
        match('y')
        match('&')
        match('b')
    elif lookahead.startswith('W'):
        match('W')
        match("'")
        match('<')
    elif lookahead.startswith('?'):
        match('?')
        parse_G()
    elif lookahead.startswith('z'):
        match('z')
    elif lookahead.startswith('2'):
        match('2')
        match('`')
        match('?')
        match('.')
        parse_I()
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['H', 'W', '?', 'z', '2']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('c'):
        match('c')

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