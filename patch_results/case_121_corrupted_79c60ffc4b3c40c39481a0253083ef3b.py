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

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('p'):
        match('p')
        match('I')
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith('p'):
            match('p')
            match('I')
            parse_L()
            match('~')
            parse_G()
        elif lookahead.startswith('J'):
            match('J')
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['p', 'J']))
        match('~')
        while pos < len(tokens) and tokens[pos].startswith('('):
            match('(')
            parse_H()
            match('k')
    elif lookahead.startswith('J'):
        match('J')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['p', 'J']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
        match('+')
    elif lookahead.startswith('C'):
        match('C')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['+', 'C']))

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('T'):
        match('T')
        parse_O()
        parse_M()

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('1'):
        match('1')
        match('`')
        match('^')
    elif lookahead.startswith('!'):
        match('!')
        match('`')
    elif lookahead.startswith('>'):
        match('>')
        parse_P()
        parse_P()
        parse_M()
    elif lookahead.startswith('I'):
        match('I')
        parse_P()
    elif lookahead.startswith('}'):
        match('}')
        match('y')
        parse_H()
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['1', '!', '>', 'I', '}']))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('>'):
        match('>')
        parse_P()
        match('^')
        match(';')
        parse_M()

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('('):
        match('(')
        parse_H()
        match('k')

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('4'):
        match('4')
        parse_R()
        match('8')
        match('Q')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_L()
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