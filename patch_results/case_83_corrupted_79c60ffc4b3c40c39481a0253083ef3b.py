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
    while pos < len(tokens) and tokens[pos].startswith('G'):
        match('G')
        match('d')
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('~'):
            match('~')
            match('F')
        else:
            error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['~', '']))
        match('T')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('D'):
            match('D')
            parse_Z()
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['D', '']))

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('D'):
        match('D')

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