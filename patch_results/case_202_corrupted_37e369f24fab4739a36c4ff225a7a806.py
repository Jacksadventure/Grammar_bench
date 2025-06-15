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

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('U'):
        match('U')
        match('v')
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith('K'):
            match('K')
            match('Q')
            parse_T()
            parse_I()
        elif lookahead.startswith('2'):
            match('2')
            match('>')
            match('@')
            match('n')
            match('a')
        elif lookahead.startswith('A'):
            match('A')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['K', '2', 'A']))
        match('e')
        match('(')
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['U', 'd']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('m'):
        match('m')
        parse_S()
    elif lookahead.startswith('{'):
        match('{')
        parse_R()
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['m', '{']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('C'):
        match('C')
        parse_I()
        parse_S()
        match('V')
        match('&')
    elif lookahead.startswith('}'):
        match('}')
        match('4')
        match("'")
    elif lookahead.startswith('$'):
        match('$')
        parse_Y()
        match('[')
    elif lookahead.startswith('9'):
        match('9')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['C', '}', '$', '9']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith(';'):
        match(';')
    elif lookahead.startswith('|'):
        match('|')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join([';', '|']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('K'):
        match('K')
        match('Q')
        parse_T()
        parse_I()
    elif lookahead.startswith('2'):
        match('2')
        match('>')
        match('@')
        match('n')
        match('a')
    elif lookahead.startswith('A'):
        match('A')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['K', '2', 'A']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('3'):
        match('3')
        parse_B()
        match('F')
        parse_T()
        match('X')
        parse_Z()
    elif lookahead.startswith('O'):
        match('O')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['3', 'O']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('l'):
        match('l')
    elif lookahead.startswith('$'):
        match('$')
        match('M')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['l', '$']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('A'):
        match('A')
        parse_H()
        parse_R()
        parse_B()
    elif lookahead.startswith('M'):
        match('M')
        match('h')
    elif lookahead.startswith('m'):
        match('m')
        match('L')
    elif lookahead.startswith('H'):
        parse_H()
        match('*')
    elif lookahead.startswith('E'):
        match('E')
        match('q')
        match('c')
        match('6')
        parse_H()
    elif lookahead.startswith('J'):
        match('J')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['A', 'M', 'm', 'H', 'E', 'J']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Z()
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