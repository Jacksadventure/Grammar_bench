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
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('T'):
        match('T')
        while pos < len(tokens) and tokens[pos].startswith('('):
            match('(')
            match("'")
            match('z')
        while pos < len(tokens) and tokens[pos].startswith('0'):
            match('0')
            match('K')
            parse_O()
            parse_N()
            parse_W()
    elif lookahead.startswith('o'):
        match('o')
    elif lookahead.startswith('?'):
        match('?')
        match('~')
    elif lookahead.startswith('<'):
        match('<')
        match('5')
    elif lookahead.startswith(';'):
        match(';')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['T', 'o', '?', '<', ';']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('F'):
        match('F')
        parse_B()
        match('o')

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('n'):
        match('n')
        match('J')
        parse_B()

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('='):
        match('=')
        match('7')
        match('x')
        match('D')
        parse_B()
    elif lookahead.startswith('b'):
        match('b')
        parse_Z()
    elif lookahead.startswith('e'):
        match('e')
        match('%')
        match('e')
        match('|')
        parse_O()
    elif lookahead.startswith('f'):
        match('f')
        match("'")
        parse_O()
        parse_B()
        match('m')
    elif lookahead.startswith(','):
        match(',')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['=', 'b', 'e', 'f', ',']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('q'):
        match('q')
        match('@')
        match('q')
        match('t')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['q', '']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('L'):
        match('L')
    elif lookahead.startswith('n'):
        match('n')
        match('t')
        parse_W()
        parse_U()
    elif lookahead.startswith('^'):
        match('^')
        match('^')
        parse_Y()
        parse_Q()
    elif lookahead.startswith('u'):
        match('u')
        match('i')
        match('<')
        match('r')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['L', 'n', '^', 'u']))

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")
        parse_O()
        parse_O()
        match(':')

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('0'):
        match('0')
        match('K')
        parse_O()
        parse_N()
        parse_W()

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('('):
        match('(')
        match("'")
        match('z')

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