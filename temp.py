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
    if pos >= len(tokens):
        error("Unexpected end of input in a")
    lookahead = tokens[pos]
    if lookahead.startswith('W'):
        match('W')
        parse_c()
        parse_b()
    elif lookahead.startswith('W'):
        match('W')
    else:
        error("Unexpected token " + lookahead + " in a, expected one of: " + ", ".join(['W', 'W']))

def parse_b():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('}'):
        match('}')
        match('}')
        match('3')
        match('3')
        match('3')
        match('3')

def parse_c():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in c")
    lookahead = tokens[pos]
    if lookahead.startswith('W'):
        match('W')
    elif lookahead.startswith('3'):
        match('3')
        match('3')
    else:
        error("Unexpected token " + lookahead + " in c, expected one of: " + ", ".join(['W', '3']))

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