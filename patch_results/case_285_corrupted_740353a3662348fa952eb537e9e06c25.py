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
    if lookahead.startswith('f'):
        match('f')
        match('Y')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('f'):
            match('f')
            match('Y')
            parse_Z()
            parse_K()
        elif lookahead.startswith('J'):
            match('J')
            parse_Z()
            match('}')
        elif lookahead.startswith('_'):
            match('_')
            parse_T()
            parse_K()
        elif lookahead.startswith('e'):
            match('e')
            parse_Z()
        elif lookahead.startswith('s'):
            match('s')
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['f', 'J', '_', 'e', 's']))
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith('B'):
            match('B')
            parse_C()
            parse_G()
        elif lookahead.startswith('4'):
            match('4')
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['B', '4']))
    elif lookahead.startswith('J'):
        match('J')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('f'):
            match('f')
            match('Y')
            parse_Z()
            parse_K()
        elif lookahead.startswith('J'):
            match('J')
            parse_Z()
            match('}')
        elif lookahead.startswith('_'):
            match('_')
            parse_T()
            parse_K()
        elif lookahead.startswith('e'):
            match('e')
            parse_Z()
        elif lookahead.startswith('s'):
            match('s')
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['f', 'J', '_', 'e', 's']))
        match('}')
    elif lookahead.startswith('_'):
        match('_')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('@'):
            match('@')
        elif lookahead.startswith('~'):
            match('~')
        elif lookahead.startswith('q'):
            match('q')
        elif lookahead.startswith('-'):
            match('-')
        elif lookahead.startswith("'"):
            match("'")
            parse_Z()
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['@', '~', 'q', '-', "'"]))
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith('B'):
            match('B')
            parse_C()
            parse_G()
        elif lookahead.startswith('4'):
            match('4')
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['B', '4']))
    elif lookahead.startswith('e'):
        match('e')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('f'):
            match('f')
            match('Y')
            parse_Z()
            parse_K()
        elif lookahead.startswith('J'):
            match('J')
            parse_Z()
            match('}')
        elif lookahead.startswith('_'):
            match('_')
            parse_T()
            parse_K()
        elif lookahead.startswith('e'):
            match('e')
            parse_Z()
        elif lookahead.startswith('s'):
            match('s')
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['f', 'J', '_', 'e', 's']))
    elif lookahead.startswith('s'):
        match('s')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['f', 'J', '_', 'e', 's']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('d'):
        match('d')
        parse_Z()
        match('e')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['d', '']))

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('0'):
        match('0')
        match('H')
        match('@')
        parse_Z()
        parse_C()

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('B'):
        match('B')
        parse_C()
        parse_G()
    elif lookahead.startswith('4'):
        match('4')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['B', '4']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('@'):
        match('@')
    elif lookahead.startswith('~'):
        match('~')
    elif lookahead.startswith('q'):
        match('q')
    elif lookahead.startswith('-'):
        match('-')
    elif lookahead.startswith("'"):
        match("'")
        parse_Z()
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['@', '~', 'q', '-', "'"]))

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