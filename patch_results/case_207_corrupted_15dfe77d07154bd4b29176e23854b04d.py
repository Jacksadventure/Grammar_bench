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
    if lookahead.startswith('3'):
        match('3')
    elif lookahead.startswith('Q'):
        match('Q')
        match('F')
    elif lookahead.startswith('X'):
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('L'):
            match('L')
            parse_B()
        elif lookahead.startswith('>'):
            match('>')
            match('_')
        elif lookahead.startswith('z'):
            match('z')
        elif lookahead.startswith('n'):
            match('n')
            match('7')
            parse_A()
            parse_X()
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['L', '>', 'z', 'n']))
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('G'):
            match('G')
            match('-')
            match('7')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['G', '']))
        while pos < len(tokens) and tokens[pos].startswith('J'):
            match('J')
            parse_T()
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('G'):
            match('G')
            match('-')
            match('7')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['G', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('4'):
            match('4')
            match('3')
            parse_A()
            match('_')
            match('2')
        elif lookahead.startswith('O'):
            match('O')
            match('L')
            parse_R()
            parse_X()
        elif lookahead.startswith('f'):
            match('f')
            parse_H()
            parse_B()
            match('c')
        elif lookahead.startswith('w'):
            match('w')
            match('t')
        elif lookahead.startswith('z'):
            match('z')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['4', 'O', 'f', 'w', 'z']))
    elif lookahead.startswith("'"):
        match("'")
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('L'):
            match('L')
            parse_B()
        elif lookahead.startswith('>'):
            match('>')
            match('_')
        elif lookahead.startswith('z'):
            match('z')
        elif lookahead.startswith('n'):
            match('n')
            match('7')
            parse_A()
            parse_X()
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['L', '>', 'z', 'n']))
    elif lookahead.startswith('v'):
        match('v')
        match('7')
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('L'):
            match('L')
            parse_B()
        elif lookahead.startswith('>'):
            match('>')
            match('_')
        elif lookahead.startswith('z'):
            match('z')
        elif lookahead.startswith('n'):
            match('n')
            match('7')
            parse_A()
            parse_X()
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['L', '>', 'z', 'n']))
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('G'):
            match('G')
            match('-')
            match('7')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['G', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith('['):
            match('[')
            parse_W()
            parse_X()
        elif lookahead.startswith('h'):
            match('h')
        elif lookahead.startswith('_'):
            match('_')
            match('J')
            parse_T()
            parse_W()
            parse_R()
        elif lookahead.startswith('7'):
            match('7')
            match('I')
            parse_T()
        else:
            error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['[', 'h', '_', '7']))
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['3', 'Q', 'X', "'", 'v']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('G'):
        match('G')
        match('-')
        match('7')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['G', '']))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('L'):
        match('L')
        parse_B()
    elif lookahead.startswith('>'):
        match('>')
        match('_')
    elif lookahead.startswith('z'):
        match('z')
    elif lookahead.startswith('n'):
        match('n')
        match('7')
        parse_A()
        parse_X()
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['L', '>', 'z', 'n']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('J'):
        match('J')
        parse_T()

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('9'):
        match('9')
        match('e')
        match('{')
        parse_V()

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('k'):
        match('k')
        match('_')
        match('G')
        parse_A()
        parse_A()

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('m'):
        match('m')
        parse_T()
        parse_D()

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('@'):
        match('@')
        parse_T()
        parse_N()

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('['):
        match('[')
        parse_W()
        parse_X()
    elif lookahead.startswith('h'):
        match('h')
    elif lookahead.startswith('_'):
        match('_')
        match('J')
        parse_T()
        parse_W()
        parse_R()
    elif lookahead.startswith('7'):
        match('7')
        match('I')
        parse_T()
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['[', 'h', '_', '7']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('4'):
        match('4')
        match('3')
        parse_A()
        match('_')
        match('2')
    elif lookahead.startswith('O'):
        match('O')
        match('L')
        parse_R()
        parse_X()
    elif lookahead.startswith('f'):
        match('f')
        parse_H()
        parse_B()
        match('c')
    elif lookahead.startswith('w'):
        match('w')
        match('t')
    elif lookahead.startswith('z'):
        match('z')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['4', 'O', 'f', 'w', 'z']))

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