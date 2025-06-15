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

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('l'):
        match('l')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('5'):
            match('5')
            parse_G()
        elif lookahead.startswith('O'):
            match('O')
            parse_B()
            parse_U()
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['5', '', 'O']))

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('5'):
        match('5')

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('1'):
        match('1')
        match('4')
        match('$')
        match('y')
        parse_L()

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(')'):
        match(')')
        match('C')
        match(',')

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('0'):
        match('0')
        match('q')
        match('T')
        match('r')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_E()
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