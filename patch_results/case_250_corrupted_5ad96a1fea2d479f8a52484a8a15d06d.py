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

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
        while pos < len(tokens) and tokens[pos].startswith('m'):
            match('m')
            match('3')
        while pos < len(tokens) and tokens[pos].startswith('l'):
            match('l')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('+'):
            match('+')
            parse_V()
            parse_A()
            parse_M()
            parse_I()
        elif lookahead.startswith('{'):
            match('{')
            parse_F()
            parse_Z()
            match('~')
            parse_F()
        elif lookahead.startswith('o'):
            match('o')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['+', '{', 'o']))
        while pos < len(tokens) and tokens[pos].startswith('b'):
            match('b')
            parse_V()
    elif lookahead.startswith('{'):
        match('{')
        while pos < len(tokens) and tokens[pos].startswith('a'):
            match('a')
            parse_Z()
            match('=')
            match("'")
            match('2')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('T'):
            match('T')
            match(':')
            match('w')
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['T', '']))
        match('~')
        while pos < len(tokens) and tokens[pos].startswith('a'):
            match('a')
            parse_Z()
            match('=')
            match("'")
            match('2')
    elif lookahead.startswith('o'):
        match('o')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['+', '{', 'o']))

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('b'):
        match('b')
        parse_V()

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('m'):
        match('m')
        match('3')

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('&'):
        match('&')
        match('`')
        parse_P()
        parse_P()
    elif lookahead.startswith('D'):
        match('D')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['&', 'D']))

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('a'):
        match('a')
        parse_Z()
        match('=')
        match("'")
        match('2')

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('l'):
        match('l')

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('T'):
        match('T')
        match(':')
        match('w')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['T', '']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_M()
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