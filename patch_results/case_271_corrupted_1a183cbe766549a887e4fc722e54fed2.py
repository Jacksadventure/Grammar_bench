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

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('M'):
        match('M')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('n'):
            match('n')
            parse_Z()
            match('H')
            parse_Z()
            parse_X()
        elif lookahead.startswith('0'):
            match('0')
            match('W')
            parse_Z()
            parse_N()
        elif lookahead.startswith('a'):
            match('a')
            parse_Z()
        elif lookahead.startswith('A'):
            match('A')
            parse_R()
            parse_R()
            parse_N()
            parse_Z()
        elif lookahead.startswith('p'):
            match('p')
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['n', '0', 'a', 'A', 'p']))
        match('_')
        match('c')
        match("'")

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('%'):
        match('%')
        match('}')
        match('1')

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('{'):
        match('{')
        parse_N()
        match('?')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['{', '']))

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('n'):
        match('n')
        parse_Z()
        match('H')
        parse_Z()
        parse_X()
    elif lookahead.startswith('0'):
        match('0')
        match('W')
        parse_Z()
        parse_N()
    elif lookahead.startswith('a'):
        match('a')
        parse_Z()
    elif lookahead.startswith('A'):
        match('A')
        parse_R()
        parse_R()
        parse_N()
        parse_Z()
    elif lookahead.startswith('p'):
        match('p')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['n', '0', 'a', 'A', 'p']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_N()
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