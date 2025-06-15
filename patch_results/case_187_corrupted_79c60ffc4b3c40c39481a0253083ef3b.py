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

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('9'):
        match('9')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('$'):
            match('$')
            match('q')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['$', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('9'):
            match('9')
            parse_J()
            parse_A()
            parse_J()
            parse_A()
        elif lookahead.startswith('P'):
            match('P')
            parse_D()
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['9', '', 'P']))
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('$'):
            match('$')
            match('q')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['$', '']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('&'):
        match('&')
        match('f')
        match('$')
        parse_E()
    elif lookahead.startswith('r'):
        match('r')
        match('%')
        parse_H()
    elif lookahead.startswith('f'):
        match('f')
        match('&')
        match('^')
    elif lookahead.startswith('k'):
        match('k')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['&', 'r', 'f', 'k']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('$'):
        match('$')
        match('q')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['$', '']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('A'):
        parse_A()
        parse_E()
        parse_J()
        match('`')
        parse_V()
    elif lookahead.startswith('<'):
        match('<')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['A', '<']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('$'):
        match('$')
        match('{')
        match('k')
    elif lookahead.startswith('4'):
        match('4')
        parse_V()
        parse_D()
        match("'")
        match('g')
    elif lookahead.startswith('!'):
        match('!')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['$', '4', '!']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('E'):
        parse_E()
        match('*')
        match('$')
        match('O')
        match('X')
    elif lookahead.startswith('c'):
        match('c')
        match("'")
    elif lookahead.startswith('{'):
        match('{')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['E', 'c', '{']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_A()
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