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

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('r'):
        match('r')
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('L'):
            match('L')
        elif lookahead.startswith("'"):
            match("'")
            parse_Y()
            match('s')
            parse_U()
            match('_')
        elif lookahead.startswith('`'):
            match('`')
        elif lookahead.startswith('k'):
            match('k')
            parse_F()
            parse_B()
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['L', "'", '`', 'k']))
        while pos < len(tokens) and tokens[pos].startswith('8'):
            match('8')
            match('z')
            parse_T()
    elif lookahead.startswith('k'):
        match('k')
        match('{')
    elif lookahead.startswith('p'):
        match('p')
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('['):
            match('[')
            match('H')
        elif lookahead.startswith('V'):
            match('V')
            match("'")
            match('2')
        elif lookahead.startswith('a'):
            match('a')
            match('G')
            parse_Y()
            parse_C()
        elif lookahead.startswith('7'):
            match('7')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['[', 'V', 'a', '7']))
        match('O')
    elif lookahead.startswith("'"):
        match("'")
        match('0')
        match('i')
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['r', 'k', 'p', "'", 'd']))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('P'):
        match('P')
        match('!')
        parse_T()
        parse_B()
        parse_T()
    elif lookahead.startswith('('):
        match('(')
    elif lookahead.startswith('6'):
        match('6')
        parse_X()
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['P', '(', '6']))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('L'):
        match('L')
    elif lookahead.startswith("'"):
        match("'")
        parse_Y()
        match('s')
        parse_U()
        match('_')
    elif lookahead.startswith('`'):
        match('`')
    elif lookahead.startswith('k'):
        match('k')
        parse_F()
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['L', "'", '`', 'k']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('['):
        match('[')
        match('H')
    elif lookahead.startswith('V'):
        match('V')
        match("'")
        match('2')
    elif lookahead.startswith('a'):
        match('a')
        match('G')
        parse_Y()
        parse_C()
    elif lookahead.startswith('7'):
        match('7')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['[', 'V', 'a', '7']))

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('S'):
        match('S')
        parse_X()
        parse_C()
        parse_U()

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('8'):
        match('8')
        match('z')
        parse_T()

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('W'):
        match('W')
        match('>')
        parse_T()
        parse_J()
        parse_B()

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('3'):
        match('3')
        match('b')
    elif lookahead.startswith('+'):
        match('+')
        match('[')
        parse_B()
        parse_C()
        parse_B()
    elif lookahead.startswith('2'):
        match('2')
        parse_X()
        match("'")
        match('Z')
        parse_C()
    elif lookahead.startswith('%'):
        match('%')
    elif lookahead.startswith('>'):
        match('>')
        match('_')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['3', '+', '2', '%', '>']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Y()
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