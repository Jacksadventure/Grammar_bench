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

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('('):
        match('(')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('X'):
            match('X')
            parse_E()
        elif lookahead.startswith('@'):
            match('@')
            parse_M()
        elif lookahead.startswith('2'):
            match('2')
            parse_D()
            match('X')
            parse_M()
            parse_A()
        elif lookahead.startswith('6'):
            match('6')
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['X', '@', '2', '6']))
        while pos < len(tokens) and tokens[pos].startswith('#'):
            match('#')
            parse_C()
            match('f')
            match('@')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('c'):
            match('c')
            match('a')
            parse_Q()
        elif lookahead.startswith('y'):
            match('y')
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['c', 'y']))
    elif lookahead.startswith('^'):
        match('^')
        match('Y')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('('):
            match('(')
            parse_G()
            parse_M()
            parse_O()
        elif lookahead.startswith('^'):
            match('^')
            match('Y')
            parse_V()
            parse_A()
            parse_C()
        elif lookahead.startswith('+'):
            match('+')
            parse_E()
            parse_G()
        elif lookahead.startswith('N'):
            match('N')
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['(', '^', '+', 'N']))
        while pos < len(tokens) and tokens[pos].startswith('l'):
            match('l')
            match('{')
            match('h')
            match('u')
        while pos < len(tokens) and tokens[pos].startswith(','):
            match(',')
            parse_A()
            parse_D()
    elif lookahead.startswith('+'):
        match('+')
        while pos < len(tokens) and tokens[pos].startswith('A'):
            parse_A()
            match('!')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('X'):
            match('X')
            parse_E()
        elif lookahead.startswith('@'):
            match('@')
            parse_M()
        elif lookahead.startswith('2'):
            match('2')
            parse_D()
            match('X')
            parse_M()
            parse_A()
        elif lookahead.startswith('6'):
            match('6')
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['X', '@', '2', '6']))
    elif lookahead.startswith('N'):
        match('N')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['(', '^', '+', 'N']))

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('A'):
        parse_A()
        match('!')

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('l'):
        match('l')
        match('{')
        match('h')
        match('u')

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('c'):
        match('c')
        match('a')
        parse_Q()
    elif lookahead.startswith('y'):
        match('y')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['c', 'y']))

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")
        match(')')

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('`'):
        match('`')
        parse_D()
        parse_P()
        match('3')

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('z'):
        match('z')
    elif lookahead.startswith('j'):
        match('j')
        parse_D()
        parse_M()
        parse_C()
        parse_V()
    elif lookahead.startswith(';'):
        match(';')
        parse_P()
        match('U')
    elif lookahead.startswith("'"):
        match("'")
        match('I')
        match('k')
        parse_G()
        match('R')
    elif lookahead.startswith('H'):
        match('H')
        parse_V()
        parse_P()
        match('4')
        parse_D()
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['z', 'j', ';', "'", 'H']))

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(','):
        match(',')
        parse_A()
        parse_D()

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('#'):
        match('#')
        parse_C()
        match('f')
        match('@')

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('X'):
        match('X')
        parse_E()
    elif lookahead.startswith('@'):
        match('@')
        parse_M()
    elif lookahead.startswith('2'):
        match('2')
        parse_D()
        match('X')
        parse_M()
        parse_A()
    elif lookahead.startswith('6'):
        match('6')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['X', '@', '2', '6']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_V()
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