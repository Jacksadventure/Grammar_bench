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

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('E'):
        while pos < len(tokens) and tokens[pos].startswith('%'):
            match('%')
            match('7')
            match('b')
        if pos >= len(tokens):
            error("Unexpected end of input in C")
        lookahead = tokens[pos]
        if lookahead.startswith('B'):
            match('B')
            match('$')
            match('9')
            parse_H()
            parse_K()
        elif lookahead.startswith('~'):
            match('~')
            parse_S()
            parse_H()
        elif lookahead.startswith('h'):
            match('h')
            parse_F()
            parse_F()
            match('u')
        elif lookahead.startswith('J'):
            match('J')
        else:
            error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['B', '~', 'h', 'J']))
    elif lookahead.startswith('i'):
        match('i')
    elif lookahead.startswith('D'):
        match('D')
        while pos < len(tokens) and tokens[pos].startswith('%'):
            match('%')
            match('7')
            match('b')
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith('*'):
            match('*')
            parse_F()
            parse_K()
        elif lookahead.startswith('-'):
            match('-')
            parse_A()
            parse_F()
            parse_W()
            parse_Q()
        elif lookahead.startswith('e'):
            match('e')
            parse_S()
            match('[')
            parse_H()
        elif lookahead.startswith('Z'):
            match('Z')
            match('U')
        elif lookahead.startswith('1'):
            match('1')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['*', '-', 'e', 'Z', '1']))
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['E', 'i', 'D']))

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('%'):
        match('%')
        match('7')
        match('b')

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        parse_E()
    elif lookahead.startswith('Z'):
        match('Z')
        parse_F()
        match('h')
    elif lookahead.startswith('q'):
        match('q')
        parse_H()
        parse_H()
        parse_F()
    elif lookahead.startswith('-'):
        match('-')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['?', 'Z', 'q', '-']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('*'):
        match('*')
        parse_F()
        parse_K()
    elif lookahead.startswith('-'):
        match('-')
        parse_A()
        parse_F()
        parse_W()
        parse_Q()
    elif lookahead.startswith('e'):
        match('e')
        parse_S()
        match('[')
        parse_H()
    elif lookahead.startswith('Z'):
        match('Z')
        match('U')
    elif lookahead.startswith('1'):
        match('1')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['*', '-', 'e', 'Z', '1']))

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('M'):
        match('M')
        match('d')

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('<'):
        match('<')
        parse_W()
        parse_W()
    elif lookahead.startswith('Q'):
        parse_Q()
        match('r')
    elif lookahead.startswith('&'):
        match('&')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['<', 'Q', '&']))

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('r'):
        match('r')
        match('w')

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('L'):
        match('L')
        match('d')
        match('v')
        match('0')
        match(';')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['L', '']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_K()
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