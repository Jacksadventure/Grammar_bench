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
    while pos < len(tokens) and tokens[pos].startswith('/'):
        match('/')
        match('R')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('/'):
            match('/')
            match('R')
            parse_M()
            match('g')
            parse_M()
        elif lookahead.startswith('a'):
            match('a')
            parse_N()
            parse_W()
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['/', '', 'a']))
        match('g')

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('C'):
        match('C')
    elif lookahead.startswith(';'):
        match(';')
        parse_M()
        match('Q')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['C', ';']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('^'):
        match('^')
        match('*')
        parse_N()
        match(')')
    elif lookahead.startswith('<'):
        match('<')
        parse_M()
        match('-')
        match('O')
        parse_M()
    elif lookahead.startswith('V'):
        match('V')
        match('s')
        match('~')
        match('L')
        match('/')
    elif lookahead.startswith('#'):
        match('#')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['^', '<', 'V', '#']))

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