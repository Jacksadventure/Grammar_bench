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

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('L'):
        while pos < len(tokens) and tokens[pos].startswith('p'):
            match('p')
            match('$')
        while pos < len(tokens) and tokens[pos].startswith(')'):
            match(')')
    elif lookahead.startswith('4'):
        match('4')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('D'):
            parse_D()
        elif lookahead.startswith('>'):
            match('>')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['D', '>']))
    elif lookahead.startswith('s'):
        match('s')
        match(',')
        while pos < len(tokens) and tokens[pos].startswith('p'):
            match('p')
            match('$')
    elif lookahead.startswith('<'):
        match('<')
        while pos < len(tokens) and tokens[pos].startswith('d'):
            match('d')
            match('Q')
            parse_N()
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('L'):
            parse_L()
            parse_M()
        elif lookahead.startswith('4'):
            match('4')
            parse_H()
        elif lookahead.startswith('s'):
            match('s')
            match(',')
            parse_L()
        elif lookahead.startswith('<'):
            match('<')
            parse_D()
            parse_X()
            match('v')
        elif lookahead.startswith('D'):
            parse_D()
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['L', '4', 's', '<', 'D']))
        match('v')
    elif lookahead.startswith('D'):
        while pos < len(tokens) and tokens[pos].startswith('d'):
            match('d')
            match('Q')
            parse_N()
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['L', '4', 's', '<', 'D']))

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('d'):
        match('d')
        match('Q')
        parse_N()

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('@'):
        match('@')
    elif lookahead.startswith('2'):
        match('2')
    elif lookahead.startswith('a'):
        match('a')
        parse_D()
        match('9')
        parse_D()
        match('n')
    elif lookahead.startswith('A'):
        match('A')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['@', '2', 'a', 'A']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('D'):
        parse_D()
    elif lookahead.startswith('>'):
        match('>')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['D', '>']))

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(')'):
        match(')')

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('p'):
        match('p')
        match('$')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_X()
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