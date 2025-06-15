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

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('|'):
        match('|')
        match('7')
        match('~')
        match('?')
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('B'):
            match('B')
            match(']')
            match('3')
            parse_E()
        elif lookahead.startswith('a'):
            match('a')
        else:
            error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['B', 'a']))
    elif lookahead.startswith('>'):
        match('>')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('1'):
            match('1')
            match('(')
            match('#')
            match("'")
        elif lookahead.startswith('l'):
            match('l')
            match('p')
            match('a')
        elif lookahead.startswith('X'):
            match('X')
            parse_J()
            match('o')
            parse_Z()
        elif lookahead.startswith('M'):
            parse_M()
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['1', 'l', 'X', 'M']))
    elif lookahead.startswith('}'):
        match('}')
    elif lookahead.startswith('f'):
        match('f')
    elif lookahead.startswith('8'):
        match('8')
        match('j')
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith('w'):
            match('w')
            match('k')
            parse_Z()
            match('W')
            parse_M()
        elif lookahead.startswith('G'):
            match('G')
            match('k')
            parse_U()
            match("'")
        elif lookahead.startswith('}'):
            match('}')
            match('#')
            match("'")
            match('v')
        elif lookahead.startswith('R'):
            match('R')
        else:
            error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['w', 'G', '}', 'R']))
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['|', '>', '}', 'f', '8']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('B'):
        match('B')
        match(']')
        match('3')
        parse_E()
    elif lookahead.startswith('a'):
        match('a')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['B', 'a']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('Z'):
        parse_Z()
        parse_E()
        match('G')
    elif lookahead.startswith('P'):
        parse_P()
        match('+')
    elif lookahead.startswith('-'):
        match('-')
        parse_D()
    elif lookahead.startswith('q'):
        match('q')
    elif lookahead.startswith('^'):
        match('^')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['Z', 'P', '-', 'q', '^']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('8'):
        match('8')
    elif lookahead.startswith('O'):
        match('O')
    elif lookahead.startswith('s'):
        match('s')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['8', 'O', 's']))

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('B'):
        match('B')
        match('`')
        match('W')
        match('4')
        match('c')
    elif lookahead.startswith(']'):
        match(']')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['B', ']']))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('r'):
        match('r')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['r']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('!'):
        match('!')
        parse_D()
        parse_T()
        match('%')
    elif lookahead.startswith('4'):
        match('4')
        match('i')
        parse_U()
        match(',')
    elif lookahead.startswith('O'):
        match('O')
        parse_D()
        match('v')
        match('z')
    elif lookahead.startswith("'"):
        match("'")
        match('H')
        match('x')
        match(';')
        match('~')
    elif lookahead.startswith('q'):
        match('q')
        match('d')
        match('1')
        match('R')
    elif lookahead.startswith('>'):
        match('>')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['!', '4', 'O', "'", 'q', '>']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        match('k')
        parse_Z()
        match('W')
        parse_M()
    elif lookahead.startswith('G'):
        match('G')
        match('k')
        parse_U()
        match("'")
    elif lookahead.startswith('}'):
        match('}')
        match('#')
        match("'")
        match('v')
    elif lookahead.startswith('R'):
        match('R')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['w', 'G', '}', 'R']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_T()
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