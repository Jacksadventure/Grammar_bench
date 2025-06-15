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

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('N'):
        match('N')
        while pos < len(tokens) and tokens[pos].startswith('I'):
            match('I')
            parse_A()
        match('P')
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith('!'):
            match('!')
            parse_A()
        elif lookahead.startswith('0'):
            match('0')
            parse_A()
            match('O')
            match('3')
            parse_X()
        elif lookahead.startswith('w'):
            match('w')
            parse_A()
            match('I')
            match('?')
            parse_A()
        elif lookahead.startswith('`'):
            match('`')
            match('<')
            parse_X()
            match(']')
            match('}')
        elif lookahead.startswith(')'):
            match(')')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['!', '0', 'w', '`', ')']))
        match('|')
    elif lookahead.startswith('0'):
        match('0')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['N', '0']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('E'):
        match('E')
        parse_X()
        match(')')
    elif lookahead.startswith('3'):
        match('3')
        match("'")
        match('a')
    elif lookahead.startswith('4'):
        match('4')
    elif lookahead.startswith('X'):
        parse_X()
        match('8')
        match('`')
        match('i')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['E', '3', '4', 'X']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_X()
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