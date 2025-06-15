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

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('A'):
        match('A')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith("'"):
            match("'")
            match('Z')
            match('/')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(["'", '']))
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith('r'):
            match('r')
            parse_K()
        elif lookahead.startswith('$'):
            match('$')
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['r', '$']))
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith('&'):
            match('&')
            parse_K()
            parse_O()
            parse_K()
            parse_W()
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['&', '']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith(';'):
        match(';')
        parse_Y()
        parse_U()
    elif lookahead.startswith('D'):
        match('D')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join([';', 'D']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('r'):
        match('r')
        parse_K()
    elif lookahead.startswith('$'):
        match('$')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['r', '$']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('&'):
        match('&')
        parse_K()
        parse_O()
        parse_K()

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        match('Z')
        match('/')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(["'", '']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Y()
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