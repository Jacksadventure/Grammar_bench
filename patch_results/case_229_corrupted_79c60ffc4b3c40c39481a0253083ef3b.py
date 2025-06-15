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
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('l'):
        match('l')
        match('m')
        while pos < len(tokens) and tokens[pos].startswith('&'):
            match('&')
        while pos < len(tokens) and tokens[pos].startswith('&'):
            match('&')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('8'):
            match('8')
            parse_G()
            parse_Z()
            parse_S()
        elif lookahead.startswith('Y'):
            match('Y')
            parse_Z()
            parse_G()
            parse_G()
            parse_G()
        elif lookahead.startswith('}'):
            match('}')
            parse_A()
            parse_A()
            parse_Z()
            parse_C()
        elif lookahead.startswith('w'):
            match('w')
            parse_A()
            parse_G()
            parse_Z()
            parse_C()
        elif lookahead.startswith('$'):
            match('$')
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['8', 'Y', '}', 'w', '$']))
    elif lookahead.startswith('4'):
        match('4')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['l', '4']))

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('('):
        match('(')
        parse_G()
        parse_S()
        parse_G()
        match('f')

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('8'):
        match('8')
        parse_G()
        parse_Z()
        parse_S()
    elif lookahead.startswith('Y'):
        match('Y')
        parse_Z()
        parse_G()
        parse_G()
        parse_G()
    elif lookahead.startswith('}'):
        match('}')
        parse_A()
        parse_A()
        parse_Z()
        parse_C()
    elif lookahead.startswith('w'):
        match('w')
        parse_A()
        parse_G()
        parse_Z()
        parse_C()
    elif lookahead.startswith('$'):
        match('$')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['8', 'Y', '}', 'w', '$']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('.'):
        match('.')
        parse_G()
        match("'")
        match('4')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['.', '']))

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('&'):
        match('&')

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