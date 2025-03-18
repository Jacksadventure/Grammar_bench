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
    if pos >= len(tokens):
        error('Unexpected end of input in A')
    lookahead = tokens[pos]
    if lookahead == 'a':
        match('a')
        match('i')
        match('d')
    elif lookahead == 'i':
        match('i')
        match('i')
        parse_C()
    elif lookahead == 'h':
        match('h')
        parse_J()
    else:
        error('Unexpected token ' + lookahead + ' in A, expected one of: ' + ', '.join(['a', 'i', 'h']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in B')
    lookahead = tokens[pos]
    if lookahead == 'a':
        match('a')
    elif lookahead == 'd':
        match('d')
        parse_B()
    else:
        error('Unexpected token ' + lookahead + ' in B, expected one of: ' + ', '.join(['a', 'd']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in C')
    lookahead = tokens[pos]
    if lookahead == 'i':
        match('i')
        parse_H()
    elif lookahead == 'j':
        match('j')
        match('b')
    elif lookahead == 'c':
        match('c')
        parse_B()
    elif lookahead == 'a':
        match('a')
    elif lookahead == 'f':
        match('f')
        match('g')
        match('e')
    elif lookahead == 'd':
        match('d')
    else:
        error('Unexpected token ' + lookahead + ' in C, expected one of: ' + ', '.join(['i', 'j', 'c', 'a', 'f', 'd']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in D')
    lookahead = tokens[pos]
    if lookahead == 'd':
        match('d')
    elif lookahead == 'j':
        match('j')
        parse_F()
        match('e')
    else:
        error('Unexpected token ' + lookahead + ' in D, expected one of: ' + ', '.join(['d', 'j']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in E')
    lookahead = tokens[pos]
    if lookahead == 'd':
        match('d')
        parse_F()
    elif lookahead == 'c':
        match('c')
    elif lookahead == 'g':
        match('g')
    else:
        error('Unexpected token ' + lookahead + ' in E, expected one of: ' + ', '.join(['d', 'c', 'g']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in F')
    lookahead = tokens[pos]
    if lookahead == 'j':
        match('j')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'i':
        match('i')
        match('e')
        parse_A()
    elif lookahead == 'g':
        match('g')
        parse_B()
        match('i')
    elif lookahead == 'h':
        match('h')
    else:
        error('Unexpected token ' + lookahead + ' in F, expected one of: ' + ', '.join(['j', 'd', 'e', 'i', 'g', 'h']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in G')
    lookahead = tokens[pos]
    if lookahead == 'j':
        match('j')
        match('a')
        parse_D()
    elif lookahead == 'c':
        match('c')
        parse_I()
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'g':
        match('g')
        match('b')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'h':
        match('h')
    else:
        error('Unexpected token ' + lookahead + ' in G, expected one of: ' + ', '.join(['j', 'c', 'i', 'b', 'g', 'e', 'f', 'h']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in H')
    lookahead = tokens[pos]
    if lookahead == 'd':
        match('d')
        match('d')
    elif lookahead == 'i':
        match('i')
        match('j')
    elif lookahead == 'a':
        match('a')
        match('f')
    elif lookahead == 'c':
        match('c')
        parse_I()
        match('i')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'h':
        match('h')
        parse_G()
        parse_F()
    elif lookahead == 'b':
        match('b')
    else:
        error('Unexpected token ' + lookahead + ' in H, expected one of: ' + ', '.join(['d', 'i', 'a', 'c', 'e', 'f', 'h', 'b']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in I')
    lookahead = tokens[pos]
    if lookahead == 'i':
        match('i')
        parse_A()
    elif lookahead == 'j':
        match('j')
        parse_H()
        match('i')
    else:
        error('Unexpected token ' + lookahead + ' in I, expected one of: ' + ', '.join(['i', 'j']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in J')
    lookahead = tokens[pos]
    if lookahead == 'h':
        match('h')
        parse_E()
        parse_F()
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'a':
        match('a')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'i':
        match('i')
        match('j')
        parse_I()
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'b':
        match('b')
        parse_B()
    elif lookahead == 'f':
        match('f')
        match('f')
        parse_D()
    elif lookahead == 'c':
        match('c')
        parse_F()
    else:
        error('Unexpected token ' + lookahead + ' in J, expected one of: ' + ', '.join(['h', 'g', 'a', 'e', 'i', 'j', 'd', 'b', 'f', 'c']))

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