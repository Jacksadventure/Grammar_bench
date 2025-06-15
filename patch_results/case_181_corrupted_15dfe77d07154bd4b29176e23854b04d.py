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
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        match(']')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('j'):
            match('j')
            parse_A()
        elif lookahead.startswith('&'):
            match('&')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['j', '&']))
        match('h')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('#'):
            match('#')
            parse_V()
            match('W')
            match('_')
        elif lookahead.startswith('x'):
            match('x')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['#', 'x']))
        match('L')
    elif lookahead.startswith('l'):
        match('l')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join([']', 'l']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('#'):
        match('#')
        parse_V()
        match('W')
        match('_')
    elif lookahead.startswith('x'):
        match('x')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['#', 'x']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('m'):
        match('m')
        match('_')
        parse_R()
    elif lookahead.startswith('+'):
        match('+')
        match("'")
        match('}')
        match('@')
        parse_R()
    elif lookahead.startswith('?'):
        match('?')
        parse_I()
        match('q')
    elif lookahead.startswith(')'):
        match(')')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['m', '+', '?', ')']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
        parse_A()
    elif lookahead.startswith('&'):
        match('&')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['j', '&']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('m'):
        match('m')
        match('/')
        match('M')
        match(',')
        match('b')
    elif lookahead.startswith('w'):
        match('w')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['m', 'w']))

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