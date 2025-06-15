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

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('a'):
        match('a')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('['):
            match('[')
            match('-')
            parse_U()
        elif lookahead.startswith('A'):
            match('A')
            parse_D()
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['[', '', 'A']))
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('Y'):
            parse_Y()
            parse_Z()
        elif lookahead.startswith(','):
            match(',')
            parse_C()
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['Y', '', ',']))
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('X'):
            match('X')
            parse_B()
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['X', '']))

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('['):
        match('[')
        match('-')

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('}'):
        match('}')
        parse_D()
        parse_J()
        parse_Y()

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('K'):
        match('K')
        parse_B()
        match('_')
        match('u')
    elif lookahead.startswith('-'):
        match('-')
        match('y')
        match('X')
        parse_U()
        parse_D()
    elif lookahead.startswith('N'):
        match('N')
    elif lookahead.startswith('e'):
        match('e')
        parse_Z()
    elif lookahead.startswith('?'):
        match('?')
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['K', '-', 'N', 'e', '?']))

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Y'):
        parse_Y()

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('X'):
        match('X')

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        parse_Z()
        match("'")
        match(';')
        match('!')
    elif lookahead.startswith('b'):
        match('b')
        parse_J()
        parse_J()
        parse_D()
        parse_Y()
    elif lookahead.startswith('3'):
        match('3')
        match('I')
        parse_C()
        match('k')
    elif lookahead.startswith("'"):
        match("'")
        match('~')
        parse_U()
    elif lookahead.startswith('g'):
        match('g')
        parse_C()
        match('f')
    elif lookahead.startswith('B'):
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['?', 'b', '3', "'", 'g', 'B']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Y()
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