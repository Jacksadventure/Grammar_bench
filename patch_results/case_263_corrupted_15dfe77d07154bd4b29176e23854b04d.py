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

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('V'):
        match('V')
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith('{'):
            match('{')
            parse_O()
            parse_H()
            parse_M()
            parse_D()
        elif lookahead.startswith('i'):
            match('i')
            parse_E()
        else:
            error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['{', '', 'i']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('S'):
        match('S')
        parse_Y()
        parse_A()
    elif lookahead.startswith('i'):
        match('i')
        parse_H()
        parse_K()
    elif lookahead.startswith('7'):
        match('7')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['S', 'i', '7']))

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('<'):
        match('<')
        match('?')
        parse_L()

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('{'):
        match('{')
        parse_O()
        parse_H()
        parse_M()

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('('):
        match('(')
        parse_M()

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('A'):
        parse_A()
        parse_K()

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('S'):
        match('S')
        parse_E()
        match('.')
        match('6')

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('0'):
        match('0')
        match('<')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['0', '']))

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('b'):
        match('b')
        parse_M()
        parse_Y()
        parse_Y()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_K()
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