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

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        match('z')
        match('N')
        while pos < len(tokens) and tokens[pos].startswith('V'):
            match('V')
            parse_Y()
        match('?')
    elif lookahead.startswith('j'):
        match('j')
        match('I')
        match('!')
        match("'")
        match('p')
    elif lookahead.startswith('l'):
        match('l')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['w', 'j', 'l']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('G'):
        match('G')
    elif lookahead.startswith('$'):
        match('$')
        match('v')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['G', '$']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_D()
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