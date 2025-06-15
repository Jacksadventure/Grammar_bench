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
    while pos < len(tokens) and tokens[pos].startswith('5'):
        match('5')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('y'):
            match('y')
            parse_L()
            parse_L()
            parse_U()
            parse_L()
            parse_U()
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['y', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith('O'):
            match('O')
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['O']))
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('y'):
            match('y')
            parse_L()
            parse_L()
            parse_U()
            parse_L()
            parse_U()
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['y', '']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('O'):
        match('O')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['O']))

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('y'):
        match('y')
        parse_L()
        parse_L()
        parse_U()
        parse_L()

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