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

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('q'):
        match('q')
        while pos < len(tokens) and tokens[pos].startswith('C'):
            match('C')
            parse_J()
            match('7')
            parse_X()
    elif lookahead.startswith('?'):
        match('?')
        while pos < len(tokens) and tokens[pos].startswith('5'):
            match('5')
            match('q')
            parse_T()
            parse_B()
    elif lookahead.startswith('x'):
        match('x')
    elif lookahead.startswith('Z'):
        match('Z')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['q', '?', 'x', 'Z']))

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('5'):
        match('5')
        match('q')
        parse_T()
        parse_B()

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('h'):
        match('h')
        parse_B()
        parse_Y()
        match('$')
    elif lookahead.startswith('V'):
        match('V')
        match('p')
        match('q')
    elif lookahead.startswith("'"):
        match("'")
        parse_E()
        parse_B()
        match('W')
        parse_Y()
    elif lookahead.startswith('/'):
        match('/')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['h', 'V', "'", '/']))

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('E'):
        parse_E()

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('#'):
        match('#')
        match('U')

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('*'):
        match('*')
    elif lookahead.startswith('v'):
        match('v')
        match('`')
        parse_M()
    elif lookahead.startswith('9'):
        match('9')
        parse_Y()
        parse_B()
        parse_T()
    elif lookahead.startswith('@'):
        match('@')
        match('P')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['*', 'v', '9', '@']))

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(';'):
        match(';')
        parse_E()
        parse_M()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_E()
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