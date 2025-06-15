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

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith(':'):
        match(':')
        match('4')
        match('B')
        match('0')
        match('=')
    elif lookahead.startswith('n'):
        match('n')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('m'):
            match('m')
            match('c')
            parse_O()
            parse_C()
            parse_C()
        elif lookahead.startswith('M'):
            match('M')
        elif lookahead.startswith('}'):
            match('}')
            match('w')
            match('!')
            match('B')
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['m', 'M', '}']))
        match('Y')
        match('8')
        match('m')
    elif lookahead.startswith('&'):
        match('&')
        match('i')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('0'):
            match('0')
            match('<')
        elif lookahead.startswith('S'):
            match('S')
        elif lookahead.startswith('r'):
            match('r')
        elif lookahead.startswith('T'):
            match('T')
        elif lookahead.startswith('k'):
            match('k')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['0', 'S', 'r', 'T', 'k']))
    elif lookahead.startswith('+'):
        match('+')
        match('-')
        match('5')
        match('u')
    elif lookahead.startswith(';'):
        match(';')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join([':', 'n', '&', '+', ';']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('x'):
        match('x')
        parse_V()
        parse_V()
    elif lookahead.startswith('^'):
        match('^')
        parse_O()
    elif lookahead.startswith('L'):
        match('L')
        match('c')
        match(':')
        parse_N()
        parse_A()
    elif lookahead.startswith('1'):
        match('1')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['x', '^', 'L', '1']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('m'):
        match('m')
        match('c')
        parse_O()
        parse_C()
        parse_C()
    elif lookahead.startswith('M'):
        match('M')
    elif lookahead.startswith('}'):
        match('}')
        match('w')
        match('!')
        match('B')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['m', 'M', '}']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('Y'):
        match('Y')
        match('5')
        match("'")
        match('K')
    elif lookahead.startswith('y'):
        match('y')
        parse_G()
    elif lookahead.startswith('T'):
        match('T')
        match('2')
        match('g')
        parse_A()
    elif lookahead.startswith("'"):
        match("'")
        match('X')
        match('>')
        match('K')
        match('3')
    elif lookahead.startswith('i'):
        match('i')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['Y', 'y', 'T', "'", 'i']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('S'):
        match('S')
        match('<')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['S', '']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('3'):
        match('3')
        parse_A()
    elif lookahead.startswith('Z'):
        match('Z')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['3', 'Z']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_N()
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