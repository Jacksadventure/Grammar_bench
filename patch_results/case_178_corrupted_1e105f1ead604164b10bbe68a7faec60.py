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
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith("'"):
            match("'")
            parse_L()
            parse_U()
            parse_V()
            parse_L()
            parse_L()
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(["'", '']))
        match('~')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('o'):
            match('o')
            parse_Q()
            parse_L()
        elif lookahead.startswith('&'):
            match('&')
            match('E')
            parse_V()
        elif lookahead.startswith('2'):
            match('2')
            parse_Q()
            parse_L()
        elif lookahead.startswith('L'):
            parse_L()
            match('n')
            match('^')
        elif lookahead.startswith('-'):
            match('-')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['o', '&', '2', 'L', '-']))
        match('t')

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")
        parse_L()
        parse_U()
        parse_V()
        parse_L()

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('h'):
        match('h')
        match("'")
    elif lookahead.startswith('u'):
        match('u')
        parse_U()
    elif lookahead.startswith(':'):
        match(':')
    elif lookahead.startswith('#'):
        match('#')
        parse_Q()
        parse_V()
        parse_U()
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['h', 'u', ':', '#']))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        parse_Q()
        parse_L()
    elif lookahead.startswith('&'):
        match('&')
        match('E')
        parse_V()
    elif lookahead.startswith('2'):
        match('2')
        parse_Q()
        parse_L()
    elif lookahead.startswith('L'):
        parse_L()
        match('n')
        match('^')
    elif lookahead.startswith('-'):
        match('-')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['o', '&', '2', 'L', '-']))

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