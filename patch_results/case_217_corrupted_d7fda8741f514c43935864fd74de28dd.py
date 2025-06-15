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

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        while pos < len(tokens) and tokens[pos].startswith('b'):
            match('b')
            match('$')
        match('@')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('S'):
            match('S')
            parse_U()
            match('8')
        elif lookahead.startswith('}'):
            match('}')
            match('N')
            parse_H()
            match('%')
            match("'")
        elif lookahead.startswith('y'):
            match('y')
            match('(')
            match('Y')
        elif lookahead.startswith('A'):
            match('A')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['S', '}', 'y', 'A']))
        while pos < len(tokens) and tokens[pos].startswith("'"):
            match("'")
            match('V')
            match('1')
            match('m')
            match('b')
    elif lookahead.startswith(';'):
        match(';')
        match('^')
        match('o')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('E'):
            match('E')
            parse_M()
            match('Q')
            match(')')
        elif lookahead.startswith('1'):
            match('1')
        elif lookahead.startswith('W'):
            parse_W()
            match('%')
        elif lookahead.startswith('o'):
            match('o')
            match("'")
            match('b')
            match('_')
            parse_J()
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['E', '1', 'W', 'o']))
    elif lookahead.startswith('0'):
        match('0')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(["'", ';', '0']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('L'):
        parse_L()
        parse_F()
        parse_H()
    elif lookahead.startswith('B'):
        match('B')
        match('6')
    elif lookahead.startswith('a'):
        match('a')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['L', 'B', 'a']))

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")
        match('V')
        match('1')
        match('m')
        match('b')

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('b'):
        match('b')
        match('$')

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('X'):
        match('X')
        match('7')
        parse_Z()
    elif lookahead.startswith('_'):
        match('_')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['X', '_']))

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('}'):
        match('}')
        match('0')
        parse_W()
        parse_G()

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('#'):
        match('#')
        match('g')
        match('y')
        match("'")
        parse_T()
    elif lookahead.startswith('*'):
        match('*')
        parse_Z()
    elif lookahead.startswith('V'):
        match('V')
        match('o')
        match('?')
    elif lookahead.startswith('o'):
        match('o')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['#', '*', 'V', 'o']))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('+'):
        match('+')
        match('k')
        match('s')
        match('4')

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('S'):
        match('S')
        parse_U()
        match('8')
    elif lookahead.startswith('}'):
        match('}')
        match('N')
        parse_H()
        match('%')
        match("'")
    elif lookahead.startswith('y'):
        match('y')
        match('(')
        match('Y')
    elif lookahead.startswith('A'):
        match('A')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['S', '}', 'y', 'A']))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('E'):
        match('E')
        parse_M()
        match('Q')
        match(')')
    elif lookahead.startswith('1'):
        match('1')
    elif lookahead.startswith('W'):
        parse_W()
        match('%')
    elif lookahead.startswith('o'):
        match('o')
        match("'")
        match('b')
        match('_')
        parse_J()
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['E', '1', 'W', 'o']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_W()
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