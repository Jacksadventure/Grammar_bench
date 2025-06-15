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

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('J'):
        match('J')
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('J'):
            match('J')
            parse_P()
            parse_U()
            parse_E()
        elif lookahead.startswith('%'):
            match('%')
            parse_U()
            parse_E()
            parse_N()
        elif lookahead.startswith('&'):
            match('&')
            parse_F()
            parse_N()
            parse_E()
            parse_N()
        elif lookahead.startswith('4'):
            match('4')
            parse_P()
            parse_E()
            parse_P()
        elif lookahead.startswith('M'):
            match('M')
            match('(')
            parse_N()
            parse_N()
            parse_U()
        elif lookahead.startswith('~'):
            match('~')
        else:
            error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['J', '%', '&', '4', 'M', '~']))
        while pos < len(tokens) and tokens[pos].startswith('z'):
            match('z')
            parse_E()
        while pos < len(tokens) and tokens[pos].startswith('t'):
            match('t')
            parse_P()
            parse_F()
            parse_U()
            parse_N()
    elif lookahead.startswith('%'):
        match('%')
        while pos < len(tokens) and tokens[pos].startswith('z'):
            match('z')
            parse_E()
        while pos < len(tokens) and tokens[pos].startswith('t'):
            match('t')
            parse_P()
            parse_F()
            parse_U()
            parse_N()
        while pos < len(tokens) and tokens[pos].startswith('>'):
            match('>')
            match('s')
            parse_E()
    elif lookahead.startswith('&'):
        match('&')
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('+'):
            match('+')
            parse_E()
            parse_F()
            match('V')
            parse_G()
        elif lookahead.startswith("'"):
            match("'")
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['+', "'"]))
        while pos < len(tokens) and tokens[pos].startswith('>'):
            match('>')
            match('s')
            parse_E()
        while pos < len(tokens) and tokens[pos].startswith('t'):
            match('t')
            parse_P()
            parse_F()
            parse_U()
            parse_N()
        while pos < len(tokens) and tokens[pos].startswith('>'):
            match('>')
            match('s')
            parse_E()
    elif lookahead.startswith('4'):
        match('4')
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('J'):
            match('J')
            parse_P()
            parse_U()
            parse_E()
        elif lookahead.startswith('%'):
            match('%')
            parse_U()
            parse_E()
            parse_N()
        elif lookahead.startswith('&'):
            match('&')
            parse_F()
            parse_N()
            parse_E()
            parse_N()
        elif lookahead.startswith('4'):
            match('4')
            parse_P()
            parse_E()
            parse_P()
        elif lookahead.startswith('M'):
            match('M')
            match('(')
            parse_N()
            parse_N()
            parse_U()
        elif lookahead.startswith('~'):
            match('~')
        else:
            error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['J', '%', '&', '4', 'M', '~']))
        while pos < len(tokens) and tokens[pos].startswith('t'):
            match('t')
            parse_P()
            parse_F()
            parse_U()
            parse_N()
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('J'):
            match('J')
            parse_P()
            parse_U()
            parse_E()
        elif lookahead.startswith('%'):
            match('%')
            parse_U()
            parse_E()
            parse_N()
        elif lookahead.startswith('&'):
            match('&')
            parse_F()
            parse_N()
            parse_E()
            parse_N()
        elif lookahead.startswith('4'):
            match('4')
            parse_P()
            parse_E()
            parse_P()
        elif lookahead.startswith('M'):
            match('M')
            match('(')
            parse_N()
            parse_N()
            parse_U()
        elif lookahead.startswith('~'):
            match('~')
        else:
            error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['J', '%', '&', '4', 'M', '~']))
    elif lookahead.startswith('M'):
        match('M')
        match('(')
        while pos < len(tokens) and tokens[pos].startswith('>'):
            match('>')
            match('s')
            parse_E()
        while pos < len(tokens) and tokens[pos].startswith('>'):
            match('>')
            match('s')
            parse_E()
        while pos < len(tokens) and tokens[pos].startswith('z'):
            match('z')
            parse_E()
    elif lookahead.startswith('~'):
        match('~')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['J', '%', '&', '4', 'M', '~']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
        parse_E()
        parse_F()
        match('V')
        parse_G()
    elif lookahead.startswith("'"):
        match("'")
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['+', "'"]))

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('t'):
        match('t')
        parse_P()
        parse_F()
        parse_U()
        parse_N()

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('>'):
        match('>')
        match('s')
        parse_E()

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('z'):
        match('z')
        parse_E()

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('P'):
        parse_P()
        match('x')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['P', '']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_P()
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