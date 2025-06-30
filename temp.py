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

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('F'):
        match('F')
        match(')')
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('+'):
            match('+')
            parse_N()
        elif lookahead.startswith('C'):
            match('C')
            match('c')
            parse_E()
            match('e')
            parse_B()
        elif lookahead.startswith('Q'):
            match('Q')
            match('.')
            parse_O()
            match('~')
        elif lookahead.startswith('j'):
            match('j')
            parse_D()
        elif lookahead.startswith('['):
            match('[')
            match('M')
            match('l')
        elif lookahead.startswith('w'):
            match('w')
        else:
            error("Parse failed")
    elif lookahead.startswith('['):
        match('[')
    else:
        error("Parse failed")

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('<'):
        match('<')
        match('C')
        match('(')
        match('q')
        parse_A()
    elif lookahead.startswith('o'):
        match('o')
    else:
        error("Parse failed")

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('H'):
        match('H')
        match('-')
        match('V')
        match('8')
    elif lookahead.startswith('A'):
        parse_A()
        parse_U()
        parse_U()
    elif lookahead.startswith('9'):
        match('9')
        match('a')
        parse_E()
    elif lookahead.startswith('#'):
        match('#')
        match('?')
        match('m')
        match('V')
        match('v')
    elif lookahead.startswith('?'):
        match('?')
    else:
        error("Parse failed")

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('c'):
        match('c')
        match('o')
        match('F')
        parse_R()
    elif lookahead.startswith('w'):
        match('w')
    else:
        error("Parse failed")

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('X'):
        parse_X()
        match('|')
        match('!')
        match(']')
    elif lookahead.startswith('q'):
        match('q')
    elif lookahead.startswith('a'):
        match('a')
        match('v')
        match(']')
        match('S')
        match('4')
    elif lookahead.startswith("'"):
        match("'")
    elif lookahead.startswith('+'):
        match('+')
    else:
        error("Parse failed")

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        parse_O()
        match('.')
        match('J')
        parse_L()
    elif lookahead.startswith('{'):
        match('{')
        match('!')
        match('0')
    elif lookahead.startswith('h'):
        match('h')
        parse_D()
    elif lookahead.startswith('m'):
        match('m')
    else:
        error("Parse failed")

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
        parse_N()
    elif lookahead.startswith('C'):
        match('C')
        match('c')
        parse_E()
        match('e')
        parse_B()
    elif lookahead.startswith('Q'):
        match('Q')
        match('.')
        parse_O()
        match('~')
    elif lookahead.startswith('j'):
        match('j')
        parse_D()
    elif lookahead.startswith('['):
        match('[')
        match('M')
        match('l')
    elif lookahead.startswith('w'):
        match('w')
    else:
        error("Parse failed")

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
        match(';')
        match('p')
        match('@')
    elif lookahead.startswith('4'):
        match('4')
        match('z')
        match('g')
        match('-')
        match('u')
    elif lookahead.startswith('A'):
        parse_A()
        match('3')
        match('1')
        match('I')
    elif lookahead.startswith('b'):
        match('b')
    else:
        error("Parse failed")

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('3'):
        match('3')
        match(']')
        parse_D()

def d dparse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('F'):
        match('F')
        match('I')
        match('m')
        parse_D()
        parse_O()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_L()
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