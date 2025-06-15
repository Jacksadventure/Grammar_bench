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

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('c'):
        match('c')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('V'):
            match('V')
            parse_R()
            parse_Q()
            parse_X()
        elif lookahead.startswith('*'):
            match('*')
            match(':')
            parse_T()
            parse_X()
            parse_R()
        elif lookahead.startswith('d'):
            match('d')
            parse_T()
            parse_R()
        elif lookahead.startswith('&'):
            match('&')
            parse_X()
            parse_X()
            parse_X()
            parse_X()
        elif lookahead.startswith('g'):
            match('g')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['V', '*', 'd', '&', 'g']))
        if pos >= len(tokens):
            error("Unexpected end of input in Q")
        lookahead = tokens[pos]
        if lookahead.startswith(')'):
            match(')')
            match('m')
        else:
            error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join([')', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('?'):
            match('?')
            parse_R()
            parse_Q()
            parse_R()
        elif lookahead.startswith('s'):
            match('s')
            parse_P()
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['?', '', 's']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('U'):
        match('U')
        match('b')
        parse_R()
    elif lookahead.startswith('7'):
        match('7')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['U', '7']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith(')'):
        match(')')
        match('m')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join([')', '']))

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('?'):
        match('?')
        parse_R()
        parse_Q()

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('V'):
        match('V')
        parse_R()
        parse_Q()
        parse_X()
    elif lookahead.startswith('*'):
        match('*')
        match(':')
        parse_T()
        parse_X()
        parse_R()
    elif lookahead.startswith('d'):
        match('d')
        parse_T()
        parse_R()
    elif lookahead.startswith('&'):
        match('&')
        parse_X()
        parse_X()
        parse_X()
        parse_X()
    elif lookahead.startswith('g'):
        match('g')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['V', '*', 'd', '&', 'g']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_X()
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