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
    if lookahead.startswith('K'):
        match('K')
        match('[')
        match('a')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('x'):
            match('x')
            match("'")
            match('`')
            parse_B()
            match('0')
        elif lookahead.startswith('('):
            match('(')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['x', '(']))
        while pos < len(tokens) and tokens[pos].startswith('x'):
            match('x')
            match('?')
            match('!')
            match('#')
    elif lookahead.startswith('['):
        match('[')
        while pos < len(tokens) and tokens[pos].startswith('x'):
            match('x')
            match('?')
            match('!')
            match('#')
    elif lookahead.startswith('t'):
        match('t')
        match('~')
        while pos < len(tokens) and tokens[pos].startswith('|'):
            match('|')
            match(',')
            parse_T()
            match('n')
        while pos < len(tokens) and tokens[pos].startswith('u'):
            match('u')
            match('?')
            match('<')
            match('1')
    elif lookahead.startswith('*'):
        match('*')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['K', '[', 't', '*']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('I'):
        match('I')
    elif lookahead.startswith('l'):
        match('l')
        parse_T()
        parse_H()
        parse_P()
        match('3')
    elif lookahead.startswith("'"):
        match("'")
        parse_B()
        parse_H()
        parse_Z()
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['I', 'l', "'"]))

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('|'):
        match('|')
        match(',')
        parse_T()
        match('n')

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('A'):
        match('A')
        parse_Z()
        parse_P()
        parse_U()
        parse_T()
    elif lookahead.startswith(']'):
        match(']')
        parse_H()
    elif lookahead.startswith('}'):
        match('}')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['A', ']', '}']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('x'):
        match('x')
        match("'")
        match('`')
        parse_B()
        match('0')
    elif lookahead.startswith('('):
        match('(')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['x', '(']))

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('u'):
        match('u')
        match('?')
        match('<')
        match('1')

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