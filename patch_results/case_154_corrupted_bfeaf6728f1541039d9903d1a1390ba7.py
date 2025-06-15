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

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('*'):
            match('*')
            parse_S()
            match('t')
            match('?')
            match('Y')
        elif lookahead.startswith('i'):
            match('i')
            parse_F()
            match('|')
            match('f')
        elif lookahead.startswith(')'):
            match(')')
            match('/')
            match('1')
            match('d')
            match('q')
        elif lookahead.startswith('q'):
            match('q')
            match('[')
            match('2')
        elif lookahead.startswith('>'):
            match('>')
            match(']')
        elif lookahead.startswith('c'):
            match('c')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['*', 'i', ')', 'q', '>', 'c']))
    elif lookahead.startswith('/'):
        match('/')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['/', '/']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('l'):
        match('l')
        match('8')
        match('+')
        match('v')
    elif lookahead.startswith('3'):
        match('3')
        match('p')
    elif lookahead.startswith('&'):
        match('&')
        parse_P()
        match('G')
    elif lookahead.startswith('o'):
        match('o')
        match('T')
    elif lookahead.startswith('*'):
        match('*')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['l', '3', '&', 'o', '*']))

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('&'):
        match('&')
        parse_P()
        parse_F()
        match('M')
        parse_X()

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('O'):
        match('O')
        match('o')
        parse_S()
        parse_X()
        parse_L()
    elif lookahead.startswith("'"):
        match("'")
    elif lookahead.startswith(')'):
        match(')')
        match('#')
        match('G')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['O', "'", ')']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('K'):
        parse_K()
        match('g')
        match('j')
        match(']')
        parse_X()
    elif lookahead.startswith('|'):
        match('|')
        parse_V()
    elif lookahead.startswith('['):
        match('[')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['K', '|', '[']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('z'):
        match('z')
        parse_E()
        match('%')
        match('=')
        match('%')
    elif lookahead.startswith('}'):
        match('}')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['z', '}']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('*'):
        match('*')
        parse_S()
        match('t')
        match('?')
        match('Y')
    elif lookahead.startswith('i'):
        match('i')
        parse_F()
        match('|')
        match('f')
    elif lookahead.startswith(')'):
        match(')')
        match('/')
        match('1')
        match('d')
        match('q')
    elif lookahead.startswith('q'):
        match('q')
        match('[')
        match('2')
    elif lookahead.startswith('>'):
        match('>')
        match(']')
    elif lookahead.startswith('c'):
        match('c')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['*', 'i', ')', 'q', '>', 'c']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('V'):
        parse_V()
        match('8')
        match('H')
        match('n')
        match('D')
    elif lookahead.startswith('A'):
        match('A')
        match('=')
        match('u')
        parse_S()
    elif lookahead.startswith('m'):
        match('m')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['V', 'A', 'm']))

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('8'):
        match('8')
        parse_B()
        parse_F()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_P()
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