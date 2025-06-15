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

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('E'):
        match('E')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('E'):
            match('E')
            parse_H()
        elif lookahead.startswith('s'):
            match('s')
            parse_N()
        elif lookahead.startswith('s'):
            match('s')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['E', 's', 's']))
    elif lookahead.startswith('s'):
        match('s')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('F'):
            match('F')
            match(']')
        elif lookahead.startswith('*'):
            match('*')
            match('`')
            match('3')
            match('L')
        elif lookahead.startswith('+'):
            match('+')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['F', '*', '+']))
    elif lookahead.startswith('s'):
        match('s')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['E', 's', 's']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('F'):
        match('F')
        match(']')
    elif lookahead.startswith('*'):
        match('*')
        match('`')
        match('3')
        match('L')
    elif lookahead.startswith('+'):
        match('+')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['F', '*', '+']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_H()
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