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

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('-'):
        match('-')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('-'):
            match('-')
            parse_I()
        elif lookahead.startswith('O'):
            match('O')
            parse_D()
        elif lookahead.startswith('O'):
            match('O')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['-', 'O', 'O']))
    elif lookahead.startswith('O'):
        match('O')
        while pos < len(tokens) and tokens[pos].startswith('S'):
            match('S')
            match('4')
            match('x')
    elif lookahead.startswith('O'):
        match('O')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['-', 'O', 'O']))

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('S'):
        match('S')
        match('4')
        match('x')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_I()
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