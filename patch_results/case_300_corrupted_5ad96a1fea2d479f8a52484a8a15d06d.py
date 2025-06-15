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

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('P'):
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('-'):
            match('-')
            parse_I()
            match('X')
        elif lookahead.startswith('m'):
            match('m')
            parse_M()
        elif lookahead.startswith('a'):
            match('a')
        elif lookahead.startswith('n'):
            match('n')
            parse_Z()
            match('#')
            parse_I()
            match('H')
        elif lookahead.startswith('2'):
            match('2')
            parse_Z()
            match('C')
            match(')')
            match('m')
        else:
            error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['-', 'm', 'a', 'n', '2']))
        match('6')
        match('^')
        match('&')
        match('A')
    elif lookahead.startswith('z'):
        match('z')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('P'):
            parse_P()
            match('6')
            match('^')
            match('&')
            match('A')
        elif lookahead.startswith('z'):
            match('z')
            parse_M()
            match('h')
            match('c')
        elif lookahead.startswith('e'):
            match('e')
            parse_B()
            match('y')
            match(')')
            match('k')
        elif lookahead.startswith('l'):
            match('l')
            parse_I()
            parse_Z()
            parse_M()
        elif lookahead.startswith('y'):
            match('y')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['P', 'z', 'e', 'l', 'y']))
        match('h')
        match('c')
    elif lookahead.startswith('e'):
        match('e')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('A'):
            match('A')
            parse_Z()
            parse_M()
            match(')')
        elif lookahead.startswith('l'):
            match('l')
        elif lookahead.startswith('X'):
            match('X')
            match('t')
            match('c')
            match("'")
        elif lookahead.startswith('('):
            match('(')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['A', 'l', 'X', '(']))
        match('y')
        match(')')
        match('k')
    elif lookahead.startswith('l'):
        match('l')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('z'):
            match('z')
            parse_P()
            parse_Z()
            match('q')
            match('w')
        elif lookahead.startswith('['):
            match('[')
            match('n')
            parse_Z()
        elif lookahead.startswith('f'):
            match('f')
            match('w')
            match('?')
            match('y')
            parse_P()
        elif lookahead.startswith('&'):
            match('&')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['z', '[', 'f', '&']))
        while pos < len(tokens) and tokens[pos].startswith('1'):
            match('1')
            match('`')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('P'):
            parse_P()
            match('6')
            match('^')
            match('&')
            match('A')
        elif lookahead.startswith('z'):
            match('z')
            parse_M()
            match('h')
            match('c')
        elif lookahead.startswith('e'):
            match('e')
            parse_B()
            match('y')
            match(')')
            match('k')
        elif lookahead.startswith('l'):
            match('l')
            parse_I()
            parse_Z()
            parse_M()
        elif lookahead.startswith('y'):
            match('y')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['P', 'z', 'e', 'l', 'y']))
    elif lookahead.startswith('y'):
        match('y')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['P', 'z', 'e', 'l', 'y']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('A'):
        match('A')
        parse_Z()
        parse_M()
        match(')')
    elif lookahead.startswith('l'):
        match('l')
    elif lookahead.startswith('X'):
        match('X')
        match('t')
        match('c')
        match("'")
    elif lookahead.startswith('('):
        match('(')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['A', 'l', 'X', '(']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('z'):
        match('z')
        parse_P()
        parse_Z()
        match('q')
        match('w')
    elif lookahead.startswith('['):
        match('[')
        match('n')
        parse_Z()
    elif lookahead.startswith('f'):
        match('f')
        match('w')
        match('?')
        match('y')
        parse_P()
    elif lookahead.startswith('&'):
        match('&')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['z', '[', 'f', '&']))

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('1'):
        match('1')
        match('`')

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('-'):
        match('-')
        parse_I()
        match('X')
    elif lookahead.startswith('m'):
        match('m')
        parse_M()
    elif lookahead.startswith('a'):
        match('a')
    elif lookahead.startswith('n'):
        match('n')
        parse_Z()
        match('#')
        parse_I()
        match('H')
    elif lookahead.startswith('2'):
        match('2')
        parse_Z()
        match('C')
        match(')')
        match('m')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['-', 'm', 'a', 'n', '2']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_M()
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