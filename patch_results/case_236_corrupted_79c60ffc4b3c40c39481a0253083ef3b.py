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

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('I'):
        match('I')
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith('2'):
            match('2')
            match('W')
            parse_L()
        elif lookahead.startswith('e'):
            match('e')
            parse_R()
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['2', '', 'e']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('`'):
        match('`')
        parse_G()
        match('X')
    elif lookahead.startswith('t'):
        match('t')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['`', 't']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('3'):
        match('3')
        match('H')
    elif lookahead.startswith('^'):
        match('^')
    elif lookahead.startswith('.'):
        match('.')
        parse_L()
        parse_G()
        match('s')
        match('w')
    elif lookahead.startswith('p'):
        match('p')
        match('U')
        match('q')
        parse_G()
    elif lookahead.startswith('s'):
        match('s')
        parse_G()
        parse_R()
        match('-')
        parse_N()
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['3', '^', '.', 'p', 's']))

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('2'):
        match('2')
        match('W')

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('q'):
        match('q')
        parse_R()
        parse_E()
        parse_G()
    elif lookahead.startswith('0'):
        match('0')
        match('y')
        parse_G()
        match('S')
    elif lookahead.startswith('7'):
        match('7')
        match('x')
        match('r')
    elif lookahead.startswith('J'):
        match('J')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['q', '0', '7', 'J']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        parse_L()
        match('`')
    elif lookahead.startswith('L'):
        parse_L()
        match('7')
    elif lookahead.startswith('u'):
        match('u')
        parse_N()
        parse_R()
        match('V')
    elif lookahead.startswith('{'):
        match('{')
        match('/')
        match('Y')
        match('/')
        match('$')
    elif lookahead.startswith(']'):
        match(']')
        parse_C()
        match('J')
        match('K')
        match('o')
    elif lookahead.startswith('5'):
        match('5')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['?', 'L', 'u', '{', ']', '5']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_E()
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