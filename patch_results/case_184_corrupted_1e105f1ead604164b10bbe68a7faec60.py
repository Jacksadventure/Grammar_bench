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

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('P'):
        match('P')
        match('w')
        match('u')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('+'):
            match('+')
            match(']')
            match('q')
            match('i')
        elif lookahead.startswith("'"):
            match("'")
        elif lookahead.startswith('s'):
            match('s')
            match('!')
            parse_J()
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['+', "'", 's']))
        match('I')
    elif lookahead.startswith('S'):
        match('S')
        match('a')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('J'):
            parse_J()
            parse_J()
            match("'")
            parse_V()
            match('~')
        elif lookahead.startswith('5'):
            match('5')
            match('i')
            parse_B()
            match('8')
        elif lookahead.startswith('2'):
            match('2')
            match('`')
            match('d')
            match('+')
        elif lookahead.startswith('s'):
            match('s')
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['J', '5', '2', 's']))
    elif lookahead.startswith('<'):
        match('<')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('+'):
            match('+')
            match(']')
            match('q')
            match('i')
        elif lookahead.startswith("'"):
            match("'")
        elif lookahead.startswith('s'):
            match('s')
            match('!')
            parse_J()
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['+', "'", 's']))
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('P'):
            match('P')
            match('w')
            match('u')
            parse_B()
            match('I')
        elif lookahead.startswith('S'):
            match('S')
            match('a')
            parse_V()
        elif lookahead.startswith('<'):
            match('<')
            parse_B()
            parse_J()
        elif lookahead.startswith('f'):
            match('f')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['P', 'S', '<', 'f']))
    elif lookahead.startswith('f'):
        match('f')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['P', 'S', '<', 'f']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('J'):
        parse_J()
        parse_J()
        match("'")
        parse_V()
        match('~')
    elif lookahead.startswith('5'):
        match('5')
        match('i')
        parse_B()
        match('8')
    elif lookahead.startswith('2'):
        match('2')
        match('`')
        match('d')
        match('+')
    elif lookahead.startswith('s'):
        match('s')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['J', '5', '2', 's']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
        match(']')
        match('q')
        match('i')
    elif lookahead.startswith("'"):
        match("'")
    elif lookahead.startswith('s'):
        match('s')
        match('!')
        parse_J()
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['+', "'", 's']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_J()
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