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
    if lookahead == 'h':
        match('h')
    elif lookahead == 'e':
        match('e')
        match('f')
        parse_D()
    elif lookahead == 'g':
        match('g')
        parse_D()
        match('f')
    elif lookahead == 'd':
        match('d')
        parse_C()
        match('e')
    elif lookahead == 'a':
        match('a')
        parse_G()
    else:
        error('Unexpected token ' + lookahead + ' in A, expected one of: ' + ', '.join(['h', 'e', 'g', 'd', 'a']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in B')
    lookahead = tokens[pos]
    if lookahead == 'h':
        match('h')
        match('b')
    elif lookahead == 'f':
        match('f')
        parse_E()
    elif lookahead == 'i':
        match('i')
        match('e')
        parse_G()
    elif lookahead == 'j':
        match('j')
        match('d')
    elif lookahead == 'e':
        match('e')
        parse_A()
    elif lookahead == 'c':
        match('c')
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'a':
        match('a')
        parse_H()
    elif lookahead == 'g':
        match('g')
    else:
        error('Unexpected token ' + lookahead + ' in B, expected one of: ' + ', '.join(['h', 'f', 'i', 'j', 'e', 'c', 'b', 'a', 'g']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in C')
    lookahead = tokens[pos]
    if lookahead == 'a':
        match('a')
        parse_J()
        parse_H()
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'c':
        match('c')
    else:
        error('Unexpected token ' + lookahead + ' in C, expected one of: ' + ', '.join(['a', 'g', 'c']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in D')
    lookahead = tokens[pos]
    if lookahead == 'g':
        match('g')
        match('h')
    elif lookahead == 'j':
        match('j')
        parse_A()
        match('i')
    elif lookahead == 'a':
        match('a')
        match('e')
        parse_F()
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'e':
        match('e')
        match('j')
    elif lookahead == 'c':
        match('c')
        parse_B()
    elif lookahead == 'h':
        match('h')
    elif lookahead == 'f':
        match('f')
        parse_J()
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'b':
        match('b')
    else:
        error('Unexpected token ' + lookahead + ' in D, expected one of: ' + ', '.join(['g', 'j', 'a', 'd', 'e', 'c', 'h', 'f', 'i', 'b']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in E')
    lookahead = tokens[pos]
    if lookahead == 'c':
        match('c')
    elif lookahead == 'd':
        match('d')
        parse_B()
        parse_J()
    elif lookahead == 'i':
        match('i')
        parse_C()
        parse_C()
    elif lookahead == 'e':
        match('e')
        parse_F()
        match('c')
    elif lookahead == 'b':
        match('b')
        parse_F()
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'f':
        match('f')
        parse_A()
        match('a')
    elif lookahead == 'h':
        match('h')
        match('g')
        match('a')
    else:
        error('Unexpected token ' + lookahead + ' in E, expected one of: ' + ', '.join(['c', 'd', 'i', 'e', 'b', 'g', 'f', 'h']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in F')
    lookahead = tokens[pos]
    if lookahead == 'g':
        match('g')
    elif lookahead == 'a':
        match('a')
        match('e')
    elif lookahead == 'h':
        match('h')
        match('c')
        match('e')
    elif lookahead == 'i':
        match('i')
        parse_F()
    elif lookahead == 'f':
        match('f')
        match('g')
    elif lookahead == 'e':
        match('e')
        match('b')
        match('f')
    elif lookahead == 'c':
        match('c')
        match('j')
        parse_D()
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'd':
        match('d')
    else:
        error('Unexpected token ' + lookahead + ' in F, expected one of: ' + ', '.join(['g', 'a', 'h', 'i', 'f', 'e', 'c', 'b', 'd']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in G')
    lookahead = tokens[pos]
    if lookahead == 'g':
        match('g')
    elif lookahead == 'b':
        match('b')
        parse_I()
    elif lookahead == 'a':
        match('a')
        parse_G()
        parse_I()
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'd':
        match('d')
    else:
        error('Unexpected token ' + lookahead + ' in G, expected one of: ' + ', '.join(['g', 'b', 'a', 'f', 'i', 'd']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in H')
    lookahead = tokens[pos]
    if lookahead == 'j':
        match('j')
        parse_H()
        parse_H()
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'a':
        match('a')
        parse_J()
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'g':
        match('g')
        match('a')
        match('a')
    elif lookahead == 'h':
        match('h')
    elif lookahead == 'd':
        match('d')
    else:
        error('Unexpected token ' + lookahead + ' in H, expected one of: ' + ', '.join(['j', 'i', 'a', 'f', 'e', 'g', 'h', 'd']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in I')
    lookahead = tokens[pos]
    if lookahead == 'i':
        match('i')
        parse_F()
        parse_E()
    elif lookahead == 'a':
        match('a')
        match('d')
        parse_J()
    elif lookahead == 'b':
        match('b')
        parse_I()
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'd':
        match('d')
        match('j')
        match('h')
    elif lookahead == 'g':
        match('g')
        parse_G()
        match('h')
    elif lookahead == 'c':
        match('c')
    elif lookahead == 'h':
        match('h')
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'e':
        match('e')
        match('a')
    else:
        error('Unexpected token ' + lookahead + ' in I, expected one of: ' + ', '.join(['i', 'a', 'b', 'j', 'd', 'g', 'c', 'h', 'f', 'e']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in J')
    lookahead = tokens[pos]
    if lookahead == 'i':
        match('i')
        match('e')
        parse_H()
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'd':
        match('d')
        match('i')
        match('j')
    elif lookahead == 'e':
        match('e')
        match('g')
    else:
        error('Unexpected token ' + lookahead + ' in J, expected one of: ' + ', '.join(['i', 'g', 'd', 'e']))

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