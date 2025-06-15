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

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('%'):
        match('%')
        match('e')
        match('@')
        match('=')
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith('i'):
            match('i')
        elif lookahead.startswith('='):
            match('=')
            parse_W()
            parse_V()
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['i', '=']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(':'):
        match(':')
        match('Y')
        parse_N()
        parse_Q()

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('`'):
        match('`')
        parse_K()
        parse_Q()
    elif lookahead.startswith('E'):
        match('E')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['`', 'E']))

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('9'):
        match('9')
        match('!')
        match('R')
        parse_A()
        parse_A()

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith(';'):
        match(';')
        match('C')
        match('&')
        match('F')
        match('?')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join([';', '']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('i'):
        match('i')
    elif lookahead.startswith('='):
        match('=')
        parse_W()
        parse_V()
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['i', '=']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('B'):
        match('B')
        parse_L()
        match('@')
        parse_N()
    elif lookahead.startswith('C'):
        match('C')
        parse_W()
        parse_N()
        match('4')
        match('/')
    elif lookahead.startswith('9'):
        match('9')
        match('P')
    elif lookahead.startswith('l'):
        match('l')
        match('^')
        parse_A()
    elif lookahead.startswith('E'):
        match('E')
        parse_K()
        parse_A()
    elif lookahead.startswith('4'):
        match('4')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['B', 'C', '9', 'l', 'E', '4']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('!'):
        match('!')
    elif lookahead.startswith('W'):
        parse_W()
        match('Y')
        parse_A()
    elif lookahead.startswith('D'):
        parse_D()
        parse_O()
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['!', 'W', 'D']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('N'):
        parse_N()
        parse_G()
    elif lookahead.startswith('@'):
        match('@')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['N', '@']))

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('t'):
        match('t')
        match('J')
        parse_Q()
        parse_D()
        parse_N()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_D()
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