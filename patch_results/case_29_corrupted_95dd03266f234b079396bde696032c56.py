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
    if lookahead.startswith('K'):
        match('K')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('K'):
            match('K')
            parse_V()
            match(';')
            parse_V()
        elif lookahead.startswith('f'):
            match('f')
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['K', 'f']))
        match(';')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('K'):
            match('K')
            parse_V()
            match(';')
            parse_V()
        elif lookahead.startswith('f'):
            match('f')
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['K', 'f']))
    elif lookahead.startswith('f'):
        match('f')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['K', 'f']))

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