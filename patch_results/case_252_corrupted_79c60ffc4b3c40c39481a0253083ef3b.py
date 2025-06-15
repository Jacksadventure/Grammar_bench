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

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('Z'):
        match('Z')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('9'):
            match('9')
            parse_C()
            parse_F()
            parse_N()
        elif lookahead.startswith('r'):
            match('r')
            parse_R()
            parse_R()
            parse_Y()
        elif lookahead.startswith('?'):
            match('?')
            parse_Y()
            parse_C()
        elif lookahead.startswith('b'):
            match('b')
            parse_D()
            match(']')
        elif lookahead.startswith('A'):
            match('A')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['9', 'r', '?', 'b', 'A']))
        while pos < len(tokens) and tokens[pos].startswith(','):
            match(',')
            parse_Y()
            parse_S()
        match('y')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('9'):
            match('9')
            parse_C()
            parse_F()
            parse_N()
        elif lookahead.startswith('r'):
            match('r')
            parse_R()
            parse_R()
            parse_Y()
        elif lookahead.startswith('?'):
            match('?')
            parse_Y()
            parse_C()
        elif lookahead.startswith('b'):
            match('b')
            parse_D()
            match(']')
        elif lookahead.startswith('A'):
            match('A')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['9', 'r', '?', 'b', 'A']))
    elif lookahead.startswith('z'):
        match('z')
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('Q'):
            match('Q')
            parse_Y()
        elif lookahead.startswith('f'):
            match('f')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['Q', 'f']))
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('9'):
            match('9')
            parse_C()
            parse_F()
            parse_N()
        elif lookahead.startswith('r'):
            match('r')
            parse_R()
            parse_R()
            parse_Y()
        elif lookahead.startswith('?'):
            match('?')
            parse_Y()
            parse_C()
        elif lookahead.startswith('b'):
            match('b')
            parse_D()
            match(']')
        elif lookahead.startswith('A'):
            match('A')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['9', 'r', '?', 'b', 'A']))
        while pos < len(tokens) and tokens[pos].startswith('%'):
            match('%')
            match('t')
            match('3')
            match('G')
            parse_E()
        while pos < len(tokens) and tokens[pos].startswith('+'):
            match('+')
            parse_E()
    elif lookahead.startswith('a'):
        match('a')
        match('L')
        while pos < len(tokens) and tokens[pos].startswith('k'):
            match('k')
            parse_E()
    elif lookahead.startswith(','):
        match(',')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['Z', 'z', 'a', ',']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('`'):
        match('`')
    elif lookahead.startswith('g'):
        match('g')
        parse_R()
        parse_N()
    elif lookahead.startswith('M'):
        match('M')
        parse_K()
        parse_N()
        parse_N()
    elif lookahead.startswith('1'):
        match('1')
        parse_D()
    elif lookahead.startswith('I'):
        match('I')
        match('W')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['`', 'g', 'M', '1', 'I']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('Q'):
        match('Q')
        parse_Y()
    elif lookahead.startswith('f'):
        match('f')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['Q', 'f']))

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('%'):
        match('%')
        match('t')
        match('3')
        match('G')
        parse_E()

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('k'):
        match('k')
        parse_E()

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('9'):
        match('9')
        parse_C()
        parse_F()
        parse_N()
    elif lookahead.startswith('r'):
        match('r')
        parse_R()
        parse_R()
        parse_Y()
    elif lookahead.startswith('?'):
        match('?')
        parse_Y()
        parse_C()
    elif lookahead.startswith('b'):
        match('b')
        parse_D()
        match(']')
    elif lookahead.startswith('A'):
        match('A')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['9', 'r', '?', 'b', 'A']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(','):
        match(',')
        parse_Y()
        parse_S()

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('V'):
        match('V')

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('B'):
        match('B')
        parse_E()
        parse_C()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_D()
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