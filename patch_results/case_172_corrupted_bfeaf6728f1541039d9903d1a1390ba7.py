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
    if lookahead.startswith('E'):
        match('E')
        match('X')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('<'):
            match('<')
            parse_T()
            match('r')
            match('!')
        elif lookahead.startswith('4'):
            match('4')
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['<', '4']))
    elif lookahead.startswith('N'):
        match('N')
        match('~')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('5'):
            match('5')
            match('l')
            match('|')
            match('^')
            match('7')
        elif lookahead.startswith('L'):
            match('L')
            parse_B()
            parse_B()
        elif lookahead.startswith('R'):
            match('R')
            match('S')
        elif lookahead.startswith('u'):
            match('u')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['5', 'L', 'R', 'u']))
        match('d')
    elif lookahead.startswith('S'):
        match('S')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['E', 'N', 'S']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('%'):
        match('%')
        match(';')
        match('d')
        match('y')
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['%', 'd']))

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