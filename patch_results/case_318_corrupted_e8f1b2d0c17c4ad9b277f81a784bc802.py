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

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('d'):
        match('d')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('t'):
            match('t')
            match('r')
        elif lookahead.startswith('<'):
            match('<')
        elif lookahead.startswith('+'):
            match('+')
            parse_Y()
            parse_P()
            match('.')
        elif lookahead.startswith('y'):
            match('y')
            parse_V()
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['t', '<', '+', 'y']))
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('w'):
            match('w')
            parse_D()
            parse_W()
            match('!')
            parse_P()
            parse_Y()
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['w', '']))
        match('_')

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('t'):
        match('t')
        match('r')
    elif lookahead.startswith('<'):
        match('<')
    elif lookahead.startswith('+'):
        match('+')
        parse_Y()
        parse_P()
        match('.')
    elif lookahead.startswith('y'):
        match('y')
        parse_V()
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['t', '<', '+', 'y']))

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('|'):
        match('|')

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('g'):
        match('g')
        match('9')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['g', '']))

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('w'):
        match('w')
        parse_D()
        parse_W()
        match('!')
        parse_P()

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('U'):
        match('U')
    elif lookahead.startswith("'"):
        match("'")
        parse_V()
        parse_D()
        parse_H()
    elif lookahead.startswith('6'):
        match('6')
        parse_P()
        parse_D()
        parse_I()
        parse_H()
    elif lookahead.startswith('Y'):
        parse_Y()
        match('0')
        parse_P()
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['U', "'", '6', 'Y']))

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('P'):
        parse_P()
        parse_P()
        match('O')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_D()
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