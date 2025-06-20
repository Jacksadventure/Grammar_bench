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

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('G'):
        match('G')
        match('>')
        match('A')
        match('a')

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('v'):
        match('v')
        match('<')
    else:
        Parse failed

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('9'):
        match('9')

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('i'):
        match('i')
        parse_Z()
        match('l')
        parse_K()
        match('I')

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('5'):
        match('5')
        match('|')
        match('d')
        match(';')
        match('z')

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('r'):
        match('r')
        parse_B()
        match('&')
        match('f')

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(':'):
        match(':')
        match(']')
        match('<')
        match(',')

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('~'):
        match('~')

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('h'):
        match('h')
        match('$')
        parse_Y()
        match(',')
        match('z')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_M()
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