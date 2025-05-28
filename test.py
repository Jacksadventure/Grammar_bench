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

def parse_a():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in a")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        match('[')
        match('[')
        match('=')
        match('O')
        parse_q()
    elif lookahead.startswith('*'):
        match('*')
    else:
        error("Unexpected token " + lookahead + " in a, expected one of: " + ", ".join(['/', '*']))

def parse_b():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('O'):
        match('O')
        match('5')
        match('t')
        match('#')
        match('=')
        match('5')
        match('=')
        parse_e()
        match('[')
        parse_m()

def parse_c():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in c")
    lookahead = tokens[pos]
    if lookahead.startswith('T'):
        match('T')
        parse_f()
        parse_f()
        parse_l()
        match('T')
        match('O')
        parse_k()
    elif lookahead.startswith('#'):
        match('#')
        parse_l()
    elif lookahead.startswith('/'):
        match('/')
        match('-')
        match('/')
        parse_f()
        match('*')
        parse_d()
    elif lookahead.startswith('^'):
        match('^')
        match('/')
    elif lookahead.startswith('w'):
        match('w')
        match('=')
    elif lookahead.startswith('X'):
        match('X')
        match('#')
        parse_d()
        parse_l()
        match('w')
        parse_n()
        parse_q()
        parse_e()
        parse_k()
        match('(')
    elif lookahead.startswith('X'):
        match('X')
    else:
        error("Unexpected token " + lookahead + " in c, expected one of: " + ", ".join(['T', '#', '/', '^', 'w', 'X', 'X']))

def parse_d():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in d")
    lookahead = tokens[pos]
    if lookahead.startswith('('):
        match('(')
        match('t')
        match('K')
        match('O')
        parse_l()
        parse_e()
        match('/')
        parse_l()
    elif lookahead.startswith('X'):
        match('X')
        match('/')
        parse_b()
        match('^')
        parse_i()
    elif lookahead.startswith('/'):
        match('/')
        match('(')
        parse_f()
        parse_q()
        parse_n()
        parse_n()
        parse_g()
        match('5')
    elif lookahead.startswith('q'):
        parse_q()
    else:
        error("Unexpected token " + lookahead + " in d, expected one of: " + ", ".join(['(', 'X', '/', 'q']))

def parse_e():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in e")
    lookahead = tokens[pos]
    if lookahead.startswith('('):
        match('(')
        match('[')
        parse_j()
    elif lookahead.startswith('T'):
        match('T')
        parse_q()
        parse_f()
        match('/')
    elif lookahead.startswith('T'):
        match('T')
    else:
        error("Unexpected token " + lookahead + " in e, expected one of: " + ", ".join(['(', 'T', 'T']))

def parse_f():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('['):
        match('[')
        parse_j()
        match('^')

def parse_g():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in g")
    lookahead = tokens[pos]
    if lookahead.startswith('#'):
        match('#')
        parse_l()
        match('=')
        match('O')
        parse_n()
        match('K')
        match('w')
        match('w')
        match('K')
        match('X')
    elif lookahead.startswith('q'):
        parse_q()
        parse_e()
        match('X')
        match('(')
        match('1')
    elif lookahead.startswith('K'):
        match('K')
    else:
        error("Unexpected token " + lookahead + " in g, expected one of: " + ", ".join(['#', 'q', 'K']))

def parse_h():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in h")
    lookahead = tokens[pos]
    if lookahead.startswith('X'):
        match('X')
        parse_n()
        parse_q()
        parse_q()
        parse_j()
        match('*')
        match('*')
        match('(')
        match('X')
        parse_q()
    elif lookahead.startswith('1'):
        match('1')
        parse_r()
    elif lookahead.startswith('K'):
        match('K')
        match('=')
        match('O')
        parse_i()
        parse_q()
        match('*')
        parse_q()
        parse_c()
    elif lookahead.startswith('q'):
        parse_q()
        match('t')
    elif lookahead.startswith('('):
        match('(')
    elif lookahead.startswith('*'):
        match('*')
        match('t')
        parse_l()
        match('1')
        parse_a()
    elif lookahead.startswith('t'):
        match('t')
        match('t')
        match('^')
        match('/')
        match('[')
        parse_a()
        match('w')
        parse_p()
    elif lookahead.startswith('='):
        match('=')
        match('5')
        match('t')
    elif lookahead.startswith('/'):
        match('/')
        parse_o()
        parse_j()
        parse_l()
        parse_n()
        match('1')
        match('/')
        parse_n()
        match('5')
    elif lookahead.startswith('O'):
        match('O')
        parse_j()
        parse_c()
        match('X')
        parse_i()
    else:
        error("Unexpected token " + lookahead + " in h, expected one of: " + ", ".join(['X', '1', 'K', 'q', '(', '*', 't', '=', '/', 'O']))

def parse_i():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in i")
    lookahead = tokens[pos]
    if lookahead.startswith('t'):
        match('t')
        parse_f()
        match('^')
    elif lookahead.startswith('q'):
        parse_q()
        match('=')
        parse_l()
        match('/')
        parse_f()
        match('=')
    elif lookahead.startswith('T'):
        match('T')
        match('#')
        match('K')
        match('*')
        match('(')
    elif lookahead.startswith('w'):
        match('w')
        parse_b()
        parse_l()
    elif lookahead.startswith('^'):
        match('^')
        parse_l()
        parse_l()
        match('/')
        match('O')
        parse_l()
        parse_l()
        parse_l()
    elif lookahead.startswith('X'):
        match('X')
        match('(')
        parse_q()
    elif lookahead.startswith('5'):
        match('5')
        match('^')
        parse_j()
        parse_q()
        parse_c()
        parse_n()
    elif lookahead.startswith('['):
        match('[')
        parse_g()
        match('^')
        match('-')
        match('[')
        match('/')
        match('/')
        match('#')
        match('(')
    elif lookahead.startswith('O'):
        match('O')
        parse_i()
        match('#')
        parse_i()
    elif lookahead.startswith('1'):
        match('1')
        match('5')
        parse_i()
        match('O')
        parse_l()
        match('w')
    elif lookahead.startswith('l'):
        parse_l()
    else:
        error("Unexpected token " + lookahead + " in i, expected one of: " + ", ".join(['t', 'q', 'T', 'w', '^', 'X', '5', '[', 'O', '1', 'l']))

def parse_j():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('['):
        match('[')
        parse_l()
        match('*')
        match('K')
        match('-')
        match('[')
        parse_q()
        match('[')
        match('T')
        match('/')

def parse_k():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in k")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        parse_j()
        match('T')
        match('X')
        parse_l()
        parse_a()
        match('#')
        match('^')
    elif lookahead.startswith('O'):
        match('O')
        parse_e()
    elif lookahead.startswith('T'):
        match('T')
        match('5')
        match('O')
        parse_l()
    elif lookahead.startswith('-'):
        match('-')
        parse_n()
        parse_r()
        match('-')
        match('T')
        match('[')
        match('t')
    elif lookahead.startswith('K'):
        match('K')
        match('X')
        parse_o()
        parse_l()
        match('K')
        parse_i()
    elif lookahead.startswith('*'):
        match('*')
        parse_l()
        parse_q()
        parse_q()
        parse_q()
        parse_n()
        match('O')
    elif lookahead.startswith('q'):
        parse_q()
        match('=')
        parse_f()
        match('(')
        parse_j()
        parse_a()
        match('^')
        match('^')
        match('K')
    elif lookahead.startswith('q'):
        parse_q()
    else:
        error("Unexpected token " + lookahead + " in k, expected one of: " + ", ".join(['w', 'O', 'T', '-', 'K', '*', 'q', 'q']))

def parse_l():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('^'):
        match('^')

def parse_m():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('#'):
        match('#')
        match('*')
        parse_l()
        match('t')
        parse_n()
        parse_h()
        match('T')

def parse_n():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in n")
    lookahead = tokens[pos]
    if lookahead.startswith('='):
        match('=')
        parse_p()
    elif lookahead.startswith('O'):
        match('O')
    else:
        error("Unexpected token " + lookahead + " in n, expected one of: " + ", ".join(['=', 'O']))

def parse_o():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('#'):
        match('#')
        parse_l()

def parse_p():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in p")
    lookahead = tokens[pos]
    if lookahead.startswith('l'):
        parse_l()
        parse_l()
        match('-')
        match('-')
        match('X')
        parse_r()
        parse_f()
        parse_l()
    elif lookahead.startswith('/'):
        match('/')
        parse_l()
        match('-')
        parse_r()
    elif lookahead.startswith('X'):
        match('X')
        match('T')
        parse_o()
        parse_d()
        match('1')
        match('^')
        parse_j()
    elif lookahead.startswith('w'):
        match('w')
        parse_l()
        match('-')
        match('/')
        match('K')
        match('K')
        match('O')
        match('*')
    elif lookahead.startswith('='):
        match('=')
        parse_l()
        parse_q()
        parse_q()
        parse_m()
        match('#')
        match('/')
        parse_q()
        match('*')
    elif lookahead.startswith('('):
        match('(')
        parse_d()
        match('K')
    elif lookahead.startswith('^'):
        match('^')
        parse_m()
        match('K')
        parse_p()
        parse_k()
        parse_g()
        match('=')
        parse_i()
    elif lookahead.startswith('-'):
        match('-')
        match('(')
        match('5')
        parse_l()
        parse_i()
    elif lookahead.startswith('1'):
        match('1')
        parse_g()
        parse_l()
        match('[')
        match('(')
        parse_f()
        parse_a()
        parse_d()
        match('[')
        parse_q()
    elif lookahead.startswith('q'):
        parse_q()
    else:
        error("Unexpected token " + lookahead + " in p, expected one of: " + ", ".join(['l', '/', 'X', 'w', '=', '(', '^', '-', '1', 'q']))

def parse_q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('5'):
        match('5')
        match('^')
        parse_h()
        match('*')
        match('#')
        match('(')
        parse_b()
        match('O')
        match('-')
        match('(')

def parse_r():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('('):
        match('(')
        match('1')
        match('-')
        match('t')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_a()
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