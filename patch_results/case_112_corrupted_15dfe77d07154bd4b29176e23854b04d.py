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
    if lookahead.startswith('<'):
        match('<')
        while pos < len(tokens) and tokens[pos].startswith('z'):
            match('z')
    elif lookahead.startswith('^'):
        match('^')
        match('P')
        match('V')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('o'):
            match('o')
            match("'")
            match('y')
            parse_Z()
        elif lookahead.startswith('U'):
            match('U')
            match('2')
            parse_O()
            match(':')
        elif lookahead.startswith('l'):
            match('l')
            parse_E()
            parse_X()
        elif lookahead.startswith('S'):
            match('S')
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['o', 'U', 'l', 'S']))
    elif lookahead.startswith(';'):
        match(';')
        match('{')
        match('~')
    elif lookahead.startswith('e'):
        match('e')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['<', '^', ';', 'e']))

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('z'):
        match('z')

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        match('Y')
        match('*')
    elif lookahead.startswith('E'):
        parse_E()
        parse_E()
        parse_E()
    elif lookahead.startswith('C'):
        match('C')
        match('A')
        match('9')
    elif lookahead.startswith('O'):
        parse_O()
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(["'", 'E', 'C', 'O']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        match("'")
        match('y')
        parse_Z()
    elif lookahead.startswith('U'):
        match('U')
        match('2')
        parse_O()
        match(':')
    elif lookahead.startswith('l'):
        match('l')
        parse_E()
        parse_X()
    elif lookahead.startswith('S'):
        match('S')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['o', 'U', 'l', 'S']))

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('x'):
        match('x')
        parse_Q()

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