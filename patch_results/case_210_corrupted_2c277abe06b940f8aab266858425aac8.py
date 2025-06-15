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

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('p'):
        match('p')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('p'):
            match('p')
            parse_G()
            match('T')
            parse_S()
            parse_I()
        elif lookahead.startswith('v'):
            match('v')
            parse_Z()
        elif lookahead.startswith('m'):
            match('m')
        elif lookahead.startswith('O'):
            match('O')
            match('>')
            match('F')
            match('C')
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['p', 'v', 'm', 'O']))
        match('T')
        while pos < len(tokens) and tokens[pos].startswith('g'):
            match('g')
            match('b')
        while pos < len(tokens) and tokens[pos].startswith('h'):
            match('h')
            parse_Z()
    elif lookahead.startswith('v'):
        match('v')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith(')'):
            match(')')
            parse_W()
            match('@')
            match('}')
            parse_Y()
        elif lookahead.startswith('c'):
            match('c')
            match('g')
            parse_E()
            parse_G()
            match('e')
        elif lookahead.startswith('{'):
            match('{')
            match('~')
            parse_G()
        elif lookahead.startswith('S'):
            parse_S()
            match('|')
            match('(')
            match('#')
        elif lookahead.startswith('T'):
            match('T')
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join([')', 'c', '{', 'S', 'T']))
    elif lookahead.startswith('m'):
        match('m')
    elif lookahead.startswith('O'):
        match('O')
        match('>')
        match('F')
        match('C')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['p', 'v', 'm', 'O']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('x'):
        match('x')
        parse_N()
        match('>')
        match('5')
    elif lookahead.startswith('u'):
        match('u')
        parse_G()
        parse_G()
        parse_Z()
    elif lookahead.startswith('%'):
        match('%')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['x', 'u', '%']))

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('g'):
        match('g')
        match('b')

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith(';'):
        match(';')
        match('$')
        parse_E()
        parse_Z()
        parse_G()
    elif lookahead.startswith('o'):
        match('o')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join([';', 'o']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('N'):
        parse_N()
        match('y')
        match('s')
        parse_Z()

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('h'):
        match('h')
        parse_Z()

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith(')'):
        match(')')
        parse_W()
        match('@')
        match('}')
        parse_Y()
    elif lookahead.startswith('c'):
        match('c')
        match('g')
        parse_E()
        parse_G()
        match('e')
    elif lookahead.startswith('{'):
        match('{')
        match('~')
        parse_G()
    elif lookahead.startswith('S'):
        parse_S()
        match('|')
        match('(')
        match('#')
    elif lookahead.startswith('T'):
        match('T')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join([')', 'c', '{', 'S', 'T']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        match('~')
        parse_N()
        match('R')
        match('/')
    elif lookahead.startswith('2'):
        match('2')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['/', '2']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_G()
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