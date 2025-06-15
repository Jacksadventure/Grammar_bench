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

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('f'):
        match('f')
        match('g')
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('('):
            match('(')
            match('g')
            match('A')
            parse_X()
        elif lookahead.startswith('N'):
            match('N')
            parse_W()
            parse_B()
            parse_M()
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['(', '', 'N']))
        match('t')
        match('G')

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        match('y')
        parse_Q()
        parse_Q()
    elif lookahead.startswith('#'):
        match('#')
        match('o')
        match('G')
    elif lookahead.startswith('B'):
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['o', '#', 'B']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('i'):
        match('i')
        parse_Z()
        match('-')
        match('A')
        parse_X()
    elif lookahead.startswith('U'):
        match('U')
        parse_Y()
        match('!')
        parse_D()
    elif lookahead.startswith('{'):
        match('{')
        match('}')
        match('{')
    elif lookahead.startswith(')'):
        match(')')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['i', 'U', '{', ')']))

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('R'):
        match('R')

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('E'):
        match('E')
        parse_Q()
    elif lookahead.startswith('8'):
        match('8')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['E', '8']))

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('!'):
        match('!')
        match('z')
        match('u')
        parse_Z()

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('s'):
        match('s')
        match('$')
        match('x')
        parse_T()
        parse_K()
    elif lookahead.startswith('n'):
        match('n')
        parse_T()
    elif lookahead.startswith('.'):
        match('.')
    elif lookahead.startswith('C'):
        match('C')
        parse_D()
        parse_X()
        match('>')
        parse_W()
    elif lookahead.startswith('M'):
        parse_M()
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['s', 'n', '.', 'C', 'M']))

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('('):
        match('(')
        match('g')
        match('A')

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('B'):
        parse_B()
    elif lookahead.startswith('v'):
        match('v')
        match('f')
        parse_B()
        parse_B()
        match('d')
    elif lookahead.startswith('o'):
        match('o')
        match('t')
        match('$')
        match('t')
    elif lookahead.startswith('='):
        match('=')
        match('-')
        parse_D()
        match('1')
    elif lookahead.startswith('*'):
        match('*')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['B', 'v', 'o', '=', '*']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('~'):
        match('~')
        match('$')
        match('r')
        match('O')
        parse_X()
    elif lookahead.startswith(')'):
        match(')')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['~', ')']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Q()
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