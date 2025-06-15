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
    if lookahead.startswith('8'):
        match('8')
        match('Z')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('$'):
            match('$')
        elif lookahead.startswith("'"):
            match("'")
        elif lookahead.startswith('5'):
            match('5')
            parse_E()
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['$', "'", '5']))
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith("'"):
            match("'")
            match('?')
            match('U')
            parse_J()
            parse_W()
        elif lookahead.startswith(','):
            match(',')
            match('@')
            parse_E()
        elif lookahead.startswith('f'):
            match('f')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(["'", ',', 'f']))
    elif lookahead.startswith('h'):
        match('h')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['8', 'h']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('$'):
        match('$')
    elif lookahead.startswith("'"):
        match("'")
    elif lookahead.startswith('5'):
        match('5')
        parse_E()
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['$', "'", '5']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        match('?')
        match('U')
        parse_J()
        parse_W()
    elif lookahead.startswith(','):
        match(',')
        match('@')
        parse_E()
    elif lookahead.startswith('f'):
        match('f')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(["'", ',', 'f']))

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