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

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('q'):
        match('q')
        match('N')
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('N'):
            match('N')
            match('*')
            match('W')
            match("'")
            match('s')
        elif lookahead.startswith('1'):
            match('1')
            match('G')
            match(':')
            match(':')
            match('[')
        elif lookahead.startswith('k'):
            match('k')
            match('O')
            parse_V()
        elif lookahead.startswith('w'):
            match('w')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['N', '1', 'k', 'w']))
        match('J')
        match('1')
    elif lookahead.startswith('|'):
        match('|')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['q', '|']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('{'):
        match('{')
    elif lookahead.startswith('*'):
        match('*')
        match('d')
        parse_X()
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['{', '*']))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('N'):
        match('N')
        match('*')
        match('W')
        match("'")
        match('s')
    elif lookahead.startswith('1'):
        match('1')
        match('G')
        match(':')
        match(':')
        match('[')
    elif lookahead.startswith('k'):
        match('k')
        match('O')
        parse_V()
    elif lookahead.startswith('w'):
        match('w')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['N', '1', 'k', 'w']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('4'):
        match('4')
        match('r')
        parse_X()
        match('M')
        parse_A()
    elif lookahead.startswith('m'):
        match('m')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['4', 'm']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_H()
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