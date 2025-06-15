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

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('l'):
        match('l')
        while pos < len(tokens) and tokens[pos].startswith(']'):
            match(']')
            match('F')
            match('(')
        match('.')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('l'):
            match('l')
            parse_J()
            match('.')
            parse_B()
            parse_J()
        elif lookahead.startswith('7'):
            match('7')
            parse_B()
        elif lookahead.startswith('z'):
            match('z')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['l', '7', 'z']))
        while pos < len(tokens) and tokens[pos].startswith(']'):
            match(']')
            match('F')
            match('(')
    elif lookahead.startswith('7'):
        match('7')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('l'):
            match('l')
            parse_J()
            match('.')
            parse_B()
            parse_J()
        elif lookahead.startswith('7'):
            match('7')
            parse_B()
        elif lookahead.startswith('z'):
            match('z')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['l', '7', 'z']))
    elif lookahead.startswith('z'):
        match('z')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['l', '7', 'z']))

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(']'):
        match(']')
        match('F')
        match('(')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_B()
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