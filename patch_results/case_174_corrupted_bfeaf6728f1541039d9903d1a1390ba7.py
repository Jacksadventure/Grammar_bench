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
    if lookahead.startswith('l'):
        match('l')
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith(']'):
            match(']')
        elif lookahead.startswith('v'):
            match('v')
            parse_Y()
            parse_J()
        elif lookahead.startswith('7'):
            match('7')
        elif lookahead.startswith('.'):
            match('.')
            match('f')
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join([']', 'v', '7', '.']))
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith(']'):
            match(']')
        elif lookahead.startswith('v'):
            match('v')
            parse_Y()
            parse_J()
        elif lookahead.startswith('7'):
            match('7')
        elif lookahead.startswith('.'):
            match('.')
            match('f')
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join([']', 'v', '7', '.']))
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('&'):
            match('&')
            match('`')
            match('C')
            parse_V()
        elif lookahead.startswith('8'):
            match('8')
            match('c')
            parse_J()
        elif lookahead.startswith('J'):
            parse_J()
            match(')')
            parse_Y()
            match('c')
            match('y')
        elif lookahead.startswith('l'):
            match('l')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['&', '8', 'J', 'l']))
    elif lookahead.startswith(','):
        match(',')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['l', ',']))

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('&'):
        match('&')

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('&'):
        match('&')
        match('`')
        match('C')
        parse_V()
    elif lookahead.startswith('8'):
        match('8')
        match('c')
        parse_J()
    elif lookahead.startswith('J'):
        parse_J()
        match(')')
        parse_Y()
        match('c')
        match('y')
    elif lookahead.startswith('l'):
        match('l')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['&', '8', 'J', 'l']))

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