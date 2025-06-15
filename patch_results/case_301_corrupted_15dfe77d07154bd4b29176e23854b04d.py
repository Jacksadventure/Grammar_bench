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

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('('):
        match('(')
        match('-')
        match('s')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('w'):
            match('w')
            match('[')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['w', '']))
        match('@')

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('c'):
        match('c')
        match('*')
        parse_Y()

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('A'):
        match('A')
        match('_')

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('{'):
        match('{')
        match('{')

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        match('[')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['w', '']))

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('4'):
        match('4')
        parse_I()
        match('t')
        parse_I()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_C()
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