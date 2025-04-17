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
    if lookahead == 's':
        match('s')
        match('c')
        parse_Q()
    elif lookahead == 'n':
        match('n')
        match('n')
        parse_F()
    elif lookahead == 'e':
        match('e')
        parse_B()
        match('q')
    elif lookahead == 'p':
        match('p')
    elif lookahead == 't':
        match('t')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'f':
        match('f')
        parse_L()
    elif lookahead == 'o':
        match('o')
        match('e')
        parse_A()
    elif lookahead == 'q':
        match('q')
        match('n')
    elif lookahead == 'm':
        match('m')
    elif lookahead == 'k':
        match('k')
        match('o')
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'h':
        match('h')
    elif lookahead == 'g':
        match('g')
        parse_C()
        match('c')
    elif lookahead == 'l':
        match('l')
        match('e')
    elif lookahead == 'a':
        match('a')
        parse_L()
        parse_E()
    elif lookahead == 'j':
        match('j')
        parse_O()
        parse_H()
    else:
        error('Unexpected token ' + lookahead + ' in A, expected one of: ' + ', '.join(['s', 'n', 'e', 'p', 't', 'd', 'f', 'o', 'q', 'm', 'k', 'b', 'h', 'g', 'l', 'a', 'j']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in B')
    lookahead = tokens[pos]
    if lookahead == 'd':
        match('d')
        parse_P()
        match('l')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'l':
        match('l')
        match('o')
    elif lookahead == 'r':
        match('r')
        parse_E()
        match('o')
    elif lookahead == 'a':
        match('a')
        parse_H()
    elif lookahead == 'm':
        match('m')
        parse_C()
        match('a')
    elif lookahead == 'o':
        match('o')
    elif lookahead == 'b':
        match('b')
        parse_N()
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'k':
        match('k')
        parse_O()
    elif lookahead == 'q':
        match('q')
        match('i')
    elif lookahead == 'c':
        match('c')
        match('r')
        match('c')
    elif lookahead == 'f':
        match('f')
        match('k')
        parse_F()
    elif lookahead == 's':
        match('s')
        match('d')
    elif lookahead == 'i':
        match('i')
        match('a')
    elif lookahead == 't':
        match('t')
        parse_N()
        parse_R()
    else:
        error('Unexpected token ' + lookahead + ' in B, expected one of: ' + ', '.join(['d', 'e', 'l', 'r', 'a', 'm', 'o', 'b', 'j', 'k', 'q', 'c', 'f', 's', 'i', 't']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in C')
    lookahead = tokens[pos]
    if lookahead == 'e':
        match('e')
        parse_C()
        parse_A()
    else:
        error('Unexpected token ' + lookahead + ' in C, expected one of: ' + ', '.join(['e']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in D')
    lookahead = tokens[pos]
    if lookahead == 'b':
        match('b')
        match('m')
        parse_S()
    elif lookahead == 'h':
        match('h')
    elif lookahead == 't':
        match('t')
    elif lookahead == 'p':
        match('p')
        parse_L()
    elif lookahead == 'k':
        match('k')
    elif lookahead == 'a':
        match('a')
        parse_D()
    elif lookahead == 'e':
        match('e')
        parse_B()
    elif lookahead == 's':
        match('s')
        match('c')
    elif lookahead == 'n':
        match('n')
        parse_G()
        match('c')
    elif lookahead == 'l':
        match('l')
        parse_E()
        match('e')
    elif lookahead == 'd':
        match('d')
        parse_M()
    elif lookahead == 'i':
        match('i')
        match('l')
    elif lookahead == 'c':
        match('c')
    elif lookahead == 'g':
        match('g')
        parse_J()
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'q':
        match('q')
    elif lookahead == 'r':
        match('r')
    else:
        error('Unexpected token ' + lookahead + ' in D, expected one of: ' + ', '.join(['b', 'h', 't', 'p', 'k', 'a', 'e', 's', 'n', 'l', 'd', 'i', 'c', 'g', 'j', 'q', 'r']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in E')
    lookahead = tokens[pos]
    if lookahead == 'h':
        match('h')
        match('i')
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'q':
        match('q')
        match('f')
        match('a')
    else:
        error('Unexpected token ' + lookahead + ' in E, expected one of: ' + ', '.join(['h', 'j', 'q']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in F')
    lookahead = tokens[pos]
    if lookahead == 'i':
        match('i')
        match('e')
        parse_K()
    elif lookahead == 'k':
        match('k')
        parse_J()
    elif lookahead == 'r':
        match('r')
    elif lookahead == 'c':
        match('c')
        parse_C()
        match('t')
    elif lookahead == 'b':
        match('b')
        parse_L()
        parse_E()
    elif lookahead == 'p':
        match('p')
    elif lookahead == 'l':
        match('l')
        match('d')
        parse_S()
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'a':
        match('a')
        match('q')
        match('e')
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'm':
        match('m')
        match('f')
        match('n')
    else:
        error('Unexpected token ' + lookahead + ' in F, expected one of: ' + ', '.join(['i', 'k', 'r', 'c', 'b', 'p', 'l', 'e', 'a', 'g', 'm']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in G')
    lookahead = tokens[pos]
    if lookahead == 'g':
        match('g')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'r':
        match('r')
        match('p')
    elif lookahead == 'j':
        match('j')
        parse_P()
        match('d')
    else:
        error('Unexpected token ' + lookahead + ' in G, expected one of: ' + ', '.join(['g', 'd', 'r', 'j']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in H')
    lookahead = tokens[pos]
    if lookahead == 'g':
        match('g')
    elif lookahead == 'i':
        match('i')
    else:
        error('Unexpected token ' + lookahead + ' in H, expected one of: ' + ', '.join(['g', 'i']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in I')
    lookahead = tokens[pos]
    if lookahead == 'o':
        match('o')
        parse_L()
        parse_G()
    elif lookahead == 'q':
        match('q')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'k':
        match('k')
        match('t')
    elif lookahead == 'n':
        match('n')
        match('k')
    elif lookahead == 'c':
        match('c')
        parse_D()
    else:
        error('Unexpected token ' + lookahead + ' in I, expected one of: ' + ', '.join(['o', 'q', 'd', 'k', 'n', 'c']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in J')
    lookahead = tokens[pos]
    if lookahead == 'p':
        match('p')
    elif lookahead == 'h':
        match('h')
        parse_A()
        parse_T()
    elif lookahead == 'e':
        match('e')
        match('m')
        match('s')
    else:
        error('Unexpected token ' + lookahead + ' in J, expected one of: ' + ', '.join(['p', 'h', 'e']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in K')
    lookahead = tokens[pos]
    if lookahead == 'b':
        match('b')
        match('d')
        parse_S()
    elif lookahead == 'o':
        match('o')
        match('s')
        parse_E()
    elif lookahead == 'n':
        match('n')
        match('h')
    elif lookahead == 'r':
        match('r')
        match('p')
    elif lookahead == 't':
        match('t')
        parse_R()
        parse_P()
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'p':
        match('p')
        match('d')
    elif lookahead == 'a':
        match('a')
        match('i')
    elif lookahead == 'q':
        match('q')
        parse_F()
    elif lookahead == 'k':
        match('k')
        parse_C()
        parse_O()
    elif lookahead == 'i':
        match('i')
        parse_T()
        parse_N()
    elif lookahead == 'h':
        match('h')
        match('o')
        parse_R()
    else:
        error('Unexpected token ' + lookahead + ' in K, expected one of: ' + ', '.join(['b', 'o', 'n', 'r', 't', 'f', 'p', 'a', 'q', 'k', 'i', 'h']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in L')
    lookahead = tokens[pos]
    if lookahead == 'k':
        match('k')
    elif lookahead == 'e':
        match('e')
        match('g')
        parse_E()
    elif lookahead == 'b':
        match('b')
        parse_A()
        parse_G()
    elif lookahead == 'n':
        match('n')
        match('m')
        match('t')
    elif lookahead == 't':
        match('t')
        parse_O()
        match('m')
    elif lookahead == 'h':
        match('h')
    elif lookahead == 's':
        match('s')
        match('l')
    elif lookahead == 'o':
        match('o')
        parse_E()
        match('n')
    elif lookahead == 'm':
        match('m')
        match('b')
        match('r')
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'q':
        match('q')
    elif lookahead == 'c':
        match('c')
        parse_M()
    elif lookahead == 'p':
        match('p')
        match('m')
        match('o')
    elif lookahead == 'r':
        match('r')
        match('k')
    elif lookahead == 'a':
        match('a')
        parse_B()
        parse_N()
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'f':
        match('f')
        match('i')
        parse_L()
    elif lookahead == 'l':
        match('l')
        parse_H()
        parse_T()
    elif lookahead == 'd':
        match('d')
        match('k')
    elif lookahead == 'j':
        match('j')
    else:
        error('Unexpected token ' + lookahead + ' in L, expected one of: ' + ', '.join(['k', 'e', 'b', 'n', 't', 'h', 's', 'o', 'm', 'g', 'q', 'c', 'p', 'r', 'a', 'i', 'f', 'l', 'd', 'j']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in M')
    lookahead = tokens[pos]
    if lookahead == 'f':
        match('f')
        parse_R()
    elif lookahead == 'l':
        match('l')
    elif lookahead == 'c':
        match('c')
        parse_D()
    elif lookahead == 'n':
        match('n')
    elif lookahead == 'e':
        match('e')
        parse_F()
        match('n')
    elif lookahead == 'd':
        match('d')
    else:
        error('Unexpected token ' + lookahead + ' in M, expected one of: ' + ', '.join(['f', 'l', 'c', 'n', 'e', 'd']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in N')
    lookahead = tokens[pos]
    if lookahead == 'f':
        match('f')
        parse_P()
        match('c')
    elif lookahead == 's':
        match('s')
    elif lookahead == 't':
        match('t')
        match('f')
        parse_L()
    elif lookahead == 'h':
        match('h')
        parse_S()
        match('c')
    elif lookahead == 'i':
        match('i')
        parse_D()
        match('o')
    elif lookahead == 'g':
        match('g')
        parse_S()
    elif lookahead == 'm':
        match('m')
        match('k')
        match('m')
    elif lookahead == 'c':
        match('c')
        parse_S()
    elif lookahead == 'a':
        match('a')
    elif lookahead == 'k':
        match('k')
        match('q')
    elif lookahead == 'j':
        match('j')
        parse_E()
    elif lookahead == 'l':
        match('l')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'n':
        match('n')
    elif lookahead == 'q':
        match('q')
    elif lookahead == 'p':
        match('p')
        parse_Q()
        parse_K()
    elif lookahead == 'b':
        match('b')
        match('h')
        match('b')
    elif lookahead == 'r':
        match('r')
        parse_A()
        parse_A()
    else:
        error('Unexpected token ' + lookahead + ' in N, expected one of: ' + ', '.join(['f', 's', 't', 'h', 'i', 'g', 'm', 'c', 'a', 'k', 'j', 'l', 'e', 'n', 'q', 'p', 'b', 'r']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in O')
    lookahead = tokens[pos]
    if lookahead == 'k':
        match('k')
        parse_C()
        parse_S()
    elif lookahead == 'n':
        match('n')
    elif lookahead == 'l':
        match('l')
        parse_F()
        match('d')
    elif lookahead == 'q':
        match('q')
        parse_I()
    elif lookahead == 'd':
        match('d')
        parse_B()
        parse_I()
    elif lookahead == 'p':
        match('p')
        match('e')
        match('t')
    elif lookahead == 'g':
        match('g')
        match('c')
        match('h')
    else:
        error('Unexpected token ' + lookahead + ' in O, expected one of: ' + ', '.join(['k', 'n', 'l', 'q', 'd', 'p', 'g']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in P')
    lookahead = tokens[pos]
    if lookahead == 'l':
        match('l')
        parse_T()
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'f':
        match('f')
        match('e')
    elif lookahead == 'n':
        match('n')
        parse_K()
    elif lookahead == 'm':
        match('m')
        match('g')
    elif lookahead == 's':
        match('s')
        match('g')
        parse_B()
    elif lookahead == 'r':
        match('r')
        match('o')
        parse_N()
    elif lookahead == 'h':
        match('h')
    elif lookahead == 'c':
        match('c')
        match('b')
        parse_L()
    elif lookahead == 't':
        match('t')
    elif lookahead == 'q':
        match('q')
        match('a')
    else:
        error('Unexpected token ' + lookahead + ' in P, expected one of: ' + ', '.join(['l', 'e', 'f', 'n', 'm', 's', 'r', 'h', 'c', 't', 'q']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in Q')
    lookahead = tokens[pos]
    if lookahead == 'p':
        match('p')
    elif lookahead == 'g':
        match('g')
        parse_I()
        parse_G()
    elif lookahead == 'c':
        match('c')
        match('h')
    elif lookahead == 'e':
        match('e')
        parse_I()
    elif lookahead == 'q':
        match('q')
        parse_R()
        match('o')
    elif lookahead == 'b':
        match('b')
        match('r')
        match('n')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'f':
        match('f')
        match('f')
        match('h')
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'r':
        match('r')
        match('o')
        match('p')
    elif lookahead == 't':
        match('t')
    else:
        error('Unexpected token ' + lookahead + ' in Q, expected one of: ' + ', '.join(['p', 'g', 'c', 'e', 'q', 'b', 'd', 'f', 'i', 'r', 't']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in R')
    lookahead = tokens[pos]
    if lookahead == 'j':
        match('j')
        match('a')
    elif lookahead == 'g':
        match('g')
        match('c')
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'k':
        match('k')
        match('k')
        match('q')
    elif lookahead == 'a':
        match('a')
        match('a')
        match('a')
    elif lookahead == 'o':
        match('o')
        match('j')
    elif lookahead == 'p':
        match('p')
        match('r')
        match('r')
    elif lookahead == 'r':
        match('r')
    elif lookahead == 's':
        match('s')
    elif lookahead == 'b':
        match('b')
    else:
        error('Unexpected token ' + lookahead + ' in R, expected one of: ' + ', '.join(['j', 'g', 'f', 'k', 'a', 'o', 'p', 'r', 's', 'b']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in S')
    lookahead = tokens[pos]
    if lookahead == 'r':
        match('r')
        parse_E()
    else:
        error('Unexpected token ' + lookahead + ' in S, expected one of: ' + ', '.join(['r']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in T')
    lookahead = tokens[pos]
    if lookahead == 'p':
        match('p')
    elif lookahead == 'h':
        match('h')
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'm':
        match('m')
        match('f')
    elif lookahead == 'q':
        match('q')
        parse_D()
        parse_K()
    elif lookahead == 'e':
        match('e')
        parse_I()
        match('f')
    elif lookahead == 'i':
        match('i')
    elif lookahead == 's':
        match('s')
        match('c')
    elif lookahead == 'r':
        match('r')
    elif lookahead == 'a':
        match('a')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'c':
        match('c')
        parse_B()
        parse_N()
    elif lookahead == 'f':
        match('f')
        match('q')
        parse_N()
    elif lookahead == 'o':
        match('o')
    elif lookahead == 'n':
        match('n')
        match('o')
    elif lookahead == 'l':
        match('l')
    else:
        error('Unexpected token ' + lookahead + ' in T, expected one of: ' + ', '.join(['p', 'h', 'j', 'm', 'q', 'e', 'i', 's', 'r', 'a', 'd', 'c', 'f', 'o', 'n', 'l']))

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