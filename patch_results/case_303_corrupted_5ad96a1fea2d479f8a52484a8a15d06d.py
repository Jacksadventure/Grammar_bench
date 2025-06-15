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

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('v'):
        match('v')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('u'):
            match('u')
            parse_B()
        elif lookahead.startswith('k'):
            match('k')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['u', 'k']))

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('/'):
        match('/')
        parse_N()

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('f'):
        match('f')
        match('z')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['f', '']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_G()
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