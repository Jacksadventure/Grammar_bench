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
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('O'):
        match('O')
        match('I')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('|'):
            match('|')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['|']))
        match('w')
        match('F')
    elif lookahead.startswith('w'):
        match('w')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('O'):
            match('O')
            match('I')
            parse_A()
            match('w')
            match('F')
        elif lookahead.startswith('w'):
            match('w')
            parse_E()
            parse_E()
            match('+')
            parse_V()
        elif lookahead.startswith('f'):
            match('f')
            parse_E()
        elif lookahead.startswith('r'):
            match('r')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['O', 'w', 'f', 'r']))
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('O'):
            match('O')
            match('I')
            parse_A()
            match('w')
            match('F')
        elif lookahead.startswith('w'):
            match('w')
            parse_E()
            parse_E()
            match('+')
            parse_V()
        elif lookahead.startswith('f'):
            match('f')
            parse_E()
        elif lookahead.startswith('r'):
            match('r')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['O', 'w', 'f', 'r']))
        match('+')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('j'):
            match('j')
            match('D')
            parse_A()
            parse_A()
        elif lookahead.startswith('a'):
            match('a')
            match('F')
        elif lookahead.startswith('c'):
            match('c')
            parse_E()
            parse_V()
            parse_A()
            parse_E()
        elif lookahead.startswith('='):
            match('=')
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['j', 'a', 'c', '=']))
    elif lookahead.startswith('f'):
        match('f')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('O'):
            match('O')
            match('I')
            parse_A()
            match('w')
            match('F')
        elif lookahead.startswith('w'):
            match('w')
            parse_E()
            parse_E()
            match('+')
            parse_V()
        elif lookahead.startswith('f'):
            match('f')
            parse_E()
        elif lookahead.startswith('r'):
            match('r')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['O', 'w', 'f', 'r']))
    elif lookahead.startswith('r'):
        match('r')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['O', 'w', 'f', 'r']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
        match('D')
        parse_A()
        parse_A()
    elif lookahead.startswith('a'):
        match('a')
        match('F')
    elif lookahead.startswith('c'):
        match('c')
        parse_E()
        parse_V()
        parse_A()
        parse_E()
    elif lookahead.startswith('='):
        match('=')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['j', 'a', 'c', '=']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('|'):
        match('|')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['|']))

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