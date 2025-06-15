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
        match('(')
        match('s')
        match('=')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('e'):
            match('e')
            parse_T()
            match('J')
            parse_K()
        elif lookahead.startswith('`'):
            match('`')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['e', '`']))
    elif lookahead.startswith('J'):
        match('J')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['-', 'J']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('e'):
        match('e')
        parse_T()
        match('J')
        parse_K()
    elif lookahead.startswith('`'):
        match('`')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['e', '`']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('V'):
        match('V')
        parse_E()
    elif lookahead.startswith('a'):
        match('a')
        match('#')
        match('D')
        match('R')
    elif lookahead.startswith('F'):
        match('F')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['V', 'a', 'F']))

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