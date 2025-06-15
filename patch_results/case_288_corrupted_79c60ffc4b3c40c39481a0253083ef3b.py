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
    if lookahead.startswith('-'):
        match('-')
        match('`')
        match('}')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('9'):
            match('9')
            parse_B()
            parse_S()
            parse_P()
            match(';')
            match('n')
        elif lookahead.startswith('('):
            match('(')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['9', '(']))
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith(']'):
            match(']')
            parse_H()
            match(':')
            parse_A()
        elif lookahead.startswith('N'):
            parse_N()
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join([']', 'N']))
    elif lookahead.startswith('0'):
        match('0')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('-'):
            match('-')
            match('`')
            match('}')
            parse_B()
            parse_X()
        elif lookahead.startswith('0'):
            match('0')
            parse_N()
            parse_S()
            match('(')
            match('r')
        elif lookahead.startswith('^'):
            match('^')
            match('K')
            match('*')
        elif lookahead.startswith('~'):
            match('~')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['-', '0', '^', '~']))
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('p'):
            match('p')
            match('.')
            match('a')
            match('@')
        elif lookahead.startswith('|'):
            match('|')
            match('0')
        elif lookahead.startswith('O'):
            match('O')
        elif lookahead.startswith('r'):
            match('r')
        elif lookahead.startswith('?'):
            match('?')
            match('M')
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['p', '|', 'O', 'r', '?']))
        match('(')
        match('r')
    elif lookahead.startswith('^'):
        match('^')
        match('K')
        match('*')
    elif lookahead.startswith('~'):
        match('~')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['-', '0', '^', '~']))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        match(']')
        parse_H()
        match(':')
        parse_A()
    elif lookahead.startswith('N'):
        parse_N()
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join([']', 'N']))

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Q'):
        match('Q')
        parse_I()
        match(')')
        match('T')

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('p'):
        match('p')
        match('.')
        match('a')
        match('@')
    elif lookahead.startswith('|'):
        match('|')
        match('0')
    elif lookahead.startswith('O'):
        match('O')
    elif lookahead.startswith('r'):
        match('r')
    elif lookahead.startswith('?'):
        match('?')
        match('M')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['p', '|', 'O', 'r', '?']))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('c'):
        match('c')
        parse_B()
        parse_I()
        parse_B()
        parse_N()

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('W'):
        match('W')
        match('D')
    elif lookahead.startswith('g'):
        match('g')
        match('@')
    elif lookahead.startswith('A'):
        parse_A()
        match('Y')
        match('K')
        match('h')
        match('=')
    elif lookahead.startswith('?'):
        match('?')
        match('&')
        parse_I()
        match('{')
        match('^')
    elif lookahead.startswith('K'):
        match('K')
        match('Y')
        match('9')
    elif lookahead.startswith('K'):
        match('K')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['W', 'g', 'A', '?', 'K', 'K']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('h'):
        match('h')
        parse_E()
    elif lookahead.startswith('_'):
        match('_')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['h', '_']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('z'):
        match('z')
    elif lookahead.startswith('*'):
        match('*')
        match('~')
        match('q')
        match('0')
    elif lookahead.startswith('e'):
        match('e')
        match('Z')
        parse_C()
    elif lookahead.startswith(':'):
        match(':')
        parse_A()
        parse_S()
    elif lookahead.startswith('V'):
        match('V')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['z', '*', 'e', ':', 'V']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('9'):
        match('9')
        parse_B()
        parse_S()
        parse_P()
        match(';')
        match('n')
    elif lookahead.startswith('('):
        match('(')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['9', '(']))

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('|'):
        match('|')
        parse_B()
        match('@')
        parse_P()

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