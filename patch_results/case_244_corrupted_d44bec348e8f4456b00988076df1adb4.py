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

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('D'):
        match('D')
        match('n')
        match('}')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('9'):
            match('9')
            parse_S()
        elif lookahead.startswith('('):
            match('(')
            parse_A()
            match('g')
            match('(')
            parse_F()
        elif lookahead.startswith('c'):
            match('c')
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['9', '(', 'c']))
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('S'):
            parse_S()
            match('z')
            match(';')
            match('W')
            parse_L()
        elif lookahead.startswith('M'):
            match('M')
            match('7')
            match('3')
            match('k')
            match('B')
        elif lookahead.startswith('y'):
            match('y')
            match('D')
            match('k')
        elif lookahead.startswith('%'):
            match('%')
            match('b')
            match('[')
        elif lookahead.startswith('_'):
            match('_')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['S', 'M', 'y', '%', '_']))
    elif lookahead.startswith('9'):
        match('9')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['D', '9']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('{'):
        match('{')
    elif lookahead.startswith('/'):
        match('/')
        match(':')
        match('{')
        match('(')
        match('P')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['{', '/']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('S'):
        parse_S()
        match('z')
        match(';')
        match('W')
        parse_L()
    elif lookahead.startswith('M'):
        match('M')
        match('7')
        match('3')
        match('k')
        match('B')
    elif lookahead.startswith('y'):
        match('y')
        match('D')
        match('k')
    elif lookahead.startswith('%'):
        match('%')
        match('b')
        match('[')
    elif lookahead.startswith('_'):
        match('_')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['S', 'M', 'y', '%', '_']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('('):
        match('(')
        parse_F()
        match('k')
        match('*')
    elif lookahead.startswith('z'):
        match('z')
        match('x')
    elif lookahead.startswith('b'):
        match('b')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['(', 'z', 'b']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        parse_I()
    elif lookahead.startswith('@'):
        match('@')
        match('g')
        match('u')
        match('i')
        match('&')
    elif lookahead.startswith('s'):
        match('s')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['w', '@', 's']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('d'):
        match('d')
        match('l')
        parse_V()
        match('x')
    elif lookahead.startswith('+'):
        match('+')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['d', '+']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('9'):
        match('9')
        parse_S()
    elif lookahead.startswith('('):
        match('(')
        parse_A()
        match('g')
        match('(')
        parse_F()
    elif lookahead.startswith('c'):
        match('c')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['9', '(', 'c']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('h'):
        match('h')
        parse_O()
        match('y')
    elif lookahead.startswith('i'):
        match('i')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['h', 'i']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        match('W')
        parse_O()
        match('t')
        parse_V()
    elif lookahead.startswith('{'):
        match('{')
        parse_I()
        match('z')
        parse_N()
    elif lookahead.startswith('J'):
        parse_J()
        parse_I()
        parse_O()
        parse_F()
    elif lookahead.startswith('C'):
        match('C')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join([',', '{', 'J', 'C']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_I()
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