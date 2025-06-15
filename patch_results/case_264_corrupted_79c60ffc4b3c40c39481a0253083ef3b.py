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

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('0'):
        match('0')
        match('+')
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith('8'):
            match('8')
            parse_W()
            parse_H()
            parse_W()
            parse_H()
            parse_W()
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['8', '']))
        match("'")

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        match(']')
        match('f')
    elif lookahead.startswith('<'):
        match('<')
        match("'")
    elif lookahead.startswith('v'):
        match('v')
        parse_H()
    elif lookahead.startswith(')'):
        match(')')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join([']', '<', 'v', ')']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('8'):
        match('8')
        parse_W()
        parse_H()
        parse_W()
        parse_H()

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('S'):
        match('S')
        parse_T()
        match('@')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Y()
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