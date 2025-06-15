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

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('u'):
        match('u')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('Z'):
            match('Z')
            match('9')
            parse_R()
        elif lookahead.startswith('|'):
            match('|')
            parse_W()
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['Z', '', '|']))
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('u'):
            match('u')
            parse_R()
            parse_Y()
            parse_Y()
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['u', '']))

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Z'):
        match('Z')
        match('9')

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('f'):
        match('f')
        match('l')
        match('<')
        match('_')
        match('Z')
    elif lookahead.startswith(')'):
        match(')')
        match('q')
        match('_')
    elif lookahead.startswith('O'):
        match('O')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['f', ')', 'O']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Y()
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