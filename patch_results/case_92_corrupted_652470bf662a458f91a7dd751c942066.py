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

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('*'):
        match('*')
        match('k')
        match('/')
        if pos >= len(tokens):
            error("Unexpected end of input in C")
        lookahead = tokens[pos]
        if lookahead.startswith('d'):
            match('d')
            parse_G()
            parse_Z()
        elif lookahead.startswith('v'):
            match('v')
            parse_T()
            match('f')
            match('^')
            parse_N()
        elif lookahead.startswith('2'):
            match('2')
        else:
            error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['d', 'v', '2']))
    elif lookahead.startswith('1'):
        match('1')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['*', '1']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('a'):
        match('a')
        match('j')
    elif lookahead.startswith('e'):
        match('e')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['a', 'e']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('d'):
        match('d')
        parse_G()
        parse_Z()
    elif lookahead.startswith('v'):
        match('v')
        parse_T()
        match('f')
        match('^')
        parse_N()
    elif lookahead.startswith('2'):
        match('2')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['d', 'v', '2']))

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('V'):
        match('V')
        parse_T()
        parse_C()
        parse_G()
    elif lookahead.startswith('s'):
        match('s')
        match('7')
        parse_Z()
        match('5')
        match('$')
    elif lookahead.startswith('$'):
        match('$')
    elif lookahead.startswith('['):
        match('[')
        parse_C()
        match('>')
        parse_G()
    elif lookahead.startswith('f'):
        match('f')
        parse_G()
        parse_N()
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['V', 's', '$', '[', 'f']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('u'):
        match('u')
    elif lookahead.startswith('E'):
        match('E')
        match('I')
        match('r')
        parse_G()
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['u', 'E']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_N()
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