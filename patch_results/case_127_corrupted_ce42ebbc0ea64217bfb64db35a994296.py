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

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('m'):
        match('m')
        match('R')
        match('l')
        while pos < len(tokens) and tokens[pos].startswith('O'):
            match('O')
            parse_Z()
    elif lookahead.startswith('I'):
        match('I')
        match("'")
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('V'):
            match('V')
            parse_M()
        elif lookahead.startswith('5'):
            match('5')
            match('&')
            parse_M()
        elif lookahead.startswith('9'):
            match('9')
            match('v')
            match('_')
            match('E')
        elif lookahead.startswith('H'):
            match('H')
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['V', '5', '9', 'H']))
        match('J')
        while pos < len(tokens) and tokens[pos].startswith('%'):
            match('%')
    elif lookahead.startswith('o'):
        match('o')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['m', 'I', 'o']))

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('I'):
        match('I')
        parse_W()
        match('.')
        parse_L()

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('r'):
        match('r')
        parse_M()
        parse_N()
        parse_Z()

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('O'):
        match('O')
        parse_Z()

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('%'):
        match('%')

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('>'):
        match('>')
        parse_Z()
        parse_U()
        parse_Z()
    elif lookahead.startswith('I'):
        match('I')
        match(';')
    elif lookahead.startswith('k'):
        match('k')
        match('O')
        parse_Z()
        parse_N()
    elif lookahead.startswith('e'):
        match('e')
    elif lookahead.startswith('|'):
        match('|')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['>', 'I', 'k', 'e', '|']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_L()
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