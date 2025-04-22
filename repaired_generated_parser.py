import sys
tokens = []
pos = 0

def error(msg):
    print('Parse error:', msg)
    sys.exit(1)

def match(expected):
    global pos, tokens
    if pos < len(tokens) and tokens[pos] == expected:
        pos += 1
    else:
        error('Expected ' + expected + ', got ' + (tokens[pos] if pos < len(tokens) else 'EOF'))

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'e':
        match('e')
        parse_I()
        parse_K()

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in B')
    lookahead = tokens[pos]
    if lookahead == 'm':
        match('m')
    elif lookahead == 'l':
        match('l')
        parse_O()
        match('l')
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'n':
        match('n')
        parse_G()
        parse_D()
    elif lookahead == 'j':
        match('j')
        parse_G()
    elif lookahead == 'c':
        match('c')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'h':
        match('h')
        match('j')
        parse_G()
    elif lookahead == 'o':
        match('o')
    elif lookahead == 'e':
        match('e')
        match('g')
    elif lookahead == 'a':
        match('a')
        parse_G()
        match('b')
    else:
        error('Unexpected token ' + lookahead + ' in B, expected one of: ' + ', '.join(['m', 'l', 'f', 'n', 'j', 'c', 'd', 'g', 'i', 'h', 'o', 'e', 'a']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in C')
    lookahead = tokens[pos]
    if lookahead == 'a':
        match('a')
        match('a')
    else:
        error('Unexpected token ' + lookahead + ' in C, expected one of: ' + ', '.join(['a']))

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'l':
        match('l')

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'l':
        match('l')
        parse_N()

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in F')
    lookahead = tokens[pos]
    if lookahead == 'c':
        match('c')
    elif lookahead == 'e':
        match('e')
        match('e')
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'o':
        match('o')
    elif lookahead == 'm':
        match('m')
        parse_H()
        parse_J()
    else:
        error('Unexpected token ' + lookahead + ' in F, expected one of: ' + ', '.join(['c', 'e', 'i', 'j', 'f', 'o', 'm']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in G')
    lookahead = tokens[pos]
    if lookahead == 'e':
        match('e')
    elif lookahead == 'c':
        match('c')
        match('i')
    elif lookahead == 'f':
        match('f')
        match('n')
    elif lookahead == 'i':
        match('i')
        parse_G()
        parse_D()
    elif lookahead == 'a':
        match('a')
        parse_J()
    elif lookahead == 'm':
        match('m')
        match('h')
        match('a')
    elif lookahead == 'h':
        match('h')
        match('e')
        match('i')
    elif lookahead == 'j':
        match('j')
    else:
        error('Unexpected token ' + lookahead + ' in G, expected one of: ' + ', '.join(['e', 'c', 'f', 'i', 'a', 'm', 'h', 'j']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in H')
    lookahead = tokens[pos]
    if lookahead == 'm':
        match('m')
    elif lookahead == 'n':
        match('n')
        parse_D()
    elif lookahead == 'a':
        match('a')
        parse_I()
    elif lookahead == 'j':
        match('j')
        match('n')
        parse_B()
    elif lookahead == 'c':
        match('c')
        match('a')
    else:
        error('Unexpected token ' + lookahead + ' in H, expected one of: ' + ', '.join(['m', 'n', 'a', 'j', 'c']))

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'b':
        match('b')

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in J')
    lookahead = tokens[pos]
    if lookahead == 'k':
        match('k')
    elif lookahead == 'h':
        match('h')
        match('o')
        parse_L()
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'a':
        match('a')
        parse_G()
        parse_O()
    else:
        error('Unexpected token ' + lookahead + ' in J, expected one of: ' + ', '.join(['k', 'h', 'e', 'a']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in K')
    lookahead = tokens[pos]
    if lookahead == 'd':
        match('d')
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'c':
        match('c')
    elif lookahead == 'i':
        match('i')
        match('d')
    elif lookahead == 'k':
        match('k')
        parse_D()
    elif lookahead == 'a':
        match('a')
    elif lookahead == 'j':
        match('j')
        match('o')
    elif lookahead == 'e':
        match('e')
        parse_B()
    elif lookahead == 'g':
        match('g')
        match('j')
    else:
        error('Unexpected token ' + lookahead + ' in K, expected one of: ' + ', '.join(['d', 'b', 'c', 'i', 'k', 'a', 'j', 'e', 'g']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in L')
    lookahead = tokens[pos]
    if lookahead == 'l':
        match('l')
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'j':
        match('j')
        match('d')
        parse_L()
    elif lookahead == 'h':
        match('h')
        match('e')
        match('g')
    elif lookahead == 'o':
        match('o')
        parse_M()
        match('d')
    elif lookahead == 'g':
        match('g')
        match('m')
        parse_N()
    elif lookahead == 'k':
        match('k')
        match('k')
        parse_D()
    else:
        error('Unexpected token ' + lookahead + ' in L, expected one of: ' + ', '.join(['l', 'f', 'j', 'h', 'o', 'g', 'k']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in M')
    lookahead = tokens[pos]
    if lookahead == 'n':
        match('n')
        parse_G()
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'h':
        match('h')
        match('g')
        match('h')
    elif lookahead == 'e':
        match('e')
        parse_C()
        parse_K()
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'l':
        match('l')
        parse_E()
    elif lookahead == 'd':
        match('d')
        match('g')
        match('c')
    elif lookahead == 'o':
        match('o')
    else:
        error('Unexpected token ' + lookahead + ' in M, expected one of: ' + ', '.join(['n', 'g', 'b', 'i', 'h', 'e', 'f', 'l', 'd', 'o']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in N')
    lookahead = tokens[pos]
    if lookahead == 'l':
        match('l')
        parse_M()
    elif lookahead == 'b':
        match('b')
        parse_B()
    elif lookahead == 'c':
        match('c')
        parse_I()
    elif lookahead == 'o':
        match('o')
    elif lookahead == 'f':
        match('f')
        parse_M()
        match('f')
    else:
        error('Unexpected token ' + lookahead + ' in N, expected one of: ' + ', '.join(['l', 'b', 'c', 'o', 'f']))

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'j':
        match('j')
        parse_J()
        parse_C()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_A()
    if pos != len(tokens):
        error('Extra tokens after parsing: ' + ' '.join(tokens[pos:]))
    print('Input accepted.')

def main():
    import sys
    if len(sys.argv) > 1:
        input_str = sys.argv[1]
        parse_input(input_str)
if __name__ == '__main__':
    main()