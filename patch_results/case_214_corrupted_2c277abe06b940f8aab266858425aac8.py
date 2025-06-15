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
    while pos < len(tokens) and tokens[pos].startswith('+'):
        match('+')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('-'):
            match('-')
            parse_P()
            match('s')
            parse_Z()
        elif lookahead.startswith('<'):
            match('<')
            parse_A()
            parse_Q()
            parse_Z()
        elif lookahead.startswith('S'):
            parse_S()
            match('B')
            parse_Z()
        elif lookahead.startswith(':'):
            match(':')
            match(':')
            match(';')
            parse_A()
            parse_Q()
        elif lookahead.startswith('K'):
            match('K')
            match('q')
        elif lookahead.startswith('7'):
            match('7')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['-', '<', 'S', ':', 'K', '7']))
        match(';')

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('M'):
        match('M')
        parse_N()
        match('y')
        match('Y')
        parse_A()

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('@'):
        match('@')
        parse_Q()
        parse_P()
        parse_J()

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('5'):
        match('5')
        parse_Q()
        match('k')
        parse_J()
    elif lookahead.startswith('7'):
        match('7')
        match('6')
    elif lookahead.startswith('>'):
        match('>')
        parse_T()
    elif lookahead.startswith('H'):
        match('H')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['5', '7', '>', 'H']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('-'):
        match('-')
        parse_P()
        match('s')
        parse_Z()
    elif lookahead.startswith('<'):
        match('<')
        parse_A()
        parse_Q()
        parse_Z()
    elif lookahead.startswith('S'):
        parse_S()
        match('B')
        parse_Z()
    elif lookahead.startswith(':'):
        match(':')
        match(':')
        match(';')
        parse_A()
        parse_Q()
    elif lookahead.startswith('K'):
        match('K')
        match('q')
    elif lookahead.startswith('7'):
        match('7')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['-', '<', 'S', ':', 'K', '7']))

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('a'):
        match('a')

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('q'):
        match('q')
        match('Y')
        parse_N()
        parse_S()

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('g'):
        match('g')
        match(']')
        match('c')
        match('g')

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