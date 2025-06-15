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

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('e'):
        match('e')
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith('s'):
            match('s')
            match('P')
            parse_K()
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['s', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('W'):
            match('W')
            match('c')
            parse_K()
            match('w')
            parse_V()
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['W', '']))
        match(';')

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('W'):
        match('W')
        match('c')
        parse_K()
        match('w')

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('s'):
        match('s')
        match('P')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Q()
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