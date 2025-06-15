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
    if lookahead.startswith('*'):
        match('*')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith(';'):
            match(';')
            match('N')
        elif lookahead.startswith('E'):
            match('E')
        elif lookahead.startswith('K'):
            match('K')
            parse_Q()
            match('U')
            match('u')
            match('B')
        elif lookahead.startswith('i'):
            match('i')
            parse_R()
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join([';', 'E', 'K', 'i']))
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('F'):
            match('F')
            match('r')
            parse_J()
        elif lookahead.startswith('7'):
            match('7')
            match(',')
            parse_J()
            match('h')
        elif lookahead.startswith('+'):
            match('+')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['F', '7', '+']))
        match('@')
    elif lookahead.startswith('s'):
        match('s')
        match('x')
        match('*')
        match('9')
        match('1')
    elif lookahead.startswith('('):
        match('(')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith(';'):
            match(';')
            match('N')
        elif lookahead.startswith('E'):
            match('E')
        elif lookahead.startswith('K'):
            match('K')
            parse_Q()
            match('U')
            match('u')
            match('B')
        elif lookahead.startswith('i'):
            match('i')
            parse_R()
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join([';', 'E', 'K', 'i']))
        match(';')
        match('|')
    elif lookahead.startswith('H'):
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('F'):
            match('F')
            match('r')
            parse_J()
        elif lookahead.startswith('7'):
            match('7')
            match(',')
            parse_J()
            match('h')
        elif lookahead.startswith('+'):
            match('+')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['F', '7', '+']))
        match('|')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('n'):
            match('n')
            parse_H()
            parse_C()
        elif lookahead.startswith('+'):
            match('+')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['n', '+']))
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('n'):
            match('n')
            parse_H()
            parse_C()
        elif lookahead.startswith('+'):
            match('+')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['n', '+']))
    elif lookahead.startswith('S'):
        match('S')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['*', 's', '(', 'H', 'S']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('n'):
        match('n')
        parse_H()
        parse_C()
    elif lookahead.startswith('+'):
        match('+')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['n', '+']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('O'):
        match('O')
        parse_R()
        parse_I()
        match(')')
    elif lookahead.startswith('L'):
        match('L')
        match('F')
        match('k')
        match('D')
    elif lookahead.startswith('r'):
        match('r')
        parse_C()
    elif lookahead.startswith('i'):
        match('i')
        match("'")
    elif lookahead.startswith('w'):
        match('w')
        match('l')
        match('[')
        match(']')
    elif lookahead.startswith('O'):
        match('O')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['O', 'L', 'r', 'i', 'w', 'O']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith(';'):
        match(';')
        match('N')
    elif lookahead.startswith('E'):
        match('E')
    elif lookahead.startswith('K'):
        match('K')
        parse_Q()
        match('U')
        match('u')
        match('B')
    elif lookahead.startswith('i'):
        match('i')
        parse_R()
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join([';', 'E', 'K', 'i']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('F'):
        match('F')
        match('r')
        parse_J()
    elif lookahead.startswith('7'):
        match('7')
        match(',')
        parse_J()
        match('h')
    elif lookahead.startswith('+'):
        match('+')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['F', '7', '+']))

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('#'):
        match('#')
        parse_R()
        match('n')

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('E'):
        match('E')
        match('i')
        match('d')
        parse_G()
        parse_Q()
    elif lookahead.startswith('4'):
        match('4')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['E', '4']))

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