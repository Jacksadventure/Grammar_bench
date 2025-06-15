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

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('S'):
        match('S')
        match('6')
        while pos < len(tokens) and tokens[pos].startswith('2'):
            match('2')
            parse_N()
            match('F')
    elif lookahead.startswith('('):
        match('(')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['S', '(']))

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('D'):
        match('D')
        match(']')
        match('K')
        parse_U()
        match('}')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_U()
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