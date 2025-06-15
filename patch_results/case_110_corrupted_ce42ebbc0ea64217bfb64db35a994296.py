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
    while pos < len(tokens) and tokens[pos].startswith('+'):
        match('+')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith(']'):
            match(']')
            parse_R()
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join([']', '']))
        match("'")

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('~'):
        match('~')
        match('5')
        parse_I()
        match('w')
        match('9')
    elif lookahead.startswith(','):
        match(',')
        parse_P()
        match('V')
    elif lookahead.startswith('|'):
        match('|')
    elif lookahead.startswith('_'):
        match('_')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['~', ',', '|', '_']))

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(']'):
        match(']')

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('_'):
        match('_')

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Z'):
        match('Z')
        parse_R()
        parse_P()
        match('b')
        parse_H()

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