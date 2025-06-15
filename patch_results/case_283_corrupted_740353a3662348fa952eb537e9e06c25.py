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
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('0'):
        match('0')
        if pos >= len(tokens):
            error("Unexpected end of input in C")
        lookahead = tokens[pos]
        if lookahead.startswith('a'):
            match('a')
            parse_J()
            parse_Y()
        elif lookahead.startswith('-'):
            match('-')
            match('w')
            parse_Y()
        elif lookahead.startswith('h'):
            match('h')
        else:
            error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['a', '-', 'h']))
        match("'")
        if pos >= len(tokens):
            error("Unexpected end of input in C")
        lookahead = tokens[pos]
        if lookahead.startswith('a'):
            match('a')
            parse_J()
            parse_Y()
        elif lookahead.startswith('-'):
            match('-')
            match('w')
            parse_Y()
        elif lookahead.startswith('h'):
            match('h')
        else:
            error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['a', '-', 'h']))
        while pos < len(tokens) and tokens[pos].startswith(','):
            match(',')
            match('7')
            match('F')
            match('d')
    elif lookahead.startswith('q'):
        match('q')
        while pos < len(tokens) and tokens[pos].startswith('y'):
            match('y')
            match('.')
    elif lookahead.startswith('d'):
        match('d')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('0'):
            match('0')
            parse_C()
            match("'")
            parse_C()
            parse_O()
        elif lookahead.startswith('q'):
            match('q')
            parse_S()
        elif lookahead.startswith('d'):
            match('d')
            parse_G()
            match('l')
        elif lookahead.startswith('p'):
            match('p')
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['0', 'q', 'd', 'p']))
        match('l')
    elif lookahead.startswith('p'):
        match('p')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['0', 'q', 'd', 'p']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('z'):
        match('z')
        parse_U()
        parse_S()
        parse_S()
    elif lookahead.startswith('G'):
        parse_G()
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['z', 'G']))

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('$'):
        match('$')

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(';'):
        match(';')
        match('K')
        parse_U()
        match('m')
        match('p')

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('y'):
        match('y')
        match('.')

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('a'):
        match('a')
        parse_J()
        parse_Y()
    elif lookahead.startswith('-'):
        match('-')
        match('w')
        parse_Y()
    elif lookahead.startswith('h'):
        match('h')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['a', '-', 'h']))

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(','):
        match(',')
        match('7')
        match('F')
        match('d')

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