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

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('X'):
        match('X')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('X'):
            match('X')
            parse_J()
        elif lookahead.startswith('$'):
            match('$')
            parse_A()
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['X', '$']))
    elif lookahead.startswith('$'):
        match('$')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('X'):
            match('X')
            parse_A()
            match('p')
            parse_A()
            match('&')
        elif lookahead.startswith('5'):
            match('5')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['X', '5']))
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['X', '$']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('X'):
        match('X')
        parse_A()
        match('p')
        parse_A()
        match('&')
    elif lookahead.startswith('5'):
        match('5')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['X', '5']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_J()
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