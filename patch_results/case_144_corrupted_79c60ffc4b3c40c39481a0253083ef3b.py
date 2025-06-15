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
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        match('3')
    elif lookahead.startswith('R'):
        match('R')
        if pos >= len(tokens):
            error("Unexpected end of input in Q")
        lookahead = tokens[pos]
        if lookahead.startswith('/'):
            match('/')
            match('3')
        elif lookahead.startswith('R'):
            match('R')
            parse_Q()
            parse_X()
            match("'")
            parse_B()
        elif lookahead.startswith('6'):
            match('6')
            match('$')
            parse_J()
            match('p')
            parse_B()
        elif lookahead.startswith('O'):
            match('O')
            match('/')
        elif lookahead.startswith('<'):
            match('<')
        else:
            error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['/', 'R', '6', 'O', '<']))
        while pos < len(tokens) and tokens[pos].startswith('n'):
            match('n')
            parse_X()
            parse_B()
            parse_S()
        match("'")
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('0'):
            match('0')
            parse_E()
        elif lookahead.startswith('='):
            match('=')
        elif lookahead.startswith('Y'):
            match('Y')
            match('8')
            match('q')
        elif lookahead.startswith('>'):
            match('>')
            parse_X()
            parse_U()
        elif lookahead.startswith('R'):
            match('R')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['0', '=', 'Y', '>', 'R']))
    elif lookahead.startswith('6'):
        match('6')
        match('$')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('?'):
            match('?')
            parse_Q()
            match('5')
            parse_H()
        elif lookahead.startswith('h'):
            match('h')
            parse_X()
            match('$')
        elif lookahead.startswith('n'):
            match('n')
            parse_J()
            match('/')
            match('Y')
            parse_S()
        elif lookahead.startswith('D'):
            match('D')
            parse_H()
            parse_U()
        elif lookahead.startswith('@'):
            match('@')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['?', 'h', 'n', 'D', '@']))
        match('p')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('0'):
            match('0')
            parse_E()
        elif lookahead.startswith('='):
            match('=')
        elif lookahead.startswith('Y'):
            match('Y')
            match('8')
            match('q')
        elif lookahead.startswith('>'):
            match('>')
            parse_X()
            parse_U()
        elif lookahead.startswith('R'):
            match('R')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['0', '=', 'Y', '>', 'R']))
    elif lookahead.startswith('O'):
        match('O')
        match('/')
    elif lookahead.startswith('<'):
        match('<')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['/', 'R', '6', 'O', '<']))

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('5'):
        match('5')
        match('Z')
        match('f')
        match('0')
        match('<')

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('y'):
        match('y')

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('X'):
        parse_X()
    elif lookahead.startswith(','):
        match(',')
        parse_H()
        parse_E()
        match('{')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['X', ',']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('0'):
        match('0')
        parse_E()
    elif lookahead.startswith('='):
        match('=')
    elif lookahead.startswith('Y'):
        match('Y')
        match('8')
        match('q')
    elif lookahead.startswith('>'):
        match('>')
        parse_X()
        parse_U()
    elif lookahead.startswith('R'):
        match('R')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['0', '=', 'Y', '>', 'R']))

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('n'):
        match('n')
        parse_X()
        parse_B()
        parse_S()

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        parse_Q()
        match('5')
        parse_H()
    elif lookahead.startswith('h'):
        match('h')
        parse_X()
        match('$')
    elif lookahead.startswith('n'):
        match('n')
        parse_J()
        match('/')
        match('Y')
        parse_S()
    elif lookahead.startswith('D'):
        match('D')
        parse_H()
        parse_U()
    elif lookahead.startswith('@'):
        match('@')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['?', 'h', 'n', 'D', '@']))

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('E'):
        parse_E()
        match('L')
        match('A')
        parse_H()

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