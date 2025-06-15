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

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('|'):
        match('|')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('e'):
            match('e')
        elif lookahead.startswith('2'):
            match('2')
            match('u')
            parse_J()
        elif lookahead.startswith('0'):
            match('0')
        elif lookahead.startswith('<'):
            match('<')
            parse_U()
            parse_X()
            match('M')
            match(')')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['e', '2', '0', '<']))
        match("'")
        match('q')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('y'):
            match('y')
            parse_Z()
            match('*')
            parse_Z()
        elif lookahead.startswith('9'):
            match('9')
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['y', '9']))
    elif lookahead.startswith('Q'):
        match('Q')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['|', 'Q']))

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('S'):
        match('S')
        parse_W()
        match('q')
        parse_Z()

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('F'):
        match('F')
        parse_J()
    elif lookahead.startswith('C'):
        match('C')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['F', 'C']))

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('y'):
        match('y')
        parse_Z()
        match('*')
        parse_Z()
    elif lookahead.startswith('9'):
        match('9')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['y', '9']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('A'):
        match('A')
        parse_J()
        match('V')
        parse_J()
        parse_W()
    elif lookahead.startswith('?'):
        match('?')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['A', '?']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_X()
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