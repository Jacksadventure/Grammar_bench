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

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('f'):
        match('f')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('='):
            match('=')
            parse_V()
        elif lookahead.startswith('!'):
            match('!')
            parse_V()
            parse_I()
            parse_V()
            parse_I()
        elif lookahead.startswith('u'):
            match('u')
            match("'")
            match('8')
        elif lookahead.startswith('v'):
            match('v')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['=', '!', 'u', 'v']))
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('T'):
            match('T')
            match('e')
        elif lookahead.startswith('$'):
            match('$')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['T', '$']))
    elif lookahead.startswith('8'):
        match('8')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['f', '8']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('='):
        match('=')
        parse_V()
    elif lookahead.startswith('!'):
        match('!')
        parse_V()
        parse_I()
        parse_V()
        parse_I()
    elif lookahead.startswith('u'):
        match('u')
        match("'")
        match('8')
    elif lookahead.startswith('v'):
        match('v')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['=', '!', 'u', 'v']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_V()
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