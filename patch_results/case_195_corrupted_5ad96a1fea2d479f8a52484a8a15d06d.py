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

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('{'):
        match('{')
        match('1')
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith('q'):
            match('q')
            match("'")
            match('|')
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['q', '']))
        match('R')

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('q'):
        match('q')
        match("'")
        match('|')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['q', '']))

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('f'):
        match('f')
        match('|')
        match('d')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_G()
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