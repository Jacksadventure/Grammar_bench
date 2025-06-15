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
    if lookahead.startswith('4'):
        match('4')
        while pos < len(tokens) and tokens[pos].startswith('2'):
            match('2')
            match('S')
            match('V')
            match('t')
        while pos < len(tokens) and tokens[pos].startswith('I'):
            match('I')
            match('}')
            parse_D()
    elif lookahead.startswith('O'):
        match('O')
        match('0')
    elif lookahead.startswith('_'):
        match('_')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['4', 'O', '_']))

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('I'):
        match('I')
        match('}')
        parse_D()

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('I'):
        match('I')
    elif lookahead.startswith('n'):
        match('n')
        parse_L()
        match('.')
        parse_L()
    elif lookahead.startswith('7'):
        match('7')
        parse_Q()
        match('V')
        parse_C()
    elif lookahead.startswith('*'):
        match('*')
        match('d')
        parse_N()
        parse_D()
        parse_L()
    elif lookahead.startswith('M'):
        match('M')
        parse_L()
        parse_C()
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['I', 'n', '7', '*', 'M']))

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('2'):
        match('2')
        match('S')
        match('V')
        match('t')

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('f'):
        match('f')
        parse_C()
    elif lookahead.startswith('+'):
        match('+')
        parse_G()
        parse_Q()
        match('Y')
        parse_G()
    elif lookahead.startswith('2'):
        match('2')
        match('_')
        match('P')
    elif lookahead.startswith('J'):
        match('J')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['f', '+', '2', 'J']))

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('l'):
        match('l')
        parse_N()
        parse_N()
        parse_G()
        match('m')

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