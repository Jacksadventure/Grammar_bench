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

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('u'):
        match('u')
        match('9')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('V'):
            match('V')
            parse_G()
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['V', '']))
        match('c')

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('M'):
        match('M')
        parse_H()
        match('3')
        parse_U()

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('V'):
        match('V')
        parse_I()
        match('a')

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('m'):
        match('m')
        match('c')
        parse_I()
        match('r')

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('V'):
        match('V')

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('$'):
        match('$')
        parse_U()
        parse_L()

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
    elif lookahead.startswith('d'):
        match('d')
    elif lookahead.startswith('l'):
        match('l')
        parse_G()
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(["'", 'd', 'l']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_P()
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