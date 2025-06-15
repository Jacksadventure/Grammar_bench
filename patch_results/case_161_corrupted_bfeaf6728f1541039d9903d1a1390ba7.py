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

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
        match('R')
        while pos < len(tokens) and tokens[pos].startswith('4'):
            match('4')
            parse_I()
            match('|')
        while pos < len(tokens) and tokens[pos].startswith('h'):
            match('h')
            match("'")
            parse_P()
            match('f')
    elif lookahead.startswith('i'):
        match('i')
    elif lookahead.startswith('I'):
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('n'):
            match('n')
        elif lookahead.startswith('U'):
            match('U')
        elif lookahead.startswith('='):
            match('=')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['n', 'U', '=']))
        while pos < len(tokens) and tokens[pos].startswith('_'):
            match('_')
        match('0')
        match('8')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('/'):
            match('/')
            match('%')
            parse_V()
            parse_P()
            parse_X()
        elif lookahead.startswith('o'):
            match('o')
            parse_P()
            match('}')
        elif lookahead.startswith('1'):
            match('1')
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['/', 'o', '1']))
    elif lookahead.startswith('&'):
        match('&')
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('j'):
            match('j')
            match('R')
            parse_E()
            parse_Q()
        elif lookahead.startswith('i'):
            match('i')
        elif lookahead.startswith('I'):
            parse_I()
            parse_X()
            match('0')
            match('8')
            parse_O()
        elif lookahead.startswith('&'):
            match('&')
            parse_Y()
            parse_C()
            parse_Y()
        elif lookahead.startswith(','):
            match(',')
            parse_P()
            parse_K()
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['j', 'i', 'I', '&', ',']))
        if pos >= len(tokens):
            error("Unexpected end of input in C")
        lookahead = tokens[pos]
        if lookahead.startswith('X'):
            parse_X()
            match('F')
        elif lookahead.startswith('$'):
            match('$')
        else:
            error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['X', '$']))
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('j'):
            match('j')
            match('R')
            parse_E()
            parse_Q()
        elif lookahead.startswith('i'):
            match('i')
        elif lookahead.startswith('I'):
            parse_I()
            parse_X()
            match('0')
            match('8')
            parse_O()
        elif lookahead.startswith('&'):
            match('&')
            parse_Y()
            parse_C()
            parse_Y()
        elif lookahead.startswith(','):
            match(',')
            parse_P()
            parse_K()
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['j', 'i', 'I', '&', ',']))
    elif lookahead.startswith(','):
        match(',')
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith(']'):
            match(']')
        elif lookahead.startswith('K'):
            parse_K()
        else:
            error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join([']', 'K']))
        while pos < len(tokens) and tokens[pos].startswith('m'):
            match('m')
            parse_Q()
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['j', 'i', 'I', '&', ',']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        match('%')
        parse_V()
        parse_P()
        parse_X()
    elif lookahead.startswith('o'):
        match('o')
        parse_P()
        match('}')
    elif lookahead.startswith('1'):
        match('1')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['/', 'o', '1']))

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('4'):
        match('4')
        parse_I()
        match('|')

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('n'):
        match('n')
    elif lookahead.startswith('U'):
        match('U')
    elif lookahead.startswith('='):
        match('=')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['n', 'U', '=']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        match(']')
    elif lookahead.startswith('K'):
        parse_K()
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join([']', 'K']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('X'):
        parse_X()
        match('F')
    elif lookahead.startswith('$'):
        match('$')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['X', '$']))

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('*'):
        match('*')

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('h'):
        match('h')
        match("'")
        parse_P()
        match('f')

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('m'):
        match('m')
        parse_Q()

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('_'):
        match('_')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Y()
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