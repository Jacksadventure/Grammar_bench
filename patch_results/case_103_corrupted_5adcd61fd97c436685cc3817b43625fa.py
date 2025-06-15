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

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(']'):
        match(']')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('*'):
            match('*')
            match("'")
            parse_T()
            match('{')
            parse_V()
            parse_V()
        elif lookahead.startswith('['):
            match('[')
            parse_M()
            parse_K()
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['*', '', '[']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('W'):
        match('W')
    elif lookahead.startswith('k'):
        match('k')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['W', 'k']))

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('*'):
        match('*')
        match("'")
        parse_T()
        match('{')
        parse_V()

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('<'):
        match('<')
    elif lookahead.startswith('A'):
        match('A')
        match('o')
        match('2')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['<', 'A']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('9'):
        match('9')
    elif lookahead.startswith('Z'):
        match('Z')
        match('c')
        match('y')
        match('d')
        parse_G()
    elif lookahead.startswith('D'):
        match('D')
        match('m')
        parse_V()
        match('v')
    elif lookahead.startswith('^'):
        match('^')
        parse_G()
        match('6')
        parse_T()
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['9', 'Z', 'D', '^']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('P'):
        match('P')
        match('|')
        match('k')
        match(':')
    elif lookahead.startswith('?'):
        match('?')
        match('/')
        match('*')
    elif lookahead.startswith('C'):
        parse_C()
        match('~')
        parse_G()
    elif lookahead.startswith('_'):
        match('_')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['P', '?', 'C', '_']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_C()
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