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

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('{'):
        match('{')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('-'):
            match('-')
            parse_T()
            parse_N()
        elif lookahead.startswith('7'):
            match('7')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['-', '7']))
        match('^')
        match(',')
        match('9')
    elif lookahead.startswith('-'):
        match('-')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['{', '-']))

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Z'):
        match('Z')
        match('X')
        match('2')
        parse_F()
        parse_D()

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('7'):
        match('7')
        match('x')
        match('<')
        match('l')

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('='):
        match('=')
        parse_T()
        parse_P()
    elif lookahead.startswith('8'):
        match('8')
        parse_Y()
        match('v')
        match('v')
    elif lookahead.startswith('0'):
        match('0')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['=', '8', '0']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('m'):
        match('m')
        parse_B()
        match('S')
        parse_N()
        parse_Y()
    elif lookahead.startswith('>'):
        match('>')
        parse_P()
        parse_F()
        match("'")
        parse_T()
    elif lookahead.startswith('9'):
        match('9')
    elif lookahead.startswith('Z'):
        match('Z')
        match('}')
        match('n')
        parse_P()
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['m', '>', '9', 'Z']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('!'):
        match('!')
        match('U')
    elif lookahead.startswith('}'):
        match('}')
        parse_F()
        match('R')
        match('}')
    elif lookahead.startswith('9'):
        match('9')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['!', '}', '9']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('0'):
        match('0')
        match('E')
        parse_L()
        parse_N()
    elif lookahead.startswith('8'):
        match('8')
    elif lookahead.startswith('G'):
        match('G')
        parse_Y()
        parse_Y()
    elif lookahead.startswith('b'):
        match('b')
        match('[')
    elif lookahead.startswith('K'):
        match('K')
        parse_B()
        parse_Y()
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['0', '8', 'G', 'b', 'K']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('_'):
        match('_')
        match('e')
        match('^')
        match('$')
    elif lookahead.startswith('a'):
        match('a')
        parse_B()
        match('A')
        match('a')
    elif lookahead.startswith('t'):
        match('t')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['_', 'a', 't']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_B()
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