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

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('*'):
        match('*')
        match('j')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('4'):
            match('4')
            match('M')
            match('q')
            match(',')
            parse_R()
        elif lookahead.startswith(']'):
            match(']')
            match('O')
            match(':')
            match('O')
            parse_B()
        elif lookahead.startswith('X'):
            match('X')
            parse_R()
            parse_W()
            parse_W()
            match('c')
        elif lookahead.startswith('&'):
            match('&')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['4', ']', 'X', '&']))
        while pos < len(tokens) and tokens[pos].startswith('A'):
            match('A')
            parse_N()
            parse_W()
    elif lookahead.startswith('%'):
        match('%')
        match('3')
        match('|')
    elif lookahead.startswith('q'):
        match('q')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['*', '%', 'q']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('4'):
        match('4')
        match('M')
        match('q')
        match(',')
        parse_R()
    elif lookahead.startswith(']'):
        match(']')
        match('O')
        match(':')
        match('O')
        parse_B()
    elif lookahead.startswith('X'):
        match('X')
        parse_R()
        parse_W()
        parse_W()
        match('c')
    elif lookahead.startswith('&'):
        match('&')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['4', ']', 'X', '&']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('i'):
        match('i')

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('@'):
        match('@')
        parse_P()
        match('e')
        parse_N()
    elif lookahead.startswith('G'):
        match('G')
        parse_P()
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['@', 'G']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('g'):
        match('g')
        match('%')
        match('Q')
    elif lookahead.startswith('8'):
        match('8')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['g', '8']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('0'):
        match('0')
    elif lookahead.startswith('1'):
        match('1')
        match('4')
        match('4')
        match(':')
    elif lookahead.startswith("'"):
        match("'")
        match('9')
        match('k')
    elif lookahead.startswith('2'):
        match('2')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['0', '1', "'", '2']))

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('A'):
        match('A')
        parse_N()
        parse_W()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_I()
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