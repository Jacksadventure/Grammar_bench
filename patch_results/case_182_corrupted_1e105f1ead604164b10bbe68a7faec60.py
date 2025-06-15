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
    if lookahead.startswith('@'):
        match('@')
        match('y')
        match('B')
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('5'):
            match('5')
            parse_I()
        elif lookahead.startswith("'"):
            match("'")
            match('o')
            parse_P()
            match('0')
        elif lookahead.startswith('o'):
            match('o')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['5', "'", 'o']))
    elif lookahead.startswith('G'):
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('R'):
            match('R')
            match('1')
            match('1')
        elif lookahead.startswith('F'):
            parse_F()
            match('H')
        elif lookahead.startswith('I'):
            parse_I()
            match('s')
            match('-')
        elif lookahead.startswith('['):
            match('[')
            match(')')
            match('+')
            match('x')
            match('7')
        elif lookahead.startswith('~'):
            match('~')
            parse_I()
            match('C')
            match('c')
        elif lookahead.startswith('Q'):
            match('Q')
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['R', 'F', 'I', '[', '~', 'Q']))
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['@', 'G']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('5'):
        match('5')
        parse_I()
    elif lookahead.startswith("'"):
        match("'")
        match('o')
        parse_P()
        match('0')
    elif lookahead.startswith('o'):
        match('o')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['5', "'", 'o']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('R'):
        match('R')
        match('1')
        match('1')
    elif lookahead.startswith('F'):
        parse_F()
        match('H')
    elif lookahead.startswith('I'):
        parse_I()
        match('s')
        match('-')
    elif lookahead.startswith('['):
        match('[')
        match(')')
        match('+')
        match('x')
        match('7')
    elif lookahead.startswith('~'):
        match('~')
        parse_I()
        match('C')
        match('c')
    elif lookahead.startswith('Q'):
        match('Q')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['R', 'F', 'I', '[', '~', 'Q']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('R'):
        match('R')
        match('f')
        parse_D()
    elif lookahead.startswith('D'):
        parse_D()
        match('v')
        match('k')
    elif lookahead.startswith('m'):
        match('m')
        parse_G()
        match('N')
        match('r')
        match('A')
    elif lookahead.startswith('O'):
        match('O')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['R', 'D', 'm', 'O']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('7'):
        match('7')
        parse_I()
        parse_P()
        match(':')
        match('Y')
    elif lookahead.startswith("'"):
        match("'")
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['7', "'"]))

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