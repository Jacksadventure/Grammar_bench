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
    if lookahead.startswith('V'):
        match('V')
        match('%')
        match('$')
        match('z')
        match('p')
    elif lookahead.startswith('R'):
        match('R')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('='):
            match('=')
            parse_H()
            match('m')
            match('W')
            match('@')
        elif lookahead.startswith('w'):
            match('w')
            match('.')
            parse_C()
        elif lookahead.startswith('?'):
            match('?')
        else:
            error("Parse failed")
        match(';')
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith('U'):
            match('U')
            parse_H()
            parse_L()
            match('s')
        elif lookahead.startswith('!'):
            match('!')
        else:
            error("Parse failed")
    elif lookahead.startswith('r'):
        match('r')
        match('3')
        match('>')
        while pos < len(tokens) and tokens[pos].startswith('K'):
            parse_K()
            match('z')
    elif lookahead.startswith('d'):
        match('d')
        match('B')
        match('b')
    elif lookahead.startswith('o'):
        match('o')
    else:
        error("Parse failed")

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('>'):
        match('>')
        parse_N()
        parse_H()
    elif lookahead.startswith('s'):
        match('s')
        match('^')
        parse_L()
        match("'")
        match('B')
    elif lookahead.startswith('y'):
        match('y')
        parse_L()
        match('&')
        parse_N()
        match('c')
    elif lookahead.startswith('9'):
        match('9')
    else:
        error("Parse failed")

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('B'):
        match('B')
        match('+')
        match('p')
    elif lookahead.startswith('F'):
        parse_F()
    elif lookahead.startswith('m'):
        match('m')
        match('Y')
    else:
        error("Parse failed")

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('U'):
        match('U')
        parse_H()
        parse_L()
        match('s')
    elif lookahead.startswith('!'):
        match('!')
    else:
        error("Parse failed")

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('}'):
        match('}')
        match('E')
        parse_P()
        parse_N()
        parse_N()
    elif lookahead.startswith('O'):
        match('O')
    elif lookahead.startswith('+'):
        match('+')
        parse_D()
        match('}')
    elif lookahead.startswith('$'):
        match('$')
        parse_H()
        match('X')
    elif lookahead.startswith('V'):
        match('V')
        match('o')
    else:
        error("Parse failed")

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('&'):
        match('&')
        match('r')
    elif lookahead.startswith('@'):
        match('@')
    else:
        error("Parse failed")

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('.'):
        match('.')
        match('9')
        parse_P()
        parse_F()
        parse_T()
    elif lookahead.startswith('l'):
        match('l')
        match(')')
        match('o')
        parse_K()
        match('+')
    elif lookahead.startswith('3'):
        match('3')
        match('j')
    elif lookahead.startswith('&'):
        match('&')
    else:
        error("Parse failed")

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('*'):
        match('*')
        match('^')

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('K'):
        parse_K()
        match('z')

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('e'):
        match('e')
        parse_C()
        match('`')
        parse_Q()
    elif lookahead.startswith('2'):
        match('2')
        match("'")
    elif lookahead.startswith('~'):
        match('~')
    else:
        error("Parse failed")

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