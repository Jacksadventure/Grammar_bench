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
    if lookahead.startswith('v'):
        match('v')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('v'):
            match('v')
            parse_J()
            parse_M()
        elif lookahead.startswith('H'):
            match('H')
            parse_J()
        elif lookahead.startswith('k'):
            match('k')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['v', 'H', 'k']))
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('y'):
            match('y')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['y']))
    elif lookahead.startswith('H'):
        match('H')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('v'):
            match('v')
            parse_J()
            parse_M()
        elif lookahead.startswith('H'):
            match('H')
            parse_J()
        elif lookahead.startswith('k'):
            match('k')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['v', 'H', 'k']))
    elif lookahead.startswith('k'):
        match('k')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['v', 'H', 'k']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('y'):
        match('y')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['y']))

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