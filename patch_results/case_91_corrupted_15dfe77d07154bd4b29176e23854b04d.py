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

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
    elif lookahead.startswith('i'):
        match('i')
        match(',')
        match('`')
        match('_')
        match('l')
    elif lookahead.startswith('k'):
        match('k')
        while pos < len(tokens) and tokens[pos].startswith(']'):
            match(']')
            match('s')
            match('&')
        while pos < len(tokens) and tokens[pos].startswith(')'):
            match(')')
            match('(')
            match('@')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['?', 'i', 'k']))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(')'):
        match(')')
        match('(')
        match('@')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_B()
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