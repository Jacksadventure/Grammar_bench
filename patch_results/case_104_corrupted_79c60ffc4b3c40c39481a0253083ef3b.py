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

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('~'):
        match('~')
        match("'")
        match('o')
        match('R')
        match('4')
    elif lookahead.startswith('f'):
        match('f')
        match('R')
        match(',')
        match('#')
        match('(')
    elif lookahead.startswith(':'):
        match(':')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('?'):
            match('?')
            match('G')
        elif lookahead.startswith('_'):
            match('_')
            match('{')
            match('R')
            match('n')
            match(']')
        elif lookahead.startswith('`'):
            match('`')
            match('q')
            parse_J()
            parse_O()
        elif lookahead.startswith('1'):
            match('1')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['?', '_', '`', '1']))
        match('U')
        while pos < len(tokens) and tokens[pos].startswith('('):
            match('(')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('W'):
            match('W')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['W']))
    elif lookahead.startswith("'"):
        match("'")
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['~', 'f', ':', "'"]))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        match('G')
    elif lookahead.startswith('_'):
        match('_')
        match('{')
        match('R')
        match('n')
        match(']')
    elif lookahead.startswith('`'):
        match('`')
        match('q')
        parse_J()
        parse_O()
    elif lookahead.startswith('1'):
        match('1')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['?', '_', '`', '1']))

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('&'):
        match('&')

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('H'):
        match('H')
        match('+')
        parse_O()
        match('6')
    elif lookahead.startswith('/'):
        match('/')
        parse_T()
        parse_A()
    elif lookahead.startswith('3'):
        match('3')
        parse_A()
        match('*')
    elif lookahead.startswith('['):
        match('[')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['H', '/', '3', '[']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_A()
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