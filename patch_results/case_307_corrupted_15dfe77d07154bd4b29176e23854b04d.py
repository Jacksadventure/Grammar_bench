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

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('Z'):
            match('Z')
        elif lookahead.startswith('M'):
            match('M')
            match('w')
            match('7')
            parse_W()
        elif lookahead.startswith('f'):
            match('f')
        elif lookahead.startswith('*'):
            match('*')
            parse_W()
            match('w')
            match('+')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['Z', 'M', 'f', '*']))
    elif lookahead.startswith('L'):
        match('L')
        match('_')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('?'):
            match('?')
        elif lookahead.startswith('X'):
            match('X')
            match('D')
            parse_W()
            parse_T()
            match('<')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['?', 'X']))
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('Z'):
            match('Z')
        elif lookahead.startswith('M'):
            match('M')
            match('w')
            match('7')
            parse_W()
        elif lookahead.startswith('f'):
            match('f')
        elif lookahead.startswith('*'):
            match('*')
            parse_W()
            match('w')
            match('+')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['Z', 'M', 'f', '*']))
    elif lookahead.startswith('E'):
        match('E')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('?'):
            match('?')
        elif lookahead.startswith('X'):
            match('X')
            match('D')
            parse_W()
            parse_T()
            match('<')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['?', 'X']))
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('B'):
            match('B')
            parse_U()
        elif lookahead.startswith('l'):
            match('l')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['B', 'l']))
    elif lookahead.startswith('['):
        match('[')
        match('m')
    elif lookahead.startswith('B'):
        match('B')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['o', 'L', 'E', '[', 'B']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('e'):
        match('e')
        match('?')

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('>'):
        match('>')
        match('#')
        match('v')
        parse_T()
        parse_U()

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
    elif lookahead.startswith('X'):
        match('X')
        match('D')
        parse_W()
        parse_T()
        match('<')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['?', 'X']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_V()
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