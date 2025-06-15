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

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('m'):
        match('m')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('A'):
            match('A')
            match(',')
            parse_Z()
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['A', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('-'):
            match('-')
            parse_M()
        elif lookahead.startswith('y'):
            match('y')
            parse_Y()
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['-', '', 'y']))

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('.'):
        match('.')
        parse_N()
        parse_S()
        parse_N()

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('O'):
        match('O')
        parse_U()

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('-'):
        match('-')

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Z'):
        parse_Z()

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('w'):
        match('w')

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('T'):
        parse_T()

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('y'):
        match('y')
        parse_L()
        parse_M()
        parse_M()
        parse_T()

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('m'):
        match('m')
        parse_L()
        parse_G()
        parse_N()
        parse_M()
    elif lookahead.startswith('%'):
        match('%')
        parse_L()
        parse_N()
        match('X')
        match('|')
    elif lookahead.startswith('9'):
        match('9')
        parse_U()
        parse_V()
    elif lookahead.startswith('b'):
        match('b')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['m', '%', '9', 'b']))

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('A'):
        match('A')
        match(',')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_U()
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