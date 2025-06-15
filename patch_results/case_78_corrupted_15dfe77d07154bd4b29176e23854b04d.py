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

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        match('F')
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('j'):
            match('j')
            match('|')
        elif lookahead.startswith('0'):
            match('0')
            parse_C()
            match('Q')
            match('U')
        elif lookahead.startswith('n'):
            match('n')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['j', '0', 'n']))
        while pos < len(tokens) and tokens[pos].startswith('/'):
            match('/')
            match('9')
            match("'")
            parse_Y()
        while pos < len(tokens) and tokens[pos].startswith('}'):
            match('}')
            match('4')
            match('y')
    elif lookahead.startswith('X'):
        match('X')
        match('B')
    elif lookahead.startswith('4'):
        match('4')
        match('f')
        while pos < len(tokens) and tokens[pos].startswith('/'):
            match('/')
            match('9')
            match("'")
            parse_Y()
        if pos >= len(tokens):
            error("Unexpected end of input in C")
        lookahead = tokens[pos]
        if lookahead.startswith('o'):
            match('o')
            match('F')
            parse_Y()
            parse_N()
            parse_R()
        elif lookahead.startswith('X'):
            match('X')
            match('B')
        elif lookahead.startswith('4'):
            match('4')
            match('f')
            parse_N()
            parse_C()
        elif lookahead.startswith('^'):
            match('^')
            parse_C()
            parse_R()
            match('4')
        elif lookahead.startswith('k'):
            match('k')
        else:
            error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['o', 'X', '4', '^', 'k']))
    elif lookahead.startswith('^'):
        match('^')
        if pos >= len(tokens):
            error("Unexpected end of input in C")
        lookahead = tokens[pos]
        if lookahead.startswith('o'):
            match('o')
            match('F')
            parse_Y()
            parse_N()
            parse_R()
        elif lookahead.startswith('X'):
            match('X')
            match('B')
        elif lookahead.startswith('4'):
            match('4')
            match('f')
            parse_N()
            parse_C()
        elif lookahead.startswith('^'):
            match('^')
            parse_C()
            parse_R()
            match('4')
        elif lookahead.startswith('k'):
            match('k')
        else:
            error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['o', 'X', '4', '^', 'k']))
        while pos < len(tokens) and tokens[pos].startswith('}'):
            match('}')
            match('4')
            match('y')
        match('4')
    elif lookahead.startswith('k'):
        match('k')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['o', 'X', '4', '^', 'k']))

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('}'):
        match('}')
        match('4')
        match('y')

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
        match('|')
    elif lookahead.startswith('0'):
        match('0')
        parse_C()
        match('Q')
        match('U')
    elif lookahead.startswith('n'):
        match('n')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['j', '0', 'n']))

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('/'):
        match('/')
        match('9')
        match("'")
        parse_Y()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_C()
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