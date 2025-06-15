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

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        match(']')
        while pos < len(tokens) and tokens[pos].startswith('0'):
            match('0')
            match('#')
            match('@')
            parse_T()
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith("'"):
            match("'")
            parse_T()
            parse_T()
        elif lookahead.startswith('r'):
            match('r')
        elif lookahead.startswith('<'):
            match('<')
            parse_Z()
            parse_K()
            parse_U()
            match('{')
        elif lookahead.startswith('8'):
            match('8')
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(["'", 'r', '<', '8']))
    elif lookahead.startswith('|'):
        match('|')
    elif lookahead.startswith('6'):
        match('6')
        while pos < len(tokens) and tokens[pos].startswith('J'):
            match('J')
            match('h')
            match("'")
            match('$')
            parse_E()
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('l'):
            match('l')
            parse_Q()
            match(']')
            parse_N()
        elif lookahead.startswith('9'):
            match('9')
            match('F')
        elif lookahead.startswith('Q'):
            parse_Q()
            parse_N()
            parse_N()
            parse_K()
        elif lookahead.startswith('S'):
            match('S')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['l', '9', 'Q', 'S']))
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith(']'):
            match(']')
            parse_E()
            parse_G()
        elif lookahead.startswith('|'):
            match('|')
        elif lookahead.startswith('6'):
            match('6')
            parse_K()
            parse_H()
            parse_U()
        elif lookahead.startswith('x'):
            match('x')
            parse_N()
            parse_K()
            parse_N()
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join([']', '|', '6', 'x']))
    elif lookahead.startswith('x'):
        match('x')
        while pos < len(tokens) and tokens[pos].startswith('Q'):
            parse_Q()
            parse_E()
            match('y')
            match('z')
        while pos < len(tokens) and tokens[pos].startswith('J'):
            match('J')
            match('h')
            match("'")
            match('$')
            parse_E()
        while pos < len(tokens) and tokens[pos].startswith('Q'):
            parse_Q()
            parse_E()
            match('y')
            match('z')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join([']', '|', '6', 'x']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('l'):
        match('l')
        parse_Q()
        match(']')
        parse_N()
    elif lookahead.startswith('9'):
        match('9')
        match('F')
    elif lookahead.startswith('Q'):
        parse_Q()
        parse_N()
        parse_N()
        parse_K()
    elif lookahead.startswith('S'):
        match('S')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['l', '9', 'Q', 'S']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('J'):
        match('J')
        match('h')
        match("'")
        match('$')
        parse_E()

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        parse_T()
        parse_T()
    elif lookahead.startswith('r'):
        match('r')
    elif lookahead.startswith('<'):
        match('<')
        parse_Z()
        parse_K()
        parse_U()
        match('{')
    elif lookahead.startswith('8'):
        match('8')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(["'", 'r', '<', '8']))

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('0'):
        match('0')
        match('#')
        match('@')
        parse_T()

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Q'):
        parse_Q()
        parse_E()
        match('y')
        match('z')

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('A'):
        match('A')

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(':'):
        match(':')
        match('y')
        match('[')

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('D'):
        match('D')
        match('O')
        match('X')
        match('?')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_U()
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