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
    if lookahead.startswith('4'):
        match('4')
        match('w')
        while pos < len(tokens) and tokens[pos].startswith('Q'):
            match('Q')
            parse_R()
            parse_G()
            parse_G()
        while pos < len(tokens) and tokens[pos].startswith('v'):
            match('v')
            parse_R()
            parse_R()
    elif lookahead.startswith(')'):
        match(')')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['4', ')']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")
        parse_W()
        parse_H()
        parse_L()

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Q'):
        match('Q')
        parse_R()
        parse_G()
        parse_G()

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('v'):
        match('v')
        parse_R()
        parse_R()

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('D'):
        match('D')
        parse_G()
        match('9')
        parse_L()

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('/'):
        match('/')
        parse_U()
        parse_L()
        parse_X()

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('d'):
        match('d')
        match("'")
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['d', '']))

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