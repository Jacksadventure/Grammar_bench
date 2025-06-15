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

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('v'):
        match('v')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('C'):
            match('C')
            match('c')
            parse_O()
        elif lookahead.startswith('O'):
            parse_O()
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['C', 'O']))
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('j'):
            match('j')
            match('b')
            match('h')
            match('W')
            parse_V()
        elif lookahead.startswith('c'):
            match('c')
            match('a')
            parse_G()
            parse_G()
            parse_V()
        elif lookahead.startswith('T'):
            match('T')
            parse_L()
            match('p')
            match('f')
            match('P')
        elif lookahead.startswith('d'):
            match('d')
            match('4')
            match('i')
        elif lookahead.startswith('D'):
            match('D')
            match('`')
        elif lookahead.startswith('0'):
            match('0')
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['j', 'c', 'T', 'd', 'D', '0']))
    elif lookahead.startswith('<'):
        match('<')
        match('Z')
    elif lookahead.startswith('.'):
        match('.')
        match('d')
        match('Z')
        match("'")
    elif lookahead.startswith('k'):
        match('k')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['v', '<', '.', 'k']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('c'):
        match('c')
        parse_V()
        parse_H()
        match('<')
    elif lookahead.startswith('+'):
        match('+')
        match('[')
        parse_R()
        parse_V()
    elif lookahead.startswith('u'):
        match('u')
        match('g')
        match('<')
        match('|')
    elif lookahead.startswith('S'):
        match('S')
        match('c')
        match('s')
    elif lookahead.startswith('&'):
        match('&')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['c', '+', 'u', 'S', '&']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
        match('b')
        match('h')
        match('W')
        parse_V()
    elif lookahead.startswith('c'):
        match('c')
        match('a')
        parse_G()
        parse_G()
        parse_V()
    elif lookahead.startswith('T'):
        match('T')
        parse_L()
        match('p')
        match('f')
        match('P')
    elif lookahead.startswith('d'):
        match('d')
        match('4')
        match('i')
    elif lookahead.startswith('D'):
        match('D')
        match('`')
    elif lookahead.startswith('0'):
        match('0')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['j', 'c', 'T', 'd', 'D', '0']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('t'):
        match('t')
        match('}')
        parse_Q()
    elif lookahead.startswith('Z'):
        match('Z')
    elif lookahead.startswith("'"):
        match("'")
        parse_H()
        match('}')
        match('a')
        match('~')
    elif lookahead.startswith('W'):
        match('W')
        match('0')
        match(')')
        match('1')
    elif lookahead.startswith('p'):
        match('p')
        match('c')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['t', 'Z', "'", 'W', 'p']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('='):
        match('=')
    elif lookahead.startswith('X'):
        match('X')
        parse_R()
        parse_R()
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['=', 'X']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('C'):
        match('C')
        match('c')
        parse_O()
    elif lookahead.startswith('O'):
        parse_O()
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['C', 'O']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        match('I')
        match('z')
        match('U')
        match('X')
    elif lookahead.startswith('Y'):
        match('Y')
        match('s')
        parse_V()
        match('Z')
    elif lookahead.startswith('l'):
        match('l')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join([',', 'Y', 'l']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Q()
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