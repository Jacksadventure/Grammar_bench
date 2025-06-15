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

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('2'):
        match('2')
        match('e')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('2'):
            match('2')
            match('e')
            parse_U()
            match('g')
        elif lookahead.startswith('c'):
            match('c')
            parse_N()
            parse_I()
            parse_U()
            match('R')
        elif lookahead.startswith('3'):
            match('3')
            parse_P()
            match("'")
            match("'")
        elif lookahead.startswith('['):
            match('[')
        elif lookahead.startswith("'"):
            match("'")
            match('1')
            parse_N()
            match('c')
            match('=')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['2', 'c', '3', '[', "'"]))
        match('g')
    elif lookahead.startswith('c'):
        match('c')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith(':'):
            match(':')
            match('l')
            match('b')
            match('>')
            parse_I()
        elif lookahead.startswith('{'):
            match('{')
            parse_P()
            parse_K()
            parse_W()
        elif lookahead.startswith('/'):
            match('/')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join([':', '{', '/']))
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('k'):
            match('k')
            match('T')
            parse_U()
            match('b')
            parse_N()
        elif lookahead.startswith("'"):
            match("'")
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['k', "'"]))
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('2'):
            match('2')
            match('e')
            parse_U()
            match('g')
        elif lookahead.startswith('c'):
            match('c')
            parse_N()
            parse_I()
            parse_U()
            match('R')
        elif lookahead.startswith('3'):
            match('3')
            parse_P()
            match("'")
            match("'")
        elif lookahead.startswith('['):
            match('[')
        elif lookahead.startswith("'"):
            match("'")
            match('1')
            parse_N()
            match('c')
            match('=')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['2', 'c', '3', '[', "'"]))
        match('R')
    elif lookahead.startswith('3'):
        match('3')
        while pos < len(tokens) and tokens[pos].startswith('{'):
            match('{')
            match(',')
            parse_I()
            parse_W()
            parse_U()
        match("'")
        match("'")
    elif lookahead.startswith('['):
        match('[')
    elif lookahead.startswith("'"):
        match("'")
        match('1')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith(':'):
            match(':')
            match('l')
            match('b')
            match('>')
            parse_I()
        elif lookahead.startswith('{'):
            match('{')
            parse_P()
            parse_K()
            parse_W()
        elif lookahead.startswith('/'):
            match('/')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join([':', '{', '/']))
        match('c')
        match('=')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['2', 'c', '3', '[', "'"]))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('k'):
        match('k')
        match('T')
        parse_U()
        match('b')
        parse_N()
    elif lookahead.startswith("'"):
        match("'")
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['k', "'"]))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('C'):
        match('C')
        match('s')
    elif lookahead.startswith('G'):
        match('G')
        match('0')
        parse_W()
        parse_U()
        parse_I()
    elif lookahead.startswith('0'):
        match('0')
    elif lookahead.startswith('8'):
        match('8')
        match('>')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['C', 'G', '0', '8']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('r'):
        match('r')

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('{'):
        match('{')
        match(',')
        parse_I()
        parse_W()
        parse_U()

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith(':'):
        match(':')
        match('l')
        match('b')
        match('>')
        parse_I()
    elif lookahead.startswith('{'):
        match('{')
        parse_P()
        parse_K()
        parse_W()
    elif lookahead.startswith('/'):
        match('/')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join([':', '{', '/']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_U()
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