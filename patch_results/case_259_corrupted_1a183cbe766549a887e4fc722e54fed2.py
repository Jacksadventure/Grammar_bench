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
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('y'):
        match('y')
        while pos < len(tokens) and tokens[pos].startswith('.'):
            match('.')
            parse_L()
            parse_O()
            parse_D()
    elif lookahead.startswith('='):
        match('=')
    elif lookahead.startswith('a'):
        match('a')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['y', '=', 'a']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
        match('W')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['+', '']))

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('.'):
        match('.')
        parse_L()
        parse_O()
        parse_D()

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('`'):
        match('`')
        match('K')
        parse_G()
        parse_D()
    elif lookahead.startswith('b'):
        match('b')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['`', 'b']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('u'):
        match('u')
        match('U')
    elif lookahead.startswith('('):
        match('(')
        parse_D()
        parse_G()
        parse_L()
        match('q')
    elif lookahead.startswith('o'):
        match('o')
        parse_L()
        parse_V()
    elif lookahead.startswith('w'):
        match('w')
        parse_O()
        parse_V()
        parse_L()
    elif lookahead.startswith(')'):
        match(')')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['u', '(', 'o', 'w', ')']))

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