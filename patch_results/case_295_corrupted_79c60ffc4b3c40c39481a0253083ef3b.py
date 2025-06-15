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
    while pos < len(tokens) and tokens[pos].startswith('P'):
        match('P')
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith('C'):
            match('C')
            parse_H()
            parse_H()
            match('5')
        elif lookahead.startswith('P'):
            match('P')
            parse_R()
            parse_J()
            match('u')
            match('s')
        elif lookahead.startswith('X'):
            match('X')
            parse_H()
            match("'")
            parse_R()
            match('-')
        elif lookahead.startswith('w'):
            match('w')
            parse_L()
            parse_R()
        elif lookahead.startswith('@'):
            match('@')
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['C', 'P', 'X', 'w', '@']))
        match('X')

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('*'):
        match('*')
        parse_N()
        match('-')

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('}'):
        match('}')
        match('C')
        match('c')

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('h'):
        match('h')
        parse_R()

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('C'):
        match('C')
        parse_H()
        parse_H()
        match('5')
    elif lookahead.startswith('P'):
        match('P')
        parse_R()
        parse_J()
        match('u')
        match('s')
    elif lookahead.startswith('X'):
        match('X')
        parse_H()
        match("'")
        parse_R()
        match('-')
    elif lookahead.startswith('w'):
        match('w')
        parse_L()
        parse_R()
    elif lookahead.startswith('@'):
        match('@')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['C', 'P', 'X', 'w', '@']))

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