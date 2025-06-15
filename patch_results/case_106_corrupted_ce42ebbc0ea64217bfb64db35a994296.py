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

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('u'):
        match('u')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('j'):
            match('j')
            parse_Y()
            parse_S()
        elif lookahead.startswith('*'):
            match('*')
            match('$')
            parse_Y()
            parse_Y()
        elif lookahead.startswith('-'):
            match('-')
        elif lookahead.startswith('t'):
            match('t')
            parse_G()
            parse_S()
            parse_Y()
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['j', '*', '-', 't']))
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('j'):
            match('j')
            parse_Y()
            parse_S()
        elif lookahead.startswith('*'):
            match('*')
            match('$')
            parse_Y()
            parse_Y()
        elif lookahead.startswith('-'):
            match('-')
        elif lookahead.startswith('t'):
            match('t')
            parse_G()
            parse_S()
            parse_Y()
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['j', '*', '-', 't']))
        match('#')

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        parse_S()
        match('T')
        parse_Y()
        parse_R()
    elif lookahead.startswith('^'):
        match('^')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join([',', '^']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
        parse_Y()
        parse_S()
    elif lookahead.startswith('*'):
        match('*')
        match('$')
        parse_Y()
        parse_Y()
    elif lookahead.startswith('-'):
        match('-')
    elif lookahead.startswith('t'):
        match('t')
        parse_G()
        parse_S()
        parse_Y()
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['j', '*', '-', 't']))

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(';'):
        match(';')
        match('p')
        match('z')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_S()
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