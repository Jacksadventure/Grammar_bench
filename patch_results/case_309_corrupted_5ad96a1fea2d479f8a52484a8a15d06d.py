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
    if lookahead.startswith('('):
        match('(')
        while pos < len(tokens) and tokens[pos].startswith('n'):
            match('n')
            parse_W()
            parse_D()
            parse_I()
        match('V')
    elif lookahead.startswith('M'):
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('='):
            match('=')
        elif lookahead.startswith('2'):
            match('2')
            match('N')
        elif lookahead.startswith('5'):
            match('5')
            match('>')
            match('z')
            match('h')
        elif lookahead.startswith('4'):
            match('4')
            match('/')
            match('B')
            match('g')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['=', '2', '5', '4']))
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('='):
            match('=')
        elif lookahead.startswith('2'):
            match('2')
            match('N')
        elif lookahead.startswith('5'):
            match('5')
            match('>')
            match('z')
            match('h')
        elif lookahead.startswith('4'):
            match('4')
            match('/')
            match('B')
            match('g')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['=', '2', '5', '4']))
        match('a')
        while pos < len(tokens) and tokens[pos].startswith('n'):
            match('n')
            parse_W()
            parse_D()
            parse_I()
    elif lookahead.startswith('P'):
        match('P')
        match('@')
        match('b')
    elif lookahead.startswith('!'):
        match('!')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('>'):
            match('>')
            match('9')
            parse_Y()
            parse_Y()
            parse_Y()
        elif lookahead.startswith('o'):
            match('o')
            match('C')
            parse_D()
            match(']')
        elif lookahead.startswith('h'):
            match('h')
            parse_G()
        elif lookahead.startswith('+'):
            match('+')
            match('$')
            parse_W()
        elif lookahead.startswith('R'):
            match('R')
            match('%')
            match('X')
        elif lookahead.startswith('p'):
            match('p')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['>', 'o', 'h', '+', 'R', 'p']))
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('%'):
            match('%')
            parse_T()
            match('Z')
        elif lookahead.startswith('8'):
            match('8')
            parse_H()
            match('N')
        elif lookahead.startswith('X'):
            match('X')
            parse_T()
            match('&')
            match('2')
            parse_M()
        elif lookahead.startswith('u'):
            match('u')
            match('3')
            match('&')
            parse_T()
        elif lookahead.startswith('p'):
            match('p')
            parse_H()
            parse_I()
        elif lookahead.startswith('d'):
            match('d')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['%', '8', 'X', 'u', 'p', 'd']))
    elif lookahead.startswith('N'):
        match('N')
        while pos < len(tokens) and tokens[pos].startswith('['):
            match('[')
    elif lookahead.startswith('@'):
        match('@')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['(', 'M', 'P', '!', 'N', '@']))

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('4'):
        match('4')

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('r'):
        match('r')
        match('v')
        parse_M()
        match('v')
        parse_H()
    elif lookahead.startswith('m'):
        match('m')
        match('&')
        match('w')
        match('d')
        parse_H()
    elif lookahead.startswith('R'):
        match('R')
        match('#')
        match('n')
        match('r')
        match('Z')
    elif lookahead.startswith('W'):
        parse_W()
        parse_T()
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['r', 'm', 'R', 'W']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('>'):
        match('>')
        match('9')
        parse_Y()
        parse_Y()
        parse_Y()
    elif lookahead.startswith('o'):
        match('o')
        match('C')
        parse_D()
        match(']')
    elif lookahead.startswith('h'):
        match('h')
        parse_G()
    elif lookahead.startswith('+'):
        match('+')
        match('$')
        parse_W()
    elif lookahead.startswith('R'):
        match('R')
        match('%')
        match('X')
    elif lookahead.startswith('p'):
        match('p')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['>', 'o', 'h', '+', 'R', 'p']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('%'):
        match('%')
        parse_T()
        match('Z')
    elif lookahead.startswith('8'):
        match('8')
        parse_H()
        match('N')
    elif lookahead.startswith('X'):
        match('X')
        parse_T()
        match('&')
        match('2')
        parse_M()
    elif lookahead.startswith('u'):
        match('u')
        match('3')
        match('&')
        parse_T()
    elif lookahead.startswith('p'):
        match('p')
        parse_H()
        parse_I()
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['%', '8', 'X', 'u', 'p', 'd']))

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('n'):
        match('n')
        parse_W()
        parse_D()
        parse_I()

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('='):
        match('=')
    elif lookahead.startswith('2'):
        match('2')
        match('N')
    elif lookahead.startswith('5'):
        match('5')
        match('>')
        match('z')
        match('h')
    elif lookahead.startswith('4'):
        match('4')
        match('/')
        match('B')
        match('g')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['=', '2', '5', '4']))

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('['):
        match('[')

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