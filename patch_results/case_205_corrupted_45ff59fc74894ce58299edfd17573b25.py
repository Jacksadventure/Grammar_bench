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

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
        match('l')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('L'):
            match('L')
            match('h')
            match('r')
            parse_X()
        elif lookahead.startswith('@'):
            match('@')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['L', '@']))
        match('z')
    elif lookahead.startswith('5'):
        match('5')
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('+'):
            match('+')
            match('l')
            parse_B()
            match('z')
        elif lookahead.startswith('5'):
            match('5')
            parse_F()
            match('o')
            parse_E()
            match('~')
        elif lookahead.startswith(','):
            match(',')
            match('&')
            match('D')
            match('1')
        elif lookahead.startswith('2'):
            match('2')
            match('y')
            parse_Q()
            match('}')
            match("'")
        elif lookahead.startswith('Q'):
            parse_Q()
            parse_U()
            match('n')
            match('a')
            parse_U()
        elif lookahead.startswith('7'):
            match('7')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['+', '5', ',', '2', 'Q', '7']))
        match('o')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('?'):
            match('?')
            match('q')
            parse_R()
        elif lookahead.startswith('5'):
            match('5')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['?', '5']))
        match('~')
    elif lookahead.startswith(','):
        match(',')
        match('&')
        match('D')
        match('1')
    elif lookahead.startswith('2'):
        match('2')
        match('y')
        while pos < len(tokens) and tokens[pos].startswith('`'):
            match('`')
        match('}')
        match("'")
    elif lookahead.startswith('Q'):
        while pos < len(tokens) and tokens[pos].startswith('`'):
            match('`')
        while pos < len(tokens) and tokens[pos].startswith('e'):
            match('e')
            match('c')
        match('n')
        match('a')
        while pos < len(tokens) and tokens[pos].startswith('e'):
            match('e')
            match('c')
    elif lookahead.startswith('7'):
        match('7')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['+', '5', ',', '2', 'Q', '7']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        match('q')
        parse_R()
    elif lookahead.startswith('5'):
        match('5')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['?', '5']))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('('):
        match('(')
        match('~')
        match('5')
        match('r')
        parse_B()
    elif lookahead.startswith('b'):
        match('b')
    elif lookahead.startswith(']'):
        match(']')
    elif lookahead.startswith('['):
        match('[')
        match("'")
        parse_B()
        match('1')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['(', 'b', ']', '[']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('h'):
        match('h')
        match('=')
        match('_')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['h', '']))

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('`'):
        match('`')

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('L'):
        match('L')
        match('h')
        match('r')
        parse_X()
    elif lookahead.startswith('@'):
        match('@')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['L', '@']))

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('e'):
        match('e')
        match('c')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_F()
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