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

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('n'):
        match('n')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('9'):
            match('9')
            parse_H()
            match('7')
            match('[')
            parse_H()
        elif lookahead.startswith('('):
            match('(')
            parse_N()
            parse_S()
            match('n')
            parse_Y()
        elif lookahead.startswith(','):
            match(',')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['9', '(', ',']))
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('h'):
            match('h')
            parse_G()
            match('*')
            match(',')
            match('9')
            parse_X()
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['h', '']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('9'):
        match('9')
        parse_H()
        match('7')
        match('[')
        parse_H()
    elif lookahead.startswith('('):
        match('(')
        parse_N()
        parse_S()
        match('n')
        parse_Y()
    elif lookahead.startswith(','):
        match(',')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['9', '(', ',']))

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('n'):
        match('n')
        match('[')

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('h'):
        match('h')
        parse_G()
        match('*')
        match(',')
        match('9')

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('^'):
        match('^')
        parse_S()

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('M'):
        match('M')
        parse_S()
        match('J')

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('e'):
        match('e')

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('T'):
        parse_T()
        parse_W()
        parse_S()
        parse_W()
        parse_H()
    elif lookahead.startswith('o'):
        match('o')
        parse_R()
        match('B')
    elif lookahead.startswith('~'):
        match('~')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['T', 'o', '~']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('='):
        match('=')
        parse_T()
        parse_H()
    elif lookahead.startswith('|'):
        match('|')
        parse_G()
        parse_Y()
    elif lookahead.startswith('q'):
        match('q')
    elif lookahead.startswith("'"):
        match("'")
        parse_H()
    elif lookahead.startswith('>'):
        match('>')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['=', '|', 'q', "'", '>']))

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('1'):
        match('1')
        match('4')
        match('d')
        parse_A()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_W()
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