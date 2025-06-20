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
    while pos < len(tokens) and tokens[pos].startswith('h'):
        match('h')

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('6'):
        match('6')
        match(':')
        parse_U()
        match('=')

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('}'):
        match('}')
        parse_F()
        parse_U()

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('Y'):
        parse_Y()
        parse_U()
        match('{')
        match('W')
    else:
        Parse failed

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('<'):
        match('<')
        match('g')
        match('S')

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('3'):
        match('3')
        parse_Y()
        parse_Z()
        match('v')
        match('0')

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('+'):
        match('+')
        match('*')
        match(':')
        parse_Z()
        parse_Z()

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('2'):
        match('2')
        parse_F()
        parse_M()
        parse_U()
        parse_J()

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