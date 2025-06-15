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

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('R'):
        match('R')
        while pos < len(tokens) and tokens[pos].startswith('t'):
            match('t')
            match('C')
            parse_M()
            match('H')
            parse_V()
        match('N')
        while pos < len(tokens) and tokens[pos].startswith('h'):
            match('h')
            parse_B()
            parse_A()
            match('q')
    elif lookahead.startswith('w'):
        match('w')
        while pos < len(tokens) and tokens[pos].startswith('8'):
            match('8')
            parse_M()
    elif lookahead.startswith('N'):
        match('N')
        while pos < len(tokens) and tokens[pos].startswith('&'):
            match('&')
    elif lookahead.startswith('X'):
        match('X')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['R', 'w', 'N', 'X']))

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('&'):
        match('&')

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('t'):
        match('t')
        match('C')
        parse_M()
        match('H')
        parse_V()

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('8'):
        match('8')
        parse_M()

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")
        parse_M()
        parse_M()

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('L'):
        match('L')
        match('L')
        parse_K()
        match('S')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_K()
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