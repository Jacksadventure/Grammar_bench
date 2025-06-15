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

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('K'):
        match('K')
        match('$')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('!'):
            match('!')
            match('G')
            parse_S()
            parse_R()
            parse_L()
        elif lookahead.startswith(')'):
            match(')')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['!', ')']))
    elif lookahead.startswith('l'):
        match('l')
        match('(')
        match('x')
    elif lookahead.startswith('_'):
        match('_')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('>'):
            match('>')
            match('p')
            match('*')
            match('*')
        elif lookahead.startswith('|'):
            match('|')
            match('?')
            match('#')
            parse_Z()
            parse_V()
        elif lookahead.startswith('7'):
            match('7')
        elif lookahead.startswith(','):
            match(',')
            match('?')
        elif lookahead.startswith('$'):
            match('$')
            match('+')
            match('q')
            match('>')
            parse_D()
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['>', '|', '7', ',', '$']))
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['K', 'l', '_', 'd']))

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('&'):
        match('&')
        match("'")

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('>'):
        match('>')
        match('p')
        match('*')
        match('*')
    elif lookahead.startswith('|'):
        match('|')
        match('?')
        match('#')
        parse_Z()
        parse_V()
    elif lookahead.startswith('7'):
        match('7')
    elif lookahead.startswith(','):
        match(',')
        match('?')
    elif lookahead.startswith('$'):
        match('$')
        match('+')
        match('q')
        match('>')
        parse_D()
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['>', '|', '7', ',', '$']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('D'):
        parse_D()
        parse_D()
        parse_Z()
        match('n')
        parse_V()
    elif lookahead.startswith('/'):
        match('/')
        match('.')
        match('0')
        match('A')
        match('~')
    elif lookahead.startswith('H'):
        match('H')
        match('W')
        match('T')
    elif lookahead.startswith('i'):
        match('i')
        match('M')
        match('!')
    elif lookahead.startswith('h'):
        match('h')
        match('P')
    elif lookahead.startswith('j'):
        match('j')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['D', '/', 'H', 'i', 'h', 'j']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('r'):
        match('r')
        match('3')
    elif lookahead.startswith('x'):
        match('x')
        match('J')
    elif lookahead.startswith('['):
        match('[')
        match('J')
        match('j')
        match('9')
    elif lookahead.startswith('q'):
        match('q')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['r', 'x', '[', 'q']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        parse_Z()
        match('7')
        match('P')
        match('o')
    elif lookahead.startswith('Z'):
        parse_Z()
        parse_L()
        match('9')
        match('%')
        match('v')
    elif lookahead.startswith(','):
        match(',')
        parse_Z()
    elif lookahead.startswith('.'):
        match('.')
        match('9')
        match('q')
    elif lookahead.startswith('R'):
        parse_R()
        match('u')
        match('5')
        parse_I()
        match('J')
    elif lookahead.startswith('w'):
        match('w')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(["'", 'Z', ',', '.', 'R', 'w']))

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('-'):
        match('-')
        match('<')
        match('B')
        parse_I()
        match('`')

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('!'):
        match('!')
        match('G')
        parse_S()
        parse_R()
        parse_L()
    elif lookahead.startswith(')'):
        match(')')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['!', ')']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('H'):
        match('H')
        parse_E()
        match('X')
        match('`')
        parse_C()
    elif lookahead.startswith('^'):
        match('^')
        match('r')
        parse_D()
        match('J')
    elif lookahead.startswith('$'):
        match('$')
        parse_I()
        match('F')
        match(';')
    elif lookahead.startswith('+'):
        match('+')
        match('H')
        match('w')
        match('>')
        match('T')
    elif lookahead.startswith('&'):
        match('&')
        match('G')
        match('<')
        parse_Z()
        match('e')
    elif lookahead.startswith('8'):
        match('8')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['H', '^', '$', '+', '&', '8']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Z()
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