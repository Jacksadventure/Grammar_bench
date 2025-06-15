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

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('#'):
        match('#')
        match('m')
        match('Z')
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('a'):
            match('a')
            match('~')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['a', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('Z'):
            match('Z')
            parse_D()
            match('=')
            parse_I()
            parse_Q()
        elif lookahead.startswith('*'):
            match('*')
            parse_H()
            match('-')
            parse_H()
        elif lookahead.startswith("'"):
            match("'")
            parse_D()
            match('%')
            parse_F()
        elif lookahead.startswith('|'):
            match('|')
            parse_X()
            match('6')
            match('&')
            match('o')
        elif lookahead.startswith('C'):
            match('C')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['Z', '*', "'", '|', 'C']))

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('y'):
        match('y')

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('r'):
        match('r')
        match('o')
    elif lookahead.startswith('|'):
        match('|')
        parse_F()
    elif lookahead.startswith('p'):
        match('p')
        parse_X()
    elif lookahead.startswith('M'):
        match('M')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['r', '|', 'p', 'M']))

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('8'):
        match('8')

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('F'):
        parse_F()

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('a'):
        match('a')
        match('~')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['a', '']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        match('o')
        parse_I()
        parse_D()
    elif lookahead.startswith("'"):
        match("'")
        parse_D()
        parse_X()
        parse_Y()
        match('R')
    elif lookahead.startswith('Q'):
        parse_Q()
        parse_Y()
    elif lookahead.startswith(','):
        match(',')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['/', "'", 'Q', ',']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('z'):
        match('z')
        match('P')
        parse_D()
    elif lookahead.startswith('8'):
        match('8')
        parse_S()
        match('Z')
        parse_H()
    elif lookahead.startswith('R'):
        match('R')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['z', '8', 'R']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_I()
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