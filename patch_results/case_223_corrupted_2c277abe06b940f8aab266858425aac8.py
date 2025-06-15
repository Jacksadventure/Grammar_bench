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

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('`'):
        match('`')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('u'):
            match('u')
            parse_P()
        elif lookahead.startswith('!'):
            match('!')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['u', '!']))
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('4'):
            match('4')
            match('c')
        elif lookahead.startswith('^'):
            match('^')
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['4', '^']))
        if pos >= len(tokens):
            error("Unexpected end of input in Q")
        lookahead = tokens[pos]
        if lookahead.startswith('R'):
            match('R')
            parse_J()
            match('0')
            match('y')
            match('R')
        elif lookahead.startswith('#'):
            match('#')
            parse_A()
            match('k')
            parse_J()
            match('f')
        elif lookahead.startswith('2'):
            match('2')
            match('u')
        elif lookahead.startswith('X'):
            match('X')
            match(']')
            match('t')
        elif lookahead.startswith('W'):
            match('W')
        else:
            error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['R', '#', '2', 'X', 'W']))
    elif lookahead.startswith('c'):
        match('c')
        match('j')
        match('0')
    elif lookahead.startswith('m'):
        match('m')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['`', 'c', 'm']))

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('L'):
        match('L')
        parse_P()
        match('/')

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('u'):
        match('u')
        parse_P()
    elif lookahead.startswith('!'):
        match('!')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['u', '!']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('8'):
        match('8')
        parse_E()
        parse_Z()
    elif lookahead.startswith('4'):
        match('4')
        parse_A()
        match('(')
        parse_V()
        match('6')
    elif lookahead.startswith('+'):
        match('+')
        match('*')
        match("'")
        match('m')
    elif lookahead.startswith('l'):
        match('l')
    elif lookahead.startswith('c'):
        match('c')
        match('<')
        match('a')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['8', '4', '+', 'l', 'c']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('4'):
        match('4')
        match('c')
    elif lookahead.startswith('^'):
        match('^')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['4', '^']))

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('['):
        match('[')
        parse_V()

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('e'):
        match('e')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_O()
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