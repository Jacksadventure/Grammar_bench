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

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('V'):
        while pos < len(tokens) and tokens[pos].startswith('2'):
            match('2')
            parse_L()
            parse_B()
            parse_P()
            parse_L()
        while pos < len(tokens) and tokens[pos].startswith('B'):
            parse_B()
            match('b')
    elif lookahead.startswith('2'):
        match('2')
        while pos < len(tokens) and tokens[pos].startswith('2'):
            match('2')
            parse_L()
            parse_B()
            parse_P()
            parse_L()
        match('_')
    elif lookahead.startswith('.'):
        match('.')
    elif lookahead.startswith('e'):
        match('e')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith(','):
            match(',')
            match('?')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join([',', '']))
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['V', '2', '.', 'e']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('1'):
        match('1')
        match('[')
        parse_N()
        parse_H()
    elif lookahead.startswith('B'):
        parse_B()
        parse_N()
        match('f')
    elif lookahead.startswith('o'):
        match('o')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['1', 'B', 'o']))

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('2'):
        match('2')
        parse_L()
        parse_B()
        parse_P()
        parse_L()

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('a'):
        match('a')
        parse_P()
        match('w')
        match('.')

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('4'):
        match('4')
        parse_B()
        parse_L()

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('B'):
        parse_B()

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        match('?')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join([',', '']))

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('k'):
        match('k')
        parse_L()
        parse_P()
        parse_V()
        parse_S()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_R()
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