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

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        match('L')
        match('M')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('v'):
            match('v')
        elif lookahead.startswith('j'):
            match('j')
            match('e')
            parse_W()
        elif lookahead.startswith('t'):
            match('t')
            match('x')
            parse_O()
        elif lookahead.startswith('J'):
            match('J')
            parse_O()
            parse_A()
            match('h')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['v', 'j', 't', 'J']))
        while pos < len(tokens) and tokens[pos].startswith('a'):
            match('a')
            match('`')
            match(':')
    elif lookahead.startswith("'"):
        match("'")
        match('|')
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('N'):
            parse_N()
            match('q')
        elif lookahead.startswith('k'):
            match('k')
            match('=')
            match(']')
            match('=')
        elif lookahead.startswith('G'):
            match('G')
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['N', 'k', 'G']))
    elif lookahead.startswith('7'):
        match('7')
        match('D')
    elif lookahead.startswith('y'):
        match('y')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['w', "'", '7', 'y']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('N'):
        parse_N()
        match('q')
    elif lookahead.startswith('k'):
        match('k')
        match('=')
        match(']')
        match('=')
    elif lookahead.startswith('G'):
        match('G')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['N', 'k', 'G']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('v'):
        match('v')
    elif lookahead.startswith('j'):
        match('j')
        match('e')
        parse_W()
    elif lookahead.startswith('t'):
        match('t')
        match('x')
        parse_O()
    elif lookahead.startswith('J'):
        match('J')
        parse_O()
        parse_A()
        match('h')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['v', 'j', 't', 'J']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('i'):
        match('i')
        match('B')
        match('I')
        parse_Y()
    elif lookahead.startswith('7'):
        match('7')
        parse_W()
        parse_W()
        match('b')
        match('7')
    elif lookahead.startswith('r'):
        match('r')
    elif lookahead.startswith('~'):
        match('~')
        match('r')
        match('P')
    elif lookahead.startswith('='):
        match('=')
        parse_A()
        parse_A()
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['i', '7', 'r', '~', '=']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('i'):
        match('i')

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('h'):
        match('h')
        parse_O()
    elif lookahead.startswith("'"):
        match("'")
        match('}')
    elif lookahead.startswith(':'):
        match(':')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['h', "'", ':']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('a'):
        match('a')
        match('`')
        match(':')

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('8'):
        match('8')
        parse_W()
        parse_K()
        parse_R()
        parse_S()

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('^'):
        match('^')
        parse_E()
        parse_R()
    elif lookahead.startswith('1'):
        match('1')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['^', '1']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_N()
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