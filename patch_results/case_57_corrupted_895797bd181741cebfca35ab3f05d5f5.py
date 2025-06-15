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

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('K'):
        match('K')
        match('m')
        match('!')
    elif lookahead.startswith('B'):
        match('B')
        match('>')
        match(')')
        match('z')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('+'):
            match('+')
            parse_D()
            parse_M()
            parse_M()
            match('`')
        elif lookahead.startswith('X'):
            match('X')
            match('5')
        elif lookahead.startswith("'"):
            match("'")
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['+', 'X', "'"]))
    elif lookahead.startswith('6'):
        match('6')
        match('x')
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith('|'):
            match('|')
            parse_U()
            match('a')
            match('8')
        elif lookahead.startswith('H'):
            match('H')
        else:
            error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['|', 'H']))
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('+'):
            match('+')
            parse_D()
            parse_M()
            parse_M()
            match('`')
        elif lookahead.startswith('X'):
            match('X')
            match('5')
        elif lookahead.startswith("'"):
            match("'")
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['+', 'X', "'"]))
        match('z')
    elif lookahead.startswith('V'):
        match('V')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['K', 'B', '6', 'V']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
        parse_D()
        parse_M()
        parse_M()
        match('`')
    elif lookahead.startswith('X'):
        match('X')
        match('5')
    elif lookahead.startswith("'"):
        match("'")
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['+', 'X', "'"]))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('|'):
        match('|')
        parse_U()
        match('a')
        match('8')
    elif lookahead.startswith('H'):
        match('H')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['|', 'H']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_U()
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