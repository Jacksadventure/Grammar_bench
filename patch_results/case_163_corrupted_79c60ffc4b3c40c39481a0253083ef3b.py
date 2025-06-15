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

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('x'):
        match('x')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('x'):
            match('x')
            parse_A()
        elif lookahead.startswith('~'):
            match('~')
            match('a')
            parse_A()
            match('2')
            parse_M()
        elif lookahead.startswith('i'):
            match('i')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['x', '~', 'i']))
    elif lookahead.startswith('~'):
        match('~')
        match('a')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('x'):
            match('x')
            parse_A()
        elif lookahead.startswith('~'):
            match('~')
            match('a')
            parse_A()
            match('2')
            parse_M()
        elif lookahead.startswith('i'):
            match('i')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['x', '~', 'i']))
        match('2')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('h'):
            match('h')
            match('_')
            parse_M()
            parse_M()
            match(';')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['h', '']))
    elif lookahead.startswith('i'):
        match('i')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['x', '~', 'i']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('h'):
        match('h')
        match('_')
        parse_M()
        parse_M()
        match(';')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['h', '']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_A()
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