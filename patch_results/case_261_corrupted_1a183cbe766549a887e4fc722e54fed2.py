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
    if lookahead.startswith('L'):
        match('L')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('L'):
            match('L')
            parse_N()
        elif lookahead.startswith('l'):
            match('l')
            parse_X()
        elif lookahead.startswith(';'):
            match(';')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['L', 'l', ';']))
    elif lookahead.startswith('l'):
        match('l')
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('i'):
            match('i')
            match('o')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['i', '']))
    elif lookahead.startswith(';'):
        match(';')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['L', 'l', ';']))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('i'):
        match('i')
        match('o')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['i', '']))

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