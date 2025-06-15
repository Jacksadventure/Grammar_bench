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

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('L'):
        match('L')
        while pos < len(tokens) and tokens[pos].startswith('.'):
            match('.')
            match('(')
        while pos < len(tokens) and tokens[pos].startswith('.'):
            match('.')
            match('(')
        while pos < len(tokens) and tokens[pos].startswith('B'):
            parse_B()
            parse_M()
            match('r')
            parse_K()
            match('}')
        while pos < len(tokens) and tokens[pos].startswith('e'):
            match('e')
            parse_W()
            parse_W()
            parse_P()
    elif lookahead.startswith('i'):
        match('i')
        while pos < len(tokens) and tokens[pos].startswith('='):
            match('=')
            match('c')
            parse_M()
            parse_M()
    elif lookahead.startswith('o'):
        match('o')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['L', 'i', 'o']))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('='):
        match('=')
        match('c')
        parse_M()
        parse_M()

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('N'):
        match('N')
        parse_H()
        parse_T()
        parse_Z()
    elif lookahead.startswith('0'):
        match('0')
        match('4')
        parse_K()
        parse_M()
        parse_K()
    elif lookahead.startswith('$'):
        match('$')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['N', '0', '$']))

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('.'):
        match('.')
        match('(')

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('g'):
        match('g')
    elif lookahead.startswith('P'):
        parse_P()
        parse_B()
        parse_H()
        parse_B()
    elif lookahead.startswith('%'):
        match('%')
        parse_W()
        match('l')
        parse_K()
        match('V')
    elif lookahead.startswith('v'):
        match('v')
        match("'")
        parse_T()
        parse_W()
    elif lookahead.startswith('M'):
        parse_M()
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['g', 'P', '%', 'v', 'M']))

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('e'):
        match('e')
        parse_W()
        parse_W()
        parse_P()

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('B'):
        parse_B()
        parse_M()
        match('r')
        parse_K()
        match('}')

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('R'):
        match('R')
        parse_B()
        match('q')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_W()
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