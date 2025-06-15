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

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('.'):
        match('.')
        match('7')
        match('>')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('G'):
            match('G')
            parse_J()
            match('#')
            match('z')
            match('e')
            parse_J()
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['G', '']))

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('H'):
        match('H')
        match('o')
        match('c')
        match('K')

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('G'):
        match('G')
        parse_J()
        match('#')
        match('z')
        match('e')

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('m'):
        match('m')
        match('{')
        parse_J()

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('D'):
        parse_D()
        parse_D()
        match('L')
        match('c')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_P()
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