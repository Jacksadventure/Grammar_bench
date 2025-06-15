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
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('k'):
        match('k')
        match('c')
        match("'")
    elif lookahead.startswith('<'):
        match('<')
        match("'")
        match('e')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith(','):
            match(',')
            parse_Q()
        elif lookahead.startswith('w'):
            match('w')
            match('O')
            match('j')
            match('P')
            match('J')
        elif lookahead.startswith('%'):
            match('%')
            match('o')
            match('e')
            match(';')
            parse_Y()
        elif lookahead.startswith('A'):
            match('A')
            match('&')
            match('f')
            match('.')
            match('-')
        elif lookahead.startswith('E'):
            match('E')
            match('w')
            parse_C()
            parse_V()
            parse_Y()
        elif lookahead.startswith('w'):
            match('w')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join([',', 'w', '%', 'A', 'E', 'w']))
    elif lookahead.startswith('`'):
        match('`')
        if pos >= len(tokens):
            error("Unexpected end of input in C")
        lookahead = tokens[pos]
        if lookahead.startswith('k'):
            match('k')
            match('c')
            match("'")
        elif lookahead.startswith('<'):
            match('<')
            match("'")
            match('e')
            parse_N()
        elif lookahead.startswith('`'):
            match('`')
            parse_C()
            parse_F()
            match('M')
        elif lookahead.startswith('@'):
            match('@')
            parse_Y()
        elif lookahead.startswith('w'):
            match('w')
        else:
            error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['k', '<', '`', '@', 'w']))
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('w'):
            match('w')
            match('u')
            parse_Q()
            match('S')
            match('B')
        elif lookahead.startswith(';'):
            match(';')
        elif lookahead.startswith('q'):
            match('q')
        elif lookahead.startswith('x'):
            match('x')
        elif lookahead.startswith('!'):
            match('!')
            parse_F()
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['w', ';', 'q', 'x', '!']))
        match('M')
    elif lookahead.startswith('@'):
        match('@')
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('u'):
            match('u')
            match('u')
            match('-')
            match('s')
        elif lookahead.startswith('W'):
            match('W')
            match(')')
            match('?')
            match('w')
        elif lookahead.startswith("'"):
            match("'")
            match('T')
        elif lookahead.startswith('@'):
            match('@')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['u', 'W', "'", '@']))
    elif lookahead.startswith('w'):
        match('w')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['k', '<', '`', '@', 'w']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('G'):
        match('G')
        parse_V()
        match('*')
        parse_N()
    elif lookahead.startswith('v'):
        match('v')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['G', 'v']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        parse_Q()
    elif lookahead.startswith('w'):
        match('w')
        match('O')
        match('j')
        match('P')
        match('J')
    elif lookahead.startswith('%'):
        match('%')
        match('o')
        match('e')
        match(';')
        parse_Y()
    elif lookahead.startswith('A'):
        match('A')
        match('&')
        match('f')
        match('.')
        match('-')
    elif lookahead.startswith('E'):
        match('E')
        match('w')
        parse_C()
        parse_V()
        parse_Y()
    elif lookahead.startswith('w'):
        match('w')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join([',', 'w', '%', 'A', 'E', 'w']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('u'):
        match('u')
        match('u')
        match('-')
        match('s')
    elif lookahead.startswith('W'):
        match('W')
        match(')')
        match('?')
        match('w')
    elif lookahead.startswith("'"):
        match("'")
        match('T')
    elif lookahead.startswith('@'):
        match('@')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['u', 'W', "'", '@']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('X'):
        match('X')
        match('z')
    elif lookahead.startswith('8'):
        match('8')
        match('n')
    elif lookahead.startswith('E'):
        match('E')
        match("'")
        parse_N()
    elif lookahead.startswith('S'):
        match('S')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['X', '8', 'E', 'S']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        match('u')
        parse_Q()
        match('S')
        match('B')
    elif lookahead.startswith(';'):
        match(';')
    elif lookahead.startswith('q'):
        match('q')
    elif lookahead.startswith('x'):
        match('x')
    elif lookahead.startswith('!'):
        match('!')
        parse_F()
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['w', ';', 'q', 'x', '!']))

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