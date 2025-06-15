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
    while pos < len(tokens) and tokens[pos].startswith('Y'):
        match('Y')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('8'):
            match('8')
        elif lookahead.startswith('*'):
            match('*')
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['8', '*']))
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('4'):
            match('4')
            parse_W()
            match(',')
            match('%')
            parse_J()
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['4', '']))
        match('x')
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith('i'):
            match('i')
            parse_O()
            parse_L()
        elif lookahead.startswith('?'):
            match('?')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['i', '?']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('8'):
        match('8')
    elif lookahead.startswith('*'):
        match('*')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['8', '*']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('i'):
        match('i')
        parse_O()
        parse_L()
    elif lookahead.startswith('?'):
        match('?')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['i', '?']))

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('7'):
        match('7')
        parse_V()
        parse_L()

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('h'):
        match('h')
        parse_L()
        parse_V()
        parse_W()
    elif lookahead.startswith('i'):
        match('i')
        parse_W()
        parse_J()
    elif lookahead.startswith('o'):
        match('o')
        parse_J()
        match('}')
        parse_I()
        match('v')
    elif lookahead.startswith('O'):
        parse_O()
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['h', 'i', 'o', 'O']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('q'):
        match('q')
    elif lookahead.startswith('-'):
        match('-')
    elif lookahead.startswith('('):
        match('(')
    elif lookahead.startswith('W'):
        parse_W()
    elif lookahead.startswith('/'):
        match('/')
        parse_I()
        parse_N()
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['q', '-', '(', 'W', '/']))

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('&'):
        match('&')
        parse_V()
        parse_N()

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('4'):
        match('4')
        parse_W()
        match(',')
        match('%')

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('n'):
        match('n')
        parse_N()
        parse_I()
        parse_S()
    elif lookahead.startswith('v'):
        match('v')
        parse_S()
        parse_J()
        parse_O()
        match('b')
    elif lookahead.startswith('P'):
        match('P')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['n', 'v', 'P']))

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