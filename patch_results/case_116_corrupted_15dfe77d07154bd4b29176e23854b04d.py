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

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('f'):
        match('f')
        match('k')
        match('/')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('u'):
            match('u')
            match('c')
            match('q')
        elif lookahead.startswith(']'):
            match(']')
            match('o')
            parse_G()
        elif lookahead.startswith('3'):
            match('3')
            match('/')
            parse_G()
            match('=')
            match('[')
        elif lookahead.startswith('c'):
            match('c')
            match('^')
            match('x')
            match("'")
            match('h')
        elif lookahead.startswith('k'):
            match('k')
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['u', ']', '3', 'c', 'k']))
        match('m')
    elif lookahead.startswith('n'):
        match('n')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('*'):
            match('*')
            match('H')
            parse_A()
            match('@')
        elif lookahead.startswith('H'):
            match('H')
        elif lookahead.startswith('-'):
            match('-')
            match('f')
            match('>')
            match('Z')
        elif lookahead.startswith('y'):
            match('y')
            match(',')
            match("'")
            match('1')
            match('8')
        elif lookahead.startswith('}'):
            match('}')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['*', 'H', '-', 'y', '}']))
    elif lookahead.startswith('@'):
        match('@')
        match('T')
        while pos < len(tokens) and tokens[pos].startswith('6'):
            match('6')
            parse_W()
        match(';')
    elif lookahead.startswith('g'):
        match('g')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['f', 'n', '@', 'g']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('*'):
        match('*')
        match('H')
        parse_A()
        match('@')
    elif lookahead.startswith('H'):
        match('H')
    elif lookahead.startswith('-'):
        match('-')
        match('f')
        match('>')
        match('Z')
    elif lookahead.startswith('y'):
        match('y')
        match(',')
        match("'")
        match('1')
        match('8')
    elif lookahead.startswith('}'):
        match('}')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['*', 'H', '-', 'y', '}']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('6'):
        match('6')
        parse_W()

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('u'):
        match('u')
        match('c')
        match('q')
    elif lookahead.startswith(']'):
        match(']')
        match('o')
        parse_G()
    elif lookahead.startswith('3'):
        match('3')
        match('/')
        parse_G()
        match('=')
        match('[')
    elif lookahead.startswith('c'):
        match('c')
        match('^')
        match('x')
        match("'")
        match('h')
    elif lookahead.startswith('k'):
        match('k')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['u', ']', '3', 'c', 'k']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Y()
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