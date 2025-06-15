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

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        match(')')
    elif lookahead.startswith(')'):
        match(')')
        match('s')
    elif lookahead.startswith('p'):
        match('p')
        match('T')
        match('D')
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('w'):
            match('w')
            match(':')
            parse_A()
            match('k')
            parse_W()
        elif lookahead.startswith('&'):
            match('&')
            match('M')
            parse_W()
            parse_O()
        elif lookahead.startswith('='):
            match('=')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['w', '&', '=']))
    elif lookahead.startswith('S'):
        match('S')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['/', ')', 'p', 'S']))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        match(':')
        parse_A()
        match('k')
        parse_W()
    elif lookahead.startswith('&'):
        match('&')
        match('M')
        parse_W()
        parse_O()
    elif lookahead.startswith('='):
        match('=')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['w', '&', '=']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('a'):
        match('a')
        match('o')
        match('{')
        parse_W()
        parse_X()

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('a'):
        match('a')
        parse_W()
    elif lookahead.startswith('?'):
        match('?')
    elif lookahead.startswith('t'):
        match('t')
        match('C')
    elif lookahead.startswith('R'):
        match('R')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['a', '?', 't', 'R']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_O()
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