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

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('}'):
        match('}')
        match('}')
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('<'):
            match('<')
            match('3')
            parse_Z()
            match('^')
        elif lookahead.startswith('$'):
            match('$')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['<', '$']))
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('<'):
            match('<')
            match('3')
            parse_Z()
            match('^')
        elif lookahead.startswith('$'):
            match('$')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['<', '$']))
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('<'):
            match('<')
            match('3')
            parse_Z()
            match('^')
        elif lookahead.startswith('$'):
            match('$')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['<', '$']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('_'):
        match('_')
        parse_W()
        parse_F()
        match('o')
    elif lookahead.startswith('m'):
        match('m')
        parse_E()
    elif lookahead.startswith('|'):
        match('|')
        parse_Z()
        parse_W()
        parse_W()
    elif lookahead.startswith('k'):
        match('k')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['_', 'm', '|', 'k']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('L'):
        match('L')
        parse_E()
        match('^')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['L', '']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('a'):
        match('a')
    elif lookahead.startswith('e'):
        match('e')
        match('2')
        match('r')
    elif lookahead.startswith('L'):
        match('L')
        parse_Z()
        parse_W()
    elif lookahead.startswith('E'):
        parse_E()
        match('f')
    elif lookahead.startswith('u'):
        match('u')
        match('D')
        match('}')
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['a', 'e', 'L', 'E', 'u']))

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('r'):
        match('r')
        parse_Z()
        match('i')
        parse_W()
    elif lookahead.startswith('n'):
        match('n')
        parse_X()
        parse_X()
        match('R')
        parse_X()
    elif lookahead.startswith('q'):
        match('q')
        match('b')
        match('#')
    elif lookahead.startswith("'"):
        match("'")
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['r', 'n', 'q', "'"]))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('<'):
        match('<')
        match('3')
        parse_Z()
        match('^')
    elif lookahead.startswith('$'):
        match('$')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['<', '$']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_B()
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