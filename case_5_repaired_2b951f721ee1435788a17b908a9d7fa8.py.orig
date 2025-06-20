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
    if lookahead.startswith('='):
        match('=')
        match('8')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('F'):
            parse_F()
            match('d')
            parse_B()
            match('/')
        elif lookahead.startswith('B'):
            parse_B()
            match('$')
            match('q')
        elif lookahead.startswith('Z'):
            parse_Z()
        elif lookahead.startswith('#'):
            match('#')
            match('`')
        elif lookahead.startswith('.'):
            match('.')
            match('?')
            match('p')
        else:
            error("Parse failed")
        match('@')
        match('@')
    elif lookahead.startswith('4'):
        match('4')
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith('-'):
            match('-')
            parse_A()
        elif lookahead.startswith('.'):
            match('.')
            match('K')
            match('x')
        elif lookahead.startswith('A'):
            parse_A()
        elif lookahead.startswith('&'):
            match('&')
            parse_M()
            match('$')
            match('_')
        else:
            error("Parse failed")
        match('X')
    elif lookahead.startswith('d'):
        match('d')
        match('5')
    elif lookahead.startswith('*'):
        match('*')
    else:
        error("Parse failed")

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('k'):
        match('k')
        parse_G()
    elif lookahead.startswith('g'):
        match('g')
    else:
        error("Parse failed")

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        parse_D()
    elif lookahead.startswith('W'):
        parse_W()
        match('?')
        match('f')
        match('%')
    elif lookahead.startswith('8'):
        match('8')
    else:
        error("Parse failed")

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('p'):
        match('p')
        parse_N()
        parse_D()
        match('#')
        parse_A()
    elif lookahead.startswith('#'):
        match('#')
        parse_F()
        match('P')
        match('i')
        match('Y')
        match('S')
    elif lookahead.startswith('0'):
        match('0')
        match('?')
        match('t')
        parse_W()
    elif lookahead.startswith('G'):
        parse_G()
        match(']')
    elif lookahead.startswith('A'):
        parse_A()
    else:
        error("Parse failed")

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('-'):
        match('-')
        parse_A()
    elif lookahead.startswith('.'):
        match('.')
        match('K')
        match('x')
    elif lookahead.startswith('A'):
        parse_A()
    elif lookahead.startswith('&'):
        match('&')
        parse_M()
        match('$')
        match('_')
    else:
        error("Parse failed")

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('u'):
        match('u')
        parse_N()
        parse_M()
        parse_N()
        parse_Z()
    elif lookahead.startswith('l'):
        match('l')
    else:
        error("Parse failed")

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('F'):
        parse_F()
        match('d')
        parse_B()
        match('/')
    elif lookahead.startswith('B'):
        parse_B()
        match('$')
        match('q')
    elif lookahead.startswith('Z'):
        parse_Z()
    elif lookahead.startswith('#'):
        match('#')
        match('`')
    elif lookahead.startswith('.'):
        match('.')
        match('?')
        match('p')
    else:
        error("Parse failed")

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('='):
        match('=')
    elif lookahead.startswith('H'):
        match('H')
    elif lookahead.startswith('t'):
        match('t')
        match('%')
        parse_M()
        match('8')
    elif lookahead.startswith('T'):
        match('T')
        parse_Z()
        match('{')
    else:
        error("Parse failed")

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('p'):
        match('p')
        match('e')
        parse_J()
    elif lookahead.startswith('2'):
        match('2')
        match('+')
        match('<')
        parse_D()
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Parse failed")

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('%'):
        match('%')
        parse_W()
        parse_F()
    elif lookahead.startswith('C'):
        match('C')
    else:
        error("Parse failed")

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('5'):
        match('5')
    elif lookahead.startswith('9'):
        match('9')
    elif lookahead.startswith(':'):
        match(':')
        match('+')
        match('=')
        parse_M()
        parse_M()
    elif lookahead.startswith(';'):
        match(';')
        match('>')
        match(']')
        match('}')
        match('C')
    else:
        error("Parse failed")

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