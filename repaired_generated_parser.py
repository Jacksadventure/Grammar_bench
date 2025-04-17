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
    if lookahead == 'g':
        match('g')
    elif lookahead == 'e':
        match('e')
        parse_G()
        parse_D()
    elif lookahead == 'f':
        match('f')
        match('e')
    elif lookahead == 'c':
        match('c')
        match('c')
    elif lookahead == 'b':
        match('b')
        parse_A()
    elif lookahead == 'h':
        match('h')
        match('e')
    elif lookahead == 'd':
        match('d')
        parse_B()
        parse_A()
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'a':
        match('a')
    elif lookahead == 'j':
        match('j')
        parse_D()
    else:
        error('Unexpected token ' + lookahead + ' in A, expected one of: ' + ', '.join(['g', 'e', 'f', 'c', 'b', 'h', 'd', 'i', 'a', 'j']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in B')
    lookahead = tokens[pos]
    if lookahead == 'j':
        match('j')
        parse_G()
        match('j')
    else:
        error('Unexpected token ' + lookahead + ' in B, expected one of: ' + ', '.join(['j']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in C')
    lookahead = tokens[pos]
    if lookahead == 'd':
        match('d')
        parse_I()
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'i':
        match('i')
        match('f')
        match('j')
    else:
        error('Unexpected token ' + lookahead + ' in C, expected one of: ' + ', '.join(['d', 'j', 'b', 'e', 'i']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in D')
    lookahead = tokens[pos]
    if lookahead == 'i':
        match('i')
        parse_F()
        parse_E()
    elif lookahead == 'j':
        match('j')
    else:
        error('Unexpected token ' + lookahead + ' in D, expected one of: ' + ', '.join(['i', 'j']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in E')
    lookahead = tokens[pos]
    if lookahead == 'f':
        match('f')
        parse_H()
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'b':
        match('b')
        match('a')
        parse_J()
    elif lookahead == 'a':
        match('a')
    else:
        error('Unexpected token ' + lookahead + ' in E, expected one of: ' + ', '.join(['f', 'g', 'd', 'j', 'b', 'a']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in F')
    lookahead = tokens[pos]
    if lookahead == 'e':
        match('e')
        parse_C()
        match('e')
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'j':
        match('j')
        match('a')
    elif lookahead == 'h':
        match('h')
        parse_G()
    elif lookahead == 'i':
        match('i')
        match('b')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'a':
        match('a')
        match('f')
        parse_I()
    elif lookahead == 'b':
        match('b')
        parse_F()
    else:
        error('Unexpected token ' + lookahead + ' in F, expected one of: ' + ', '.join(['e', 'g', 'j', 'h', 'i', 'd', 'a', 'b']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in G')
    lookahead = tokens[pos]
    if lookahead == 'j':
        match('j')
        match('j')
        match('d')
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'f':
        match('f')
    else:
        error('Unexpected token ' + lookahead + ' in G, expected one of: ' + ', '.join(['j', 'g', 'f']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in H')
    lookahead = tokens[pos]
    if lookahead == 'h':
        match('h')
    elif lookahead == 'c':
        match('c')
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'a':
        match('a')
        match('d')
    elif lookahead == 'j':
        match('j')
        parse_B()
    elif lookahead == 'f':
        match('f')
    else:
        error('Unexpected token ' + lookahead + ' in H, expected one of: ' + ', '.join(['h', 'c', 'b', 'a', 'j', 'f']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in I')
    lookahead = tokens[pos]
    if lookahead == 'f':
        match('f')
        parse_B()
        parse_J()
    else:
        error('Unexpected token ' + lookahead + ' in I, expected one of: ' + ', '.join(['f']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in J')
    lookahead = tokens[pos]
    if lookahead == 'i':
        match('i')
        parse_C()
    else:
        error('Unexpected token ' + lookahead + ' in J, expected one of: ' + ', '.join(['i']))

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