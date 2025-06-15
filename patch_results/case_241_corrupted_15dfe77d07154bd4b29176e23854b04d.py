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
    if lookahead.startswith('^'):
        match('^')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('^'):
            match('^')
            parse_Z()
            match('e')
        elif lookahead.startswith('H'):
            parse_H()
        elif lookahead.startswith('q'):
            match('q')
            match('w')
            match('p')
            parse_H()
            parse_D()
        elif lookahead.startswith('x'):
            match('x')
            parse_J()
            parse_J()
            match('e')
        elif lookahead.startswith('P'):
            match('P')
            match('5')
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['^', 'H', 'q', 'x', 'P']))
        match('e')
    elif lookahead.startswith('H'):
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('+'):
            match('+')
        elif lookahead.startswith('Q'):
            match('Q')
        elif lookahead.startswith('B'):
            match('B')
            parse_Z()
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['+', 'Q', 'B']))
    elif lookahead.startswith('q'):
        match('q')
        match('w')
        match('p')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('+'):
            match('+')
        elif lookahead.startswith('Q'):
            match('Q')
        elif lookahead.startswith('B'):
            match('B')
            parse_Z()
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['+', 'Q', 'B']))
        while pos < len(tokens) and tokens[pos].startswith('`'):
            match('`')
            parse_D()
            parse_D()
            parse_J()
    elif lookahead.startswith('x'):
        match('x')
        while pos < len(tokens) and tokens[pos].startswith('_'):
            match('_')
            parse_H()
            parse_K()
        while pos < len(tokens) and tokens[pos].startswith('_'):
            match('_')
            parse_H()
            parse_K()
        match('e')
    elif lookahead.startswith('P'):
        match('P')
        match('5')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['^', 'H', 'q', 'x', 'P']))

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('_'):
        match('_')
        parse_H()
        parse_K()

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('k'):
        match('k')

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('`'):
        match('`')
        parse_D()
        parse_D()
        parse_J()

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
    elif lookahead.startswith('Q'):
        match('Q')
    elif lookahead.startswith('B'):
        match('B')
        parse_Z()
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['+', 'Q', 'B']))

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