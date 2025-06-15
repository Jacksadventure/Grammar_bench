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

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('n'):
        match('n')
        match("'")
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('q'):
            match('q')
            parse_Y()
            match('x')
            match('o')
        elif lookahead.startswith('L'):
            match('L')
        elif lookahead.startswith('f'):
            match('f')
            match('=')
        elif lookahead.startswith('y'):
            match('y')
            parse_H()
        elif lookahead.startswith('-'):
            match('-')
            match(']')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['q', 'L', 'f', 'y', '-']))
    elif lookahead.startswith('e'):
        match('e')
        while pos < len(tokens) and tokens[pos].startswith('F'):
            match('F')
            match('{')
            match('b')
    elif lookahead.startswith('('):
        match('(')
    elif lookahead.startswith('M'):
        while pos < len(tokens) and tokens[pos].startswith('G'):
            match('G')
            match('K')
            match('w')
            match("'")
            match('~')
        while pos < len(tokens) and tokens[pos].startswith('G'):
            match('G')
            match('K')
            match('w')
            match("'")
            match('~')
        while pos < len(tokens) and tokens[pos].startswith('f'):
            match('f')
            match('g')
            match('z')
            match('r')
        match('G')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['n', 'e', '(', 'M']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('q'):
        match('q')
        parse_Y()
        match('x')
        match('o')
    elif lookahead.startswith('L'):
        match('L')
    elif lookahead.startswith('f'):
        match('f')
        match('=')
    elif lookahead.startswith('y'):
        match('y')
        parse_H()
    elif lookahead.startswith('-'):
        match('-')
        match(']')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['q', 'L', 'f', 'y', '-']))

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('F'):
        match('F')
        match('{')
        match('b')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_W()
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