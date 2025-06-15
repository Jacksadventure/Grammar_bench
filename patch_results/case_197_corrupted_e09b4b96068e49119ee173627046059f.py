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

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('l'):
        match('l')
        match(':')
        match('7')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('>'):
            match('>')
            match('[')
            parse_Z()
            parse_K()
        elif lookahead.startswith('8'):
            match('8')
            match('Q')
        elif lookahead.startswith('t'):
            match('t')
        elif lookahead.startswith('u'):
            match('u')
            parse_U()
            parse_N()
        elif lookahead.startswith('G'):
            match('G')
            match('G')
            parse_R()
            parse_K()
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['>', '8', 't', 'u', 'G']))
    elif lookahead.startswith('b'):
        match('b')
    elif lookahead.startswith('^'):
        match('^')
        match('0')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['l', 'b', '^']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('f'):
        match('f')
        parse_N()
        parse_R()

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('J'):
        match('J')
        parse_N()
        match('T')
        parse_U()
        match(')')
    elif lookahead.startswith('`'):
        match('`')
        parse_R()
    elif lookahead.startswith("'"):
        match("'")
        match('W')
    elif lookahead.startswith('l'):
        match('l')
        match('C')
        match('J')
        match('V')
    elif lookahead.startswith('.'):
        match('.')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['J', '`', "'", 'l', '.']))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('>'):
        match('>')
        match('[')
        parse_Z()
        parse_K()
    elif lookahead.startswith('8'):
        match('8')
        match('Q')
    elif lookahead.startswith('t'):
        match('t')
    elif lookahead.startswith('u'):
        match('u')
        parse_U()
        parse_N()
    elif lookahead.startswith('G'):
        match('G')
        match('G')
        parse_R()
        parse_K()
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['>', '8', 't', 'u', 'G']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('K'):
        parse_K()
        match('c')
        match('#')
    elif lookahead.startswith('Q'):
        match('Q')
        match('o')
        match('W')
    elif lookahead.startswith('A'):
        match('A')
        match('g')
        match('X')
        match('b')
    elif lookahead.startswith('_'):
        match('_')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['K', 'Q', 'A', '_']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Z()
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