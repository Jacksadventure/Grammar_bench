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

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('f'):
        match('f')
        match('@')
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('1'):
            match('1')
            parse_N()
            match('R')
            parse_W()
            match('Y')
        elif lookahead.startswith('?'):
            match('?')
            match('.')
        elif lookahead.startswith('m'):
            match('m')
        elif lookahead.startswith('!'):
            match('!')
            match('*')
            match('@')
            match('n')
        else:
            error("Parse failed")
    elif lookahead.startswith('z'):
        match('z')
    else:
        error("Parse failed")

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('G'):
        match('G')
        match('[')
        parse_E()
    elif lookahead.startswith('+'):
        match('+')
    else:
        error("Parse failed")

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('.'):
        match('.')
        parse_D()
        match('`')
        parse_P()
    elif lookahead.startswith(']'):
        match(']')
    else:
        error("Parse failed")

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        parse_D()
    elif lookahead.startswith('*'):
        match('*')
        parse_D()
        match('o')
        match('~')
        parse_C()
    elif lookahead.startswith('J'):
        match('J')
    elif lookahead.startswith('V'):
        match('V')
        parse_C()
        match('?')
        match('F')
        match('V')
    elif lookahead.startswith('_'):
        match('_')
    else:
        error("Parse failed")

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('1'):
        match('1')
        parse_N()
        match('R')
        parse_W()
        match('Y')
    elif lookahead.startswith('?'):
        match('?')
        match('.')
    elif lookahead.startswith('m'):
        match('m')
    elif lookahead.startswith('!'):
        match('!')
        match('*')
        match('@')
        match('n')
    else:
        error("Parse failed")

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('r'):
        match('r')
        parse_N()
    elif lookahead.startswith('G'):
        match('G')
    elif lookahead.startswith('('):
        match('(')
        match('6')
        match('.')
        match('j')
    elif lookahead.startswith('H'):
        parse_H()
        match("'")
        match('*')
        parse_N()
        match("'")
    else:
        error("Parse failed")

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        parse_I()
    elif lookahead.startswith('L'):
        match('L')
        match('k')
    elif lookahead.startswith("'"):
        match("'")
        parse_H()
        parse_A()
    elif lookahead.startswith('+'):
        match('+')
        parse_P()
        match('B')
        match('k')
    elif lookahead.startswith('m'):
        match('m')
    else:
        error("Parse failed")

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('N'):
        parse_N()
        parse_Z()
        match('-')
    elif lookahead.startswith('>'):
        match('>')
        match('&')
    elif lookahead.startswith('9'):
        match('9')
        match('?')
        match('%')
    elif lookahead.startswith('J'):
        match('J')
    else:
        error("Parse failed")

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('b'):
        match('b')
        parse_N()
        match('!')
        match('l')
        parse_C()

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('['):
        match('[')
        parse_Z()
        match('[')
        match('j')
        match('-')
    elif lookahead.startswith('2'):
        match('2')
        parse_N()
        parse_W()
        parse_E()
    elif lookahead.startswith('='):
        match('=')
        match('d')
        match('S')
    elif lookahead.startswith(']'):
        match(']')
    else:
        error("Parse failed")

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        match('j')
        parse_P()
        match('9')
        parse_X()
    elif lookahead.startswith('E'):
        parse_E()
        match('=')
        match('_')
    elif lookahead.startswith('%'):
        match('%')
        match('9')
    elif lookahead.startswith('U'):
        match('U')
        parse_Z()
        parse_N()
        match('V')
    elif lookahead.startswith('M'):
        match('M')
    else:
        error("Parse failed")

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Z()
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