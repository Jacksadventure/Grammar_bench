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

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('6'):
        match('6')
    elif lookahead.startswith('1'):
        match('1')
        while pos < len(tokens) and tokens[pos].startswith('/'):
            match('/')
            match('6')
            match('w')
            match('r')
            parse_J()
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith('6'):
            match('6')
        elif lookahead.startswith('1'):
            match('1')
            parse_N()
            parse_W()
        elif lookahead.startswith('^'):
            match('^')
            parse_B()
        elif lookahead.startswith('b'):
            match('b')
            parse_U()
            parse_I()
        elif lookahead.startswith('H'):
            match('H')
            match('=')
            match('&')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['6', '1', '^', 'b', 'H']))
    elif lookahead.startswith('^'):
        match('^')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('J'):
            parse_J()
            parse_J()
            parse_B()
        elif lookahead.startswith('&'):
            match('&')
            match('{')
        elif lookahead.startswith('&'):
            match('&')
            match('{')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['J', '&', '&']))
    elif lookahead.startswith('b'):
        match('b')
        while pos < len(tokens) and tokens[pos].startswith('P'):
            match('P')
            match('i')
            match("'")
            parse_B()
            match('1')
        while pos < len(tokens) and tokens[pos].startswith('j'):
            match('j')
    elif lookahead.startswith('H'):
        match('H')
        match('=')
        match('&')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['6', '1', '^', 'b', 'H']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('J'):
        parse_J()
        parse_J()
        parse_B()
    elif lookahead.startswith('&'):
        match('&')
        match('{')
    elif lookahead.startswith('&'):
        match('&')
        match('{')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['J', '&', '&']))

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('/'):
        match('/')
        match('6')
        match('w')
        match('r')
        parse_J()

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('-'):
        match('-')
        match('!')
        parse_A()
    elif lookahead.startswith('R'):
        match('R')
        parse_K()
    elif lookahead.startswith('B'):
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['-', 'R', 'B']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('A'):
        parse_A()
        parse_N()
    elif lookahead.startswith('@'):
        match('@')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['A', '@']))

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('P'):
        match('P')
        match('i')
        match("'")
        parse_B()
        match('1')

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('j'):
        match('j')

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('N'):
        parse_N()
        parse_K()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_W()
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