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
        parse_E()
    elif lookahead == 'n':
        match('n')
        parse_L()
        match('e')
    elif lookahead == 'm':
        match('m')
        match('k')
        parse_J()
    elif lookahead == 'f':
        match('f')
        match('g')
    elif lookahead == 'e':
        match('e')
        match('f')
    elif lookahead == 'r':
        match('r')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'a':
        match('a')
    elif lookahead == 'b':
        match('b')
        parse_N()
    elif lookahead == 'l':
        match('l')
        match('b')
        parse_J()
    elif lookahead == 'i':
        match('i')
        parse_C()
        parse_N()
    elif lookahead == 'q':
        match('q')
    elif lookahead == 'g':
        match('g')
        match('q')
        match('p')
    elif lookahead == 's':
        match('s')
        match('e')
        match('s')
    else:
        error('Unexpected token ' + lookahead + ' in A, expected one of: ' + ', '.join(['h', 'n', 'm', 'f', 'e', 'r', 'd', 'a', 'b', 'l', 'i', 'q', 'g', 's']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in B')
    lookahead = tokens[pos]
    if lookahead == 'b':
        match('b')
        match('q')
        match('t')
    elif lookahead == 'c':
        match('c')
    elif lookahead == 'l':
        match('l')
    elif lookahead == 'n':
        match('n')
    elif lookahead == 'r':
        match('r')
    elif lookahead == 'h':
        match('h')
        parse_L()
    else:
        error('Unexpected token ' + lookahead + ' in B, expected one of: ' + ', '.join(['b', 'c', 'l', 'n', 'r', 'h']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in C')
    lookahead = tokens[pos]
    if lookahead == 'm':
        match('m')
        parse_C()
        match('t')
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'b':
        match('b')
        parse_K()
    elif lookahead == 'n':
        match('n')
        parse_P()
    elif lookahead == 'r':
        match('r')
        match('g')
        match('j')
    elif lookahead == 'o':
        match('o')
        match('l')
        match('c')
    elif lookahead == 'd':
        match('d')
        parse_L()
        match('m')
    elif lookahead == 'f':
        match('f')
        match('b')
    elif lookahead == 'h':
        match('h')
        match('p')
    elif lookahead == 's':
        match('s')
    elif lookahead == 'c':
        match('c')
        match('k')
        match('p')
    elif lookahead == 'i':
        match('i')
        parse_H()
        match('s')
    elif lookahead == 'j':
        match('j')
        match('o')
        match('t')
    elif lookahead == 'k':
        match('k')
        parse_M()
    elif lookahead == 't':
        match('t')
    elif lookahead == 'q':
        match('q')
    else:
        error('Unexpected token ' + lookahead + ' in C, expected one of: ' + ', '.join(['m', 'g', 'b', 'n', 'r', 'o', 'd', 'f', 'h', 's', 'c', 'i', 'j', 'k', 't', 'q']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in D')
    lookahead = tokens[pos]
    if lookahead == 'h':
        match('h')
    elif lookahead == 'n':
        match('n')
        match('t')
        parse_S()
    elif lookahead == 't':
        match('t')
        parse_C()
    elif lookahead == 'a':
        match('a')
        match('r')
        match('h')
    elif lookahead == 'q':
        match('q')
        match('q')
        match('o')
    elif lookahead == 'j':
        match('j')
        match('j')
    elif lookahead == 'f':
        match('f')
        match('l')
    elif lookahead == 'o':
        match('o')
        match('n')
        match('q')
    elif lookahead == 'p':
        match('p')
    elif lookahead == 'l':
        match('l')
        parse_G()
        match('r')
    elif lookahead == 'k':
        match('k')
    elif lookahead == 'd':
        match('d')
        match('g')
    elif lookahead == 'm':
        match('m')
        parse_S()
        parse_M()
    elif lookahead == 'e':
        match('e')
        match('k')
        parse_T()
    elif lookahead == 'r':
        match('r')
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'c':
        match('c')
    elif lookahead == 's':
        match('s')
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'b':
        match('b')
        parse_O()
    else:
        error('Unexpected token ' + lookahead + ' in D, expected one of: ' + ', '.join(['h', 'n', 't', 'a', 'q', 'j', 'f', 'o', 'p', 'l', 'k', 'd', 'm', 'e', 'r', 'g', 'c', 's', 'i', 'b']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in E')
    lookahead = tokens[pos]
    if lookahead == 'm':
        match('m')
    elif lookahead == 'c':
        match('c')
        match('n')
        match('m')
    elif lookahead == 'l':
        match('l')
        parse_R()
        match('b')
    elif lookahead == 'h':
        match('h')
        match('c')
    elif lookahead == 'r':
        match('r')
        parse_T()
        match('f')
    elif lookahead == 'b':
        match('b')
        parse_E()
    elif lookahead == 'i':
        match('i')
        match('p')
        match('t')
    elif lookahead == 'k':
        match('k')
    elif lookahead == 'q':
        match('q')
        parse_O()
    elif lookahead == 's':
        match('s')
        match('o')
        match('p')
    elif lookahead == 'p':
        match('p')
        parse_G()
        match('j')
    else:
        error('Unexpected token ' + lookahead + ' in E, expected one of: ' + ', '.join(['m', 'c', 'l', 'h', 'r', 'b', 'i', 'k', 'q', 's', 'p']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in F')
    lookahead = tokens[pos]
    if lookahead == 'r':
        match('r')
        match('t')
        parse_N()
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'l':
        match('l')
    elif lookahead == 'k':
        match('k')
        match('a')
    elif lookahead == 'h':
        match('h')
        match('r')
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'q':
        match('q')
        match('j')
        match('d')
    elif lookahead == 'n':
        match('n')
        parse_M()
        parse_N()
    elif lookahead == 'a':
        match('a')
    elif lookahead == 'g':
        match('g')
        match('h')
    elif lookahead == 'o':
        match('o')
        match('d')
        match('i')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'm':
        match('m')
    elif lookahead == 't':
        match('t')
        parse_H()
    elif lookahead == 'j':
        match('j')
    elif lookahead == 's':
        match('s')
        parse_B()
        parse_P()
    else:
        error('Unexpected token ' + lookahead + ' in F, expected one of: ' + ', '.join(['r', 'f', 'l', 'k', 'h', 'i', 'b', 'q', 'n', 'a', 'g', 'o', 'd', 'm', 't', 'j', 's']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in G')
    lookahead = tokens[pos]
    if lookahead == 'p':
        match('p')
        match('h')
        match('r')
    elif lookahead == 'j':
        match('j')
        parse_B()
        parse_A()
    elif lookahead == 'h':
        match('h')
        parse_C()
    elif lookahead == 's':
        match('s')
    elif lookahead == 'o':
        match('o')
    elif lookahead == 'a':
        match('a')
        parse_D()
    elif lookahead == 'b':
        match('b')
        parse_Q()
        parse_M()
    elif lookahead == 'm':
        match('m')
    elif lookahead == 'i':
        match('i')
        match('m')
        parse_A()
    elif lookahead == 'g':
        match('g')
        parse_A()
    elif lookahead == 'r':
        match('r')
    elif lookahead == 'q':
        match('q')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'k':
        match('k')
        parse_G()
    elif lookahead == 'c':
        match('c')
        match('n')
    elif lookahead == 'n':
        match('n')
        parse_Q()
        match('n')
    else:
        error('Unexpected token ' + lookahead + ' in G, expected one of: ' + ', '.join(['p', 'j', 'h', 's', 'o', 'a', 'b', 'm', 'i', 'g', 'r', 'q', 'd', 'e', 'f', 'k', 'c', 'n']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in H')
    lookahead = tokens[pos]
    if lookahead == 'f':
        match('f')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'p':
        match('p')
    elif lookahead == 'h':
        match('h')
        match('t')
    elif lookahead == 'c':
        match('c')
        parse_A()
        parse_A()
    elif lookahead == 'j':
        match('j')
        match('l')
        parse_O()
    elif lookahead == 'n':
        match('n')
        match('f')
        parse_S()
    elif lookahead == 'l':
        match('l')
        parse_A()
    elif lookahead == 'r':
        match('r')
        match('g')
        match('o')
    elif lookahead == 'g':
        match('g')
    elif lookahead == 's':
        match('s')
        match('s')
    elif lookahead == 'a':
        match('a')
    else:
        error('Unexpected token ' + lookahead + ' in H, expected one of: ' + ', '.join(['f', 'e', 'p', 'h', 'c', 'j', 'n', 'l', 'r', 'g', 's', 'a']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in I')
    lookahead = tokens[pos]
    if lookahead == 'o':
        match('o')
    elif lookahead == 'h':
        match('h')
        parse_K()
        match('j')
    elif lookahead == 'k':
        match('k')
        match('e')
    elif lookahead == 't':
        match('t')
        match('c')
    elif lookahead == 'i':
        match('i')
        parse_K()
        parse_H()
    elif lookahead == 's':
        match('s')
        parse_M()
        match('s')
    elif lookahead == 'a':
        match('a')
    elif lookahead == 'l':
        match('l')
        parse_K()
        match('e')
    elif lookahead == 'f':
        match('f')
        parse_C()
    elif lookahead == 'n':
        match('n')
    elif lookahead == 'c':
        match('c')
    elif lookahead == 'q':
        match('q')
    elif lookahead == 'e':
        match('e')
        match('m')
        parse_Q()
    elif lookahead == 'm':
        match('m')
        match('m')
        match('o')
    elif lookahead == 'p':
        match('p')
    elif lookahead == 'g':
        match('g')
        match('t')
        match('i')
    elif lookahead == 'd':
        match('d')
        parse_E()
    elif lookahead == 'r':
        match('r')
        match('o')
    else:
        error('Unexpected token ' + lookahead + ' in I, expected one of: ' + ', '.join(['o', 'h', 'k', 't', 'i', 's', 'a', 'l', 'f', 'n', 'c', 'q', 'e', 'm', 'p', 'g', 'd', 'r']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in J')
    lookahead = tokens[pos]
    if lookahead == 'i':
        match('i')
    elif lookahead == 'o':
        match('o')
    elif lookahead == 'c':
        match('c')
        parse_Q()
    elif lookahead == 'k':
        match('k')
    elif lookahead == 'h':
        match('h')
        match('e')
    elif lookahead == 'n':
        match('n')
    elif lookahead == 'j':
        match('j')
        parse_G()
    elif lookahead == 'm':
        match('m')
        parse_P()
        match('m')
    elif lookahead == 'd':
        match('d')
        match('q')
        match('h')
    elif lookahead == 'g':
        match('g')
        match('t')
    elif lookahead == 'l':
        match('l')
        parse_O()
    elif lookahead == 's':
        match('s')
        match('i')
        parse_G()
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'b':
        match('b')
        match('o')
        parse_I()
    elif lookahead == 'p':
        match('p')
        parse_O()
    else:
        error('Unexpected token ' + lookahead + ' in J, expected one of: ' + ', '.join(['i', 'o', 'c', 'k', 'h', 'n', 'j', 'm', 'd', 'g', 'l', 's', 'f', 'b', 'p']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in K')
    lookahead = tokens[pos]
    if lookahead == 'm':
        match('m')
        parse_S()
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'a':
        match('a')
    elif lookahead == 't':
        match('t')
        match('d')
        parse_D()
    elif lookahead == 'q':
        match('q')
        parse_P()
        match('a')
    elif lookahead == 'h':
        match('h')
    elif lookahead == 'j':
        match('j')
    else:
        error('Unexpected token ' + lookahead + ' in K, expected one of: ' + ', '.join(['m', 'd', 'a', 't', 'q', 'h', 'j']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in L')
    lookahead = tokens[pos]
    if lookahead == 'h':
        match('h')
        parse_I()
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'r':
        match('r')
        parse_N()
        match('g')
    elif lookahead == 'm':
        match('m')
        parse_B()
        parse_P()
    elif lookahead == 'o':
        match('o')
        match('s')
        parse_M()
    elif lookahead == 'n':
        match('n')
        parse_K()
        parse_C()
    elif lookahead == 'l':
        match('l')
        parse_M()
    elif lookahead == 'q':
        match('q')
        match('s')
        match('s')
    elif lookahead == 'f':
        match('f')
    elif lookahead == 't':
        match('t')
        match('j')
    elif lookahead == 'b':
        match('b')
    else:
        error('Unexpected token ' + lookahead + ' in L, expected one of: ' + ', '.join(['h', 'e', 'r', 'm', 'o', 'n', 'l', 'q', 'f', 't', 'b']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in M')
    lookahead = tokens[pos]
    if lookahead == 'a':
        match('a')
    elif lookahead == 't':
        match('t')
        match('b')
        match('i')
    elif lookahead == 'p':
        match('p')
    elif lookahead == 'f':
        match('f')
        parse_R()
        match('t')
    elif lookahead == 'k':
        match('k')
        match('d')
    elif lookahead == 'h':
        match('h')
        match('r')
    else:
        error('Unexpected token ' + lookahead + ' in M, expected one of: ' + ', '.join(['a', 't', 'p', 'f', 'k', 'h']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in N')
    lookahead = tokens[pos]
    if lookahead == 'a':
        match('a')
    elif lookahead == 'q':
        match('q')
        parse_S()
    elif lookahead == 'g':
        match('g')
        parse_N()
    elif lookahead == 's':
        match('s')
    elif lookahead == 'l':
        match('l')
        match('c')
    elif lookahead == 'p':
        match('p')
        match('t')
        parse_C()
    else:
        error('Unexpected token ' + lookahead + ' in N, expected one of: ' + ', '.join(['a', 'q', 'g', 's', 'l', 'p']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in O')
    lookahead = tokens[pos]
    if lookahead == 'f':
        match('f')
    elif lookahead == 'd':
        match('d')
        parse_Q()
        match('q')
    elif lookahead == 'i':
        match('i')
    else:
        error('Unexpected token ' + lookahead + ' in O, expected one of: ' + ', '.join(['f', 'd', 'i']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in P')
    lookahead = tokens[pos]
    if lookahead == 'n':
        match('n')
    else:
        error('Unexpected token ' + lookahead + ' in P, expected one of: ' + ', '.join(['n']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in Q')
    lookahead = tokens[pos]
    if lookahead == 'q':
        match('q')
    elif lookahead == 'k':
        match('k')
        parse_M()
    elif lookahead == 's':
        match('s')
    elif lookahead == 'f':
        match('f')
        match('o')
        parse_T()
    elif lookahead == 'm':
        match('m')
        parse_N()
    elif lookahead == 'j':
        match('j')
        match('h')
    elif lookahead == 'e':
        match('e')
        match('f')
    elif lookahead == 'd':
        match('d')
        match('f')
        parse_Q()
    elif lookahead == 'p':
        match('p')
        parse_J()
    elif lookahead == 'l':
        match('l')
        match('i')
    elif lookahead == 'r':
        match('r')
        match('c')
    elif lookahead == 'i':
        match('i')
        parse_E()
    elif lookahead == 'g':
        match('g')
        parse_E()
        match('m')
    elif lookahead == 'a':
        match('a')
        parse_A()
        match('l')
    else:
        error('Unexpected token ' + lookahead + ' in Q, expected one of: ' + ', '.join(['q', 'k', 's', 'f', 'm', 'j', 'e', 'd', 'p', 'l', 'r', 'i', 'g', 'a']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in R')
    lookahead = tokens[pos]
    if lookahead == 'n':
        match('n')
        parse_Q()
    elif lookahead == 'p':
        match('p')
        match('g')
        match('n')
    elif lookahead == 'c':
        match('c')
        match('d')
    elif lookahead == 'k':
        match('k')
        match('o')
    elif lookahead == 'f':
        match('f')
        match('f')
        parse_C()
    elif lookahead == 'm':
        match('m')
    else:
        error('Unexpected token ' + lookahead + ' in R, expected one of: ' + ', '.join(['n', 'p', 'c', 'k', 'f', 'm']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in S')
    lookahead = tokens[pos]
    if lookahead == 'l':
        match('l')
        match('g')
    elif lookahead == 'r':
        match('r')
    elif lookahead == 'i':
        match('i')
        parse_P()
    elif lookahead == 'n':
        match('n')
    elif lookahead == 's':
        match('s')
        parse_H()
        match('t')
    elif lookahead == 'p':
        match('p')
    elif lookahead == 'b':
        match('b')
        parse_F()
    elif lookahead == 'k':
        match('k')
        match('b')
        match('f')
    elif lookahead == 't':
        match('t')
        match('k')
        match('t')
    elif lookahead == 'm':
        match('m')
        match('h')
    elif lookahead == 'q':
        match('q')
        match('i')
        match('r')
    elif lookahead == 'e':
        match('e')
        parse_F()
    elif lookahead == 'o':
        match('o')
    else:
        error('Unexpected token ' + lookahead + ' in S, expected one of: ' + ', '.join(['l', 'r', 'i', 'n', 's', 'p', 'b', 'k', 't', 'm', 'q', 'e', 'o']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in T')
    lookahead = tokens[pos]
    if lookahead == 'f':
        match('f')
    elif lookahead == 'q':
        match('q')
        match('m')
        parse_I()
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'i':
        match('i')
        parse_E()
    elif lookahead == 'a':
        match('a')
    elif lookahead == 'h':
        match('h')
        parse_I()
        match('t')
    elif lookahead == 'b':
        match('b')
        match('t')
    elif lookahead == 'l':
        match('l')
        parse_S()
        parse_S()
    elif lookahead == 'k':
        match('k')
        match('s')
        parse_M()
    elif lookahead == 't':
        match('t')
    elif lookahead == 'o':
        match('o')
        parse_T()
        parse_N()
    elif lookahead == 'm':
        match('m')
        match('g')
        match('c')
    elif lookahead == 'd':
        match('d')
        match('s')
    elif lookahead == 's':
        match('s')
        parse_P()
        parse_I()
    elif lookahead == 'e':
        match('e')
        parse_C()
    else:
        error('Unexpected token ' + lookahead + ' in T, expected one of: ' + ', '.join(['f', 'q', 'j', 'i', 'a', 'h', 'b', 'l', 'k', 't', 'o', 'm', 'd', 's', 'e']))

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