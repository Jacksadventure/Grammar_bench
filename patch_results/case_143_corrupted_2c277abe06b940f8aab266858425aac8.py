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
    if lookahead.startswith('E'):
        match('E')
        while pos < len(tokens) and tokens[pos].startswith('Q'):
            match('Q')
            parse_X()
            parse_B()
            parse_K()
        match('%')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('/'):
            match('/')
            match('p')
            match('r')
            parse_F()
            parse_O()
        elif lookahead.startswith('N'):
            match('N')
            parse_F()
        elif lookahead.startswith('P'):
            match('P')
            parse_W()
            parse_G()
            parse_Y()
            parse_O()
        elif lookahead.startswith('('):
            match('(')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['/', 'N', 'P', '(']))
    elif lookahead.startswith('m'):
        match('m')
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('0'):
            match('0')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['0']))
        match('y')
        while pos < len(tokens) and tokens[pos].startswith('.'):
            match('.')
            parse_G()
            match('N')
            match('_')
        match('s')
    elif lookahead.startswith('b'):
        match('b')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('r'):
            match('r')
            match('7')
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['r', '']))
        match('f')
    elif lookahead.startswith('J'):
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('D'):
            match('D')
            match('e')
        elif lookahead.startswith('x'):
            match('x')
            match('C')
        elif lookahead.startswith('_'):
            match('_')
            match('5')
            match('m')
            parse_O()
            match('L')
        elif lookahead.startswith('b'):
            match('b')
            parse_Y()
            match(';')
            match('r')
            parse_J()
        elif lookahead.startswith('}'):
            match('}')
            parse_K()
            parse_J()
        elif lookahead.startswith('2'):
            match('2')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['D', 'x', '_', 'b', '}', '2']))
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['E', 'm', 'b', 'J']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('r'):
        match('r')
        match('7')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['r', '']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
        match('4')
        parse_X()
        parse_O()
        parse_F()
    elif lookahead.startswith('~'):
        match('~')
        parse_J()
        parse_B()
    elif lookahead.startswith('2'):
        match('2')
        parse_G()
        parse_W()
        match(']')
    elif lookahead.startswith('6'):
        match('6')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['j', '~', '2', '6']))

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('.'):
        match('.')
        parse_G()
        match('N')
        match('_')

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        match('p')
        match('r')
        parse_F()
        parse_O()
    elif lookahead.startswith('N'):
        match('N')
        parse_F()
    elif lookahead.startswith('P'):
        match('P')
        parse_W()
        parse_G()
        parse_Y()
        parse_O()
    elif lookahead.startswith('('):
        match('(')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['/', 'N', 'P', '(']))

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Q'):
        match('Q')
        parse_X()
        parse_B()
        parse_K()

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('D'):
        match('D')
        match('e')
    elif lookahead.startswith('x'):
        match('x')
        match('C')
    elif lookahead.startswith('_'):
        match('_')
        match('5')
        match('m')
        parse_O()
        match('L')
    elif lookahead.startswith('b'):
        match('b')
        parse_Y()
        match(';')
        match('r')
        parse_J()
    elif lookahead.startswith('}'):
        match('}')
        parse_K()
        parse_J()
    elif lookahead.startswith('2'):
        match('2')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['D', 'x', '_', 'b', '}', '2']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('0'):
        match('0')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['0']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('f'):
        match('f')
        parse_O()
        match('>')
        match('u')
    elif lookahead.startswith('F'):
        parse_F()
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['f', 'F']))

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