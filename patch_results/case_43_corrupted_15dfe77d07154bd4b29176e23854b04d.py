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

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('f'):
        match('f')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('d'):
            match('d')
            parse_Q()
            parse_Q()
        elif lookahead.startswith('='):
            match('=')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['d', '=']))
        if pos >= len(tokens):
            error("Unexpected end of input in Q")
        lookahead = tokens[pos]
        if lookahead.startswith('f'):
            match('f')
            parse_T()
            parse_Q()
            match('4')
            match('e')
        elif lookahead.startswith('z'):
            match('z')
            parse_T()
        elif lookahead.startswith('@'):
            match('@')
        else:
            error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['f', 'z', '@']))
        match('4')
        match('e')
    elif lookahead.startswith('z'):
        match('z')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('d'):
            match('d')
            parse_Q()
            parse_Q()
        elif lookahead.startswith('='):
            match('=')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['d', '=']))
    elif lookahead.startswith('@'):
        match('@')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['f', 'z', '@']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('d'):
        match('d')
        parse_Q()
        parse_Q()
    elif lookahead.startswith('='):
        match('=')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['d', '=']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Q()
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