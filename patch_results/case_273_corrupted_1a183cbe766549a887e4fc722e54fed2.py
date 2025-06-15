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
    if lookahead.startswith('2'):
        match('2')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('='):
            match('=')
            match('8')
        elif lookahead.startswith('h'):
            match('h')
            parse_N()
            match(')')
            match('5')
            match('P')
        elif lookahead.startswith('B'):
            match('B')
            match('[')
            parse_V()
        elif lookahead.startswith('T'):
            match('T')
            parse_N()
            parse_O()
            match('I')
        elif lookahead.startswith('V'):
            parse_V()
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['=', 'h', 'B', 'T', 'V']))
    elif lookahead.startswith('A'):
        match('A')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['2', 'A']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('y'):
        match('y')
        match('t')
        parse_V()
        parse_H()
    elif lookahead.startswith('E'):
        match('E')
        match(')')
    elif lookahead.startswith('*'):
        match('*')
        match('o')
        match('o')
        match('6')
        match('u')
    elif lookahead.startswith('<'):
        match('<')
        match('<')
        match('S')
    elif lookahead.startswith('.'):
        match('.')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['y', 'E', '*', '<', '.']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('|'):
        match('|')
        match('u')
        match('G')
        parse_R()
        parse_H()
    elif lookahead.startswith('2'):
        match('2')
        match('2')
        match('r')
        match(']')
    elif lookahead.startswith('s'):
        match('s')
        match('e')
        parse_N()
        match('f')
    elif lookahead.startswith('s'):
        match('s')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['|', '2', 's', 's']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('G'):
        match('G')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['G']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('Q'):
        match('Q')
        match('6')
        match("'")
        parse_F()
    elif lookahead.startswith('L'):
        match('L')
    elif lookahead.startswith('8'):
        match('8')
        parse_O()
        match('-')
        match('Q')
    elif lookahead.startswith(','):
        match(',')
        match('&')
        match('T')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['Q', 'L', '8', ',']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('='):
        match('=')
        match('8')
    elif lookahead.startswith('h'):
        match('h')
        parse_N()
        match(')')
        match('5')
        match('P')
    elif lookahead.startswith('B'):
        match('B')
        match('[')
        parse_V()
    elif lookahead.startswith('T'):
        match('T')
        parse_N()
        parse_O()
        match('I')
    elif lookahead.startswith('V'):
        parse_V()
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['=', 'h', 'B', 'T', 'V']))

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