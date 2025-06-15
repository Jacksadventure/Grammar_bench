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

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
    elif lookahead.startswith('@'):
        match('@')
        match('(')
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('}'):
            match('}')
            parse_F()
            match('_')
        elif lookahead.startswith("'"):
            match("'")
            match('R')
        elif lookahead.startswith('R'):
            match('R')
            match('8')
        elif lookahead.startswith('j'):
            match('j')
        elif lookahead.startswith('A'):
            parse_A()
            match('p')
            parse_U()
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['}', "'", 'R', 'j', 'A']))
        match('h')
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('w'):
            match('w')
            match('m')
        elif lookahead.startswith('='):
            match('=')
            match('4')
        elif lookahead.startswith('G'):
            match('G')
        else:
            error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['w', '=', 'G']))
    elif lookahead.startswith('I'):
        match('I')
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('}'):
            match('}')
            parse_F()
            match('_')
        elif lookahead.startswith("'"):
            match("'")
            match('R')
        elif lookahead.startswith('R'):
            match('R')
            match('8')
        elif lookahead.startswith('j'):
            match('j')
        elif lookahead.startswith('A'):
            parse_A()
            match('p')
            parse_U()
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['}', "'", 'R', 'j', 'A']))
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('4'):
            match('4')
            parse_A()
            parse_B()
            parse_B()
            match(';')
        elif lookahead.startswith('t'):
            match('t')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['4', 't']))
    elif lookahead.startswith('z'):
        match('z')
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith(','):
            match(',')
        elif lookahead.startswith('@'):
            match('@')
            match('(')
            parse_S()
            match('h')
            parse_P()
        elif lookahead.startswith('I'):
            match('I')
            parse_S()
            parse_A()
        elif lookahead.startswith('z'):
            match('z')
            parse_F()
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join([',', '@', 'I', 'z']))
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join([',', '@', 'I', 'z']))

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('V'):
        match('V')
        parse_B()
        parse_F()
        parse_K()

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('E'):
        match('E')
        parse_F()
        match('g')
        match('q')
    elif lookahead.startswith('#'):
        match('#')
        match('t')
        parse_F()
        parse_Y()
        parse_A()
    elif lookahead.startswith('H'):
        match('H')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['E', '#', 'H']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        match('m')
    elif lookahead.startswith('='):
        match('=')
        match('4')
    elif lookahead.startswith('G'):
        match('G')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['w', '=', 'G']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('M'):
        match('M')
    elif lookahead.startswith('='):
        match('=')
        parse_T()
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['M', '=']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('4'):
        match('4')
        parse_A()
        parse_B()
        parse_B()
        match(';')
    elif lookahead.startswith('t'):
        match('t')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['4', 't']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('|'):
        match('|')
        match('b')
        parse_U()
    elif lookahead.startswith('('):
        match('(')
        match("'")
        match('Q')
        match('!')
        parse_S()
    elif lookahead.startswith('?'):
        match('?')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['|', '(', '?']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('R'):
        match('R')
    elif lookahead.startswith('z'):
        match('z')
    elif lookahead.startswith('i'):
        match('i')
        parse_B()
        parse_T()
    elif lookahead.startswith('V'):
        match('V')
        match('>')
        match('x')
        parse_F()
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['R', 'z', 'i', 'V']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('}'):
        match('}')
        parse_F()
        match('_')
    elif lookahead.startswith("'"):
        match("'")
        match('R')
    elif lookahead.startswith('R'):
        match('R')
        match('8')
    elif lookahead.startswith('j'):
        match('j')
    elif lookahead.startswith('A'):
        parse_A()
        match('p')
        parse_U()
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['}', "'", 'R', 'j', 'A']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_F()
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