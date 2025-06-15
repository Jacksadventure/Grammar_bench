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

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('x'):
        match('x')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('!'):
            match('!')
            parse_Z()
            parse_G()
        elif lookahead.startswith('c'):
            match('c')
            parse_D()
        elif lookahead.startswith('_'):
            match('_')
            parse_O()
            parse_D()
            parse_Y()
        elif lookahead.startswith('b'):
            match('b')
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['!', 'c', '_', 'b']))
        match('=')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('!'):
            match('!')
            parse_Z()
            parse_G()
        elif lookahead.startswith('c'):
            match('c')
            parse_D()
        elif lookahead.startswith('_'):
            match('_')
            parse_O()
            parse_D()
            parse_Y()
        elif lookahead.startswith('b'):
            match('b')
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['!', 'c', '_', 'b']))
    elif lookahead.startswith('e'):
        match('e')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('!'):
            match('!')
            parse_Z()
            parse_G()
        elif lookahead.startswith('c'):
            match('c')
            parse_D()
        elif lookahead.startswith('_'):
            match('_')
            parse_O()
            parse_D()
            parse_Y()
        elif lookahead.startswith('b'):
            match('b')
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['!', 'c', '_', 'b']))
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('F'):
            match('F')
            match('E')
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['F', '']))
        while pos < len(tokens) and tokens[pos].startswith('E'):
            match('E')
            match('{')
            parse_G()
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('x'):
            match('x')
            parse_O()
            match('=')
            parse_O()
        elif lookahead.startswith('e'):
            match('e')
            parse_O()
            parse_G()
            parse_D()
            parse_Y()
        elif lookahead.startswith('}'):
            match('}')
            match('0')
            parse_D()
            parse_H()
            match('(')
        elif lookahead.startswith('N'):
            match('N')
            parse_Y()
            match('9')
        elif lookahead.startswith('a'):
            match('a')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['x', 'e', '}', 'N', 'a']))
    elif lookahead.startswith('}'):
        match('}')
        match('0')
        while pos < len(tokens) and tokens[pos].startswith('E'):
            match('E')
            match('{')
            parse_G()
        while pos < len(tokens) and tokens[pos].startswith('9'):
            match('9')
            parse_D()
            match('#')
            match('x')
            match('f')
        match('(')
    elif lookahead.startswith('N'):
        match('N')
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('x'):
            match('x')
            parse_O()
            match('=')
            parse_O()
        elif lookahead.startswith('e'):
            match('e')
            parse_O()
            parse_G()
            parse_D()
            parse_Y()
        elif lookahead.startswith('}'):
            match('}')
            match('0')
            parse_D()
            parse_H()
            match('(')
        elif lookahead.startswith('N'):
            match('N')
            parse_Y()
            match('9')
        elif lookahead.startswith('a'):
            match('a')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['x', 'e', '}', 'N', 'a']))
        match('9')
    elif lookahead.startswith('a'):
        match('a')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['x', 'e', '}', 'N', 'a']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('!'):
        match('!')
        parse_Z()
        parse_G()
    elif lookahead.startswith('c'):
        match('c')
        parse_D()
    elif lookahead.startswith('_'):
        match('_')
        parse_O()
        parse_D()
        parse_Y()
    elif lookahead.startswith('b'):
        match('b')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['!', 'c', '_', 'b']))

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('E'):
        match('E')
        match('{')
        parse_G()

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('F'):
        match('F')
        match('E')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['F', '']))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('9'):
        match('9')
        parse_D()
        match('#')
        match('x')
        match('f')

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('E'):
        match('E')
        match('y')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Y()
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