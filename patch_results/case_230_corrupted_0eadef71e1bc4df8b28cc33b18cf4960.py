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
    if lookahead.startswith('%'):
        match('%')
        match(';')
        if pos >= len(tokens):
            error("Unexpected end of input in C")
        lookahead = tokens[pos]
        if lookahead.startswith('p'):
            match('p')
            parse_F()
            match('}')
            match('H')
            match('d')
        elif lookahead.startswith('2'):
            match('2')
            match('D')
            parse_Y()
        elif lookahead.startswith('+'):
            match('+')
        else:
            error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['p', '2', '+']))
        match(',')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('8'):
            match('8')
            parse_Y()
            match('~')
            match('~')
        elif lookahead.startswith('i'):
            match('i')
            match('[')
            parse_A()
            match('.')
            parse_R()
        elif lookahead.startswith('^'):
            match('^')
            match('&')
            parse_Y()
            match('`')
        elif lookahead.startswith('.'):
            match('.')
            match('j')
            match('9')
        elif lookahead.startswith('}'):
            match('}')
            match('f')
            match('X')
            match('p')
            match('e')
        elif lookahead.startswith("'"):
            match("'")
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['8', 'i', '^', '.', '}', "'"]))
    elif lookahead.startswith('>'):
        match('>')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['%', '>']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('1'):
        match('1')
        match("'")
        parse_E()
        match('p')
    elif lookahead.startswith('?'):
        match('?')
        match('t')
    elif lookahead.startswith('2'):
        match('2')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['1', '?', '2']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('8'):
        match('8')
        parse_Y()
        match('~')
        match('~')
    elif lookahead.startswith('i'):
        match('i')
        match('[')
        parse_A()
        match('.')
        parse_R()
    elif lookahead.startswith('^'):
        match('^')
        match('&')
        parse_Y()
        match('`')
    elif lookahead.startswith('.'):
        match('.')
        match('j')
        match('9')
    elif lookahead.startswith('}'):
        match('}')
        match('f')
        match('X')
        match('p')
        match('e')
    elif lookahead.startswith("'"):
        match("'")
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['8', 'i', '^', '.', '}', "'"]))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith(';'):
        match(';')
        match('H')
        match('#')
        match('d')
        match('x')
    elif lookahead.startswith('V'):
        match('V')
        match('a')
        match('q')
        parse_E()
        parse_F()
    elif lookahead.startswith('w'):
        match('w')
        match('/')
        match('0')
    elif lookahead.startswith('o'):
        match('o')
        match('=')
        match('l')
        match('5')
        match('d')
    elif lookahead.startswith('t'):
        match('t')
        match('s')
        parse_F()
    elif lookahead.startswith('.'):
        match('.')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join([';', 'V', 'w', 'o', 't', '.']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('i'):
        match('i')
        match('+')
        match("'")
    elif lookahead.startswith('@'):
        match('@')
        match('}')
        match('q')
    elif lookahead.startswith('h'):
        match('h')
        parse_E()
    elif lookahead.startswith('m'):
        match('m')
        match('^')
        parse_A()
        match(',')
        match('I')
    elif lookahead.startswith('9'):
        match('9')
        match('c')
    elif lookahead.startswith('f'):
        match('f')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['i', '@', 'h', 'm', '9', 'f']))

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