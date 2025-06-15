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

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('V'):
        match('V')
        while pos < len(tokens) and tokens[pos].startswith('$'):
            match('$')
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith('y'):
            match('y')
        elif lookahead.startswith('I'):
            match('I')
            match('^')
            parse_L()
            match('J')
            match('J')
        elif lookahead.startswith('E'):
            match('E')
        elif lookahead.startswith('@'):
            match('@')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['y', 'I', 'E', '@']))
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('>'):
            match('>')
            parse_N()
        elif lookahead.startswith('#'):
            match('#')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['>', '#']))
    elif lookahead.startswith('d'):
        match('d')
        match('F')
        match('y')
        match('}')
        match('I')
    elif lookahead.startswith('3'):
        match('3')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['V', 'd', '3']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('L'):
        parse_L()
        match('V')
        match(';')
        match('|')
    elif lookahead.startswith('4'):
        match('4')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['L', '4']))

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('$'):
        match('$')

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('k'):
        match('k')
        parse_H()
    elif lookahead.startswith('?'):
        match('?')
    elif lookahead.startswith('s'):
        match('s')
        match('=')
        match('-')
        parse_L()
    elif lookahead.startswith('('):
        match('(')
        match('O')
        match('V')
    elif lookahead.startswith('#'):
        match('#')
        match('V')
        match(':')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['k', '?', 's', '(', '#']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_R()
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