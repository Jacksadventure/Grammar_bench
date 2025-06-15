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

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('W'):
        match('W')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('u'):
            match('u')
            match('q')
            parse_H()
            match(')')
        elif lookahead.startswith('C'):
            match('C')
            parse_R()
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['u', 'C']))
        while pos < len(tokens) and tokens[pos].startswith('C'):
            match('C')
            match('7')
    elif lookahead.startswith('n'):
        match('n')
        match('b')
    elif lookahead.startswith('M'):
        match('M')
        match('$')
    elif lookahead.startswith('-'):
        match('-')
    elif lookahead.startswith('T'):
        match('T')
        if pos >= len(tokens):
            error("Unexpected end of input in Q")
        lookahead = tokens[pos]
        if lookahead.startswith('i'):
            match('i')
            parse_Y()
            match('0')
            parse_K()
            parse_N()
        elif lookahead.startswith(';'):
            match(';')
        else:
            error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['i', ';']))
        if pos >= len(tokens):
            error("Unexpected end of input in Q")
        lookahead = tokens[pos]
        if lookahead.startswith('i'):
            match('i')
            parse_Y()
            match('0')
            parse_K()
            parse_N()
        elif lookahead.startswith(';'):
            match(';')
        else:
            error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['i', ';']))
        match('$')
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith('8'):
            match('8')
            parse_N()
            parse_H()
            parse_Q()
        elif lookahead.startswith('L'):
            match('L')
            match('i')
            parse_Y()
            parse_K()
            match('-')
        elif lookahead.startswith('!'):
            match('!')
            parse_Y()
        elif lookahead.startswith('&'):
            match('&')
            parse_Q()
            match('G')
            match('d')
            match('}')
        elif lookahead.startswith('&'):
            match('&')
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['8', 'L', '!', '&', '&']))
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['W', 'n', 'M', '-', 'T']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        match('&')
        parse_Y()
        match('}')
    elif lookahead.startswith(';'):
        match(';')
        parse_Y()
    elif lookahead.startswith('s'):
        match('s')
        parse_R()
        parse_K()
        parse_H()
        match('r')
    elif lookahead.startswith(','):
        match(',')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['o', ';', 's', ',']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('i'):
        match('i')
        parse_Y()
        match('0')
        parse_K()
        parse_N()
    elif lookahead.startswith(';'):
        match(';')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['i', ';']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('8'):
        match('8')
        parse_N()
        parse_H()
        parse_Q()
    elif lookahead.startswith('L'):
        match('L')
        match('i')
        parse_Y()
        parse_K()
        match('-')
    elif lookahead.startswith('!'):
        match('!')
        parse_Y()
    elif lookahead.startswith('&'):
        match('&')
        parse_Q()
        match('G')
        match('d')
        match('}')
    elif lookahead.startswith('&'):
        match('&')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['8', 'L', '!', '&', '&']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('X'):
        match('X')
    elif lookahead.startswith('G'):
        match('G')
        match('T')
    elif lookahead.startswith('R'):
        parse_R()
        parse_H()
        match('$')
        parse_N()
        match('(')
    elif lookahead.startswith('O'):
        match('O')
        parse_Y()
        match('*')
        match('$')
    elif lookahead.startswith('@'):
        match('@')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['X', 'G', 'R', 'O', '@']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('u'):
        match('u')
        match('q')
        parse_H()
        match(')')
    elif lookahead.startswith('C'):
        match('C')
        parse_R()
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['u', 'C']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_H()
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