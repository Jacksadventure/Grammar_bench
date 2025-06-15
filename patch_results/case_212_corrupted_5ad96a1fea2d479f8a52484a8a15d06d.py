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

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('g'):
        match('g')
        match('R')
        match('6')
        while pos < len(tokens) and tokens[pos].startswith("'"):
            match("'")
    elif lookahead.startswith('|'):
        match('|')
        if pos >= len(tokens):
            error("Unexpected end of input in Q")
        lookahead = tokens[pos]
        if lookahead.startswith('`'):
            match('`')
            match('9')
            match('c')
            parse_X()
        elif lookahead.startswith('n'):
            match('n')
            match('n')
            parse_Q()
        elif lookahead.startswith('N'):
            match('N')
        else:
            error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['`', 'n', 'N']))
        match('*')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('>'):
            match('>')
        elif lookahead.startswith('A'):
            match('A')
            parse_Q()
            parse_Q()
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['>', 'A']))
        match('=')
    elif lookahead.startswith('5'):
        match('5')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['g', '|', '5']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('`'):
        match('`')
        match('9')
        match('c')
        parse_X()
    elif lookahead.startswith('n'):
        match('n')
        match('n')
        parse_Q()
    elif lookahead.startswith('N'):
        match('N')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['`', 'n', 'N']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_X()
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