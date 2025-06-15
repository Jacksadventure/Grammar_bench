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

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('='):
        match('=')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('>'):
            match('>')
            match('q')
            parse_T()
            match('-')
            match('H')
        elif lookahead.startswith('#'):
            match('#')
            parse_X()
            match('L')
            match('!')
            match('J')
        elif lookahead.startswith('W'):
            match('W')
            parse_M()
            match(':')
        elif lookahead.startswith(']'):
            match(']')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['>', '#', 'W', ']']))
        match('?')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('='):
            match('=')
            parse_U()
            match('?')
            parse_N()
            match('E')
        elif lookahead.startswith('~'):
            match('~')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['=', '~']))
        match('E')
    elif lookahead.startswith('~'):
        match('~')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['=', '~']))

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('B'):
        match('B')
        parse_F()
        match('=')

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('3'):
        match('3')
        parse_M()
        match("'")
        parse_X()
    elif lookahead.startswith('^'):
        match('^')
        match('*')
        match(']')
        match('h')
        match('D')
    elif lookahead.startswith('t'):
        match('t')
        match('j')
    elif lookahead.startswith('&'):
        match('&')
        parse_N()
        match('4')
        match('w')
    elif lookahead.startswith('~'):
        match('~')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['3', '^', 't', '&', '~']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('y'):
        match('y')
        match('-')
        parse_V()
    elif lookahead.startswith('_'):
        match('_')
    elif lookahead.startswith('M'):
        parse_M()
        match('#')
        match('(')
        match('e')
    elif lookahead.startswith("'"):
        match("'")
        match('_')
        match('q')
        match('f')
        match('=')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['y', '_', 'M', "'"]))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('>'):
        match('>')
        match('q')
        parse_T()
        match('-')
        match('H')
    elif lookahead.startswith('#'):
        match('#')
        parse_X()
        match('L')
        match('!')
        match('J')
    elif lookahead.startswith('W'):
        match('W')
        parse_M()
        match(':')
    elif lookahead.startswith(']'):
        match(']')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['>', '#', 'W', ']']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('d'):
        match('d')
        match('2')
        parse_K()
        match('S')
        parse_Q()
    elif lookahead.startswith('B'):
        match('B')
        parse_I()
        match('E')
        match('.')
        match('[')
    elif lookahead.startswith('b'):
        match('b')
        parse_T()
        parse_T()
        match('5')
    elif lookahead.startswith('.'):
        match('.')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['d', 'B', 'b', '.']))

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('@'):
        match('@')
        match("'")
        match('(')
        match('3')
    else:
        error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['@', '']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
        match('j')
        match("'")
        match('3')
    elif lookahead.startswith('j'):
        match('j')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['j', 'j']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('&'):
        match('&')
        match('4')
        parse_V()
    elif lookahead.startswith("'"):
        match("'")
        match('m')
        parse_X()
    elif lookahead.startswith('*'):
        match('*')
    elif lookahead.startswith('}'):
        match('}')
        match('P')
    elif lookahead.startswith(')'):
        match(')')
        parse_K()
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['&', "'", '*', '}', ')']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('q'):
        match('q')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['q']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_N()
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