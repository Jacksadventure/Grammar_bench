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
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith("'"):
            match("'")
            parse_P()
            match('>')
            parse_G()
            parse_C()
            parse_P()
        else:
            error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(["'", '']))
        match('>')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('U'):
            match('U')
            parse_F()
            parse_G()
            parse_G()
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['U', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in C")
        lookahead = tokens[pos]
        if lookahead.startswith('/'):
            match('/')
            parse_Q()
        elif lookahead.startswith('I'):
            match('I')
            match('p')
        elif lookahead.startswith('W'):
            match('W')
        elif lookahead.startswith('g'):
            match('g')
            parse_K()
            parse_G()
            parse_V()
            parse_Q()
        elif lookahead.startswith('t'):
            match('t')
            parse_Q()
            parse_V()
            match('8')
        else:
            error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['/', 'I', 'W', 'g', 't']))

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Y'):
        match('Y')
        parse_F()
        match('R')

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        match("'")
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['/', '']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('?'):
        match('?')
        parse_K()
        parse_G()
        parse_F()
        parse_C()

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('<'):
        match('<')
        parse_P()
        parse_Q()
    elif lookahead.startswith('r'):
        match('r')
        parse_G()
        parse_K()
    elif lookahead.startswith('J'):
        match('J')
    elif lookahead.startswith(')'):
        match(')')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['<', 'r', 'J', ')']))

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('U'):
        match('U')
        parse_F()
        parse_G()

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        parse_Q()
    elif lookahead.startswith('I'):
        match('I')
        match('p')
    elif lookahead.startswith('W'):
        match('W')
    elif lookahead.startswith('g'):
        match('g')
        parse_K()
        parse_G()
        parse_V()
        parse_Q()
    elif lookahead.startswith('t'):
        match('t')
        parse_Q()
        parse_V()
        match('8')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['/', 'I', 'W', 'g', 't']))

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