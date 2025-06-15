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

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('5'):
        match('5')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('_'):
            match('_')
        elif lookahead.startswith('^'):
            match('^')
            match('%')
            match(']')
            parse_V()
        elif lookahead.startswith('&'):
            match('&')
            parse_C()
        elif lookahead.startswith('1'):
            match('1')
            match('w')
            match('{')
        elif lookahead.startswith(')'):
            match(')')
            parse_L()
            parse_G()
            match('N')
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['_', '^', '&', '1', ')']))
    elif lookahead.startswith('('):
        match('(')
        match('p')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('|'):
            match('|')
            match('S')
            parse_L()
            match('=')
        elif lookahead.startswith('!'):
            match('!')
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['|', '!']))
        match('|')
        match('j')
    elif lookahead.startswith('^'):
        match('^')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['5', '(', '^']))

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('I'):
        match('I')
        parse_M()
        match('f')

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('c'):
        match('c')
        match('!')
        parse_L()
        match('>')
        match("'")
    elif lookahead.startswith('i'):
        match('i')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['c', 'i']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('q'):
        match('q')
    elif lookahead.startswith('@'):
        match('@')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['q', '@']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('_'):
        match('_')
    elif lookahead.startswith('^'):
        match('^')
        match('%')
        match(']')
        parse_V()
    elif lookahead.startswith('&'):
        match('&')
        parse_C()
    elif lookahead.startswith('1'):
        match('1')
        match('w')
        match('{')
    elif lookahead.startswith(')'):
        match(')')
        parse_L()
        parse_G()
        match('N')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['_', '^', '&', '1', ')']))

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('|'):
        match('|')
        match('S')
        parse_L()
        match('=')
    elif lookahead.startswith('!'):
        match('!')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['|', '!']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('p'):
        match('p')
    elif lookahead.startswith('E'):
        match('E')
        parse_L()
        match('0')
        parse_V()
        match('$')
    elif lookahead.startswith('<'):
        match('<')
        match('v')
        parse_Z()
    elif lookahead.startswith('Y'):
        match('Y')
        parse_M()
        parse_A()
    elif lookahead.startswith('7'):
        match('7')
        parse_F()
        match('s')
        match('i')
        match('N')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['p', 'E', '<', 'Y', '7']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('T'):
        match('T')
        match('j')
        match('=')
    elif lookahead.startswith('V'):
        parse_V()
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['T', 'V']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_F()
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