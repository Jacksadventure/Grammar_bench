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
    if lookahead.startswith('W'):
        match('W')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('T'):
            match('T')
            parse_N()
        elif lookahead.startswith('n'):
            match('n')
            parse_X()
            parse_U()
        elif lookahead.startswith('2'):
            match('2')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['T', 'n', '2']))
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('T'):
            match('T')
            parse_N()
        elif lookahead.startswith('n'):
            match('n')
            parse_X()
            parse_U()
        elif lookahead.startswith('2'):
            match('2')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['T', 'n', '2']))
    elif lookahead.startswith('&'):
        match('&')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['W', '&']))

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('n'):
        match('n')
        match('$')
        match('F')
        match('6')

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('c'):
        match('c')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['c']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('T'):
        match('T')
        parse_N()
    elif lookahead.startswith('n'):
        match('n')
        parse_X()
        parse_U()
    elif lookahead.startswith('2'):
        match('2')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['T', 'n', '2']))

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