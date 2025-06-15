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
    while pos < len(tokens) and tokens[pos].startswith('4'):
        match('4')
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('n'):
            match('n')
            match('<')
        elif lookahead.startswith('U'):
            match('U')
            match('E')
            match("'")
            match('.')
            match(':')
        elif lookahead.startswith('l'):
            match('l')
            match('M')
            match("'")
            match('~')
            match('&')
        elif lookahead.startswith('>'):
            match('>')
            match('k')
            parse_L()
            parse_F()
            parse_W()
        elif lookahead.startswith('~'):
            match('~')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['n', 'U', 'l', '>', '~']))
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith('2'):
            match('2')
            match('s')
        elif lookahead.startswith('m'):
            match('m')
            parse_I()
            match('u')
            match('U')
        elif lookahead.startswith('|'):
            match('|')
            parse_S()
            match('#')
            parse_L()
            match("'")
        elif lookahead.startswith('W'):
            parse_W()
            parse_K()
            match('G')
            parse_K()
        elif lookahead.startswith('i'):
            match('i')
            parse_L()
            match('2')
            parse_X()
        elif lookahead.startswith('A'):
            match('A')
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['2', 'm', '|', 'W', 'i', 'A']))
        match('?')

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('n'):
        match('n')
        match('<')
    elif lookahead.startswith('U'):
        match('U')
        match('E')
        match("'")
        match('.')
        match(':')
    elif lookahead.startswith('l'):
        match('l')
        match('M')
        match("'")
        match('~')
        match('&')
    elif lookahead.startswith('>'):
        match('>')
        match('k')
        parse_L()
        parse_F()
        parse_W()
    elif lookahead.startswith('~'):
        match('~')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['n', 'U', 'l', '>', '~']))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('<'):
        match('<')
        match('w')
        match('h')
    elif lookahead.startswith('S'):
        parse_S()
    elif lookahead.startswith('9'):
        match('9')
        match('>')
    elif lookahead.startswith('r'):
        match('r')
        match('c')
        parse_L()
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['<', 'S', '9', 'r']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        match(']')
        match('=')
    elif lookahead.startswith('h'):
        match('h')
        match('k')
    elif lookahead.startswith('#'):
        match('#')
        match('i')
    elif lookahead.startswith('x'):
        match('x')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join([']', 'h', '#', 'x']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('e'):
        match('e')
        match('u')
        match('R')
        match('c')
        match('Z')
    elif lookahead.startswith('3'):
        match('3')
        match('&')
        match('9')
        match('P')
        match('n')
    elif lookahead.startswith('6'):
        match('6')
        match('l')
    elif lookahead.startswith(':'):
        match(':')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['e', '3', '6', ':']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('2'):
        match('2')
        match('s')
    elif lookahead.startswith('m'):
        match('m')
        parse_I()
        match('u')
        match('U')
    elif lookahead.startswith('|'):
        match('|')
        parse_S()
        match('#')
        parse_L()
        match("'")
    elif lookahead.startswith('W'):
        parse_W()
        parse_K()
        match('G')
        parse_K()
    elif lookahead.startswith('i'):
        match('i')
        parse_L()
        match('2')
        parse_X()
    elif lookahead.startswith('A'):
        match('A')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['2', 'm', '|', 'W', 'i', 'A']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('M'):
        match('M')
    elif lookahead.startswith('J'):
        match('J')
        match('u')
        match('H')
        parse_K()
        match('E')
    elif lookahead.startswith('.'):
        match('.')
        parse_F()
        match('c')
        parse_F()
        parse_S()
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['M', 'J', '.']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('s'):
        match('s')
    elif lookahead.startswith('E'):
        match('E')
    elif lookahead.startswith('g'):
        match('g')
        parse_I()
        match('z')
    elif lookahead.startswith('<'):
        match('<')
        parse_Y()
    elif lookahead.startswith('.'):
        match('.')
        parse_X()
        match('p')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['s', 'E', 'g', '<', '.']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('S'):
        parse_S()
        parse_D()
    elif lookahead.startswith('W'):
        parse_W()
        match('(')
    elif lookahead.startswith('K'):
        parse_K()
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['S', 'W', 'K']))

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