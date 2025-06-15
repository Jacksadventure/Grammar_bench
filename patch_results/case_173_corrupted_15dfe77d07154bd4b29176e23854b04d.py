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
    if lookahead.startswith(']'):
        match(']')
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('Q'):
            match('Q')
        elif lookahead.startswith('L'):
            match('L')
            parse_S()
            parse_S()
            match('f')
            match(':')
        elif lookahead.startswith('c'):
            match('c')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['Q', 'L', 'c']))
    elif lookahead.startswith('p'):
        match('p')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith(']'):
            match(']')
            parse_Y()
        elif lookahead.startswith('p'):
            match('p')
            parse_N()
        elif lookahead.startswith('('):
            match('(')
            parse_N()
            parse_S()
            parse_M()
        elif lookahead.startswith('U'):
            match('U')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join([']', 'p', '(', 'U']))
    elif lookahead.startswith('('):
        match('(')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith(']'):
            match(']')
            parse_Y()
        elif lookahead.startswith('p'):
            match('p')
            parse_N()
        elif lookahead.startswith('('):
            match('(')
            parse_N()
            parse_S()
            parse_M()
        elif lookahead.startswith('U'):
            match('U')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join([']', 'p', '(', 'U']))
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('9'):
            match('9')
            parse_M()
            parse_M()
            parse_S()
            match('[')
        elif lookahead.startswith(')'):
            match(')')
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['9', ')']))
        while pos < len(tokens) and tokens[pos].startswith("'"):
            match("'")
            match('C')
            match('t')
            match('d')
            match('v')
    elif lookahead.startswith('U'):
        match('U')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join([']', 'p', '(', 'U']))

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")
        match('C')
        match('t')
        match('d')
        match('v')

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('9'):
        match('9')
        parse_M()
        parse_M()
        parse_S()
        match('[')
    elif lookahead.startswith(')'):
        match(')')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['9', ')']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('Q'):
        match('Q')
    elif lookahead.startswith('L'):
        match('L')
        parse_S()
        parse_S()
        match('f')
        match(':')
    elif lookahead.startswith('c'):
        match('c')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['Q', 'L', 'c']))

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