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
    if lookahead.startswith(';'):
        match(';')
        match('s')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('C'):
            match('C')
            match('o')
            match('u')
            match(',')
            match('3')
        elif lookahead.startswith('M'):
            match('M')
        elif lookahead.startswith('Q'):
            match('Q')
            match(',')
        elif lookahead.startswith('3'):
            match('3')
            parse_G()
            parse_K()
        elif lookahead.startswith('t'):
            match('t')
            match('O')
            match('v')
            parse_G()
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['C', 'M', 'Q', '3', 't']))
    elif lookahead.startswith('p'):
        match('p')
    elif lookahead.startswith('H'):
        match('H')
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith('m'):
            match('m')
            parse_Z()
        elif lookahead.startswith('}'):
            match('}')
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['m', '}']))
        match(')')
    elif lookahead.startswith('='):
        match('=')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('f'):
            match('f')
            match(':')
            match('?')
            match('t')
        elif lookahead.startswith('y'):
            match('y')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['f', 'y']))
        match('8')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join([';', 'p', 'H', '=']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('@'):
        match('@')
        parse_X()
        match('|')
    elif lookahead.startswith('x'):
        match('x')
        match('}')
    elif lookahead.startswith('T'):
        parse_T()
        match('j')
        match('/')
        parse_T()
    elif lookahead.startswith('#'):
        match('#')
        match('O')
        match('9')
        parse_T()
    elif lookahead.startswith('p'):
        match('p')
        match('[')
        match('[')
        parse_B()
    elif lookahead.startswith('['):
        match('[')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['@', 'x', 'T', '#', 'p', '[']))

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('r'):
        match('r')
        parse_B()
        match('o')
        parse_X()
        match('=')
    elif lookahead.startswith('w'):
        match('w')
        match('Q')
    elif lookahead.startswith('('):
        match('(')
        match('Y')
        match('(')
    elif lookahead.startswith('D'):
        match('D')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['r', 'w', '(', 'D']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('m'):
        match('m')
        parse_Z()
    elif lookahead.startswith('}'):
        match('}')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['m', '}']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith(')'):
        match(')')
        match('z')
    elif lookahead.startswith('='):
        match('=')
    elif lookahead.startswith('V'):
        match('V')
        parse_B()
    elif lookahead.startswith('&'):
        match('&')
        match('a')
        match('5')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join([')', '=', 'V', '&']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('f'):
        match('f')
        match(':')
        match('?')
        match('t')
    elif lookahead.startswith('y'):
        match('y')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['f', 'y']))

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