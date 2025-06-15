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

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('*'):
        match('*')
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('T'):
            match('T')
            match('N')
            match('^')
            parse_F()
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['T', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith('p'):
            match('p')
            parse_P()
            parse_D()
        elif lookahead.startswith('6'):
            match('6')
            parse_F()
            match('2')
            match('N')
        elif lookahead.startswith('-'):
            match('-')
            match('V')
            match('8')
        elif lookahead.startswith('G'):
            parse_G()
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['p', '6', '-', 'G']))
        match('1')

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('7'):
        match('7')
        parse_M()
    elif lookahead.startswith('.'):
        match('.')
        parse_M()
    elif lookahead.startswith('p'):
        match('p')
        parse_F()
        parse_P()
    elif lookahead.startswith('I'):
        match('I')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['7', '.', 'p', 'I']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('*'):
        match('*')
    elif lookahead.startswith('{'):
        match('{')
    elif lookahead.startswith('L'):
        match('L')
    elif lookahead.startswith('e'):
        match('e')
    elif lookahead.startswith('g'):
        match('g')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['*', '{', 'L', 'e', 'g']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('n'):
        match('n')
    elif lookahead.startswith('0'):
        match('0')
        match('g')
    elif lookahead.startswith('$'):
        match('$')
    elif lookahead.startswith(','):
        match(',')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['n', '0', '$', ',']))

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('P'):
        parse_P()

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('T'):
        match('T')
        match('N')
        match('^')

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('c'):
        match('c')
    elif lookahead.startswith('6'):
        match('6')
        parse_F()
    elif lookahead.startswith('+'):
        match('+')
        match('L')
        match('j')
    elif lookahead.startswith('0'):
        match('0')
        match('K')
        parse_U()
        parse_U()
    elif lookahead.startswith('M'):
        parse_M()
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['c', '6', '+', '0', 'M']))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('$'):
        match('$')
    elif lookahead.startswith('?'):
        match('?')
        match('r')
        parse_G()
        match('n')
    elif lookahead.startswith('Y'):
        match('Y')
    elif lookahead.startswith('H'):
        parse_H()
        match('/')
        parse_D()
        match('s')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['$', '?', 'Y', 'H']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('%'):
        match('%')
        parse_G()
        parse_P()
        parse_Q()
    elif lookahead.startswith('|'):
        match('|')
        match('y')
    elif lookahead.startswith('a'):
        match('a')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['%', '|', 'a']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_O()
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