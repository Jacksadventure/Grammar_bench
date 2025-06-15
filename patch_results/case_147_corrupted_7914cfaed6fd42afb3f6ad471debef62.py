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

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('T'):
            match('T')
            match('=')
            match('(')
            parse_B()
            parse_K()
        elif lookahead.startswith('_'):
            match('_')
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['T', '_']))
        match('o')
    elif lookahead.startswith('?'):
        match('?')
        match('$')
        while pos < len(tokens) and tokens[pos].startswith("'"):
            match("'")
            parse_O()
            match('(')
            match("'")
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['/', '?', 'd']))

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('T'):
        match('T')
        match('=')
        match('(')
        parse_B()
        parse_K()
    elif lookahead.startswith('_'):
        match('_')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['T', '_']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('#'):
        match('#')
        match('t')
        match('/')
        match('r')
        match('H')
    elif lookahead.startswith('A'):
        match('A')
        match('|')
        match(']')
        parse_O()
        parse_O()
    elif lookahead.startswith('`'):
        match('`')
        match('c')
        parse_O()
        parse_O()
        match(',')
    elif lookahead.startswith('Z'):
        parse_Z()
    elif lookahead.startswith('C'):
        match('C')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['#', 'A', '`', 'Z', 'C']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('Q'):
        match('Q')
    elif lookahead.startswith('U'):
        match('U')
        parse_W()
        parse_O()
        parse_O()
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['Q', 'U']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        parse_Y()
        match('e')
        match('T')
        parse_E()
    elif lookahead.startswith('9'):
        match('9')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['?', '9']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('!'):
        match('!')
        match('>')
    elif lookahead.startswith('a'):
        match('a')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['!', 'a']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('j'):
        match('j')
        match('D')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_O()
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