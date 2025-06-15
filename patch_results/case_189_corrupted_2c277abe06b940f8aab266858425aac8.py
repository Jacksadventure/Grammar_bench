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
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('4'):
            match('4')
            parse_N()
        elif lookahead.startswith('&'):
            match('&')
            parse_F()
            match('a')
        elif lookahead.startswith('k'):
            match('k')
            match('`')
            parse_L()
            parse_U()
            match('[')
        elif lookahead.startswith('}'):
            match('}')
            match('~')
            parse_B()
            parse_F()
        elif lookahead.startswith('e'):
            match('e')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['4', '&', 'k', '}', 'e']))
        while pos < len(tokens) and tokens[pos].startswith('Q'):
            match('Q')
            match('.')
            parse_C()
            parse_L()
    elif lookahead.startswith('1'):
        match('1')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['?', '1']))

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('H'):
        match('H')
        parse_C()
        match('/')

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('e'):
        match('e')
    elif lookahead.startswith('^'):
        match('^')
        match('X')
        parse_F()
        match("'")
    elif lookahead.startswith('Y'):
        match('Y')
        match('o')
    elif lookahead.startswith('A'):
        match('A')
        parse_U()
        parse_B()
        parse_U()
    elif lookahead.startswith('`'):
        match('`')
        parse_B()
        match('x')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['e', '^', 'Y', 'A', '`']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('4'):
        match('4')
        parse_N()
    elif lookahead.startswith('&'):
        match('&')
        parse_F()
        match('a')
    elif lookahead.startswith('k'):
        match('k')
        match('`')
        parse_L()
        parse_U()
        match('[')
    elif lookahead.startswith('}'):
        match('}')
        match('~')
        parse_B()
        parse_F()
    elif lookahead.startswith('e'):
        match('e')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['4', '&', 'k', '}', 'e']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('b'):
        match('b')
        match('0')
        parse_N()
        parse_C()
    elif lookahead.startswith('o'):
        match('o')
    elif lookahead.startswith('z'):
        match('z')
    elif lookahead.startswith('}'):
        match('}')
    elif lookahead.startswith('h'):
        match('h')
        parse_F()
        match('K')
        match('T')
        match("'")
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['b', 'o', 'z', '}', 'h']))

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Q'):
        match('Q')
        match('.')
        parse_C()
        parse_L()

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