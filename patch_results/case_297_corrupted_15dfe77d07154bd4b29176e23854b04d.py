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

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('E'):
        match('E')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('E'):
            match('E')
            parse_H()
            parse_H()
        elif lookahead.startswith('~'):
            match('~')
            parse_A()
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['E', '', '~']))

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('2'):
        match('2')
        parse_X()
        parse_P()
        match('|')

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('5'):
        match('5')
        parse_A()
        parse_H()
        parse_P()
        parse_H()

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('y'):
        match('y')
        parse_I()
        parse_J()
        parse_X()

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('V'):
        match('V')
        parse_Y()
        match('_')
        parse_X()
        match('i')

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('N'):
        match('N')
        parse_X()
        parse_T()

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('u'):
        match('u')
        parse_T()
        parse_I()
    elif lookahead.startswith('6'):
        match('6')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['u', '6']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('9'):
        match('9')
        parse_H()
        match('4')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['9', '']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('|'):
        match('|')
        parse_H()
    elif lookahead.startswith('T'):
        parse_T()
        parse_P()
    elif lookahead.startswith('G'):
        match('G')
        parse_J()
        parse_H()
        match(';')
    elif lookahead.startswith('{'):
        match('{')
        parse_K()
        parse_T()
        parse_J()
        parse_I()
    elif lookahead.startswith('y'):
        match('y')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['|', 'T', 'G', '{', 'y']))

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Q'):
        match('Q')
        parse_H()
        match('{')
        parse_R()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_H()
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