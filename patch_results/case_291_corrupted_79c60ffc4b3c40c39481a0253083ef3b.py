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
    while pos < len(tokens) and tokens[pos].startswith('6'):
        match('6')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('('):
            match('(')
            match("'")
            match('2')
        elif lookahead.startswith('J'):
            match('J')
            parse_E()
            parse_A()
            match('>')
        elif lookahead.startswith('d'):
            match('d')
            match('C')
        elif lookahead.startswith('q'):
            match('q')
            parse_N()
            parse_G()
            parse_A()
        elif lookahead.startswith('3'):
            match('3')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['(', 'J', 'd', 'q', '3']))
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('('):
            match('(')
            match("'")
            match('2')
        elif lookahead.startswith('J'):
            match('J')
            parse_E()
            parse_A()
            match('>')
        elif lookahead.startswith('d'):
            match('d')
            match('C')
        elif lookahead.startswith('q'):
            match('q')
            parse_N()
            parse_G()
            parse_A()
        elif lookahead.startswith('3'):
            match('3')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['(', 'J', 'd', 'q', '3']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('W'):
        match('W')
    elif lookahead.startswith('{'):
        match('{')
        parse_Q()
        match('Y')
    elif lookahead.startswith('a'):
        match('a')
        parse_G()
        match(']')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['W', '{', 'a']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('('):
        match('(')
        match("'")
        match('2')
    elif lookahead.startswith('J'):
        match('J')
        parse_E()
        parse_A()
        match('>')
    elif lookahead.startswith('d'):
        match('d')
        match('C')
    elif lookahead.startswith('q'):
        match('q')
        parse_N()
        parse_G()
        parse_A()
    elif lookahead.startswith('3'):
        match('3')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['(', 'J', 'd', 'q', '3']))

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('!'):
        match('!')
        match('9')

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('C'):
        match('C')
        parse_E()
        parse_E()
        parse_Q()
        parse_K()

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('X'):
        match('X')
        parse_Z()
        parse_S()

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('1'):
        match('1')
        match('4')
        parse_S()
        parse_I()
        parse_N()
    elif lookahead.startswith('z'):
        match('z')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['1', 'z']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('T'):
        parse_T()
        parse_I()
        parse_Q()
        parse_S()

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('s'):
        match('s')
        parse_I()
        parse_N()

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('~'):
        match('~')
        parse_K()

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