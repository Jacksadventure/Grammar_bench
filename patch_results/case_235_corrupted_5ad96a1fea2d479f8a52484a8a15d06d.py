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

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('}'):
        match('}')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('.'):
            match('.')
            match('~')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['.', '']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('.'):
        match('.')
        match('~')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['.', '']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
        parse_I()
        parse_G()
        parse_L()
    elif lookahead.startswith('-'):
        match('-')
        match('%')
        parse_R()
        parse_I()
        match('Z')
    elif lookahead.startswith('~'):
        match('~')
        parse_L()
        parse_I()
    elif lookahead.startswith('.'):
        match('.')
        parse_V()
    elif lookahead.startswith('{'):
        match('{')
        parse_A()
        parse_V()
        parse_G()
        parse_V()
    elif lookahead.startswith('U'):
        match('U')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['+', '-', '~', '.', '{', 'U']))

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('C'):
        match('C')
        parse_L()
        match(';')

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('%'):
        match('%')
        parse_L()

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('A'):
        parse_A()
        match('l')
        match('4')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_V()
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