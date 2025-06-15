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
    if lookahead.startswith('0'):
        match('0')
        match('0')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith(';'):
            match(';')
            parse_A()
            match('5')
            match('`')
        elif lookahead.startswith('>'):
            match('>')
        elif lookahead.startswith('m'):
            match('m')
            parse_X()
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join([';', '>', 'm']))
        match('H')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('l'):
            match('l')
            parse_E()
        elif lookahead.startswith('i'):
            match('i')
            match('7')
            parse_X()
            parse_F()
        elif lookahead.startswith('_'):
            match('_')
            parse_X()
            match('r')
            parse_E()
        elif lookahead.startswith('U'):
            match('U')
            parse_E()
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['l', 'i', '_', 'U']))
    elif lookahead.startswith('n'):
        match('n')
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('0'):
            match('0')
            match('0')
            parse_A()
            match('H')
            parse_E()
        elif lookahead.startswith('n'):
            match('n')
            parse_X()
        elif lookahead.startswith('d'):
            match('d')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['0', 'n', 'd']))
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['0', 'n', 'd']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith(';'):
        match(';')
        parse_A()
        match('5')
        match('`')
    elif lookahead.startswith('>'):
        match('>')
    elif lookahead.startswith('m'):
        match('m')
        parse_X()
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join([';', '>', 'm']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('l'):
        match('l')
        parse_E()
    elif lookahead.startswith('i'):
        match('i')
        match('7')
        parse_X()
        parse_F()
    elif lookahead.startswith('_'):
        match('_')
        parse_X()
        match('r')
        parse_E()
    elif lookahead.startswith('U'):
        match('U')
        parse_E()
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['l', 'i', '_', 'U']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('>'):
        match('>')
        match('~')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['>', '']))

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