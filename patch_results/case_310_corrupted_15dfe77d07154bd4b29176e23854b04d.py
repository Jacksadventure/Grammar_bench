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

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('?'):
        match('?')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('%'):
            match('%')
            match('a')
            parse_Y()
            parse_Y()
        elif lookahead.startswith('W'):
            parse_W()
            parse_M()
            parse_M()
            parse_Q()
        elif lookahead.startswith("'"):
            match("'")
            parse_M()
            match('p')
            parse_K()
        elif lookahead.startswith('O'):
            match('O')
            parse_M()
            parse_X()
            parse_L()
        elif lookahead.startswith('S'):
            match('S')
            parse_W()
            parse_X()
            parse_X()
        elif lookahead.startswith('A'):
            match('A')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['%', 'W', "'", 'O', 'S', 'A']))

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('e'):
        match('e')
        parse_K()

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('e'):
        match('e')
        parse_Y()
        parse_K()
    elif lookahead.startswith('d'):
        match('d')
        parse_L()
        parse_R()
        parse_L()
    elif lookahead.startswith('-'):
        match('-')
        parse_Y()
        parse_W()
        parse_W()
        parse_K()
    elif lookahead.startswith('g'):
        match('g')
        parse_R()
        parse_L()
        parse_K()
        parse_X()
    elif lookahead.startswith('x'):
        match('x')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['e', 'd', '-', 'g', 'x']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('%'):
        match('%')
        match('a')
        parse_Y()
        parse_Y()
    elif lookahead.startswith('W'):
        parse_W()
        parse_M()
        parse_M()
        parse_Q()
    elif lookahead.startswith("'"):
        match("'")
        parse_M()
        match('p')
        parse_K()
    elif lookahead.startswith('O'):
        match('O')
        parse_M()
        parse_X()
        parse_L()
    elif lookahead.startswith('S'):
        match('S')
        parse_W()
        parse_X()
        parse_X()
    elif lookahead.startswith('A'):
        match('A')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['%', 'W', "'", 'O', 'S', 'A']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('N'):
        match('N')
        match(':')
        parse_R()
        parse_X()
    elif lookahead.startswith('?'):
        match('?')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['N', '?']))

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('7'):
        match('7')
        parse_Y()
        parse_M()
        parse_W()
        parse_Q()

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('&'):
        match('&')
        parse_Q()
        parse_M()
        match('0')
        parse_Y()
    elif lookahead.startswith('U'):
        match('U')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['&', 'U']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('-'):
        match('-')
        parse_Q()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Q()
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