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
    while pos < len(tokens) and tokens[pos].startswith('!'):
        match('!')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('M'):
            match('M')
            match('#')
            parse_U()
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['M', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in Q")
        lookahead = tokens[pos]
        if lookahead.startswith('|'):
            match('|')
            parse_E()
            parse_Q()
            parse_U()
            parse_T()
        elif lookahead.startswith('V'):
            parse_V()
            match('z')
            match('q')
            parse_Q()
        elif lookahead.startswith('@'):
            match('@')
        else:
            error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['|', 'V', '@']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('c'):
        match('c')
        parse_E()
        parse_E()
    elif lookahead.startswith('h'):
        match('h')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['c', 'h']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('|'):
        match('|')
        parse_E()
        parse_Q()
        parse_U()
        parse_T()
    elif lookahead.startswith('V'):
        parse_V()
        match('z')
        match('q')
        parse_Q()
    elif lookahead.startswith('@'):
        match('@')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['|', 'V', '@']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        match(']')
        match('~')
    elif lookahead.startswith('#'):
        match('#')
        parse_U()
        parse_X()
    elif lookahead.startswith('g'):
        match('g')
        parse_B()
        parse_X()
    elif lookahead.startswith('i'):
        match('i')
        parse_E()
        parse_U()
        parse_X()
        match('L')
    elif lookahead.startswith('&'):
        match('&')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join([']', '#', 'g', 'i', '&']))

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('M'):
        match('M')
        match('#')

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('h'):
        match('h')
        parse_T()
        parse_B()
        parse_X()
        parse_F()

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('&'):
        match('&')
        match('u')

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Y'):
        match('Y')
        match('!')
        parse_B()

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