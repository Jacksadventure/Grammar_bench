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

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('W'):
        match('W')
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith('W'):
            match('W')
            parse_D()
            parse_D()
        elif lookahead.startswith('?'):
            match('?')
            parse_R()
            parse_H()
            parse_A()
        else:
            error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['W', '', '?']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('9'):
        match('9')
        parse_D()
        match('?')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['9', '']))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('2'):
        match('2')

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('x'):
        match('x')
        parse_G()
    elif lookahead.startswith('('):
        match('(')
        parse_D()
    elif lookahead.startswith('x'):
        match('x')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['x', '(', 'x']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('S'):
        match('S')
        parse_A()
        parse_R()
    elif lookahead.startswith('s'):
        match('s')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['S', 's']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_D()
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