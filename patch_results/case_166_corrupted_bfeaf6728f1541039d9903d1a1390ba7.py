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

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('-'):
        match('-')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('-'):
            match('-')
            parse_T()
        elif lookahead.startswith('G'):
            match('G')
            parse_U()
            parse_S()
        elif lookahead.startswith('t'):
            match('t')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['-', 'G', 't']))
    elif lookahead.startswith('G'):
        match('G')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('?'):
            match('?')
            match('E')
        elif lookahead.startswith("'"):
            match("'")
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['?', "'"]))
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('5'):
            match('5')
            parse_T()
            parse_T()
        elif lookahead.startswith('T'):
            parse_T()
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['5', 'T']))
    elif lookahead.startswith('t'):
        match('t')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['-', 'G', 't']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('5'):
        match('5')
        parse_T()
        parse_T()
    elif lookahead.startswith('T'):
        parse_T()
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['5', 'T']))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        match('E')
    elif lookahead.startswith("'"):
        match("'")
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['?', "'"]))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_T()
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