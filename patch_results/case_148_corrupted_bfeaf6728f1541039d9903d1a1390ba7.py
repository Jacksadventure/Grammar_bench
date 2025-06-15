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

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('#'):
        match('#')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('#'):
            match('#')
            parse_G()
            parse_G()
        elif lookahead.startswith('9'):
            match('9')
            parse_B()
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['#', '', '9']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('{'):
        match('{')
        match('X')
        match('c')

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('-'):
        match('-')
        parse_G()
        match('+')
        parse_C()
        match('*')

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('('):
        match('(')
    elif lookahead.startswith('|'):
        match('|')
        match('6')
        parse_G()
        parse_G()
        parse_L()
    elif lookahead.startswith('d'):
        match('d')
        match('^')
    elif lookahead.startswith('E'):
        match('E')
    elif lookahead.startswith('Y'):
        match('Y')
        parse_L()
        parse_D()
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['(', '|', 'd', 'E', 'Y']))

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('$'):
        match('$')
        match('m')
        parse_L()

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('k'):
        match('k')
        match('j')
        match('Z')
        parse_L()
        parse_G()

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('*'):
        match('*')

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('{'):
        match('{')
        parse_L()
        parse_G()
        parse_C()
        parse_W()
    elif lookahead.startswith('Z'):
        match('Z')
        parse_Q()
    elif lookahead.startswith(','):
        match(',')
        parse_D()
        match("'")
        match('%')
        parse_J()
    elif lookahead.startswith('a'):
        match('a')
        parse_W()
        parse_C()
        parse_W()
        parse_G()
    elif lookahead.startswith('$'):
        match('$')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['{', 'Z', ',', 'a', '$']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_G()
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