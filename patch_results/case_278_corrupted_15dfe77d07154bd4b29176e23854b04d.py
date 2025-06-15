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
    if lookahead.startswith('-'):
        match('-')
        while pos < len(tokens) and tokens[pos].startswith('k'):
            match('k')
            match('E')
        while pos < len(tokens) and tokens[pos].startswith('k'):
            match('k')
            match('E')
        while pos < len(tokens) and tokens[pos].startswith('k'):
            match('k')
            match('E')
    elif lookahead.startswith('y'):
        match('y')
        match(':')
        while pos < len(tokens) and tokens[pos].startswith(','):
            match(',')
            parse_N()
            parse_D()
        while pos < len(tokens) and tokens[pos].startswith('l'):
            match('l')
        while pos < len(tokens) and tokens[pos].startswith(','):
            match(',')
            parse_N()
            parse_D()
    elif lookahead.startswith('r'):
        match('r')
        while pos < len(tokens) and tokens[pos].startswith('r'):
            match('r')
            match('C')
    elif lookahead.startswith('9'):
        match('9')
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('-'):
            match('-')
            parse_D()
            parse_D()
            parse_D()
        elif lookahead.startswith('y'):
            match('y')
            match(':')
            parse_P()
            parse_M()
            parse_P()
        elif lookahead.startswith('r'):
            match('r')
            parse_N()
        elif lookahead.startswith('9'):
            match('9')
            parse_X()
            parse_D()
            parse_X()
            parse_X()
        elif lookahead.startswith('p'):
            match('p')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['-', 'y', 'r', '9', 'p']))
        while pos < len(tokens) and tokens[pos].startswith('k'):
            match('k')
            match('E')
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('-'):
            match('-')
            parse_D()
            parse_D()
            parse_D()
        elif lookahead.startswith('y'):
            match('y')
            match(':')
            parse_P()
            parse_M()
            parse_P()
        elif lookahead.startswith('r'):
            match('r')
            parse_N()
        elif lookahead.startswith('9'):
            match('9')
            parse_X()
            parse_D()
            parse_X()
            parse_X()
        elif lookahead.startswith('p'):
            match('p')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['-', 'y', 'r', '9', 'p']))
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('-'):
            match('-')
            parse_D()
            parse_D()
            parse_D()
        elif lookahead.startswith('y'):
            match('y')
            match(':')
            parse_P()
            parse_M()
            parse_P()
        elif lookahead.startswith('r'):
            match('r')
            parse_N()
        elif lookahead.startswith('9'):
            match('9')
            parse_X()
            parse_D()
            parse_X()
            parse_X()
        elif lookahead.startswith('p'):
            match('p')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['-', 'y', 'r', '9', 'p']))
    elif lookahead.startswith('p'):
        match('p')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['-', 'y', 'r', '9', 'p']))

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('r'):
        match('r')
        match('C')

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('l'):
        match('l')

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('k'):
        match('k')
        match('E')

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(','):
        match(',')
        parse_N()
        parse_D()

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