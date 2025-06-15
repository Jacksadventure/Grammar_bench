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
    if lookahead.startswith('F'):
        match('F')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('G'):
            match('G')
            match(']')
            match('y')
            parse_E()
        elif lookahead.startswith('>'):
            match('>')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['G', '>']))
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('j'):
            match('j')
            match('I')
            match(':')
            match('[')
            match('}')
        elif lookahead.startswith('/'):
            match('/')
            match('t')
            parse_T()
        elif lookahead.startswith('.'):
            match('.')
            match('e')
            match('z')
            match('B')
            match('`')
        elif lookahead.startswith('d'):
            match('d')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['j', '/', '.', 'd']))
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('A'):
            match('A')
            parse_Y()
            match('k')
            match('J')
            match('c')
            match('=')
        elif lookahead.startswith('2'):
            match('2')
        elif lookahead.startswith('X'):
            parse_X()
            match('*')
            match(';')
            parse_Y()
            match('O')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['A', '2', 'X']))
    elif lookahead.startswith('>'):
        match('>')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['F', '>']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('J'):
        match('J')
        match("'")
        match('q')
        match('q')
        match('!')
    elif lookahead.startswith('v'):
        match('v')
    elif lookahead.startswith('{'):
        match('{')
        parse_Y()
    elif lookahead.startswith('f'):
        match('f')
        parse_Z()
        match('m')
        parse_E()
    elif lookahead.startswith('I'):
        match('I')
        parse_Y()
        match('8')
        parse_X()
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['J', 'v', '{', 'f', 'I']))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
        match('I')
        match(':')
        match('[')
        match('}')
    elif lookahead.startswith('/'):
        match('/')
        match('t')
        parse_T()
    elif lookahead.startswith('.'):
        match('.')
        match('e')
        match('z')
        match('B')
        match('`')
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['j', '/', '.', 'd']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('G'):
        match('G')
        match(']')
        match('y')
        parse_E()
    elif lookahead.startswith('>'):
        match('>')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['G', '>']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('A'):
        match('A')
        parse_Y()
        match('k')
        match('J')
        match('c')
        match('=')
    elif lookahead.startswith('2'):
        match('2')
    elif lookahead.startswith('X'):
        parse_X()
        match('*')
        match(';')
        parse_Y()
        match('O')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['A', '2', 'X']))

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