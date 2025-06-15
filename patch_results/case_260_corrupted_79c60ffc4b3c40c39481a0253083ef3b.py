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

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('1'):
        match('1')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith(')'):
            match(')')
            match('m')
            parse_X()
            parse_T()
        elif lookahead.startswith('N'):
            match('N')
            parse_M()
            parse_Z()
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join([')', '', 'N']))

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(')'):
        match(')')
        match('m')
        parse_X()

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('g'):
        match('g')
        match(';')
        match('x')

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('O'):
        match('O')
        match('b')
        parse_C()
        parse_R()
        parse_K()
    elif lookahead.startswith('<'):
        match('<')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['O', '<']))

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('K'):
        parse_K()
        match('~')
        parse_R()

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('&'):
        match('&')
        parse_Z()
        match('|')
        match('V')

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('+'):
        match('+')
        match('}')
        match('y')
        match('y')
        match('0')

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")
        match('B')
        match('/')
        match('s')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Q()
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