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

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(')'):
        match(')')
        match('I')
        match('z')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('r'):
            match('r')
            match('q')
            parse_J()
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['r', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('o'):
            match('o')
            parse_T()
            match("'")
            parse_T()
        elif lookahead.startswith('*'):
            match('*')
            parse_B()
        elif lookahead.startswith('4'):
            match('4')
            parse_R()
        elif lookahead.startswith('H'):
            match('H')
            parse_K()
            match('8')
        elif lookahead.startswith('^'):
            match('^')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['o', '*', '4', 'H', '^']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        parse_T()
        match("'")
        parse_T()
    elif lookahead.startswith('*'):
        match('*')
        parse_B()
    elif lookahead.startswith('4'):
        match('4')
        parse_R()
    elif lookahead.startswith('H'):
        match('H')
        parse_K()
        match('8')
    elif lookahead.startswith('^'):
        match('^')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['o', '*', '4', 'H', '^']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('t'):
        match('t')
        match('I')

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('g'):
        match('g')
        parse_T()
        parse_B()

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('r'):
        match('r')
        match('q')

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('t'):
        match('t')
        parse_N()
        parse_K()
        parse_K()
        match('1')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_N()
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