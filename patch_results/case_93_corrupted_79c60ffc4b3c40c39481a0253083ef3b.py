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

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('F'):
        match('F')
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith('P'):
            match('P')
            match('D')
        elif lookahead.startswith('l'):
            match('l')
            parse_W()
            parse_G()
            match('&')
            match('R')
        elif lookahead.startswith('A'):
            match('A')
        elif lookahead.startswith('@'):
            match('@')
            parse_W()
            match('F')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['P', 'l', 'A', '@']))
        while pos < len(tokens) and tokens[pos].startswith('#'):
            match('#')
            parse_W()
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith('x'):
            match('x')
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['x']))
    elif lookahead.startswith('E'):
        match('E')
        while pos < len(tokens) and tokens[pos].startswith('K'):
            parse_K()
            parse_W()
            match('e')
        match(']')
        match('_')
        match('U')
    elif lookahead.startswith('Z'):
        match('Z')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['F', 'E', 'Z']))

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('K'):
        parse_K()
        parse_W()
        match('e')

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('x'):
        match('x')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['x']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('P'):
        match('P')
        match('D')
    elif lookahead.startswith('l'):
        match('l')
        parse_W()
        parse_G()
        match('&')
        match('R')
    elif lookahead.startswith('A'):
        match('A')
    elif lookahead.startswith('@'):
        match('@')
        parse_W()
        match('F')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['P', 'l', 'A', '@']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_T()
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