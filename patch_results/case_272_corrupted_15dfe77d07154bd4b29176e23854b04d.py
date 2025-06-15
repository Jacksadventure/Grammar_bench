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

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('Y'):
        match('Y')
        match('N')
        match('Q')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('Y'):
            match('Y')
            match('N')
            match('Q')
            parse_T()
        elif lookahead.startswith('c'):
            match('c')
            parse_B()
            match('7')
        elif lookahead.startswith('z'):
            match('z')
            parse_V()
            parse_C()
            match('N')
            match('3')
        elif lookahead.startswith('{'):
            match('{')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['Y', 'c', 'z', '{']))
    elif lookahead.startswith('c'):
        match('c')
        while pos < len(tokens) and tokens[pos].startswith('y'):
            match('y')
            match('$')
            parse_B()
        match('7')
    elif lookahead.startswith('z'):
        match('z')
        while pos < len(tokens) and tokens[pos].startswith('O'):
            match('O')
            match(':')
        while pos < len(tokens) and tokens[pos].startswith('y'):
            match('y')
            match('W')
            parse_F()
        match('N')
        match('3')
    elif lookahead.startswith('{'):
        match('{')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['Y', 'c', 'z', '{']))

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('y'):
        match('y')
        match('$')
        parse_B()

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('y'):
        match('y')
        match(',')

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('O'):
        match('O')
        match(':')

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('y'):
        match('y')
        match('W')
        parse_F()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_T()
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