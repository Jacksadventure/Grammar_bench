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

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('/'):
        match('/')
        match('1')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('/'):
            match('/')
            match('1')
            parse_V()
            parse_V()
        elif lookahead.startswith('v'):
            match('v')
            parse_Z()
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['/', '', 'v']))

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('7'):
        match('7')
        parse_J()
        parse_V()
        parse_V()

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('5'):
        match('5')
        parse_V()
        parse_C()

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('9'):
        match('9')
        match('2')
        parse_C()
        match('}')
    elif lookahead.startswith('B'):
        match('B')
        parse_C()
        parse_C()
        parse_V()
        parse_Z()
    elif lookahead.startswith('z'):
        match('z')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['9', 'B', 'z']))

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('d'):
        match('d')
        parse_C()
        parse_C()
        parse_J()
        parse_J()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_V()
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