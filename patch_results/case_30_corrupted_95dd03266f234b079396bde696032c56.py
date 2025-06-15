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

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('t'):
        match('t')
        while pos < len(tokens) and tokens[pos].startswith("'"):
            match("'")
            match('f')
        while pos < len(tokens) and tokens[pos].startswith("'"):
            match("'")
            match('f')
        match('r')
        match('s')
    elif lookahead.startswith('@'):
        match('@')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('t'):
            match('t')
            parse_W()
            parse_W()
            match('r')
            match('s')
        elif lookahead.startswith('@'):
            match('@')
            parse_R()
            parse_W()
            match('t')
        elif lookahead.startswith('G'):
            match('G')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['t', '@', 'G']))
        while pos < len(tokens) and tokens[pos].startswith("'"):
            match("'")
            match('f')
        match('t')
    elif lookahead.startswith('G'):
        match('G')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['t', '@', 'G']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")
        match('f')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_R()
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