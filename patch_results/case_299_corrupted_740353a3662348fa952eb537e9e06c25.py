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

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('g'):
        match('g')
        match('c')
    elif lookahead.startswith('T'):
        match('T')
    elif lookahead.startswith('t'):
        match('t')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('d'):
            match('d')
            parse_E()
            parse_I()
            parse_E()
            match('?')
        elif lookahead.startswith('t'):
            match('t')
            parse_C()
            parse_S()
            parse_I()
        elif lookahead.startswith('k'):
            match('k')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['d', 't', 'k']))
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['g', 'T', 't']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        parse_Q()
        parse_F()
        parse_Q()
    elif lookahead.startswith('s'):
        match('s')
        parse_J()
        parse_F()
    elif lookahead.startswith('P'):
        match('P')
        parse_Q()
        match('*')
        parse_F()
        parse_J()
    elif lookahead.startswith('J'):
        parse_J()
        parse_J()
        parse_H()
    elif lookahead.startswith('+'):
        match('+')
        parse_F()
        match('K')
        parse_I()
        parse_F()
    elif lookahead.startswith('6'):
        match('6')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join([',', 's', 'P', 'J', '+', '6']))

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('k'):
        match('k')
        match('3')
        match('[')
        parse_S()
        match('+')

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('G'):
        match('G')
        match('m')
        match('m')
        match(':')
        match('#')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['G', '']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('.'):
        match('.')
        match('<')
        match(';')
        match('#')
    elif lookahead.startswith('m'):
        match('m')
    elif lookahead.startswith('{'):
        match('{')
        parse_J()
    elif lookahead.startswith('x'):
        match('x')
        parse_H()
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['.', 'm', '{', 'x']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('N'):
        match('N')
        parse_H()
        match('n')
        parse_Q()
        parse_S()
    elif lookahead.startswith('y'):
        match('y')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['N', 'y']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('['):
        match('[')
        parse_S()
        parse_F()
    elif lookahead.startswith('|'):
        match('|')
        match(':')
    elif lookahead.startswith('j'):
        match('j')
        match('Z')
    elif lookahead.startswith('f'):
        match('f')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['[', '|', 'j', 'f']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('5'):
        match('5')
        match('<')
        parse_S()
        parse_F()
    elif lookahead.startswith('o'):
        match('o')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['5', 'o']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_S()
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