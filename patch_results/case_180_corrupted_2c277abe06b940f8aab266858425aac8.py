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
    if lookahead.startswith('m'):
        match('m')
        while pos < len(tokens) and tokens[pos].startswith('7'):
            match('7')
            match('e')
            match('<')
            match('7')
        while pos < len(tokens) and tokens[pos].startswith('r'):
            match('r')
            match('S')
            match('4')
    elif lookahead.startswith('I'):
        match('I')
        while pos < len(tokens) and tokens[pos].startswith('7'):
            match('7')
            match('e')
            match('<')
            match('7')
        match('^')
        match('#')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('m'):
            match('m')
            parse_Z()
            parse_G()
        elif lookahead.startswith('I'):
            match('I')
            parse_Z()
            match('^')
            match('#')
            parse_R()
        elif lookahead.startswith('7'):
            match('7')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['m', 'I', '7']))
    elif lookahead.startswith('7'):
        match('7')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['m', 'I', '7']))

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('r'):
        match('r')
        match('S')
        match('4')

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('7'):
        match('7')
        match('e')
        match('<')
        match('7')

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