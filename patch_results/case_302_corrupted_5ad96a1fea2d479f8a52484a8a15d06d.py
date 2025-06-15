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
    if lookahead.startswith('5'):
        match('5')
        while pos < len(tokens) and tokens[pos].startswith('<'):
            match('<')
            parse_F()
            parse_F()
            parse_V()
            parse_K()
        match('u')
    elif lookahead.startswith('*'):
        match('*')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['5', '*']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('v'):
        match('v')
        match('v')
        parse_K()
    elif lookahead.startswith('m'):
        match('m')
    elif lookahead.startswith('J'):
        match('J')
        match('3')
        match('t')
        match(')')
    elif lookahead.startswith('y'):
        match('y')
        parse_I()
        match('f')
        parse_V()
        parse_V()
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['v', 'm', 'J', 'y']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('1'):
        match('1')
        match("'")
        match('4')
    elif lookahead.startswith('/'):
        match('/')
    elif lookahead.startswith('a'):
        match('a')
        match('k')
        match('%')
        parse_V()
        match('/')
    elif lookahead.startswith('~'):
        match('~')
        parse_K()
        parse_K()
        parse_K()
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['1', '/', 'a', '~']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('A'):
        match('A')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['A']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('6'):
        match('6')
    elif lookahead.startswith('2'):
        match('2')
        match('q')
        parse_G()
    elif lookahead.startswith('3'):
        match('3')
        match('%')
        match('z')
        match('/')
    elif lookahead.startswith('}'):
        match('}')
        match('R')
        match("'")
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['6', '2', '3', '}']))

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