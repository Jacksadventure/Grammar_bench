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
    if lookahead.startswith(')'):
        match(')')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith(')'):
            match(')')
            parse_N()
        elif lookahead.startswith('A'):
            match('A')
            parse_J()
        elif lookahead.startswith(':'):
            match(':')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join([')', 'A', ':']))
    elif lookahead.startswith('A'):
        match('A')
        while pos < len(tokens) and tokens[pos].startswith('5'):
            match('5')
            parse_J()
            parse_N()
            match('P')
            match('A')
    elif lookahead.startswith(':'):
        match(':')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join([')', 'A', ':']))

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('5'):
        match('5')
        parse_J()
        parse_N()
        match('P')
        match('A')

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