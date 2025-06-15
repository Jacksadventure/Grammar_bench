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

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('H'):
        match('H')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('H'):
            match('H')
            parse_T()
            match('b')
            match(',')
            match('.')
        elif lookahead.startswith('G'):
            match('G')
            match('_')
            match('o')
            match('x')
            parse_B()
        elif lookahead.startswith('I'):
            match('I')
            match(')')
            parse_E()
            parse_E()
            parse_T()
        elif lookahead.startswith('`'):
            match('`')
            match('h')
            match('.')
            parse_A()
        elif lookahead.startswith(']'):
            match(']')
            match('b')
            match('j')
        elif lookahead.startswith(')'):
            match(')')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['H', 'G', 'I', '`', ']', ')']))
        match('b')
        match(',')
        match('.')
    elif lookahead.startswith('G'):
        match('G')
        match('_')
        match('o')
        match('x')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('7'):
            match('7')
            match('|')
            parse_O()
            parse_W()
        elif lookahead.startswith('o'):
            match('o')
            match('/')
            match('?')
            parse_D()
            parse_D()
        elif lookahead.startswith('$'):
            match('$')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['7', 'o', '$']))
    elif lookahead.startswith('I'):
        match('I')
        match(')')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('?'):
            match('?')
            match('9')
            match('*')
        elif lookahead.startswith('}'):
            match('}')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['?', '}']))
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('?'):
            match('?')
            match('9')
            match('*')
        elif lookahead.startswith('}'):
            match('}')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['?', '}']))
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('H'):
            match('H')
            parse_T()
            match('b')
            match(',')
            match('.')
        elif lookahead.startswith('G'):
            match('G')
            match('_')
            match('o')
            match('x')
            parse_B()
        elif lookahead.startswith('I'):
            match('I')
            match(')')
            parse_E()
            parse_E()
            parse_T()
        elif lookahead.startswith('`'):
            match('`')
            match('h')
            match('.')
            parse_A()
        elif lookahead.startswith(']'):
            match(']')
            match('b')
            match('j')
        elif lookahead.startswith(')'):
            match(')')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['H', 'G', 'I', '`', ']', ')']))
    elif lookahead.startswith('`'):
        match('`')
        match('h')
        match('.')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('0'):
            match('0')
            match('N')
            parse_Y()
            parse_O()
            match('+')
        elif lookahead.startswith(']'):
            match(']')
        elif lookahead.startswith('Y'):
            parse_Y()
            match('P')
            match('m')
            match('?')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['0', ']', 'Y']))
    elif lookahead.startswith(']'):
        match(']')
        match('b')
        match('j')
    elif lookahead.startswith(')'):
        match(')')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['H', 'G', 'I', '`', ']', ')']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        match('9')
        match('*')
    elif lookahead.startswith('}'):
        match('}')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['?', '}']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('`'):
        match('`')
        match(',')
        match('`')
    elif lookahead.startswith('y'):
        match('y')
    elif lookahead.startswith(']'):
        match(']')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['`', 'y', ']']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('`'):
        match('`')
    elif lookahead.startswith('5'):
        match('5')
    elif lookahead.startswith('f'):
        match('f')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['`', '5', 'f']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('t'):
        match('t')
    elif lookahead.startswith('n'):
        match('n')
        match('$')
        match('l')
        match('m')
    elif lookahead.startswith('2'):
        match('2')
        match('x')
    elif lookahead.startswith('c'):
        match('c')
        match('{')
        match('(')
        match("'")
    elif lookahead.startswith('k'):
        match('k')
        match('_')
        parse_E()
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['t', 'n', '2', 'c', 'k']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('7'):
        match('7')
        match('|')
        parse_O()
        parse_W()
    elif lookahead.startswith('o'):
        match('o')
        match('/')
        match('?')
        parse_D()
        parse_D()
    elif lookahead.startswith('$'):
        match('$')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['7', 'o', '$']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('0'):
        match('0')
        match('N')
        parse_Y()
        parse_O()
        match('+')
    elif lookahead.startswith(']'):
        match(']')
    elif lookahead.startswith('Y'):
        parse_Y()
        match('P')
        match('m')
        match('?')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['0', ']', 'Y']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('$'):
        match('$')
        match('5')
        parse_R()
        match('X')
        parse_F()
    elif lookahead.startswith(':'):
        match(':')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['$', ':']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['w']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('x'):
        match('x')
        match('G')
        match(')')
        match('Z')
    elif lookahead.startswith('u'):
        match('u')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['x', 'u']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_T()
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