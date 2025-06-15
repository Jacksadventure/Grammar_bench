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

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('W'):
        match('W')
        while pos < len(tokens) and tokens[pos].startswith('B'):
            match('B')
            match('T')
            match('r')
            parse_H()
    elif lookahead.startswith('-'):
        match('-')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('W'):
            match('W')
            parse_H()
        elif lookahead.startswith('-'):
            match('-')
            parse_M()
        elif lookahead.startswith('d'):
            match('d')
            parse_H()
            parse_H()
        elif lookahead.startswith('H'):
            parse_H()
            parse_J()
            parse_A()
            parse_Q()
        elif lookahead.startswith('E'):
            match('E')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['W', '-', 'd', 'H', 'E']))
    elif lookahead.startswith('d'):
        match('d')
        while pos < len(tokens) and tokens[pos].startswith('B'):
            match('B')
            match('T')
            match('r')
            parse_H()
        while pos < len(tokens) and tokens[pos].startswith('B'):
            match('B')
            match('T')
            match('r')
            parse_H()
    elif lookahead.startswith('H'):
        while pos < len(tokens) and tokens[pos].startswith('B'):
            match('B')
            match('T')
            match('r')
            parse_H()
        while pos < len(tokens) and tokens[pos].startswith('r'):
            match('r')
            match('z')
            match('%')
            match('!')
            parse_Q()
        while pos < len(tokens) and tokens[pos].startswith('x'):
            match('x')
            match('n')
            match(':')
        if pos >= len(tokens):
            error("Unexpected end of input in Q")
        lookahead = tokens[pos]
        if lookahead.startswith('1'):
            match('1')
            parse_L()
            parse_L()
        elif lookahead.startswith("'"):
            match("'")
            match('^')
            parse_Q()
            parse_L()
            parse_L()
        elif lookahead.startswith('!'):
            match('!')
        else:
            error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['1', "'", '!']))
    elif lookahead.startswith('E'):
        match('E')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['W', '-', 'd', 'H', 'E']))

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('b'):
        match('b')
        parse_A()
        parse_S()
        match('I')

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('1'):
        match('1')
        parse_L()
        parse_L()
    elif lookahead.startswith("'"):
        match("'")
        match('^')
        parse_Q()
        parse_L()
        parse_L()
    elif lookahead.startswith('!'):
        match('!')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['1', "'", '!']))

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('r'):
        match('r')
        match('z')
        match('%')
        match('!')
        parse_Q()

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('B'):
        match('B')
        match('T')
        match('r')
        parse_H()

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('9'):
        match('9')
        match('6')
        parse_H()
        match('z')

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith(':'):
        match(':')
        parse_A()
        match('%')
        parse_K()
        match('h')
    elif lookahead.startswith('V'):
        match('V')
        parse_L()
        match('4')
        parse_Q()
        parse_M()
    elif lookahead.startswith('2'):
        match('2')
        match(',')
        match('h')
    elif lookahead.startswith('q'):
        match('q')
        parse_H()
        match('d')
        parse_A()
        parse_J()
    elif lookahead.startswith('x'):
        match('x')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join([':', 'V', '2', 'q', 'x']))

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('x'):
        match('x')
        match('n')
        match(':')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_M()
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