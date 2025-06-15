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

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('J'):
        match('J')
        while pos < len(tokens) and tokens[pos].startswith('_'):
            match('_')
            match('h')
            match('E')
            parse_X()
            parse_I()
    elif lookahead.startswith('7'):
        match('7')
        while pos < len(tokens) and tokens[pos].startswith('|'):
            match('|')
            match('2')
            match(']')
            match('z')
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith("'"):
            match("'")
            match('!')
            match('/')
        elif lookahead.startswith('a'):
            match('a')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(["'", 'a']))
        match('h')
    elif lookahead.startswith('j'):
        match('j')
        match('@')
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('J'):
            match('J')
            parse_F()
        elif lookahead.startswith('7'):
            match('7')
            parse_M()
            parse_W()
            match('h')
        elif lookahead.startswith('j'):
            match('j')
            match('@')
            parse_X()
        elif lookahead.startswith('h'):
            match('h')
            match('-')
        elif lookahead.startswith('O'):
            match('O')
            parse_W()
        elif lookahead.startswith('W'):
            parse_W()
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['J', '7', 'j', 'h', 'O', 'W']))
    elif lookahead.startswith('h'):
        match('h')
        match('-')
    elif lookahead.startswith('O'):
        match('O')
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith("'"):
            match("'")
            match('!')
            match('/')
        elif lookahead.startswith('a'):
            match('a')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(["'", 'a']))
    elif lookahead.startswith('W'):
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith("'"):
            match("'")
            match('!')
            match('/')
        elif lookahead.startswith('a'):
            match('a')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(["'", 'a']))
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['J', '7', 'j', 'h', 'O', 'W']))

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('_'):
        match('_')
        match('h')
        match('E')
        parse_X()
        parse_I()

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('q'):
        match('q')
        match('O')
    elif lookahead.startswith('|'):
        match('|')
    elif lookahead.startswith('e'):
        match('e')
        match('D')
        match(']')
        match('8')
        match(',')
    elif lookahead.startswith('}'):
        match('}')
        match('8')
        parse_F()
        parse_W()
        parse_F()
    elif lookahead.startswith('2'):
        match('2')
        match('c')
        match('+')
        match('#')
        match('b')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['q', '|', 'e', '}', '2']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        match('!')
        match('/')
    elif lookahead.startswith('a'):
        match('a')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(["'", 'a']))

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('|'):
        match('|')
        match('2')
        match(']')
        match('z')

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('F'):
        parse_F()
        match('N')
        parse_F()
    elif lookahead.startswith('u'):
        match('u')
        parse_X()
        parse_T()
    elif lookahead.startswith('Q'):
        match('Q')
    elif lookahead.startswith('9'):
        match('9')
        match('+')
        match("'")
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['F', 'u', 'Q', '9']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_X()
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