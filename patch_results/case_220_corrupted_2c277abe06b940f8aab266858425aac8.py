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
    if lookahead.startswith('e'):
        match('e')
        match('=')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('s'):
            match('s')
            parse_Z()
            match('O')
        elif lookahead.startswith('y'):
            match('y')
            match('r')
            match('s')
            parse_K()
            match('<')
        elif lookahead.startswith('4'):
            match('4')
            match('s')
            match('l')
            match('b')
            parse_N()
        elif lookahead.startswith('B'):
            match('B')
            parse_V()
            parse_N()
            match('h')
        elif lookahead.startswith('_'):
            match('_')
            match('Q')
            match('~')
            match('(')
            match(',')
        elif lookahead.startswith('C'):
            parse_C()
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['s', 'y', '4', 'B', '_', 'C']))
    elif lookahead.startswith('}'):
        match('}')
        if pos >= len(tokens):
            error("Unexpected end of input in C")
        lookahead = tokens[pos]
        if lookahead.startswith('e'):
            match('e')
            match('=')
            parse_I()
        elif lookahead.startswith('}'):
            match('}')
            parse_C()
            match('>')
        elif lookahead.startswith('U'):
            match('U')
        else:
            error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['e', '}', 'U']))
        match('>')
    elif lookahead.startswith('U'):
        match('U')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['e', '}', 'U']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('r'):
        match('r')
        match('G')
    elif lookahead.startswith('T'):
        match('T')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['r', 'T']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('u'):
        match('u')
        parse_C()
    elif lookahead.startswith('6'):
        match('6')
        parse_R()
        match('O')
        parse_X()
    elif lookahead.startswith('}'):
        match('}')
        match("'")
    elif lookahead.startswith('U'):
        match('U')
        match('a')
        match('|')
        parse_S()
    elif lookahead.startswith('L'):
        match('L')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['u', '6', '}', 'U', 'L']))

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('h'):
        match('h')
        match('/')
        parse_N()

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('.'):
        match('.')
        parse_R()
        match('E')
        parse_X()
        parse_W()
    elif lookahead.startswith('h'):
        match('h')
        match('G')
        match('9')
        match('^')
    elif lookahead.startswith("'"):
        match("'")
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['.', 'h', "'"]))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('A'):
        match('A')
        parse_Z()
        match(',')
        match('>')
    elif lookahead.startswith('n'):
        match('n')
        match('3')
    elif lookahead.startswith('E'):
        match('E')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['A', 'n', 'E']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('s'):
        match('s')
        match(';')
        parse_N()
    elif lookahead.startswith('/'):
        match('/')
        parse_Z()
        parse_V()
        parse_I()
        match('a')
    elif lookahead.startswith('('):
        match('(')
        parse_C()
        match("'")
        match('9')
    elif lookahead.startswith('('):
        match('(')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['s', '/', '(', '(']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('s'):
        match('s')
        parse_Z()
        match('O')
    elif lookahead.startswith('y'):
        match('y')
        match('r')
        match('s')
        parse_K()
        match('<')
    elif lookahead.startswith('4'):
        match('4')
        match('s')
        match('l')
        match('b')
        parse_N()
    elif lookahead.startswith('B'):
        match('B')
        parse_V()
        parse_N()
        match('h')
    elif lookahead.startswith('_'):
        match('_')
        match('Q')
        match('~')
        match('(')
        match(',')
    elif lookahead.startswith('C'):
        parse_C()
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['s', 'y', '4', 'B', '_', 'C']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('d'):
        match('d')

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('|'):
        match('|')
        match('t')
        parse_X()
        parse_Z()
    elif lookahead.startswith('F'):
        match('F')
        parse_Z()
        match('m')
        match('~')
        parse_V()
    elif lookahead.startswith('>'):
        match('>')
        parse_V()
        match('Y')
    elif lookahead.startswith('~'):
        match('~')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['|', 'F', '>', '~']))

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