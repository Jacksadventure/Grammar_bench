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

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('l'):
        match('l')
        match('g')
        match('<')
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('%'):
            match('%')
            match('>')
            match('Z')
            parse_W()
            match('N')
        elif lookahead.startswith('L'):
            parse_L()
            match('*')
        elif lookahead.startswith('m'):
            match('m')
            match('(')
            match('4')
        elif lookahead.startswith('{'):
            match('{')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['%', 'L', 'm', '{']))
    elif lookahead.startswith('['):
        match('[')
        match('b')
        match('C')
    elif lookahead.startswith('B'):
        match('B')
        match('~')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('='):
            match('=')
            match('u')
            match('n')
            match('f')
            parse_X()
        elif lookahead.startswith('C'):
            match('C')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['=', 'C']))
        match('h')
    elif lookahead.startswith('~'):
        match('~')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['l', '[', 'B', '~']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('e'):
        match('e')
        match('%')
    elif lookahead.startswith('='):
        match('=')
        match('?')
        parse_D()
        match('K')
    elif lookahead.startswith('Q'):
        match('Q')
        match('w')
        match('.')
        match('~')
        match('l')
    elif lookahead.startswith('/'):
        match('/')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['e', '=', 'Q', '/']))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        match('x')
    elif lookahead.startswith('<'):
        match('<')
    elif lookahead.startswith('m'):
        match('m')
    elif lookahead.startswith('g'):
        match('g')
        parse_W()
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(["'", '<', 'm', 'g']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('='):
        match('=')
        match('u')
        match('n')
        match('f')
        parse_X()
    elif lookahead.startswith('C'):
        match('C')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['=', 'C']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('I'):
        match('I')
        parse_E()
    elif lookahead.startswith('-'):
        match('-')
        match("'")
        match('_')
        match('i')
        parse_W()
    elif lookahead.startswith('&'):
        match('&')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['I', '-', '&']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_L()
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