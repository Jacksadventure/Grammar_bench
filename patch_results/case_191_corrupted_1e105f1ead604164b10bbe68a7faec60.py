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
    if lookahead.startswith('_'):
        match('_')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('*'):
            match('*')
            parse_Z()
            parse_X()
            parse_Z()
        elif lookahead.startswith('6'):
            match('6')
            parse_J()
        elif lookahead.startswith('g'):
            match('g')
            match('R')
            parse_Q()
            parse_V()
        elif lookahead.startswith(','):
            match(',')
            parse_U()
            parse_K()
            match('.')
            match('q')
        elif lookahead.startswith('Q'):
            parse_Q()
            parse_Z()
            parse_C()
            parse_L()
            match("'")
        elif lookahead.startswith('C'):
            parse_C()
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['*', '6', 'g', ',', 'Q', 'C']))
        match('@')
    elif lookahead.startswith('c'):
        match('c')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['_', 'c']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('F'):
        match('F')
        parse_C()
        parse_V()
        parse_M()
    elif lookahead.startswith('+'):
        match('+')
        match("'")
        parse_C()
    elif lookahead.startswith('a'):
        match('a')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['F', '+', 'a']))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('f'):
        match('f')
        parse_X()
        match('3')
        parse_Q()
        match('w')
    elif lookahead.startswith('i'):
        match('i')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['f', 'i']))

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('W'):
        match('W')
        match('@')
        match('6')
        match('B')

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('D'):
        match('D')
    elif lookahead.startswith('r'):
        match('r')
        parse_X()
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['D', 'r']))

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('n'):
        match('n')
        parse_Q()
        parse_X()
        match('d')

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('R'):
        match('R')
        match(',')
        match('G')
        match('I')
    elif lookahead.startswith('.'):
        match('.')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['R', '.']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('['):
        match('[')
        parse_V()
        parse_X()
        parse_J()
        match('x')
    elif lookahead.startswith('D'):
        match('D')
        parse_L()
        parse_L()
        parse_L()
    elif lookahead.startswith(']'):
        match(']')
    elif lookahead.startswith('T'):
        match('T')
        match('D')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['[', 'D', ']', 'T']))

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('*'):
        match('*')
        parse_Z()
        parse_X()
        parse_Z()
    elif lookahead.startswith('6'):
        match('6')
        parse_J()
    elif lookahead.startswith('g'):
        match('g')
        match('R')
        parse_Q()
        parse_V()
    elif lookahead.startswith(','):
        match(',')
        parse_U()
        parse_K()
        match('.')
        match('q')
    elif lookahead.startswith('Q'):
        parse_Q()
        parse_Z()
        parse_C()
        parse_L()
        match("'")
    elif lookahead.startswith('C'):
        parse_C()
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['*', '6', 'g', ',', 'Q', 'C']))

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('A'):
        match('A')
        parse_C()
        match('!')
        match('>')
        match("'")

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