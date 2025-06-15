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

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('F'):
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('&'):
            match('&')
            parse_O()
            match('y')
            match('U')
            parse_O()
        elif lookahead.startswith('6'):
            match('6')
            match('I')
            match('I')
            match('x')
        elif lookahead.startswith('d'):
            match('d')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['&', '6', 'd']))
    elif lookahead.startswith('S'):
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('n'):
            match('n')
            parse_L()
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['n', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('`'):
            match('`')
            parse_X()
            parse_L()
        elif lookahead.startswith('&'):
            match('&')
        elif lookahead.startswith(')'):
            match(')')
        elif lookahead.startswith('e'):
            match('e')
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['`', '&', ')', 'e']))
        while pos < len(tokens) and tokens[pos].startswith('5'):
            match('5')
            match('I')
            parse_F()
            match('|')
        match(']')
    elif lookahead.startswith('C'):
        if pos >= len(tokens):
            error("Unexpected end of input in C")
        lookahead = tokens[pos]
        if lookahead.startswith('t'):
            match('t')
            parse_Z()
            parse_D()
        elif lookahead.startswith(','):
            match(',')
        else:
            error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['t', ',']))
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('&'):
            match('&')
            parse_O()
            match('y')
            match('U')
            parse_O()
        elif lookahead.startswith('6'):
            match('6')
            match('I')
            match('I')
            match('x')
        elif lookahead.startswith('d'):
            match('d')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['&', '6', 'd']))
    elif lookahead.startswith('t'):
        match('t')
        match('&')
        match('U')
        match('I')
    elif lookahead.startswith('P'):
        match('P')
        match('u')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('`'):
            match('`')
            parse_X()
            parse_L()
        elif lookahead.startswith('&'):
            match('&')
        elif lookahead.startswith(')'):
            match(')')
        elif lookahead.startswith('e'):
            match('e')
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['`', '&', ')', 'e']))
        match(':')
        while pos < len(tokens) and tokens[pos].startswith('5'):
            match('5')
            match('I')
            parse_F()
            match('|')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['F', 'S', 'C', 't', 'P']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('`'):
        match('`')
        parse_X()
        parse_L()
    elif lookahead.startswith('&'):
        match('&')
    elif lookahead.startswith(')'):
        match(')')
    elif lookahead.startswith('e'):
        match('e')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['`', '&', ')', 'e']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('q'):
        match('q')
        parse_X()
        match('+')
    elif lookahead.startswith('m'):
        match('m')
        parse_S()
        match('&')
    elif lookahead.startswith('3'):
        match('3')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['q', 'm', '3']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('y'):
        match('y')
        parse_Q()
        parse_F()
        match('o')
    elif lookahead.startswith('h'):
        match('h')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['y', 'h']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('n'):
        match('n')
        parse_L()
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['n', '']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('&'):
        match('&')
        parse_O()
        match('y')
        match('U')
        parse_O()
    elif lookahead.startswith('6'):
        match('6')
        match('I')
        match('I')
        match('x')
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['&', '6', 'd']))

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('5'):
        match('5')
        match('I')
        parse_F()
        match('|')

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('t'):
        match('t')
        parse_Z()
        parse_D()
    elif lookahead.startswith(','):
        match(',')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['t', ',']))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('L'):
        parse_L()
        match('#')
        parse_O()
        parse_C()
    elif lookahead.startswith('/'):
        match('/')
    elif lookahead.startswith('k'):
        match('k')
        match("'")
        parse_C()
        parse_Y()
    elif lookahead.startswith('P'):
        match('P')
        match('^')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['L', '/', 'k', 'P']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('W'):
        match('W')
        match('K')
        parse_Q()
        match('|')
    elif lookahead.startswith('P'):
        match('P')
        parse_Z()
        parse_L()
        parse_Z()
    elif lookahead.startswith(','):
        match(',')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['W', 'P', ',']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Z()
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