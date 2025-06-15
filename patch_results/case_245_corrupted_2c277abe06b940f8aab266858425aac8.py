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

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('J'):
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('t'):
            match('t')
            parse_K()
            match('M')
            parse_K()
            parse_A()
        elif lookahead.startswith(')'):
            match(')')
            match('s')
            parse_Q()
            parse_O()
        elif lookahead.startswith('J'):
            parse_J()
            parse_J()
            parse_R()
        elif lookahead.startswith('$'):
            match('$')
            parse_R()
        elif lookahead.startswith(';'):
            match(';')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['t', ')', 'J', '$', ';']))
        match('?')
    elif lookahead.startswith('b'):
        match('b')
        while pos < len(tokens) and tokens[pos].startswith('M'):
            match('M')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('s'):
            match('s')
            parse_R()
        elif lookahead.startswith('{'):
            match('{')
        elif lookahead.startswith('J'):
            parse_J()
            match('{')
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['s', '{', 'J']))
    elif lookahead.startswith('p'):
        match('p')
        match('w')
    elif lookahead.startswith('7'):
        match('7')
        match('^')
    elif lookahead.startswith('|'):
        match('|')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['J', 'b', 'p', '7', '|']))

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(','):
        match(',')
        parse_C()
        parse_E()
        match('c')

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('t'):
        match('t')
        parse_K()
        match('M')
        parse_K()
        parse_A()
    elif lookahead.startswith(')'):
        match(')')
        match('s')
        parse_Q()
        parse_O()
    elif lookahead.startswith('J'):
        parse_J()
        parse_J()
        parse_R()
    elif lookahead.startswith('$'):
        match('$')
        parse_R()
    elif lookahead.startswith(';'):
        match(';')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['t', ')', 'J', '$', ';']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('9'):
        match('9')
        parse_A()
        parse_R()
        parse_K()
    elif lookahead.startswith('p'):
        match('p')
        parse_D()
        parse_E()
        parse_A()
    elif lookahead.startswith('X'):
        match('X')
        match('Y')
        parse_Q()
    elif lookahead.startswith('S'):
        match('S')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['9', 'p', 'X', 'S']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(','):
        match(',')

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('s'):
        match('s')
        parse_R()
    elif lookahead.startswith('{'):
        match('{')
    elif lookahead.startswith('J'):
        parse_J()
        match('{')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['s', '{', 'J']))

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('e'):
        match('e')
        match('o')
        parse_R()
        parse_J()

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('M'):
        match('M')

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('%'):
        match('%')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Q()
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