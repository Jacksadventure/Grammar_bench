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

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('?'):
        match('?')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('o'):
            match('o')
            match('o')
            parse_O()
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['o', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('-'):
            match('-')
            parse_G()
            parse_D()
            parse_O()
            match('A')
            parse_Z()
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['-', '']))
        match('>')

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")
        parse_F()
        parse_N()
        match('0')
        match('s')

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('-'):
        match('-')
        parse_G()
        parse_D()
        parse_O()
        match('A')

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('J'):
        match('J')
        match(')')

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('o'):
        match('o')
        match('o')

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
    elif lookahead.startswith('0'):
        match('0')
        parse_Z()
    elif lookahead.startswith('Y'):
        match('Y')
        match('f')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['j', '0', 'Y']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_F()
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