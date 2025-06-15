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

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('?'):
        match('?')
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('^'):
            match('^')
            match('=')
            match('4')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['^', '']))
        match('b')

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('v'):
        match('v')
    elif lookahead.startswith('E'):
        match('E')
        parse_Y()
        parse_W()
        parse_V()
        parse_H()
    elif lookahead.startswith('F'):
        match('F')
        parse_W()
    elif lookahead.startswith('J'):
        match('J')
        parse_X()
    elif lookahead.startswith('B'):
        match('B')
        parse_X()
        parse_H()
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['v', 'E', 'F', 'J', 'B']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('l'):
        match('l')
        parse_H()
        parse_W()
        match('M')
        parse_Y()
    elif lookahead.startswith('J'):
        match('J')
        parse_W()
        parse_W()
    elif lookahead.startswith('-'):
        match('-')
        match('o')
        parse_V()
        parse_W()
        parse_H()
    elif lookahead.startswith('x'):
        match('x')
        match('G')
        parse_W()
        parse_W()
    elif lookahead.startswith('r'):
        match('r')
        match('i')
        parse_Y()
        parse_H()
        match('!')
    elif lookahead.startswith('{'):
        match('{')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['l', 'J', '-', 'x', 'r', '{']))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('^'):
        match('^')
        match('=')
        match('4')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['^', '']))

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('5'):
        match('5')
        parse_Y()
        match('3')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_H()
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