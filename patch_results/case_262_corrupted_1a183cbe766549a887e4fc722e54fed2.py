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

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('4'):
        match('4')
        match('/')
        match('4')
    elif lookahead.startswith('t'):
        match('t')
        match('T')
        match('p')
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('Y'):
            match('Y')
        elif lookahead.startswith('7'):
            match('7')
        elif lookahead.startswith(';'):
            match(';')
            parse_R()
        elif lookahead.startswith(']'):
            match(']')
            match('_')
            match('%')
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['Y', '7', ';', ']']))
        match('2')
    elif lookahead.startswith('%'):
        match('%')
    elif lookahead.startswith('('):
        match('(')
        match('y')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('I'):
            match('I')
        elif lookahead.startswith('9'):
            match('9')
            match(')')
            match('Q')
            match("'")
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['I', '9']))
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('?'):
            match('?')
            match('C')
            match(';')
            match('g')
        elif lookahead.startswith('H'):
            match('H')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['?', 'H']))
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith('4'):
            match('4')
            match('/')
            match('4')
        elif lookahead.startswith('t'):
            match('t')
            match('T')
            match('p')
            parse_S()
            match('2')
        elif lookahead.startswith('%'):
            match('%')
        elif lookahead.startswith('('):
            match('(')
            match('y')
            parse_M()
            parse_E()
            parse_L()
        elif lookahead.startswith('-'):
            match('-')
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['4', 't', '%', '(', '-']))
    elif lookahead.startswith('-'):
        match('-')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['4', 't', '%', '(', '-']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('Y'):
        match('Y')
    elif lookahead.startswith('7'):
        match('7')
    elif lookahead.startswith(';'):
        match(';')
        parse_R()
    elif lookahead.startswith(']'):
        match(']')
        match('_')
        match('%')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['Y', '7', ';', ']']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('I'):
        match('I')
    elif lookahead.startswith('9'):
        match('9')
        match(')')
        match('Q')
        match("'")
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['I', '9']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('C'):
        match('C')

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        match('C')
        match(';')
        match('g')
    elif lookahead.startswith('H'):
        match('H')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['?', 'H']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
        match('n')
        parse_K()
    elif lookahead.startswith('A'):
        match('A')
    elif lookahead.startswith('|'):
        match('|')
        parse_R()
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['j', 'A', '|']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_L()
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