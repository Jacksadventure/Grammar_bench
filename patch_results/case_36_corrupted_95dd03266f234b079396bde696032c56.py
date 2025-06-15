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

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('N'):
        match('N')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('N'):
            match('N')
            parse_Z()
            match('4')
            match('g')
            parse_U()
        elif lookahead.startswith('z'):
            match('z')
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['N', 'z']))
        match('4')
        match('g')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('B'):
            match('B')
            match('w')
            match('9')
            match('<')
        elif lookahead.startswith('?'):
            match('?')
            match('3')
            match('s')
            match('z')
            match('c')
        elif lookahead.startswith(','):
            match(',')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['B', '?', ',']))
    elif lookahead.startswith('z'):
        match('z')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['N', 'z']))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('B'):
        match('B')
        match('w')
        match('9')
        match('<')
    elif lookahead.startswith('?'):
        match('?')
        match('3')
        match('s')
        match('z')
        match('c')
    elif lookahead.startswith(','):
        match(',')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['B', '?', ',']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Z()
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