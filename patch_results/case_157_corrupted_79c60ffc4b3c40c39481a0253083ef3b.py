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

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('D'):
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith('7'):
            match('7')
            parse_U()
            match('k')
            parse_M()
            match('v')
        elif lookahead.startswith('E'):
            match('E')
            match('%')
            match('-')
            match('m')
            match('[')
        elif lookahead.startswith('A'):
            parse_A()
        else:
            error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['7', 'E', 'A']))
        match('s')
        match('7')
        match('#')
    elif lookahead.startswith('('):
        match('(')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('3'):
            match('3')
            parse_Q()
            match('v')
        elif lookahead.startswith('`'):
            match('`')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['3', '`']))
        match('+')
        while pos < len(tokens) and tokens[pos].startswith('T'):
            match('T')
            match('3')
            parse_P()
    elif lookahead.startswith('J'):
        match('J')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['D', '(', 'J']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('7'):
        match('7')
        parse_U()
        match('k')
        parse_M()
        match('v')
    elif lookahead.startswith('E'):
        match('E')
        match('%')
        match('-')
        match('m')
        match('[')
    elif lookahead.startswith('A'):
        parse_A()
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['7', 'E', 'A']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('3'):
        match('3')
        parse_Q()
        match('v')
    elif lookahead.startswith('`'):
        match('`')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['3', '`']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('8'):
        match('8')
        match('Z')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['8', '']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('4'):
        match('4')
        parse_H()
        parse_D()
        parse_W()
    elif lookahead.startswith('0'):
        match('0')
        match('.')
        parse_K()
    elif lookahead.startswith('o'):
        match('o')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['4', '0', 'o']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('E'):
        match('E')
    elif lookahead.startswith('R'):
        match('R')
        match('(')
        match("'")
        match('{')
        parse_A()
    elif lookahead.startswith('%'):
        match('%')
        parse_A()
        match('B')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['E', 'R', '%']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('2'):
        match('2')
        match("'")
    elif lookahead.startswith('d'):
        match('d')
        match('9')
    elif lookahead.startswith('P'):
        parse_P()
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['2', 'd', 'P']))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('T'):
        match('T')
        match('3')
        parse_P()

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('V'):
        parse_V()
    elif lookahead.startswith('N'):
        match('N')
        match('B')
        match('c')
        match('m')
        match('j')
    elif lookahead.startswith('$'):
        match('$')
        match('}')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['V', 'N', '$']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('a'):
        match('a')
        match('q')
        match('*')
        match('l')
    elif lookahead.startswith('['):
        match('[')
    elif lookahead.startswith('^'):
        match('^')
        match('E')
        match('8')
        parse_V()
        match('@')
    elif lookahead.startswith('?'):
        match('?')
        match('@')
        parse_K()
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['a', '[', '^', '?']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_U()
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