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

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('G'):
        match('G')
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith('K'):
            match('K')
            match('Z')
            match('X')
            parse_Q()
            parse_R()
        elif lookahead.startswith('y'):
            match('y')
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['K', 'y']))
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('-'):
            match('-')
            parse_J()
            match('F')
            match('e')
        elif lookahead.startswith('e'):
            match('e')
            parse_U()
            parse_L()
        elif lookahead.startswith('/'):
            match('/')
            match('M')
        elif lookahead.startswith('#'):
            match('#')
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['-', 'e', '/', '#']))
    elif lookahead.startswith("'"):
        match("'")
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['G', "'"]))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('}'):
        match('}')
        parse_J()
    elif lookahead.startswith('K'):
        match('K')
        parse_U()
        parse_D()
        match('6')
    elif lookahead.startswith('W'):
        match('W')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['}', 'K', 'W']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('{'):
        match('{')
    elif lookahead.startswith('G'):
        match('G')
        match('-')
        match('4')
        match('o')
        parse_Q()
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['{', 'G']))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
        parse_L()
    elif lookahead.startswith('C'):
        match('C')
        parse_Q()
        match('^')
        match('k')
        parse_U()
    elif lookahead.startswith('a'):
        match('a')
        match('Z')
        match('v')
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['j', 'C', 'a', 'd']))

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('('):
        match('(')

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('K'):
        match('K')
        match('Z')
        match('X')
        parse_Q()
        parse_R()
    elif lookahead.startswith('y'):
        match('y')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['K', 'y']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('S'):
        match('S')
        match('d')
        match('P')
    elif lookahead.startswith('h'):
        match('h')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['S', 'h']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_E()
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