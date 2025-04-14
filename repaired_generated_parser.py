import sys

class Token:

    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f'Token({{self.type}}, {{self.value}})'

class Lexer:

    def __init__(self, token_rules):
        self.token_rules = []
        for token_type, pattern in token_rules:
            if pattern.endswith('+'):
                self.token_rules.append((token_type, pattern[:-1], 'repeat'))
            else:
                self.token_rules.append((token_type, pattern, 'exact'))

    def tokenize(self, text):
        pos = 0
        tokens = []
        while pos < len(text):
            if text[pos].isspace():
                pos += 1
                continue
            match_found = False
            for token_type, literal, match_type in self.token_rules:
                if match_type == 'exact':
                    if text.startswith(literal, pos):
                        tokens.append(Token(token_type, literal))
                        pos += len(literal)
                        match_found = True
                        break
                elif text[pos] == literal:
                    start = pos
                    while pos < len(text) and text[pos] == literal:
                        pos += 1
                    tokens.append(Token(token_type, text[start:pos]))
                    match_found = True
                    break
            if not match_found:
                error("Lexer error: Unexpected character '{}' at position {}".format(text[pos], pos))
        return tokens
token_rules = [('a', 'a'), ('b', 'b+'), ('c', 'c'), ('d', 'd'), ('e', 'e+'), ('f', 'f+'), ('g', 'g+'), ('h', 'h+'), ('i', 'i+'), ('j', 'j'), ('k', 'k'), ('l', 'l'), ('m', 'm'), ('n', 'n'), ('o', 'o'), ('p', 'p'), ('q', 'q+'), ('r', 'r'), ('s', 's'), ('t', 't')]
lexer = Lexer(token_rules)
tokens = []
pos = 0

def error(msg):
    print('Parse error:', msg)
    sys.exit(1)

def match(expected):
    global pos, tokens
    if pos < len(tokens) and tokens[pos].type == expected:
        pos += 1
    else:
        current = tokens[pos].value if pos < len(tokens) else 'EOF'
        error(f"Expected token type '{expected}', got {current}")

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in A')
    lookahead = tokens[pos].type
    if lookahead == 'k':
        match('k')
        parse_P()
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'q':
        match('q')
        match('k')
    elif lookahead == 'h':
        match('h')
        match('g')
    elif lookahead == 'o':
        match('o')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'm':
        match('m')
    elif lookahead == 'f':
        match('f')
        match('j')
        match('c')
    elif lookahead == 'l':
        match('l')
    elif lookahead == 'r':
        match('r')
        parse_G()
        match('q')
    elif lookahead == 'a':
        match('a')
    elif lookahead == 't':
        match('t')
    elif lookahead == 'c':
        match('c')
        match('m')
        match('k')
    elif lookahead == 'n':
        match('n')
        parse_G()
    elif lookahead == 's':
        match('s')
        parse_N()
        match('e')
    elif lookahead == 'g':
        match('g')
        parse_T()
    elif lookahead == 'p':
        match('p')
        parse_A()
        match('d')
    elif lookahead == 'd':
        match('d')
        parse_P()
    elif lookahead == 'j':
        match('j')
        parse_O()
    elif lookahead == 'i':
        match('i')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in A, expected one of: ' + ', '.join(['k', 'b', 'q', 'h', 'o', 'e', 'm', 'f', 'l', 'r', 'a', 't', 'c', 'n', 's', 'g', 'p', 'd', 'j', 'i']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in B')
    lookahead = tokens[pos].type
    if lookahead == 'e':
        match('e')
        parse_C()
        parse_P()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in B, expected one of: ' + ', '.join(['e']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in C')
    lookahead = tokens[pos].type
    if lookahead == 'd':
        match('d')
    elif lookahead == 'o':
        match('o')
        parse_D()
        parse_O()
    elif lookahead == 'r':
        match('r')
        parse_N()
        parse_S()
    elif lookahead == 'e':
        match('e')
        parse_L()
        match('i')
    elif lookahead == 'n':
        match('n')
        match('n')
        parse_Q()
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'k':
        match('k')
        parse_K()
        match('n')
    elif lookahead == 'c':
        match('c')
        match('o')
        parse_C()
    elif lookahead == 'p':
        match('p')
    elif lookahead == 't':
        match('t')
    elif lookahead == 'b':
        match('b')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in C, expected one of: ' + ', '.join(['d', 'o', 'r', 'e', 'n', 'j', 'k', 'c', 'p', 't', 'b']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in D')
    lookahead = tokens[pos].type
    if lookahead == 'f':
        match('f')
        match('h')
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'h':
        match('h')
        match('j')
        parse_K()
    elif lookahead == 'r':
        match('r')
        match('k')
    elif lookahead == 'g':
        match('g')
    elif lookahead == 't':
        match('t')
        parse_R()
    elif lookahead == 'a':
        match('a')
        match('o')
        parse_D()
    elif lookahead == 'p':
        match('p')
    elif lookahead == 'b':
        match('b')
        parse_L()
        parse_N()
    elif lookahead == 'd':
        match('d')
        parse_K()
    elif lookahead == 'n':
        match('n')
        match('d')
    elif lookahead == 'm':
        match('m')
        parse_N()
        parse_P()
    elif lookahead == 'c':
        match('c')
    elif lookahead == 'l':
        match('l')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in D, expected one of: ' + ', '.join(['f', 'i', 'h', 'r', 'g', 't', 'a', 'p', 'b', 'd', 'n', 'm', 'c', 'l']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in E')
    lookahead = tokens[pos].type
    if lookahead == 'g':
        match('g')
        parse_P()
    elif lookahead == 'q':
        match('q')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in E, expected one of: ' + ', '.join(['g', 'q']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in F')
    lookahead = tokens[pos].type
    if lookahead == 'a':
        match('a')
    elif lookahead == 'n':
        match('n')
        parse_Q()
    elif lookahead == 'r':
        match('r')
        match('a')
        match('r')
    elif lookahead == 's':
        match('s')
    elif lookahead == 'd':
        match('d')
        parse_J()
        parse_C()
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'e':
        match('e')
        match('b')
        parse_G()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in F, expected one of: ' + ', '.join(['a', 'n', 'r', 's', 'd', 'i', 'e']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in G')
    lookahead = tokens[pos].type
    if lookahead == 'r':
        match('r')
        match('b')
    elif lookahead == 'd':
        match('d')
        parse_P()
    elif lookahead == 's':
        match('s')
        parse_Q()
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'm':
        match('m')
        parse_C()
    elif lookahead == 'c':
        match('c')
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'e':
        match('e')
        parse_R()
        match('c')
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'k':
        match('k')
        parse_Q()
        parse_E()
    elif lookahead == 'n':
        match('n')
    elif lookahead == 'f':
        match('f')
        parse_S()
        match('k')
    elif lookahead == 'p':
        match('p')
        parse_P()
    elif lookahead == 'h':
        match('h')
        match('r')
        parse_R()
    elif lookahead == 'a':
        match('a')
        match('h')
    elif lookahead == 'q':
        match('q')
    elif lookahead == 't':
        match('t')
        match('b')
    elif lookahead == 'o':
        match('o')
    elif lookahead == 'l':
        match('l')
        parse_E()
    elif lookahead == 'b':
        match('b')
        match('t')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in G, expected one of: ' + ', '.join(['r', 'd', 's', 'j', 'm', 'c', 'g', 'e', 'i', 'k', 'n', 'f', 'p', 'h', 'a', 'q', 't', 'o', 'l', 'b']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in H')
    lookahead = tokens[pos].type
    if lookahead == 'h':
        match('h')
    elif lookahead == 't':
        match('t')
        parse_I()
    elif lookahead == 'b':
        match('b')
        parse_Q()
    elif lookahead == 'c':
        match('c')
        parse_C()
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'o':
        match('o')
    elif lookahead == 'q':
        match('q')
        parse_S()
    elif lookahead == 'j':
        match('j')
        parse_Q()
    elif lookahead == 'r':
        match('r')
        match('b')
        parse_F()
    elif lookahead == 'a':
        match('a')
        match('s')
        match('a')
    elif lookahead == 's':
        match('s')
        match('k')
    elif lookahead == 'n':
        match('n')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in H, expected one of: ' + ', '.join(['h', 't', 'b', 'c', 'd', 'o', 'q', 'j', 'r', 'a', 's', 'n']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in I')
    lookahead = tokens[pos].type
    if lookahead == 'e':
        match('e')
    elif lookahead == 't':
        match('t')
    elif lookahead == 'b':
        match('b')
        match('i')
        parse_J()
    elif lookahead == 'm':
        match('m')
        parse_L()
    elif lookahead == 's':
        match('s')
        parse_I()
        match('c')
    elif lookahead == 'k':
        match('k')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in I, expected one of: ' + ', '.join(['e', 't', 'b', 'm', 's', 'k']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in J')
    lookahead = tokens[pos].type
    if lookahead == 'g':
        match('g')
    elif lookahead == 't':
        match('t')
        match('e')
    elif lookahead == 'k':
        match('k')
        match('i')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in J, expected one of: ' + ', '.join(['g', 't', 'k']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in K')
    lookahead = tokens[pos].type
    if lookahead == 'f':
        match('f')
    elif lookahead == 'm':
        match('m')
        match('l')
        parse_M()
    elif lookahead == 'o':
        match('o')
        parse_P()
        parse_Q()
    elif lookahead == 't':
        match('t')
        parse_A()
        parse_A()
    elif lookahead == 'd':
        match('d')
        parse_J()
        parse_P()
    elif lookahead == 'h':
        match('h')
        match('k')
        parse_G()
    elif lookahead == 'i':
        match('i')
        parse_T()
    elif lookahead == 'r':
        match('r')
        parse_G()
        match('c')
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'q':
        match('q')
        match('h')
        match('e')
    elif lookahead == 'c':
        match('c')
        parse_B()
        parse_R()
    elif lookahead == 'e':
        match('e')
        match('j')
        parse_R()
    elif lookahead == 'l':
        match('l')
    elif lookahead == 'n':
        match('n')
    elif lookahead == 'b':
        match('b')
        match('l')
        parse_R()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in K, expected one of: ' + ', '.join(['f', 'm', 'o', 't', 'd', 'h', 'i', 'r', 'g', 'q', 'c', 'e', 'l', 'n', 'b']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in L')
    lookahead = tokens[pos].type
    if lookahead == 'o':
        match('o')
    elif lookahead == 'i':
        match('i')
        match('n')
    elif lookahead == 'l':
        match('l')
        match('o')
    elif lookahead == 'j':
        match('j')
        parse_Q()
        match('f')
    elif lookahead == 'n':
        match('n')
        match('a')
        parse_N()
    elif lookahead == 'c':
        match('c')
    elif lookahead == 'm':
        match('m')
        match('k')
    elif lookahead == 'd':
        match('d')
        parse_L()
        parse_S()
    elif lookahead == 'g':
        match('g')
        parse_A()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in L, expected one of: ' + ', '.join(['o', 'i', 'l', 'j', 'n', 'c', 'm', 'd', 'g']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in M')
    lookahead = tokens[pos].type
    if lookahead == 'b':
        match('b')
        match('k')
        match('q')
    elif lookahead == 'n':
        match('n')
        parse_B()
    elif lookahead == 'h':
        match('h')
        parse_J()
    elif lookahead == 'k':
        match('k')
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'f':
        match('f')
        match('d')
    elif lookahead == 'a':
        match('a')
        match('n')
        match('n')
    elif lookahead == 'o':
        match('o')
        parse_C()
        parse_C()
    elif lookahead == 'm':
        match('m')
        match('i')
        match('t')
    elif lookahead == 't':
        match('t')
    elif lookahead == 'd':
        match('d')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in M, expected one of: ' + ', '.join(['b', 'n', 'h', 'k', 'i', 'f', 'a', 'o', 'm', 't', 'd']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in N')
    lookahead = tokens[pos].type
    if lookahead == 'c':
        match('c')
        match('d')
    elif lookahead == 'k':
        match('k')
    elif lookahead == 'g':
        match('g')
        parse_J()
    elif lookahead == 't':
        match('t')
        match('p')
        match('n')
    elif lookahead == 'a':
        match('a')
        parse_H()
        match('a')
    elif lookahead == 'h':
        match('h')
        match('t')
        match('n')
    elif lookahead == 'b':
        match('b')
        parse_I()
    elif lookahead == 'l':
        match('l')
    elif lookahead == 'n':
        match('n')
        parse_E()
        parse_E()
    elif lookahead == 'o':
        match('o')
        parse_L()
    elif lookahead == 'j':
        match('j')
        parse_I()
        parse_T()
    elif lookahead == 'p':
        match('p')
        parse_F()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in N, expected one of: ' + ', '.join(['c', 'k', 'g', 't', 'a', 'h', 'b', 'l', 'n', 'o', 'j', 'p']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in O')
    lookahead = tokens[pos].type
    if lookahead == 'l':
        match('l')
        parse_G()
        match('m')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in O, expected one of: ' + ', '.join(['l']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in P')
    lookahead = tokens[pos].type
    if lookahead == 'b':
        match('b')
        match('l')
        match('n')
    elif lookahead == 'q':
        match('q')
        parse_H()
        parse_G()
    elif lookahead == 'j':
        match('j')
        match('b')
    elif lookahead == 'o':
        match('o')
    elif lookahead == 'r':
        match('r')
        parse_B()
    elif lookahead == 'l':
        match('l')
        parse_L()
        parse_D()
    elif lookahead == 'e':
        match('e')
        parse_F()
    elif lookahead == 'p':
        match('p')
    elif lookahead == 'c':
        match('c')
        parse_O()
    elif lookahead == 'd':
        match('d')
        parse_B()
    elif lookahead == 't':
        match('t')
    elif lookahead == 'k':
        match('k')
        match('o')
    elif lookahead == 'h':
        match('h')
        match('l')
    elif lookahead == 'f':
        match('f')
        parse_I()
    elif lookahead == 'n':
        match('n')
        parse_L()
    elif lookahead == 's':
        match('s')
    elif lookahead == 'a':
        match('a')
        parse_G()
    elif lookahead == 'm':
        match('m')
        match('a')
        parse_G()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in P, expected one of: ' + ', '.join(['b', 'q', 'j', 'o', 'r', 'l', 'e', 'p', 'c', 'd', 't', 'k', 'h', 'f', 'n', 's', 'a', 'm']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in Q')
    lookahead = tokens[pos].type
    if lookahead == 'q':
        match('q')
        match('o')
    elif lookahead == 'l':
        match('l')
    elif lookahead == 'c':
        match('c')
        match('i')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'h':
        match('h')
        match('f')
        parse_J()
    elif lookahead == 'p':
        match('p')
        parse_K()
    elif lookahead == 'b':
        match('b')
        parse_Q()
    elif lookahead == 'r':
        match('r')
        match('d')
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'k':
        match('k')
        match('p')
    elif lookahead == 't':
        match('t')
    elif lookahead == 'o':
        match('o')
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'm':
        match('m')
        parse_M()
        match('m')
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'j':
        match('j')
        match('e')
        match('a')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in Q, expected one of: ' + ', '.join(['q', 'l', 'c', 'd', 'h', 'p', 'b', 'r', 'g', 'k', 't', 'o', 'i', 'm', 'f', 'j']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in R')
    lookahead = tokens[pos].type
    if lookahead == 'k':
        match('k')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'q':
        match('q')
        parse_S()
        parse_R()
    elif lookahead == 'o':
        match('o')
        parse_A()
        parse_S()
    elif lookahead == 'g':
        match('g')
        match('h')
    elif lookahead == 't':
        match('t')
        match('m')
    elif lookahead == 'm':
        match('m')
        parse_P()
        parse_O()
    elif lookahead == 'i':
        match('i')
        parse_O()
        parse_L()
    elif lookahead == 'n':
        match('n')
    elif lookahead == 'p':
        match('p')
        match('r')
    elif lookahead == 'r':
        match('r')
        match('i')
        parse_Q()
    elif lookahead == 'a':
        match('a')
        match('e')
    elif lookahead == 'c':
        match('c')
        match('r')
    elif lookahead == 'j':
        match('j')
    elif lookahead == 's':
        match('s')
        match('j')
        parse_I()
    elif lookahead == 'f':
        match('f')
        parse_H()
        match('m')
    elif lookahead == 'l':
        match('l')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in R, expected one of: ' + ', '.join(['k', 'e', 'b', 'q', 'o', 'g', 't', 'm', 'i', 'n', 'p', 'r', 'a', 'c', 'j', 's', 'f', 'l']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in S')
    lookahead = tokens[pos].type
    if lookahead == 'l':
        match('l')
        parse_D()
        parse_F()
    elif lookahead == 'k':
        match('k')
        match('d')
        parse_L()
    elif lookahead == 's':
        match('s')
        match('a')
        parse_I()
    elif lookahead == 'c':
        match('c')
        match('h')
        match('t')
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'n':
        match('n')
    elif lookahead == 't':
        match('t')
        parse_F()
    elif lookahead == 'b':
        match('b')
        match('c')
        parse_P()
    elif lookahead == 'r':
        match('r')
        match('o')
        parse_B()
    elif lookahead == 'q':
        match('q')
        parse_S()
    elif lookahead == 'h':
        match('h')
        parse_J()
        match('t')
    elif lookahead == 'f':
        match('f')
        parse_E()
        parse_M()
    elif lookahead == 'm':
        match('m')
        parse_G()
    elif lookahead == 'o':
        match('o')
        parse_L()
    elif lookahead == 'e':
        match('e')
        parse_I()
        parse_F()
    elif lookahead == 'j':
        match('j')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in S, expected one of: ' + ', '.join(['l', 'k', 's', 'c', 'i', 'g', 'n', 't', 'b', 'r', 'q', 'h', 'f', 'm', 'o', 'e', 'j']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in T')
    lookahead = tokens[pos].type
    if lookahead == 'b':
        match('b')
        match('k')
        match('q')
    elif lookahead == 'c':
        match('c')
        parse_T()
        match('c')
    elif lookahead == 'h':
        match('h')
        parse_S()
        match('c')
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'f':
        match('f')
        parse_O()
        parse_P()
    elif lookahead == 'k':
        match('k')
        match('p')
    elif lookahead == 'g':
        match('g')
        match('k')
    elif lookahead == 'r':
        match('r')
    elif lookahead == 'm':
        match('m')
        parse_I()
        parse_S()
    elif lookahead == 'l':
        match('l')
        parse_E()
        match('n')
    elif lookahead == 'd':
        match('d')
        parse_Q()
    elif lookahead == 'a':
        match('a')
        match('n')
        match('f')
    elif lookahead == 'o':
        match('o')
        parse_H()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in T, expected one of: ' + ', '.join(['b', 'c', 'h', 'j', 'e', 'f', 'k', 'g', 'r', 'm', 'l', 'd', 'a', 'o']))

def parse_input(input_str):
    global tokens, pos
    try:
        tokens = lexer.tokenize(input_str)
    except Exception as e:
        error(str(e))
    pos = 0
    parse_A()
    if pos != len(tokens):
        error('Extra tokens after parsing: ' + ' '.join((token.value for token in tokens[pos:])))
    print('Input accepted.')

def main():
    import sys
    if len(sys.argv) > 1:
        input_str = sys.argv[1]
        parse_input(input_str)
    else:
        print('Usage: python generated_parser.py <input_string>')
if __name__ == '__main__':
    main()