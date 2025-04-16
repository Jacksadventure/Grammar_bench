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
        parse_H()
        parse_E()
    elif lookahead == 'c':
        match('c')
        match('d')
    elif lookahead == 'j':
        match('j')
        parse_H()
    elif lookahead == 'a':
        match('a')
    elif lookahead == 'f':
        match('f')
        match('f')
    elif lookahead == 'd':
        match('d')
        match('e')
        match('j')
    else:
        error('Unexpected token ' + lookahead + ' in A, expected one of: ' + ', '.join(['h', 'e', 'c', 'j', 'a', 'f', 'd']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in B')
    lookahead = tokens[pos]
    if lookahead == 'j':
        match('j')
        parse_F()
    elif lookahead == 'i':
        match('i')
        parse_B()
        match('a')
    else:
        error('Unexpected token ' + lookahead + ' in B, expected one of: ' + ', '.join(['j', 'i']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in C')
    lookahead = tokens[pos]
    if lookahead == 'e':
        match('e')
    elif lookahead == 'j':
        match('j')
        match('d')
    elif lookahead == 'd':
        match('d')
        match('a')
        parse_C()
    elif lookahead == 'i':
        match('i')
        match('b')
    elif lookahead == 'c':
        match('c')
        match('i')
    elif lookahead == 'b':
        match('b')
        match('e')
    elif lookahead == 'g':
        match('g')
        match('a')
        match('a')
    else:
        error('Unexpected token ' + lookahead + ' in C, expected one of: ' + ', '.join(['e', 'j', 'd', 'i', 'c', 'b', 'g']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in D')
    lookahead = tokens[pos]
    if lookahead == 'h':
        match('h')
        parse_C()
    elif lookahead == 'c':
        match('c')
        match('i')
    elif lookahead == 'g':
        match('g')
        match('b')
    elif lookahead == 'f':
        match('f')
        match('a')
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'd':
        match('d')
        parse_G()
    else:
        error('Unexpected token ' + lookahead + ' in D, expected one of: ' + ', '.join(['h', 'c', 'g', 'f', 'b', 'd']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in E')
    lookahead = tokens[pos]
    if lookahead == 'f':
        match('f')
        parse_J()
        parse_J()
    elif lookahead == 'a':
        match('a')
        parse_E()
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'g':
        match('g')
        parse_I()
    elif lookahead == 'c':
        match('c')
        parse_G()
    elif lookahead == 'j':
        match('j')
        match('f')
        match('f')
    elif lookahead == 'e':
        match('e')
        match('b')
        match('e')
    else:
        error('Unexpected token ' + lookahead + ' in E, expected one of: ' + ', '.join(['f', 'a', 'b', 'g', 'c', 'j', 'e']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in F')
    lookahead = tokens[pos]
    if lookahead == 'e':
        match('e')
    elif lookahead == 'b':
        match('b')
        match('b')
        match('j')
    elif lookahead == 'g':
        match('g')
        match('j')
        match('j')
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'h':
        match('h')
        match('b')
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'd':
        match('d')
        parse_G()
        match('i')
    elif lookahead == 'c':
        match('c')
        parse_B()
        parse_B()
    elif lookahead == 'a':
        match('a')
        parse_I()
    elif lookahead == 'j':
        match('j')
    else:
        error('Unexpected token ' + lookahead + ' in F, expected one of: ' + ', '.join(['e', 'b', 'g', 'i', 'h', 'f', 'd', 'c', 'a', 'j']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in G')
    lookahead = tokens[pos]
    if lookahead == 'c':
        match('c')
        match('a')
        match('d')
    elif lookahead == 'i':
        match('i')
        parse_J()
    elif lookahead == 'h':
        match('h')
    elif lookahead == 'e':
        match('e')
        parse_J()
        parse_B()
    else:
        error('Unexpected token ' + lookahead + ' in G, expected one of: ' + ', '.join(['c', 'i', 'h', 'e']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in H')
    lookahead = tokens[pos]
    if lookahead == 'i':
        match('i')
        match('a')
        match('g')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'b':
        match('b')
        match('h')
        parse_B()
    elif lookahead == 'd':
        match('d')
        parse_D()
        match('j')
    elif lookahead == 'c':
        match('c')
    elif lookahead == 'a':
        match('a')
        match('j')
        match('g')
    else:
        error('Unexpected token ' + lookahead + ' in H, expected one of: ' + ', '.join(['i', 'e', 'b', 'd', 'c', 'a']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in I')
    lookahead = tokens[pos]
    if lookahead == 'f':
        match('f')
    elif lookahead == 'g':
        match('g')
        parse_I()
    else:
        error('Unexpected token ' + lookahead + ' in I, expected one of: ' + ', '.join(['f', 'g']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in J')
    lookahead = tokens[pos]
    if lookahead == 'h':
        match('h')
        parse_H()
    elif lookahead == 'j':
        match('j')
        match('b')
        match('i')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'c':
        match('c')
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'g':
        match('g')
        parse_B()
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'a':
        match('a')
        match('c')
    elif lookahead == 'd':
        match('d')
    else:
        error('Unexpected token ' + lookahead + ' in J, expected one of: ' + ', '.join(['h', 'j', 'e', 'c', 'b', 'g', 'i', 'a', 'd']))

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