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

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        match('A')
        while pos < len(tokens) and tokens[pos].startswith('B'):
            match('B')
            parse_R()
            parse_W()
            parse_J()
            parse_V()
    elif lookahead.startswith('{'):
        match('{')
    elif lookahead.startswith('O'):
        match('O')
        match('s')
        match('@')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join([',', '{', 'O']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('-'):
        match('-')
        parse_W()
        parse_W()
        match('(')
    elif lookahead.startswith('u'):
        match('u')
        match('q')
        match('N')
        parse_V()
    elif lookahead.startswith('_'):
        match('_')
        match('p')
    elif lookahead.startswith('+'):
        match('+')
    elif lookahead.startswith("'"):
        match("'")
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['-', 'u', '_', '+', "'"]))

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('+'):
        match('+')
        match('Y')
        parse_J()
        match('5')
        parse_H()

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['+']))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('B'):
        match('B')
        parse_R()
        parse_W()
        parse_J()
        parse_V()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_W()
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