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
    while pos < len(tokens) and tokens[pos].startswith('#'):
        match('#')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('I'):
            parse_I()
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['I']))
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith(':'):
            match(':')
            match('+')
            parse_I()
        elif lookahead.startswith('z'):
            match('z')
        elif lookahead.startswith('s'):
            match('s')
            parse_Z()
            match('K')
            match('Y')
        elif lookahead.startswith('9'):
            match('9')
            match('c')
            match('`')
            parse_B()
        elif lookahead.startswith('$'):
            match('$')
            match('p')
            match('J')
            parse_P()
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join([':', 'z', 's', '9', '$']))
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith(':'):
            match(':')
            match('+')
            parse_I()
        elif lookahead.startswith('z'):
            match('z')
        elif lookahead.startswith('s'):
            match('s')
            parse_Z()
            match('K')
            match('Y')
        elif lookahead.startswith('9'):
            match('9')
            match('c')
            match('`')
            parse_B()
        elif lookahead.startswith('$'):
            match('$')
            match('p')
            match('J')
            parse_P()
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join([':', 'z', 's', '9', '$']))

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('t'):
        match('t')
        match('`')
        match('x')
        match('s')
        parse_Q()

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('H'):
        match('H')
        parse_M()

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        parse_P()
        match('(')
        match('7')
    elif lookahead.startswith('@'):
        match('@')
        match('9')
        match('<')
        match('m')
    elif lookahead.startswith('>'):
        match('>')
        match('1')
        match('n')
        match('n')
    elif lookahead.startswith('C'):
        match('C')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(["'", '@', '>', 'C']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith(':'):
        match(':')
        match('O')
        parse_L()
        parse_B()
        match('q')
    elif lookahead.startswith('/'):
        match('/')
        parse_A()
        match('^')
        match('f')
    elif lookahead.startswith('G'):
        match('G')
        match('x')
    elif lookahead.startswith('O'):
        match('O')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join([':', '/', 'G', 'O']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('4'):
        match('4')
    elif lookahead.startswith('N'):
        match('N')
        parse_M()
    elif lookahead.startswith('>'):
        match('>')
        match('y')
    elif lookahead.startswith('3'):
        match('3')
        parse_L()
        parse_P()
        parse_Q()
        parse_L()
    elif lookahead.startswith('@'):
        match('@')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['4', 'N', '>', '3', '@']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('I'):
        parse_I()
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['I']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('f'):
        match('f')
        match('>')
        match(';')
        match('k')
    elif lookahead.startswith('F'):
        match('F')
        parse_Z()
        parse_A()
    elif lookahead.startswith('a'):
        match('a')
        match('#')
    elif lookahead.startswith('e'):
        match('e')
        match('J')
    elif lookahead.startswith('q'):
        match('q')
        match('3')
        match('n')
    elif lookahead.startswith('9'):
        match('9')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['f', 'F', 'a', 'e', 'q', '9']))

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