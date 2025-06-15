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
    if lookahead.startswith('y'):
        match('y')
        match('k')
        match('6')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('C'):
            match('C')
            match('u')
            match('Z')
            parse_E()
        elif lookahead.startswith('='):
            match('=')
        elif lookahead.startswith('_'):
            match('_')
            match('d')
            match('S')
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['C', '=', '_']))
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('$'):
            match('$')
            match('4')
            match('p')
            match('C')
            match('b')
        elif lookahead.startswith('s'):
            match('s')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['$', 's']))
    elif lookahead.startswith('_'):
        match('_')
        match('S')
    elif lookahead.startswith('b'):
        match('b')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('y'):
            match('y')
            match('k')
            match('6')
            parse_V()
            parse_J()
        elif lookahead.startswith('_'):
            match('_')
            match('S')
        elif lookahead.startswith('b'):
            match('b')
            parse_E()
        elif lookahead.startswith('x'):
            match('x')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['y', '_', 'b', 'x']))
    elif lookahead.startswith('x'):
        match('x')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['y', '_', 'b', 'x']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('C'):
        match('C')
        match('u')
        match('Z')
        parse_E()
    elif lookahead.startswith('='):
        match('=')
    elif lookahead.startswith('_'):
        match('_')
        match('d')
        match('S')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['C', '=', '_']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('$'):
        match('$')
        match('4')
        match('p')
        match('C')
        match('b')
    elif lookahead.startswith('s'):
        match('s')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['$', 's']))

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