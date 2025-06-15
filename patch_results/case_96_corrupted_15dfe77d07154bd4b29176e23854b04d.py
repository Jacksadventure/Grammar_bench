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
    while pos < len(tokens) and tokens[pos].startswith('A'):
        match('A')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('A'):
            match('A')
            parse_G()
            parse_Q()
            parse_G()
        elif lookahead.startswith('/'):
            match('/')
            parse_Z()
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['A', '', '/']))
        if pos >= len(tokens):
            error("Unexpected end of input in Q")
        lookahead = tokens[pos]
        if lookahead.startswith('>'):
            match('>')
            parse_Q()
        elif lookahead.startswith('/'):
            match('/')
            parse_B()
            parse_V()
        else:
            error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['>', '', '/']))

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('o'):
        match('o')
        parse_V()
        parse_G()
        match('~')
        match('A')

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('>'):
        match('>')

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('G'):
        parse_G()
        parse_G()

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(';'):
        match(';')
        match(';')
        match('D')
        match('F')
        match('e')

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