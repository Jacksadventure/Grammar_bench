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
    if lookahead.startswith('c'):
        match('c')
        match('*')
        match(':')
        match('r')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('a'):
            match('a')
            parse_S()
            parse_O()
            parse_O()
            parse_B()
        elif lookahead.startswith('<'):
            match('<')
            match('X')
            match('Y')
            match('M')
            parse_S()
        elif lookahead.startswith('H'):
            match('H')
            match('{')
        elif lookahead.startswith('K'):
            match('K')
            parse_B()
            match('=')
        elif lookahead.startswith('u'):
            match('u')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['a', '<', 'H', 'K', 'u']))
    elif lookahead.startswith('3'):
        match('3')
        match('`')
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith('o'):
            match('o')
            match('Y')
            match('?')
            parse_O()
            match('{')
        elif lookahead.startswith('e'):
            match('e')
            match('t')
            parse_D()
            match('_')
            parse_O()
        elif lookahead.startswith('h'):
            match('h')
        else:
            error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['o', 'e', 'h']))
    elif lookahead.startswith('`'):
        match('`')
        match('0')
    elif lookahead.startswith('A'):
        match('A')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['c', '3', '`', 'A']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        match('Y')
        match('?')
        parse_O()
        match('{')
    elif lookahead.startswith('e'):
        match('e')
        match('t')
        parse_D()
        match('_')
        parse_O()
    elif lookahead.startswith('h'):
        match('h')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['o', 'e', 'h']))

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('X'):
        match('X')
        parse_O()
        match('Y')
        parse_P()
        match('V')

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('o'):
        match('o')
        parse_S()

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('a'):
        match('a')
        parse_S()
        parse_O()
        parse_O()
        parse_B()
    elif lookahead.startswith('<'):
        match('<')
        match('X')
        match('Y')
        match('M')
        parse_S()
    elif lookahead.startswith('H'):
        match('H')
        match('{')
    elif lookahead.startswith('K'):
        match('K')
        parse_B()
        match('=')
    elif lookahead.startswith('u'):
        match('u')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['a', '<', 'H', 'K', 'u']))

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('P'):
        parse_P()
        match('F')
        parse_O()

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