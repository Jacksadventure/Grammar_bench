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

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith(')'):
        match(')')
        match('|')
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('V'):
            match('V')
            match('-')
            match('r')
        elif lookahead.startswith("'"):
            match("'")
            match('7')
        elif lookahead.startswith('c'):
            match('c')
            parse_H()
            parse_R()
            match('*')
        elif lookahead.startswith('v'):
            match('v')
            match('n')
        elif lookahead.startswith('['):
            match('[')
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['V', "'", 'c', 'v', '[']))
        while pos < len(tokens) and tokens[pos].startswith('R'):
            parse_R()
            parse_R()
            parse_A()
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('T'):
            match('T')
            match('s')
            parse_S()
        elif lookahead.startswith('r'):
            match('r')
            parse_S()
            parse_H()
            match('4')
            match('g')
        elif lookahead.startswith('Q'):
            match('Q')
            match('n')
            match('z')
            match('2')
            parse_A()
        elif lookahead.startswith('.'):
            match('.')
            match('&')
            match('p')
            match('f')
            parse_P()
        elif lookahead.startswith('x'):
            match('x')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['T', 'r', 'Q', '.', 'x']))
    elif lookahead.startswith('y'):
        match('y')
        while pos < len(tokens) and tokens[pos].startswith('.'):
            match('.')
            parse_O()
        while pos < len(tokens) and tokens[pos].startswith('r'):
            match('r')
    elif lookahead.startswith('a'):
        match('a')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join([')', 'y', 'a']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('<'):
        match('<')
        match('i')
        match('$')
        match('c')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['<', '']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('V'):
        match('V')
        match('-')
        match('r')
    elif lookahead.startswith("'"):
        match("'")
        match('7')
    elif lookahead.startswith('c'):
        match('c')
        parse_H()
        parse_R()
        match('*')
    elif lookahead.startswith('v'):
        match('v')
        match('n')
    elif lookahead.startswith('['):
        match('[')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['V', "'", 'c', 'v', '[']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('.'):
        match('.')
        parse_H()
        match('Q')
    elif lookahead.startswith('6'):
        match('6')
        match('b')
        parse_A()
        parse_P()
        parse_O()
    elif lookahead.startswith('('):
        match('(')
    elif lookahead.startswith('k'):
        match('k')
        parse_D()
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['.', '6', '(', 'k']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('d'):
        match('d')
        match('J')
        parse_O()
    elif lookahead.startswith('|'):
        match('|')
        match('B')
        match('K')
        match('t')
        match('/')
    elif lookahead.startswith('e'):
        match('e')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['d', '|', 'e']))

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('m'):
        match('m')
        parse_P()

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('R'):
        parse_R()
        parse_R()
        parse_A()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_P()
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