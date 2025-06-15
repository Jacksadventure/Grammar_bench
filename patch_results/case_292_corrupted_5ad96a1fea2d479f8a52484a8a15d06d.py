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
    while pos < len(tokens) and tokens[pos].startswith('A'):
        match('A')
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('^'):
            match('^')
            parse_F()
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['^', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('?'):
            match('?')
            parse_F()
            parse_N()
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['?', '']))
        match(':')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('t'):
            match('t')
            parse_C()
            parse_N()
            parse_G()
        elif lookahead.startswith('4'):
            match('4')
            parse_H()
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['t', '', '4']))

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('^'):
        match('^')

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('?'):
        match('?')
        parse_F()

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('@'):
        match('@')
        parse_F()
    elif lookahead.startswith('I'):
        match('I')
        parse_N()
        parse_F()
    elif lookahead.startswith('~'):
        match('~')
        parse_G()
        parse_N()
    elif lookahead.startswith('J'):
        match('J')
        parse_G()
        parse_F()
    elif lookahead.startswith('w'):
        match('w')
        match('J')
        parse_H()
        match('s')
    elif lookahead.startswith('7'):
        match('7')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['@', 'I', '~', 'J', 'w', '7']))

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('t'):
        match('t')
        parse_C()
        parse_N()

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