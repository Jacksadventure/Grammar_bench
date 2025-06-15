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

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('<'):
        match('<')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('w'):
            match('w')
            match('C')
            match('{')
            parse_R()
            parse_P()
        elif lookahead.startswith('p'):
            match('p')
            match('M')
            parse_Z()
            parse_Z()
            match('m')
        elif lookahead.startswith('g'):
            match('g')
            match('/')
            parse_Y()
        elif lookahead.startswith('J'):
            parse_J()
            parse_P()
        elif lookahead.startswith('H'):
            parse_H()
            match('x')
            parse_P()
        elif lookahead.startswith('i'):
            match('i')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['w', 'p', 'g', 'J', 'H', 'i']))
        match(']')

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('i'):
        match('i')
        parse_R()
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['i', 'd']))

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('h'):
        match('h')
        parse_Y()
        parse_H()
        match('k')

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('~'):
        match('~')

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('.'):
        match('.')
        match('(')

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        match('C')
        match('{')
        parse_R()
        parse_P()
    elif lookahead.startswith('p'):
        match('p')
        match('M')
        parse_Z()
        parse_Z()
        match('m')
    elif lookahead.startswith('g'):
        match('g')
        match('/')
        parse_Y()
    elif lookahead.startswith('J'):
        parse_J()
        parse_P()
    elif lookahead.startswith('H'):
        parse_H()
        match('x')
        parse_P()
    elif lookahead.startswith('i'):
        match('i')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['w', 'p', 'g', 'J', 'H', 'i']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
        parse_Y()
    elif lookahead.startswith("'"):
        match("'")
        parse_J()
        parse_R()
        parse_L()
    elif lookahead.startswith('['):
        match('[')
        parse_H()
        parse_L()
    elif lookahead.startswith('o'):
        match('o')
        match('A')
        parse_O()
        parse_H()
    elif lookahead.startswith('A'):
        match('A')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['+', "'", '[', 'o', 'A']))

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('_'):
        match('_')
        parse_J()
        match(',')
        parse_Y()
    elif lookahead.startswith(':'):
        match(':')
    elif lookahead.startswith('r'):
        match('r')
        parse_H()
        parse_Z()
        parse_F()
    elif lookahead.startswith('W'):
        match('W')
        parse_J()
        parse_O()
    elif lookahead.startswith('!'):
        match('!')
        match('r')
        parse_P()
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['_', ':', 'r', 'W', '!']))

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('p'):
        match('p')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_J()
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