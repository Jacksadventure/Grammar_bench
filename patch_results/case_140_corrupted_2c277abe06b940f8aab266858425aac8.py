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
    while pos < len(tokens) and tokens[pos].startswith('<'):
        match('<')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('w'):
            match('w')
        elif lookahead.startswith('V'):
            match('V')
            parse_O()
            parse_R()
            parse_G()
        elif lookahead.startswith('H'):
            match('H')
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['w', 'V', 'H']))
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('+'):
            match('+')
            parse_R()
            parse_E()
            parse_O()
        elif lookahead.startswith('G'):
            parse_G()
        elif lookahead.startswith('8'):
            match('8')
            parse_E()
            parse_R()
        elif lookahead.startswith('M'):
            match('M')
            parse_G()
            parse_U()
            parse_P()
            parse_K()
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['+', 'G', '8', 'M']))
        match('}')

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
        parse_R()
        parse_E()
        parse_O()
    elif lookahead.startswith('G'):
        parse_G()
    elif lookahead.startswith('8'):
        match('8')
        parse_E()
        parse_R()
    elif lookahead.startswith('M'):
        match('M')
        parse_G()
        parse_U()
        parse_P()
        parse_K()
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['+', 'G', '8', 'M']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
    elif lookahead.startswith('V'):
        match('V')
        parse_O()
        parse_R()
        parse_G()
    elif lookahead.startswith('H'):
        match('H')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['w', 'V', 'H']))

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('a'):
        match('a')

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
        parse_E()
        match('*')
    elif lookahead.startswith('J'):
        match('J')
        parse_O()
        parse_P()
        parse_U()
        parse_O()
    elif lookahead.startswith('('):
        match('(')
        parse_G()
        match('Z')
    elif lookahead.startswith('b'):
        match('b')
        parse_R()
        match('?')
        parse_U()
    elif lookahead.startswith('E'):
        parse_E()
        parse_R()
        parse_G()
        parse_U()
        parse_O()
    elif lookahead.startswith('%'):
        match('%')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['+', 'J', '(', 'b', 'E', '%']))

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('M'):
        match('M')
        match('c')
        parse_O()

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")
        match('}')
        match('i')
        match('o')

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