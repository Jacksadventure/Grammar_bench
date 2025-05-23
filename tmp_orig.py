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

def parse_a():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('['):
        match('[')
        match('[')

def parse_b():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in b")
    lookahead = tokens[pos]
    if lookahead.startswith('W'):
        parse_c()
        parse_a()
        parse_c()
        match('c')
    elif lookahead.startswith('['):
        parse_c()
        parse_d()
        match('[')
    elif lookahead.startswith('e'):
        match('W')
    elif lookahead.startswith('e'):
        match('e')
    else:
        error("Unexpected token " + lookahead + " in b, expected one of: " + ", ".join(['W', '[', 'e', 'e']))

def parse_c():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('['):
        match('[')
        match('[')
        match('[')
        parse_a()
        match('=')
        match('W')
        parse_b()
        match('e')
        match('e')

def parse_d():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in d")
    lookahead = tokens[pos]
    if lookahead.startswith('='):
        match('=')
    elif lookahead.startswith('e'):
        parse_a()
        match('=')
    elif lookahead.startswith('['):
        parse_d()
        match('e')
    else:
        error("Unexpected token " + lookahead + " in d, expected one of: " + ", ".join(['=', 'e', '[']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_a()
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