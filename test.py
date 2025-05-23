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
    if lookahead.startswith('I'):
        parse_b()
        match('b')
    elif lookahead.startswith('I'):
        match('I')
    else:
        error("Unexpected token " + lookahead + " in a, expected one of: " + ", ".join(['I', 'I']))

def parse_b():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in b")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        parse_c()
        match('c')
    elif lookahead.startswith('I'):
        match(']')
    elif lookahead.startswith('7'):
        match('7')
    else:
        error("Unexpected token " + lookahead + " in b, expected one of: " + ", ".join([']', 'I', '7']))

def parse_c():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in c")
    lookahead = tokens[pos]
    if lookahead.startswith('7'):
        parse_c()
        match('c')
    elif lookahead.startswith('7'):
        match('7')
    else:
        error("Unexpected token " + lookahead + " in c, expected one of: " + ", ".join(['7', '7']))

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