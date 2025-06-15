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

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('s'):
            match('s')
            parse_P()
            parse_W()
            parse_W()
            match('q')
        elif lookahead.startswith(']'):
            match(']')
            parse_P()
            parse_P()
            match('v')
        elif lookahead.startswith('G'):
            match('G')
            match('E')
            parse_K()
            parse_P()
            parse_K()
        elif lookahead.startswith('~'):
            match('~')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['s', ']', 'G', '~']))
    elif lookahead.startswith('&'):
        match('&')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['o', '&']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('V'):
        parse_V()
        match('f')

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('X'):
        match('X')
        parse_F()
        parse_F()
        match('v')
        match(')')
    elif lookahead.startswith('b'):
        match('b')
    elif lookahead.startswith('('):
        match('(')
    elif lookahead.startswith("'"):
        match("'")
        parse_K()
        match('<')
        parse_J()
    elif lookahead.startswith('T'):
        match('T')
        parse_F()
        parse_U()
        match('-')
        match('u')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['X', 'b', '(', "'", 'T']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('s'):
        match('s')
        parse_P()
        parse_W()
        parse_W()
        match('q')
    elif lookahead.startswith(']'):
        match(']')
        parse_P()
        parse_P()
        match('v')
    elif lookahead.startswith('G'):
        match('G')
        match('E')
        parse_K()
        parse_P()
        parse_K()
    elif lookahead.startswith('~'):
        match('~')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['s', ']', 'G', '~']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('u'):
        match('u')
        parse_F()
        match(':')
        parse_V()

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
    elif lookahead.startswith('`'):
        match('`')
        parse_F()
    elif lookahead.startswith('t'):
        match('t')
        match('q')
        match(';')
        parse_K()
        parse_K()
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join([',', '`', 't']))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('X'):
        match('X')
        match('[')
        match('L')
    elif lookahead.startswith('>'):
        match('>')
        parse_K()
    elif lookahead.startswith('u'):
        match('u')
    elif lookahead.startswith('A'):
        match('A')
        parse_K()
        parse_J()
        match('Y')
        parse_J()
    elif lookahead.startswith('^'):
        match('^')
        parse_W()
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['X', '>', 'u', 'A', '^']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_V()
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