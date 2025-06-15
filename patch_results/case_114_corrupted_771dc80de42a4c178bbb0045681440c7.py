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

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('@'):
        match('@')
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith('v'):
            match('v')
            parse_N()
        elif lookahead.startswith('k'):
            match('k')
            parse_S()
            match('w')
            parse_X()
        elif lookahead.startswith('O'):
            match('O')
            parse_X()
        elif lookahead.startswith('Z'):
            match('Z')
            match('{')
            match('B')
            parse_X()
        elif lookahead.startswith('0'):
            match('0')
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['v', 'k', 'O', 'Z', '0']))
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('='):
            match('=')
            match('0')
            parse_X()
        elif lookahead.startswith('t'):
            match('t')
            match('_')
        elif lookahead.startswith('0'):
            match('0')
            parse_P()
            parse_L()
        elif lookahead.startswith('/'):
            match('/')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['=', 't', '0', '/']))

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('w'):
        match('w')
        match('?')
        parse_X()
        match('O')
        match('j')

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('v'):
        match('v')
        parse_N()
    elif lookahead.startswith('k'):
        match('k')
        parse_S()
        match('w')
        parse_X()
    elif lookahead.startswith('O'):
        match('O')
        parse_X()
    elif lookahead.startswith('Z'):
        match('Z')
        match('{')
        match('B')
        parse_X()
    elif lookahead.startswith('0'):
        match('0')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['v', 'k', 'O', 'Z', '0']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('='):
        match('=')
        match('0')
        parse_X()
    elif lookahead.startswith('t'):
        match('t')
        match('_')
    elif lookahead.startswith('0'):
        match('0')
        parse_P()
        parse_L()
    elif lookahead.startswith('/'):
        match('/')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['=', 't', '0', '/']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('H'):
        match('H')
        match('I')
        parse_L()
        parse_S()
        parse_L()
    elif lookahead.startswith(']'):
        match(']')
    elif lookahead.startswith('{'):
        match('{')
        parse_S()
        parse_X()
        match('!')
        parse_N()
    elif lookahead.startswith('v'):
        match('v')
        parse_X()
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['H', ']', '{', 'v']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_P()
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