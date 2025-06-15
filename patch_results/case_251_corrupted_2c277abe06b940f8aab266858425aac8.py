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

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('d'):
        match('d')
        match('B')
    elif lookahead.startswith('{'):
        match('{')
    elif lookahead.startswith('a'):
        match('a')
        match('N')
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith(':'):
            match(':')
            parse_F()
        elif lookahead.startswith('-'):
            match('-')
            parse_D()
            parse_H()
        elif lookahead.startswith('a'):
            match('a')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join([':', '-', 'a']))
        while pos < len(tokens) and tokens[pos].startswith('c'):
            match('c')
            match('7')
            parse_S()
            parse_F()
            parse_E()
        while pos < len(tokens) and tokens[pos].startswith('c'):
            match('c')
            match('7')
            parse_S()
            parse_F()
            parse_E()
    elif lookahead.startswith('r'):
        match('r')
    elif lookahead.startswith('9'):
        match('9')
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith(':'):
            match(':')
            parse_F()
        elif lookahead.startswith('-'):
            match('-')
            parse_D()
            parse_H()
        elif lookahead.startswith('a'):
            match('a')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join([':', '-', 'a']))
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['d', '{', 'a', 'r', '9']))

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('d'):
        match('d')

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('='):
        match('=')
        parse_D()

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith(':'):
        match(':')
        parse_F()
    elif lookahead.startswith('-'):
        match('-')
        parse_D()
        parse_H()
    elif lookahead.startswith('a'):
        match('a')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join([':', '-', 'a']))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('T'):
        match('T')
        parse_I()

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('>'):
        match('>')
        parse_H()
        match("'")
        match('W')
        parse_S()

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('c'):
        match('c')
        match('7')
        parse_S()
        parse_F()
        parse_E()

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('~'):
        match('~')
        match('M')
        match('l')
        parse_Y()
    elif lookahead.startswith('K'):
        match('K')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['~', 'K']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_O()
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