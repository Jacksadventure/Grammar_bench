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

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('J'):
        match('J')
        while pos < len(tokens) and tokens[pos].startswith('6'):
            match('6')
            parse_L()
            match('7')
        match('V')
        match('u')
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('D'):
            parse_D()
        elif lookahead.startswith('I'):
            match('I')
            parse_Y()
        elif lookahead.startswith('C'):
            match('C')
            parse_O()
            match('0')
        elif lookahead.startswith(':'):
            match(':')
            match('s')
            parse_O()
            parse_Y()
        elif lookahead.startswith('_'):
            match('_')
            parse_A()
            match('J')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['D', 'I', 'C', ':', '_']))
    elif lookahead.startswith('U'):
        match('U')
        match('?')
        while pos < len(tokens) and tokens[pos].startswith('>'):
            match('>')
            parse_L()
            match('B')
            match('b')
            match("'")
    elif lookahead.startswith('V'):
        match('V')
        match('H')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('J'):
            match('J')
            parse_L()
            match('V')
            match('u')
            parse_Y()
        elif lookahead.startswith('U'):
            match('U')
            match('?')
            parse_W()
        elif lookahead.startswith('V'):
            match('V')
            match('H')
            parse_A()
        elif lookahead.startswith('U'):
            match('U')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['J', 'U', 'V', 'U']))
    elif lookahead.startswith('U'):
        match('U')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['J', 'U', 'V', 'U']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('D'):
        parse_D()
    elif lookahead.startswith('I'):
        match('I')
        parse_Y()
    elif lookahead.startswith('C'):
        match('C')
        parse_O()
        match('0')
    elif lookahead.startswith(':'):
        match(':')
        match('s')
        parse_O()
        parse_Y()
    elif lookahead.startswith('_'):
        match('_')
        parse_A()
        match('J')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['D', 'I', 'C', ':', '_']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('x'):
        match('x')
        parse_D()
    elif lookahead.startswith('g'):
        match('g')
    elif lookahead.startswith('o'):
        match('o')
        match(')')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['x', 'g', 'o']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('>'):
        match('>')
        parse_L()
        match('B')
        match('b')
        match("'")

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('8'):
        match('8')
        parse_L()
        match('~')
        match('-')
        match('.')

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('6'):
        match('6')
        parse_L()
        match('7')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_A()
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