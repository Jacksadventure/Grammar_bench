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

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('i'):
        match('i')
        match(':')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('%'):
            match('%')
            parse_N()
            parse_Z()
            parse_T()
            parse_I()
        elif lookahead.startswith('t'):
            match('t')
            match('k')
            match("'")
        elif lookahead.startswith('8'):
            match('8')
            match('$')
            parse_U()
        elif lookahead.startswith('6'):
            match('6')
            match('^')
            match('(')
            parse_X()
        elif lookahead.startswith('g'):
            match('g')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['%', 't', '8', '6', 'g']))
    elif lookahead.startswith('0'):
        match('0')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith(';'):
            match(';')
            match('F')
            match('L')
        elif lookahead.startswith('?'):
            match('?')
            match('=')
            match('k')
        elif lookahead.startswith('C'):
            match('C')
            match('o')
        elif lookahead.startswith('>'):
            match('>')
            parse_Z()
            match(',')
            match('&')
            match('O')
        elif lookahead.startswith('s'):
            match('s')
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join([';', '?', 'C', '>', 's']))
        match('p')
        match('Q')
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('k'):
            match('k')
            match('[')
            match('D')
            parse_Z()
            match(':')
        elif lookahead.startswith('['):
            match('[')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['k', '[']))
    elif lookahead.startswith('o'):
        match('o')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['i', '0', 'o']))

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('?'):
        match('?')
        match('m')
        parse_N()
        parse_Y()
        parse_U()

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('k'):
        match('k')
        match('[')
        match('D')
        parse_Z()
        match(':')
    elif lookahead.startswith('['):
        match('[')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['k', '[']))

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('z'):
        match('z')

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        match('k')
        parse_Z()
    elif lookahead.startswith('!'):
        match('!')
    elif lookahead.startswith('7'):
        match('7')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['o', '!', '7']))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('z'):
        match('z')
        match('n')
    elif lookahead.startswith('s'):
        match('s')
        parse_Y()
        parse_X()
    elif lookahead.startswith('<'):
        match('<')
        match('g')
        match('1')
    elif lookahead.startswith(','):
        match(',')
        match('&')
        match('Q')
        match('h')
    elif lookahead.startswith('f'):
        match('f')
        match('n')
        match('5')
    elif lookahead.startswith('L'):
        match('L')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['z', 's', '<', ',', 'f', 'L']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('%'):
        match('%')
        parse_N()
        parse_Z()
        parse_T()
        parse_I()
    elif lookahead.startswith('t'):
        match('t')
        match('k')
        match("'")
    elif lookahead.startswith('8'):
        match('8')
        match('$')
        parse_U()
    elif lookahead.startswith('6'):
        match('6')
        match('^')
        match('(')
        parse_X()
    elif lookahead.startswith('g'):
        match('g')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['%', 't', '8', '6', 'g']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_X()
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