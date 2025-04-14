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
token_rules = [('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd'), ('e', 'e'), ('f', 'f'), ('g', 'g'), ('h', 'h'), ('i', 'i+'), ('j', 'j+'), ('k', 'k'), ('l', 'l+'), ('m', 'm'), ('n', 'n+'), ('o', 'o'), ('p', 'p+'), ('q', 'q'), ('r', 'r+'), ('s', 's+'), ('t', 't+')]
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
    if lookahead == 'd':
        match('d')
        parse_H()
    elif lookahead == 'f':
        match('f')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in A, expected one of: ' + ', '.join(['d', 'f']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in B')
    lookahead = tokens[pos].type
    if lookahead == 'l':
        match('l')
        parse_H()
    elif lookahead == 'n':
        match('n')
        match('l')
    elif lookahead == 'p':
        match('p')
        match('g')
        match('l')
    elif lookahead == 'h':
        match('h')
        parse_B()
    elif lookahead == 'k':
        match('k')
        match('f')
    elif lookahead == 'j':
        match('j')
    elif lookahead == 's':
        match('s')
        parse_C()
    elif lookahead == 'o':
        match('o')
        parse_O()
    elif lookahead == 'r':
        match('r')
    elif lookahead == 'a':
        match('a')
    elif lookahead == 'i':
        match('i')
        parse_G()
    elif lookahead == 'q':
        match('q')
        parse_C()
        parse_E()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in B, expected one of: ' + ', '.join(['l', 'n', 'p', 'h', 'k', 'j', 's', 'o', 'r', 'a', 'i', 'q']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in C')
    lookahead = tokens[pos].type
    if lookahead == 't':
        match('t')
        match('q')
    elif lookahead == 'n':
        match('n')
        match('q')
    elif lookahead == 'b':
        match('b')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in C, expected one of: ' + ', '.join(['t', 'n', 'b']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in D')
    lookahead = tokens[pos].type
    if lookahead == 'm':
        match('m')
        match('p')
        match('o')
    elif lookahead == 'b':
        match('b')
        parse_H()
    elif lookahead == 'k':
        match('k')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'l':
        match('l')
        match('e')
    elif lookahead == 's':
        match('s')
        parse_F()
        parse_J()
    elif lookahead == 'g':
        match('g')
        parse_O()
    elif lookahead == 'a':
        match('a')
        match('k')
        match('p')
    elif lookahead == 'o':
        match('o')
        parse_D()
        parse_C()
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'n':
        match('n')
        parse_G()
    elif lookahead == 'r':
        match('r')
    elif lookahead == 'j':
        match('j')
        parse_O()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in D, expected one of: ' + ', '.join(['m', 'b', 'k', 'e', 'l', 's', 'g', 'a', 'o', 'f', 'n', 'r', 'j']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in E')
    lookahead = tokens[pos].type
    if lookahead == 'k':
        match('k')
        parse_O()
        match('f')
    elif lookahead == 'a':
        match('a')
        match('r')
        parse_F()
    elif lookahead == 'm':
        match('m')
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 't':
        match('t')
    elif lookahead == 'h':
        match('h')
        parse_N()
    elif lookahead == 'b':
        match('b')
        match('d')
    elif lookahead == 'c':
        match('c')
        match('a')
        parse_L()
    elif lookahead == 'r':
        match('r')
        match('g')
        match('g')
    elif lookahead == 'l':
        match('l')
    elif lookahead == 'q':
        match('q')
        match('a')
    elif lookahead == 'p':
        match('p')
        match('i')
    elif lookahead == 'n':
        match('n')
        parse_T()
        match('a')
    elif lookahead == 'o':
        match('o')
        parse_C()
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'd':
        match('d')
        parse_K()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in E, expected one of: ' + ', '.join(['k', 'a', 'm', 'j', 'e', 't', 'h', 'b', 'c', 'r', 'l', 'q', 'p', 'n', 'o', 'i', 'd']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in F')
    lookahead = tokens[pos].type
    if lookahead == 'p':
        match('p')
        match('p')
        parse_S()
    elif lookahead == 'b':
        match('b')
        match('e')
    elif lookahead == 'n':
        match('n')
        parse_D()
    elif lookahead == 's':
        match('s')
        parse_P()
    elif lookahead == 'l':
        match('l')
    elif lookahead == 'f':
        match('f')
        parse_A()
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'm':
        match('m')
        parse_C()
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'a':
        match('a')
        parse_P()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in F, expected one of: ' + ', '.join(['p', 'b', 'n', 's', 'l', 'f', 'e', 'm', 'i', 'a']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in G')
    lookahead = tokens[pos].type
    if lookahead == 'c':
        match('c')
        parse_K()
        match('n')
    elif lookahead == 'q':
        match('q')
        match('p')
    elif lookahead == 'p':
        match('p')
    elif lookahead == 'o':
        match('o')
        parse_P()
        match('s')
    elif lookahead == 'f':
        match('f')
        parse_E()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in G, expected one of: ' + ', '.join(['c', 'q', 'p', 'o', 'f']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in H')
    lookahead = tokens[pos].type
    if lookahead == 'a':
        match('a')
        parse_Q()
        parse_K()
    elif lookahead == 'q':
        match('q')
    elif lookahead == 'h':
        match('h')
    elif lookahead == 's':
        match('s')
        parse_J()
    elif lookahead == 'i':
        match('i')
        match('n')
    elif lookahead == 'r':
        match('r')
        parse_O()
    elif lookahead == 'n':
        match('n')
    elif lookahead == 'b':
        match('b')
        match('d')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in H, expected one of: ' + ', '.join(['a', 'q', 'h', 's', 'i', 'r', 'n', 'b']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in I')
    lookahead = tokens[pos].type
    if lookahead == 'n':
        match('n')
        match('d')
    elif lookahead == 'c':
        match('c')
        match('i')
    elif lookahead == 'q':
        match('q')
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'm':
        match('m')
        parse_L()
        parse_B()
    elif lookahead == 'r':
        match('r')
    elif lookahead == 'a':
        match('a')
        parse_K()
        match('i')
    elif lookahead == 'b':
        match('b')
        parse_L()
    elif lookahead == 'p':
        match('p')
    elif lookahead == 'h':
        match('h')
        match('b')
        parse_Q()
    elif lookahead == 's':
        match('s')
    elif lookahead == 'f':
        match('f')
        parse_A()
        parse_M()
    elif lookahead == 't':
        match('t')
        parse_C()
    elif lookahead == 'o':
        match('o')
        match('g')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in I, expected one of: ' + ', '.join(['n', 'c', 'q', 'g', 'm', 'r', 'a', 'b', 'p', 'h', 's', 'f', 't', 'o']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in J')
    lookahead = tokens[pos].type
    if lookahead == 'h':
        match('h')
    elif lookahead == 'd':
        match('d')
        match('b')
    elif lookahead == 's':
        match('s')
        parse_T()
        match('i')
    elif lookahead == 'i':
        match('i')
        match('l')
    elif lookahead == 'n':
        match('n')
    elif lookahead == 't':
        match('t')
        match('g')
        match('p')
    elif lookahead == 'j':
        match('j')
        parse_S()
        match('m')
    elif lookahead == 'k':
        match('k')
        parse_T()
        match('s')
    elif lookahead == 'f':
        match('f')
        parse_F()
    elif lookahead == 'm':
        match('m')
    elif lookahead == 'a':
        match('a')
        match('b')
        parse_M()
    elif lookahead == 'q':
        match('q')
        match('f')
        match('n')
    elif lookahead == 'c':
        match('c')
        match('a')
        parse_Q()
    elif lookahead == 'p':
        match('p')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in J, expected one of: ' + ', '.join(['h', 'd', 's', 'i', 'n', 't', 'j', 'k', 'f', 'm', 'a', 'q', 'c', 'p']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in K')
    lookahead = tokens[pos].type
    if lookahead == 'p':
        match('p')
        parse_A()
    elif lookahead == 'i':
        match('i')
        match('q')
        match('l')
    elif lookahead == 'o':
        match('o')
        match('h')
    elif lookahead == 'b':
        match('b')
        match('s')
    elif lookahead == 'l':
        match('l')
        parse_M()
        match('c')
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'c':
        match('c')
        match('c')
    elif lookahead == 'd':
        match('d')
        match('h')
    elif lookahead == 'j':
        match('j')
        match('f')
    elif lookahead == 'r':
        match('r')
        match('h')
    elif lookahead == 't':
        match('t')
    elif lookahead == 's':
        match('s')
    elif lookahead == 'k':
        match('k')
        match('r')
        parse_T()
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'a':
        match('a')
    elif lookahead == 'g':
        match('g')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in K, expected one of: ' + ', '.join(['p', 'i', 'o', 'b', 'l', 'f', 'c', 'd', 'j', 'r', 't', 's', 'k', 'e', 'a', 'g']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in L')
    lookahead = tokens[pos].type
    if lookahead == 'c':
        match('c')
        parse_N()
    elif lookahead == 't':
        match('t')
        parse_L()
        match('t')
    elif lookahead == 's':
        match('s')
    elif lookahead == 'g':
        match('g')
    elif lookahead == 'k':
        match('k')
        parse_F()
        parse_Q()
    elif lookahead == 'm':
        match('m')
        parse_J()
    elif lookahead == 'b':
        match('b')
        match('e')
    elif lookahead == 'r':
        match('r')
        parse_J()
        match('j')
    elif lookahead == 'h':
        match('h')
    elif lookahead == 'o':
        match('o')
        parse_T()
        parse_N()
    elif lookahead == 'q':
        match('q')
        parse_Q()
        match('b')
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'n':
        match('n')
    elif lookahead == 'a':
        match('a')
        parse_J()
    elif lookahead == 'i':
        match('i')
        match('e')
    elif lookahead == 'e':
        match('e')
        parse_H()
        parse_J()
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'p':
        match('p')
        match('q')
    elif lookahead == 'l':
        match('l')
        match('o')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in L, expected one of: ' + ', '.join(['c', 't', 's', 'g', 'k', 'm', 'b', 'r', 'h', 'o', 'q', 'f', 'n', 'a', 'i', 'e', 'd', 'j', 'p', 'l']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in M')
    lookahead = tokens[pos].type
    if lookahead == 'e':
        match('e')
    elif lookahead == 'o':
        match('o')
    elif lookahead == 'm':
        match('m')
        match('p')
    elif lookahead == 'f':
        match('f')
    elif lookahead == 's':
        match('s')
        parse_A()
        match('n')
    elif lookahead == 'b':
        match('b')
        parse_L()
        match('k')
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'h':
        match('h')
    elif lookahead == 'q':
        match('q')
        parse_G()
        match('q')
    elif lookahead == 'p':
        match('p')
        parse_H()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in M, expected one of: ' + ', '.join(['e', 'o', 'm', 'f', 's', 'b', 'i', 'h', 'q', 'p']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in N')
    lookahead = tokens[pos].type
    if lookahead == 'n':
        match('n')
        match('j')
        parse_Q()
    elif lookahead == 'b':
        match('b')
        parse_S()
        parse_I()
    elif lookahead == 'i':
        match('i')
        match('g')
        parse_O()
    elif lookahead == 's':
        match('s')
        parse_A()
    elif lookahead == 'f':
        match('f')
        parse_D()
        match('d')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'g':
        match('g')
        parse_M()
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'k':
        match('k')
        parse_F()
    elif lookahead == 'o':
        match('o')
        match('g')
        parse_E()
    elif lookahead == 'p':
        match('p')
    elif lookahead == 'h':
        match('h')
    elif lookahead == 'l':
        match('l')
        match('k')
        parse_B()
    elif lookahead == 't':
        match('t')
        match('m')
        match('n')
    elif lookahead == 'm':
        match('m')
    elif lookahead == 'q':
        match('q')
        parse_C()
        match('h')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in N, expected one of: ' + ', '.join(['n', 'b', 'i', 's', 'f', 'd', 'e', 'g', 'j', 'k', 'o', 'p', 'h', 'l', 't', 'm', 'q']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in O')
    lookahead = tokens[pos].type
    if lookahead == 'c':
        match('c')
        parse_D()
        parse_F()
    elif lookahead == 'b':
        match('b')
        match('s')
    elif lookahead == 'a':
        match('a')
        match('t')
        parse_I()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in O, expected one of: ' + ', '.join(['c', 'b', 'a']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in P')
    lookahead = tokens[pos].type
    if lookahead == 'r':
        match('r')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'i':
        match('i')
        parse_S()
        match('f')
    elif lookahead == 'p':
        match('p')
    elif lookahead == 'j':
        match('j')
        match('p')
    elif lookahead == 'n':
        match('n')
    elif lookahead == 'm':
        match('m')
        match('d')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in P, expected one of: ' + ', '.join(['r', 'e', 'i', 'p', 'j', 'n', 'm']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in Q')
    lookahead = tokens[pos].type
    if lookahead == 'i':
        match('i')
        match('q')
        parse_H()
    elif lookahead == 'd':
        match('d')
        match('p')
    elif lookahead == 'k':
        match('k')
        match('n')
        match('j')
    elif lookahead == 's':
        match('s')
        match('c')
    elif lookahead == 'e':
        match('e')
    elif lookahead == 'h':
        match('h')
    elif lookahead == 'q':
        match('q')
    elif lookahead == 'f':
        match('f')
    elif lookahead == 'c':
        match('c')
        parse_K()
    elif lookahead == 'j':
        match('j')
        parse_G()
        parse_R()
    elif lookahead == 'r':
        match('r')
    elif lookahead == 'o':
        match('o')
        match('l')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in Q, expected one of: ' + ', '.join(['i', 'd', 'k', 's', 'e', 'h', 'q', 'f', 'c', 'j', 'r', 'o']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in R')
    lookahead = tokens[pos].type
    if lookahead == 'n':
        match('n')
        parse_L()
    elif lookahead == 'i':
        match('i')
    elif lookahead == 'g':
        match('g')
        match('g')
    elif lookahead == 's':
        match('s')
        parse_D()
        parse_E()
    elif lookahead == 't':
        match('t')
        match('g')
    elif lookahead == 'r':
        match('r')
    elif lookahead == 'm':
        match('m')
    elif lookahead == 'l':
        match('l')
        match('t')
    elif lookahead == 'h':
        match('h')
        match('f')
    elif lookahead == 'd':
        match('d')
        parse_M()
        match('b')
    elif lookahead == 'p':
        match('p')
        parse_L()
        parse_A()
    elif lookahead == 'c':
        match('c')
        parse_P()
    elif lookahead == 'f':
        match('f')
        match('t')
    elif lookahead == 'o':
        match('o')
        parse_T()
        match('a')
    elif lookahead == 'b':
        match('b')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in R, expected one of: ' + ', '.join(['n', 'i', 'g', 's', 't', 'r', 'm', 'l', 'h', 'd', 'p', 'c', 'f', 'o', 'b']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in S')
    lookahead = tokens[pos].type
    if lookahead == 'r':
        match('r')
    elif lookahead == 'o':
        match('o')
    elif lookahead == 'j':
        match('j')
    elif lookahead == 'e':
        match('e')
        match('a')
        parse_N()
    elif lookahead == 'n':
        match('n')
        match('k')
    elif lookahead == 'g':
        match('g')
        parse_K()
    elif lookahead == 'h':
        match('h')
        match('i')
        match('p')
    elif lookahead == 'q':
        match('q')
        parse_K()
    elif lookahead == 'i':
        match('i')
        parse_J()
    elif lookahead == 'k':
        match('k')
        parse_J()
    elif lookahead == 'd':
        match('d')
        parse_T()
    elif lookahead == 't':
        match('t')
    elif lookahead == 's':
        match('s')
        parse_K()
        match('s')
    elif lookahead == 'c':
        match('c')
        parse_A()
        parse_D()
    elif lookahead == 'b':
        match('b')
        parse_D()
        parse_S()
    elif lookahead == 'p':
        match('p')
    elif lookahead == 'f':
        match('f')
        parse_M()
        match('a')
    elif lookahead == 'a':
        match('a')
        parse_A()
        match('c')
    elif lookahead == 'm':
        match('m')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in S, expected one of: ' + ', '.join(['r', 'o', 'j', 'e', 'n', 'g', 'h', 'q', 'i', 'k', 'd', 't', 's', 'c', 'b', 'p', 'f', 'a', 'm']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in T')
    lookahead = tokens[pos].type
    if lookahead == 'r':
        match('r')
        match('b')
    elif lookahead == 'o':
        match('o')
        match('t')
        parse_Q()
    elif lookahead == 's':
        match('s')
        match('f')
        parse_F()
    elif lookahead == 'b':
        match('b')
        match('t')
        parse_G()
    elif lookahead == 'j':
        match('j')
        parse_L()
    elif lookahead == 'l':
        match('l')
        match('t')
    elif lookahead == 'k':
        match('k')
    elif lookahead == 'm':
        match('m')
    elif lookahead == 'h':
        match('h')
        parse_O()
    elif lookahead == 'e':
        match('e')
        parse_O()
        match('c')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in T, expected one of: ' + ', '.join(['r', 'o', 's', 'b', 'j', 'l', 'k', 'm', 'h', 'e']))

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