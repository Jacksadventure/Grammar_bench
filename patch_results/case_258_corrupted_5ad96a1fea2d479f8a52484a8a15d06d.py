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

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('4'):
        match('4')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('.'):
            match('.')
            match('Z')
            match('H')
            match('2')
            parse_K()
        elif lookahead.startswith('o'):
            match('o')
            match('(')
            parse_Y()
            parse_W()
            match('C')
        elif lookahead.startswith('*'):
            match('*')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['.', 'o', '*']))
    elif lookahead.startswith('|'):
        match('|')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['4', '|']))

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('2'):
        match('2')

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('S'):
        match('S')
        parse_B()
        parse_W()
        parse_J()
        parse_W()
        parse_R()
    elif lookahead.startswith('2'):
        match('2')
        parse_L()
        parse_P()
    elif lookahead.startswith('p'):
        match('p')
        match('9')
        match('F')
        parse_W()
        parse_T()
    elif lookahead.startswith("'"):
        match("'")
        parse_P()
        parse_R()
    elif lookahead.startswith('X'):
        match('X')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['S', '2', 'p', "'", 'X']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('&'):
        match('&')
        parse_L()
        match('*')
        parse_B()
    elif lookahead.startswith('M'):
        match('M')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['&', 'M']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('6'):
        match('6')
        match('Q')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['6', '']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('.'):
        match('.')
        match('Z')
        match('H')
        match('2')
        parse_K()
    elif lookahead.startswith('o'):
        match('o')
        match('(')
        parse_Y()
        parse_W()
        match('C')
    elif lookahead.startswith('*'):
        match('*')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['.', 'o', '*']))

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('C'):
        match('C')

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('_'):
        match('_')
        match('~')
        match('8')
        match("'")

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('6'):
        match('6')
    elif lookahead.startswith('$'):
        match('$')
        match('%')
        match('e')
        parse_Y()
        parse_Y()
    elif lookahead.startswith("'"):
        match("'")
        parse_T()
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['6', '$', "'"]))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_R()
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