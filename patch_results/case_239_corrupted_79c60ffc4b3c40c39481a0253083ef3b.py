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

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('h'):
        match('h')
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('('):
            match('(')
            parse_D()
            parse_D()
            parse_D()
        elif lookahead.startswith('%'):
            match('%')
            parse_B()
            parse_D()
            match('X')
            parse_F()
        elif lookahead.startswith('s'):
            match('s')
            match('d')
            parse_R()
            parse_W()
            parse_B()
        elif lookahead.startswith('`'):
            match('`')
            parse_W()
            parse_R()
            parse_D()
            parse_R()
        elif lookahead.startswith('n'):
            match('n')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['(', '%', 's', '`', 'n']))
    elif lookahead.startswith('S'):
        match('S')
        while pos < len(tokens) and tokens[pos].startswith('*'):
            match('*')
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith('`'):
            match('`')
            parse_D()
            parse_B()
        elif lookahead.startswith('l'):
            match('l')
        elif lookahead.startswith('p'):
            match('p')
            parse_B()
            match('k')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['`', 'l', 'p']))
    elif lookahead.startswith('|'):
        match('|')
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('('):
            match('(')
            parse_D()
            parse_D()
            parse_D()
        elif lookahead.startswith('%'):
            match('%')
            parse_B()
            parse_D()
            match('X')
            parse_F()
        elif lookahead.startswith('s'):
            match('s')
            match('d')
            parse_R()
            parse_W()
            parse_B()
        elif lookahead.startswith('`'):
            match('`')
            parse_W()
            parse_R()
            parse_D()
            parse_R()
        elif lookahead.startswith('n'):
            match('n')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['(', '%', 's', '`', 'n']))
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('q'):
            match('q')
        elif lookahead.startswith('P'):
            match('P')
            parse_D()
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['q', 'P']))
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('h'):
            match('h')
            parse_F()
        elif lookahead.startswith('S'):
            match('S')
            parse_B()
            parse_W()
        elif lookahead.startswith('|'):
            match('|')
            parse_F()
            parse_G()
            parse_R()
        elif lookahead.startswith('^'):
            match('^')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['h', 'S', '|', '^']))
    elif lookahead.startswith('^'):
        match('^')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['h', 'S', '|', '^']))

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('*'):
        match('*')

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('('):
        match('(')
        parse_D()
        parse_D()
        parse_D()
    elif lookahead.startswith('%'):
        match('%')
        parse_B()
        parse_D()
        match('X')
        parse_F()
    elif lookahead.startswith('s'):
        match('s')
        match('d')
        parse_R()
        parse_W()
        parse_B()
    elif lookahead.startswith('`'):
        match('`')
        parse_W()
        parse_R()
        parse_D()
        parse_R()
    elif lookahead.startswith('n'):
        match('n')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['(', '%', 's', '`', 'n']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('q'):
        match('q')
    elif lookahead.startswith('P'):
        match('P')
        parse_D()
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['q', 'P']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('`'):
        match('`')
        parse_D()
        parse_B()
    elif lookahead.startswith('l'):
        match('l')
    elif lookahead.startswith('p'):
        match('p')
        parse_B()
        match('k')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['`', 'l', 'p']))

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(';'):
        match(';')
        match('z')
        parse_R()
        match('P')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_R()
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