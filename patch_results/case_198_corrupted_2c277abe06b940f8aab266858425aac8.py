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
    while pos < len(tokens) and tokens[pos].startswith('P'):
        match('P')
        match('e')
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith('H'):
            match('H')
            parse_A()
            parse_B()
            match('i')
        elif lookahead.startswith('B'):
            parse_B()
            parse_C()
            parse_C()
            parse_F()
        elif lookahead.startswith('k'):
            match('k')
            match('o')
            parse_U()
            match('D')
            match('2')
        elif lookahead.startswith('_'):
            match('_')
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['H', 'B', 'k', '_']))

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('s'):
        match('s')
        parse_V()
        parse_V()
        match('m')
        parse_V()

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('s'):
        match('s')
        parse_U()

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('v'):
        match('v')
        parse_C()
        parse_C()
        parse_F()
        match('h')
    elif lookahead.startswith('/'):
        match('/')
    elif lookahead.startswith('g'):
        match('g')
    elif lookahead.startswith('P'):
        match('P')
        parse_V()
        parse_F()
        parse_B()
        parse_A()
    elif lookahead.startswith('s'):
        match('s')
        parse_K()
        parse_F()
        match('e')
        parse_F()
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['v', '/', 'g', 'P', 's']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('H'):
        match('H')
        parse_A()
        parse_B()
        match('i')
    elif lookahead.startswith('B'):
        parse_B()
        parse_C()
        parse_C()
        parse_F()
    elif lookahead.startswith('k'):
        match('k')
        match('o')
        parse_U()
        match('D')
        match('2')
    elif lookahead.startswith('_'):
        match('_')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['H', 'B', 'k', '_']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('&'):
        match('&')
        parse_F()
    elif lookahead.startswith('n'):
        match('n')
        parse_U()
    elif lookahead.startswith('~'):
        match('~')
        parse_B()
        parse_A()
        match('L')
    elif lookahead.startswith('?'):
        match('?')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['&', 'n', '~', '?']))

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('z'):
        match('z')

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