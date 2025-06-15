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
    if lookahead.startswith('T'):
        match('T')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('T'):
            match('T')
            parse_E()
            match('A')
        elif lookahead.startswith('~'):
            match('~')
            parse_U()
            parse_R()
            match('2')
            parse_I()
        elif lookahead.startswith('2'):
            match('2')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['T', '~', '2']))
        match('A')
    elif lookahead.startswith('~'):
        match('~')
        while pos < len(tokens) and tokens[pos].startswith('>'):
            match('>')
            match('l')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('K'):
            match('K')
        elif lookahead.startswith(','):
            match(',')
            match('n')
            match('8')
        elif lookahead.startswith('<'):
            match('<')
            match('8')
            match('}')
        elif lookahead.startswith('P'):
            parse_P()
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['K', ',', '<', 'P']))
        match('2')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('x'):
            match('x')
            match('x')
            match('h')
        elif lookahead.startswith('%'):
            match('%')
            parse_R()
            parse_N()
            parse_J()
            parse_E()
        elif lookahead.startswith('L'):
            match('L')
            parse_E()
            match('Z')
            match('l')
        elif lookahead.startswith('Q'):
            match('Q')
            match('=')
        elif lookahead.startswith('+'):
            match('+')
            parse_N()
            match('@')
            match('u')
        elif lookahead.startswith('*'):
            match('*')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['x', '%', 'L', 'Q', '+', '*']))
    elif lookahead.startswith('2'):
        match('2')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['T', '~', '2']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith(')'):
        match(')')
        parse_R()
        match('$')
    elif lookahead.startswith('l'):
        match('l')
    elif lookahead.startswith('2'):
        match('2')
    elif lookahead.startswith("'"):
        match("'")
        match('&')
        match('u')
        parse_W()
    elif lookahead.startswith('9'):
        match('9')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join([')', 'l', '2', "'", '9']))

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('>'):
        match('>')
        match('l')

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('U'):
        parse_U()
    elif lookahead.startswith('%'):
        match('%')
    elif lookahead.startswith('='):
        match('=')
        match('v')
        match('<')
        match('i')
    elif lookahead.startswith('e'):
        match('e')
        parse_U()
        match('0')
        parse_O()
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['U', '%', '=', 'e']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('Z'):
        match('Z')
    elif lookahead.startswith('6'):
        match('6')
        match('S')
    elif lookahead.startswith('{'):
        match('{')
        match('w')
        parse_R()
        match('q')
    elif lookahead.startswith('p'):
        match('p')
        match(',')
    elif lookahead.startswith('G'):
        match('G')
        match('r')
        match('$')
        parse_W()
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['Z', '6', '{', 'p', 'G']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('K'):
        match('K')
    elif lookahead.startswith(','):
        match(',')
        match('n')
        match('8')
    elif lookahead.startswith('<'):
        match('<')
        match('8')
        match('}')
    elif lookahead.startswith('P'):
        parse_P()
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['K', ',', '<', 'P']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('x'):
        match('x')
        match('x')
        match('h')
    elif lookahead.startswith('%'):
        match('%')
        parse_R()
        parse_N()
        parse_J()
        parse_E()
    elif lookahead.startswith('L'):
        match('L')
        parse_E()
        match('Z')
        match('l')
    elif lookahead.startswith('Q'):
        match('Q')
        match('=')
    elif lookahead.startswith('+'):
        match('+')
        parse_N()
        match('@')
        match('u')
    elif lookahead.startswith('*'):
        match('*')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['x', '%', 'L', 'Q', '+', '*']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('G'):
        match('G')
    elif lookahead.startswith('+'):
        match('+')
        match('M')
    elif lookahead.startswith('V'):
        match('V')
        parse_R()
        match('G')
        match('^')
        parse_O()
    elif lookahead.startswith('O'):
        parse_O()
        parse_E()
        parse_O()
        parse_P()
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['G', '+', 'V', 'O']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('l'):
        match('l')
    elif lookahead.startswith('>'):
        match('>')
    elif lookahead.startswith('C'):
        match('C')
        match('a')
        match('}')
    elif lookahead.startswith('n'):
        match('n')
        match('q')
        match('d')
        parse_U()
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['l', '>', 'C', 'n']))

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