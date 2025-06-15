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
    while pos < len(tokens) and tokens[pos].startswith('-'):
        match('-')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('M'):
            match('M')
            match('b')
            match('o')
            parse_R()
        elif lookahead.startswith('v'):
            match('v')
            parse_K()
            parse_Q()
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['M', '', 'v']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('%'):
        match('%')
        match('3')
    elif lookahead.startswith(')'):
        match(')')
        parse_Q()
    elif lookahead.startswith('i'):
        match('i')
        parse_I()
        parse_R()
        parse_K()
    elif lookahead.startswith('a'):
        match('a')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['%', ')', 'i', 'a']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('j'):
        match('j')
        match('f')
        match('L')
        parse_K()

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('M'):
        match('M')
        match('b')
        match('o')

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('?'):
        match('?')
        parse_C()
        match(']')

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