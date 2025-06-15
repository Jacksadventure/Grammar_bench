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

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('V'):
        match('V')
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith('z'):
            match('z')
            parse_P()
        elif lookahead.startswith('$'):
            match('$')
            match('M')
            parse_K()
            parse_K()
        elif lookahead.startswith('v'):
            match('v')
            parse_J()
            match('s')
        elif lookahead.startswith('H'):
            match('H')
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['z', '$', 'v', 'H']))
        while pos < len(tokens) and tokens[pos].startswith('2'):
            match('2')
            parse_P()
            parse_X()
            match('`')
            parse_K()
        while pos < len(tokens) and tokens[pos].startswith('2'):
            match('2')
            parse_P()
            parse_X()
            match('`')
            parse_K()
    elif lookahead.startswith('Y'):
        match('Y')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['V', 'Y']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('*'):
        match('*')
        match(';')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['*', '']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('z'):
        match('z')
        parse_P()
    elif lookahead.startswith('$'):
        match('$')
        match('M')
        parse_K()
        parse_K()
    elif lookahead.startswith('v'):
        match('v')
        parse_J()
        match('s')
    elif lookahead.startswith('H'):
        match('H')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['z', '$', 'v', 'H']))

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('2'):
        match('2')
        parse_P()
        parse_X()
        match('`')
        parse_K()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_P()
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