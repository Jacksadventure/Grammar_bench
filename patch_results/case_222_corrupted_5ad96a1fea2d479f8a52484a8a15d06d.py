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
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('W'):
        match('W')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('S'):
            match('S')
            parse_B()
            match('=')
        elif lookahead.startswith('r'):
            match('r')
            match('!')
            match(')')
        elif lookahead.startswith('Y'):
            match('Y')
            parse_A()
            parse_B()
        elif lookahead.startswith('m'):
            match('m')
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['S', 'r', 'Y', 'm']))
        match('%')
    elif lookahead.startswith('F'):
        while pos < len(tokens) and tokens[pos].startswith('4'):
            match('4')
            match('5')
            match("'")
            parse_U()
            match('z')
        match('*')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('Q'):
            match('Q')
            parse_A()
            parse_U()
            match('N')
            match('#')
        elif lookahead.startswith(':'):
            match(':')
        elif lookahead.startswith('j'):
            match('j')
            parse_Z()
            match('r')
            parse_O()
            parse_A()
        elif lookahead.startswith('~'):
            match('~')
            parse_F()
            match(':')
            parse_Z()
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['Q', ':', 'j', '~']))
        while pos < len(tokens) and tokens[pos].startswith('T'):
            match('T')
            match('N')
            match('k')
    elif lookahead.startswith('~'):
        match('~')
        while pos < len(tokens) and tokens[pos].startswith('4'):
            match('4')
            match('5')
            match("'")
            parse_U()
            match('z')
        match('s')
        match('&')
    elif lookahead.startswith('X'):
        while pos < len(tokens) and tokens[pos].startswith('_'):
            match('_')
            match('=')
            match('u')
            match('^')
            parse_O()
        while pos < len(tokens) and tokens[pos].startswith('4'):
            match('4')
            match('5')
            match("'")
            parse_U()
            match('z')
        while pos < len(tokens) and tokens[pos].startswith('4'):
            match('4')
            match('5')
            match("'")
            parse_U()
            match('z')
        match("'")
        match('a')
    elif lookahead.startswith("'"):
        match("'")
        match('~')
        match('/')
    elif lookahead.startswith('*'):
        match('*')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['W', 'F', '~', 'X', "'", '*']))

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('4'):
        match('4')
        match('5')
        match("'")
        parse_U()
        match('z')

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('Q'):
        match('Q')
        parse_A()
        parse_U()
        match('N')
        match('#')
    elif lookahead.startswith(':'):
        match(':')
    elif lookahead.startswith('j'):
        match('j')
        parse_Z()
        match('r')
        parse_O()
        parse_A()
    elif lookahead.startswith('~'):
        match('~')
        parse_F()
        match(':')
        parse_Z()
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['Q', ':', 'j', '~']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('S'):
        match('S')
        parse_B()
        match('=')
    elif lookahead.startswith('r'):
        match('r')
        match('!')
        match(')')
    elif lookahead.startswith('Y'):
        match('Y')
        parse_A()
        parse_B()
    elif lookahead.startswith('m'):
        match('m')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['S', 'r', 'Y', 'm']))

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('T'):
        match('T')
        match('N')
        match('k')

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('p'):
        match('p')
        match('4')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['p', '']))

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