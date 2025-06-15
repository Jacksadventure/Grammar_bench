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
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('*'):
        match('*')
        match('@')
        while pos < len(tokens) and tokens[pos].startswith('t'):
            match('t')
            parse_R()
            parse_Z()
            match('H')
            match('*')
        while pos < len(tokens) and tokens[pos].startswith('f'):
            match('f')
        while pos < len(tokens) and tokens[pos].startswith('Z'):
            parse_Z()
            match('V')
    elif lookahead.startswith('f'):
        match('f')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['*', 'f']))

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('f'):
        match('f')

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('1'):
        match('1')
        match('!')
        parse_Q()
    elif lookahead.startswith('z'):
        match('z')
        match('p')
        parse_C()
        parse_R()
        parse_D()
    elif lookahead.startswith('4'):
        match('4')
        match('F')
    elif lookahead.startswith('n'):
        match('n')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['1', 'z', '4', 'n']))

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('-'):
        match('-')
        match('a')

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        match('+')
        parse_R()
        parse_C()
        parse_Y()
    elif lookahead.startswith('9'):
        match('9')
        match('7')
        parse_R()
        match('M')
        match('2')
    elif lookahead.startswith('z'):
        match('z')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['?', '9', 'z']))

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Z'):
        parse_Z()
        match('V')

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('5'):
        match('5')
        parse_A()
    elif lookahead.startswith('6'):
        match('6')
        parse_Y()
        match('T')
        parse_J()
        parse_J()
    elif lookahead.startswith('~'):
        match('~')
        match('d')
        parse_Q()
        match('_')
    elif lookahead.startswith('u'):
        match('u')
        parse_Q()
        parse_D()
        parse_C()
        match('!')
        parse_Q()
    elif lookahead.startswith('p'):
        match('p')
        parse_Q()
        parse_G()
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['5', '6', '~', 'u', 'p', 'd']))

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('0'):
        match('0')
        parse_J()
        match('z')
        parse_J()
        parse_Z()

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")
        match('P')
        match('{')

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