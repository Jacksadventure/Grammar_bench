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

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('4'):
        match('4')
        match('2')
        match('*')
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('k'):
            match('k')
            match('&')
            match('b')
            match('K')
        elif lookahead.startswith('M'):
            match('M')
            parse_A()
        elif lookahead.startswith('X'):
            match('X')
            parse_Y()
            parse_S()
            match('m')
        elif lookahead.startswith('1'):
            match('1')
            match('>')
            match('3')
        elif lookahead.startswith('o'):
            match('o')
            match('j')
        elif lookahead.startswith('d'):
            match('d')
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['k', 'M', 'X', '1', 'o', 'd']))
    elif lookahead.startswith('%'):
        match('%')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['4', '%']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith(';'):
        match(';')
        parse_S()
        match('w')
    elif lookahead.startswith(','):
        match(',')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join([';', ',']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('8'):
        match('8')
        match('$')
        match('-')
        parse_I()
        match("'")
    elif lookahead.startswith('z'):
        match('z')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['8', 'z']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('L'):
        match('L')
        match('E')
        match('U')
        parse_Y()
        match('~')
    elif lookahead.startswith('b'):
        match('b')
        parse_Z()
        parse_G()
    elif lookahead.startswith('q'):
        match('q')
        parse_I()
        match('8')
    elif lookahead.startswith('^'):
        match('^')
        match('_')
        match('_')
        parse_A()
    elif lookahead.startswith('l'):
        match('l')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['L', 'b', 'q', '^', 'l']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('k'):
        match('k')
        match('&')
        match('b')
        match('K')
    elif lookahead.startswith('M'):
        match('M')
        parse_A()
    elif lookahead.startswith('X'):
        match('X')
        parse_Y()
        parse_S()
        match('m')
    elif lookahead.startswith('1'):
        match('1')
        match('>')
        match('3')
    elif lookahead.startswith('o'):
        match('o')
        match('j')
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['k', 'M', 'X', '1', 'o', 'd']))

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('h'):
        match('h')
        match("'")

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")
        match(',')
        parse_H()

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('Z'):
        parse_Z()
        parse_W()
    elif lookahead.startswith('i'):
        match('i')
        match('~')
        match('u')
        parse_H()
    elif lookahead.startswith('D'):
        match('D')
        match('!')
        match('x')
        match('}')
        match('e')
    elif lookahead.startswith('d'):
        match('d')
        match('V')
        parse_A()
    elif lookahead.startswith('8'):
        match('8')
        parse_S()
    elif lookahead.startswith('F'):
        match('F')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['Z', 'i', 'D', 'd', '8', 'F']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Y()
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