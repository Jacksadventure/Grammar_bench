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
    if lookahead.startswith(','):
        match(',')
        while pos < len(tokens) and tokens[pos].startswith('D'):
            parse_D()
            parse_E()
            parse_Z()
            match('l')
    elif lookahead.startswith('w'):
        match('w')
        match('9')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith(';'):
            match(';')
            parse_C()
            match('6')
            parse_S()
        elif lookahead.startswith('2'):
            match('2')
            match('|')
        elif lookahead.startswith('C'):
            parse_C()
            match('4')
        elif lookahead.startswith('$'):
            match('$')
            match('n')
        elif lookahead.startswith('2'):
            match('2')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join([';', '2', 'C', '$', '2']))
    elif lookahead.startswith('I'):
        match('I')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join([',', 'w', 'I']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('W'):
        match('W')
        parse_D()
        match('n')
        parse_C()
    elif lookahead.startswith('M'):
        parse_M()
        parse_D()
        parse_X()
        match('U')
    elif lookahead.startswith('#'):
        match('#')
        match('b')
    elif lookahead.startswith('('):
        match('(')
    elif lookahead.startswith('u'):
        match('u')
        parse_E()
        match("'")
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['W', 'M', '#', '(', 'u']))

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('D'):
        parse_D()
        parse_E()
        parse_A()
        parse_M()

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('K'):
        match('K')
        match('I')
        match('`')
        match('=')
    elif lookahead.startswith('w'):
        match('w')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['K', 'w']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('k'):
        match('k')
        match('^')
        parse_E()
    elif lookahead.startswith('K'):
        match('K')
        match(']')
        match('O')
        match('P')
    elif lookahead.startswith('_'):
        match('_')
        match('0')
        match('(')
        match('<')
        match('o')
    elif lookahead.startswith(']'):
        match(']')
    elif lookahead.startswith(','):
        match(',')
        match('(')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['k', 'K', '_', ']', ',']))

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('D'):
        parse_D()
        parse_E()
        parse_Z()
        match('l')

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('Y'):
        match('Y')
        parse_X()
    elif lookahead.startswith('P'):
        match('P')
        parse_C()
    elif lookahead.startswith('x'):
        match('x')
        match('7')
        parse_C()
    elif lookahead.startswith('u'):
        match('u')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['Y', 'P', 'x', 'u']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith(';'):
        match(';')
        parse_C()
        match('6')
        parse_S()
    elif lookahead.startswith('2'):
        match('2')
        match('|')
    elif lookahead.startswith('C'):
        parse_C()
        match('4')
    elif lookahead.startswith('$'):
        match('$')
        match('n')
    elif lookahead.startswith('2'):
        match('2')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join([';', '2', 'C', '$', '2']))

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