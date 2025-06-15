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
    while pos < len(tokens) and tokens[pos].startswith('$'):
        match('$')
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('O'):
            match('O')
            parse_B()
            parse_D()
        elif lookahead.startswith('0'):
            match('0')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['O', '0']))
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('O'):
            match('O')
            parse_B()
            parse_D()
        elif lookahead.startswith('0'):
            match('0')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['O', '0']))
        match('(')

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('*'):
        match('*')
        match('A')
        match('1')
        parse_B()
        parse_I()
    elif lookahead.startswith('a'):
        match('a')
    elif lookahead.startswith('G'):
        match('G')
        match('=')
        parse_D()
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['*', 'a', 'G']))

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('!'):
        match('!')
        match('H')

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