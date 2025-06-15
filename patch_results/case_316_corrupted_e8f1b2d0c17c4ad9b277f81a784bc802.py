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
    while pos < len(tokens) and tokens[pos].startswith('}'):
        match('}')
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('C'):
            match('C')
            parse_A()
            match('x')
            parse_F()
            parse_J()
        elif lookahead.startswith('5'):
            match('5')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['C', '5']))
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('I'):
            match('I')
            parse_E()
            parse_Z()
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['I', '']))

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('/'):
        match('/')

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
    elif lookahead.startswith('>'):
        match('>')
        parse_A()
        parse_A()
        parse_Z()
    elif lookahead.startswith('7'):
        match('7')
        parse_P()
        match('?')
        parse_E()
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['o', '>', '7']))

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('L'):
        match('L')

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('I'):
        match('I')
        parse_E()

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        parse_G()
        parse_P()
        parse_G()
        parse_M()
    elif lookahead.startswith('Z'):
        parse_Z()
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['?', 'Z']))

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(':'):
        match(':')
        match('%')
        match('?')
        match('W')
        parse_J()

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('C'):
        match('C')
        parse_A()
        match('x')
        parse_F()
        parse_J()
    elif lookahead.startswith('5'):
        match('5')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['C', '5']))

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('h'):
        match('h')
        parse_Z()
        match('D')
        parse_E()

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