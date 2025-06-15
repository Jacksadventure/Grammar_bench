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

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('K'):
        match('K')
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('@'):
            match('@')
            match('J')
            parse_Z()
            parse_P()
            match('V')
        elif lookahead.startswith('>'):
            match('>')
            parse_E()
            parse_W()
            match('T')
        elif lookahead.startswith('C'):
            match('C')
            parse_W()
            parse_Z()
            match('7')
            parse_W()
        elif lookahead.startswith(';'):
            match(';')
            match("'")
            match('/')
        elif lookahead.startswith('['):
            match('[')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['@', '>', 'C', ';', '[']))
    elif lookahead.startswith('$'):
        match('$')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['K', '$']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('B'):
        match('B')
        parse_Z()
        parse_G()
    elif lookahead.startswith('Y'):
        match('Y')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['B', 'Y']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('Q'):
        match('Q')
    elif lookahead.startswith('a'):
        match('a')
        parse_P()
        match('1')
    elif lookahead.startswith('1'):
        match('1')
        match('^')
        match('1')
        match('3')
        parse_E()
    elif lookahead.startswith('H'):
        match('H')
        parse_P()
    elif lookahead.startswith('G'):
        parse_G()
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['Q', 'a', '1', 'H', 'G']))

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('X'):
        match('X')

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('b'):
        match('b')
        match('C')

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('@'):
        match('@')
        match('J')
        parse_Z()
        parse_P()
        match('V')
    elif lookahead.startswith('>'):
        match('>')
        parse_E()
        parse_W()
        match('T')
    elif lookahead.startswith('C'):
        match('C')
        parse_W()
        parse_Z()
        match('7')
        parse_W()
    elif lookahead.startswith(';'):
        match(';')
        match("'")
        match('/')
    elif lookahead.startswith('['):
        match('[')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['@', '>', 'C', ';', '[']))

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('5'):
        match('5')
        parse_O()
        parse_S()
    elif lookahead.startswith('o'):
        match('o')
        match(':')
        match('d')
        match('v')
        match('o')
    elif lookahead.startswith('}'):
        match('}')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['5', 'o', '}']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('5'):
        match('5')
        match('0')
        parse_E()
        parse_F()
        parse_S()
    elif lookahead.startswith('G'):
        parse_G()
    elif lookahead.startswith('a'):
        match('a')
        match('x')
        parse_F()
        match('}')
        match('A')
    elif lookahead.startswith('V'):
        match('V')
        match('t')
        match('3')
        parse_S()
    elif lookahead.startswith('Z'):
        parse_Z()
        match('b')
        parse_E()
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['5', 'G', 'a', 'V', 'Z']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_E()
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