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

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('6'):
        match('6')
        while pos < len(tokens) and tokens[pos].startswith('d'):
            match('d')
            parse_S()
            match('(')
            parse_W()
            match("'")
    elif lookahead.startswith('5'):
        match('5')
        while pos < len(tokens) and tokens[pos].startswith('^'):
            match('^')
            parse_W()
            match('*')
        while pos < len(tokens) and tokens[pos].startswith('F'):
            match('F')
            match('u')
            match('/')
            match('o')
        match('+')
    elif lookahead.startswith('I'):
        match('I')
        match(',')
    elif lookahead.startswith('h'):
        match('h')
        match('=')
    elif lookahead.startswith('s'):
        match('s')
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('#'):
            match('#')
            match('8')
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['#', '']))
        match('B')
        match('r')
    elif lookahead.startswith('e'):
        match('e')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['6', '5', 'I', 'h', 's', 'e']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('#'):
        match('#')
        match('8')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['#', '']))

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('d'):
        match('d')
        parse_S()
        match('(')
        parse_W()
        match("'")

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('g'):
        match('g')

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('d'):
        match('d')
        parse_S()
        match("'")
        parse_O()
        match('U')

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('F'):
        match('F')
        match('u')
        match('/')
        match('o')

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('^'):
        match('^')
        parse_W()
        match('*')

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('X'):
        match('X')
        match('_')
        match('8')
        match('z')
    elif lookahead.startswith('x'):
        match('x')
        parse_W()
        parse_E()
        parse_W()
    elif lookahead.startswith('#'):
        match('#')
    elif lookahead.startswith('T'):
        parse_T()
        parse_K()
    elif lookahead.startswith('c'):
        match('c')
        parse_P()
        parse_M()
        match('v')
        match('A')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['X', 'x', '#', 'T', 'c']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_K()
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