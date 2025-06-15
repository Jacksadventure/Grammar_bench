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
    while pos < len(tokens) and tokens[pos].startswith('|'):
        match('|')
        match('J')
        match('G')
        match("'")
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('T'):
            match('T')
            parse_P()
            parse_P()
        elif lookahead.startswith('H'):
            match('H')
            parse_M()
            parse_N()
            parse_U()
        elif lookahead.startswith('+'):
            match('+')
            match('T')
            parse_M()
            parse_P()
            parse_M()
        elif lookahead.startswith('Z'):
            match('Z')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['T', 'H', '+', 'Z']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        match('c')
        match(':')
        parse_M()
    elif lookahead.startswith('&'):
        match('&')
    elif lookahead.startswith('d'):
        match('d')
        parse_M()
        match('`')
        parse_P()
        match('e')
    elif lookahead.startswith('W'):
        match('W')
        parse_P()
        parse_P()
        parse_U()
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['/', '&', 'd', 'W']))

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('B'):
        match('B')
        parse_M()

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('T'):
        match('T')
        parse_P()
        parse_P()
    elif lookahead.startswith('H'):
        match('H')
        parse_M()
        parse_N()
        parse_U()
    elif lookahead.startswith('+'):
        match('+')
        match('T')
        parse_M()
        parse_P()
        parse_M()
    elif lookahead.startswith('Z'):
        match('Z')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['T', 'H', '+', 'Z']))

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