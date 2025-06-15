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
    if lookahead.startswith('='):
        match('=')
        match('9')
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith('='):
            match('=')
            match('9')
            parse_W()
        elif lookahead.startswith('<'):
            match('<')
            match('0')
            match('4')
            parse_N()
        elif lookahead.startswith('k'):
            match('k')
            match('0')
        elif lookahead.startswith('>'):
            match('>')
            parse_P()
            match('.')
            match(':')
            match('n')
        elif lookahead.startswith('H'):
            match('H')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['=', '<', 'k', '>', 'H']))
    elif lookahead.startswith('<'):
        match('<')
        match('0')
        match('4')
        while pos < len(tokens) and tokens[pos].startswith('0'):
            match('0')
            parse_F()
            match('5')
    elif lookahead.startswith('k'):
        match('k')
        match('0')
    elif lookahead.startswith('>'):
        match('>')
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('*'):
            match('*')
            parse_E()
            match('B')
            match('s')
            parse_M()
        elif lookahead.startswith('u'):
            match('u')
            match(',')
            match('[')
            match('7')
            match('<')
        elif lookahead.startswith('$'):
            match('$')
        else:
            error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['*', 'u', '$']))
        match('.')
        match(':')
        match('n')
    elif lookahead.startswith('H'):
        match('H')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['=', '<', 'k', '>', 'H']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('s'):
        match('s')
        match('*')
        match('a')
    elif lookahead.startswith('n'):
        match('n')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['s', 'n']))

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('D'):
        match('D')
        match('.')

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        match(']')
        parse_T()
        parse_V()
    elif lookahead.startswith('G'):
        match('G')
        match('}')
        match('q')
        match('=')
        parse_O()
    elif lookahead.startswith(','):
        match(',')
        parse_O()
    elif lookahead.startswith('>'):
        match('>')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join([']', 'G', ',', '>']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('p'):
        match('p')
        match('+')
        parse_V()
    elif lookahead.startswith('b'):
        match('b')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['p', 'b']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('('):
        match('(')
        parse_W()
        parse_P()
    elif lookahead.startswith('M'):
        parse_M()
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['(', 'M']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('*'):
        match('*')
        parse_E()
        match('B')
        match('s')
        parse_M()
    elif lookahead.startswith('u'):
        match('u')
        match(',')
        match('[')
        match('7')
        match('<')
    elif lookahead.startswith('$'):
        match('$')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['*', 'u', '$']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('u'):
        match('u')
    elif lookahead.startswith('x'):
        match('x')
        match("'")
        parse_E()
    elif lookahead.startswith("'"):
        match("'")
        parse_F()
        match('d')
        parse_F()
        parse_F()
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['u', 'x', "'"]))

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('0'):
        match('0')
        parse_F()
        match('5')

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