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

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('T'):
        match('T')
        match('v')
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('n'):
            match('n')
            parse_X()
        elif lookahead.startswith('x'):
            match('x')
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['n', 'x']))
        match('!')
        if pos >= len(tokens):
            error("Unexpected end of input in Q")
        lookahead = tokens[pos]
        if lookahead.startswith(']'):
            match(']')
        else:
            error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join([']']))
    elif lookahead.startswith('I'):
        match('I')
    elif lookahead.startswith('P'):
        match('P')
    elif lookahead.startswith('n'):
        match('n')
        match('4')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['T', 'I', 'P', 'n']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('z'):
        match('z')
        match('c')
        match('b')
        parse_Y()
    elif lookahead.startswith('('):
        match('(')
        match('A')
        parse_S()
        match('w')
        match('[')
    elif lookahead.startswith('h'):
        match('h')
        parse_S()
        match('$')
    elif lookahead.startswith('T'):
        match('T')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['z', '(', 'h', 'T']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        match(']')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join([']']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('R'):
        match('R')
        parse_J()
    elif lookahead.startswith('i'):
        match('i')
        parse_N()
    elif lookahead.startswith('p'):
        match('p')
        parse_S()
        match('~')
    elif lookahead.startswith('<'):
        match('<')
    elif lookahead.startswith('h'):
        match('h')
        parse_X()
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['R', 'i', 'p', '<', 'h']))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('|'):
        match('|')
        parse_V()
    elif lookahead.startswith('k'):
        match('k')
        match('h')
        parse_N()
        match('L')
    elif lookahead.startswith('8'):
        match('8')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['|', 'k', '8']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('4'):
        match('4')
        match(')')
        match('i')
        parse_S()
    elif lookahead.startswith(';'):
        match(';')
        match('{')
    elif lookahead.startswith('Q'):
        parse_Q()
        match('a')
        match('y')
    elif lookahead.startswith('F'):
        match('F')
        match('A')
        match('W')
        match('y')
        match(')')
    elif lookahead.startswith('7'):
        match('7')
        match('b')
        match('Z')
    elif lookahead.startswith(':'):
        match(':')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['4', ';', 'Q', 'F', '7', ':']))

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('r'):
        match('r')

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('n'):
        match('n')
        parse_X()
    elif lookahead.startswith('x'):
        match('x')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['n', 'x']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_U()
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