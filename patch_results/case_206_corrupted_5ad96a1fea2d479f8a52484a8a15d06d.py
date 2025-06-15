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
    if lookahead.startswith('A'):
        match('A')
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('i'):
            match('i')
            parse_Y()
            match('X')
            parse_B()
            match('<')
        elif lookahead.startswith('/'):
            match('/')
            parse_Y()
            match('(')
        elif lookahead.startswith('D'):
            match('D')
            parse_Q()
        elif lookahead.startswith('_'):
            match('_')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['i', '/', 'D', '_']))
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('D'):
            match('D')
            match('n')
            parse_O()
        elif lookahead.startswith('C'):
            match('C')
            match('g')
            parse_K()
            parse_G()
            parse_B()
        elif lookahead.startswith('2'):
            match('2')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['D', 'C', '2']))
        while pos < len(tokens) and tokens[pos].startswith('G'):
            parse_G()
            parse_Y()
            parse_F()
    elif lookahead.startswith('='):
        match('=')
    elif lookahead.startswith('}'):
        match('}')
        match('U')
    elif lookahead.startswith('.'):
        match('.')
        match('x')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['A', '=', '}', '.']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('D'):
        match('D')
        match('n')
        parse_O()
    elif lookahead.startswith('C'):
        match('C')
        match('g')
        parse_K()
        parse_G()
        parse_B()
    elif lookahead.startswith('2'):
        match('2')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['D', 'C', '2']))

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(')'):
        match(')')
        parse_Q()

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('U'):
        match('U')
    elif lookahead.startswith('m'):
        match('m')
        match('p')
        match('*')
    elif lookahead.startswith('K'):
        parse_K()
    elif lookahead.startswith('c'):
        match('c')
        parse_G()
        match('V')
    elif lookahead.startswith('('):
        match('(')
        match('u')
        match('h')
        parse_I()
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['U', 'm', 'K', 'c', '(']))

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('G'):
        parse_G()
        parse_Y()
        parse_F()

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('i'):
        match('i')
        parse_Y()
        match('X')
        parse_B()
        match('<')
    elif lookahead.startswith('/'):
        match('/')
        parse_Y()
        match('(')
    elif lookahead.startswith('D'):
        match('D')
        parse_Q()
    elif lookahead.startswith('_'):
        match('_')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['i', '/', 'D', '_']))

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('z'):
        match('z')

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('/'):
        match('/')

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