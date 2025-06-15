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
    if lookahead.startswith('H'):
        match('H')
        while pos < len(tokens) and tokens[pos].startswith('L'):
            parse_L()
            parse_G()
        while pos < len(tokens) and tokens[pos].startswith('a'):
            match('a')
            parse_V()
            parse_I()
    elif lookahead.startswith('4'):
        match('4')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['H', '4']))

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('$'):
        match('$')
        parse_B()
        parse_B()

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('L'):
        parse_L()
        parse_G()

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('G'):
        parse_G()
        parse_R()
        match('0')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['G', '']))

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('w'):
        match('w')
        parse_Q()
        parse_L()
        match('-')
        parse_Y()

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('~'):
        match('~')
        match('!')
        parse_G()
        parse_V()
        parse_Y()
    elif lookahead.startswith('_'):
        match('_')
        parse_V()
        match('D')
        parse_B()
    elif lookahead.startswith(':'):
        match(':')
        parse_I()
        match('v')
        match('_')
        parse_G()
    elif lookahead.startswith('Z'):
        match('Z')
        match('%')
        parse_G()
        match('=')
    elif lookahead.startswith('F'):
        match('F')
        match('/')
        parse_J()
        parse_J()
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['~', '_', ':', 'Z', 'F', 'd']))

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('g'):
        match('g')

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('j'):
        match('j')
        parse_L()
        parse_L()
        parse_L()

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('a'):
        match('a')
        parse_V()
        parse_I()

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