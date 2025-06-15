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

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('P'):
        match('P')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('I'):
            match('I')
            match('v')
            match('0')
        elif lookahead.startswith('q'):
            match('q')
            parse_N()
            match('{')
            match('u')
        elif lookahead.startswith('m'):
            match('m')
            match(',')
        elif lookahead.startswith('a'):
            match('a')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['I', 'q', 'm', 'a']))
    elif lookahead.startswith('7'):
        match('7')
        match('M')
    elif lookahead.startswith(';'):
        match(';')
        match('|')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('P'):
            match('P')
            parse_R()
        elif lookahead.startswith('7'):
            match('7')
            match('M')
        elif lookahead.startswith(';'):
            match(';')
            match('|')
            parse_B()
            parse_N()
            match('*')
        elif lookahead.startswith('W'):
            match('W')
            match('|')
        elif lookahead.startswith('r'):
            match('r')
            match('X')
        elif lookahead.startswith('S'):
            match('S')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['P', '7', ';', 'W', 'r', 'S']))
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('b'):
            match('b')
            parse_B()
            match('_')
        elif lookahead.startswith('('):
            match('(')
            match('+')
        elif lookahead.startswith('D'):
            match('D')
            match('_')
            match('4')
        elif lookahead.startswith('Q'):
            match('Q')
            parse_B()
            parse_O()
            match('-')
        elif lookahead.startswith('f'):
            match('f')
            match('.')
            match('Y')
            parse_E()
        elif lookahead.startswith(':'):
            match(':')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['b', '(', 'D', 'Q', 'f', ':']))
        match('*')
    elif lookahead.startswith('W'):
        match('W')
        match('|')
    elif lookahead.startswith('r'):
        match('r')
        match('X')
    elif lookahead.startswith('S'):
        match('S')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['P', '7', ';', 'W', 'r', 'S']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('b'):
        match('b')
        parse_B()
        match('_')
    elif lookahead.startswith('('):
        match('(')
        match('+')
    elif lookahead.startswith('D'):
        match('D')
        match('_')
        match('4')
    elif lookahead.startswith('Q'):
        match('Q')
        parse_B()
        parse_O()
        match('-')
    elif lookahead.startswith('f'):
        match('f')
        match('.')
        match('Y')
        parse_E()
    elif lookahead.startswith(':'):
        match(':')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['b', '(', 'D', 'Q', 'f', ':']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('!'):
        match('!')
        match('=')
        match('7')
        match(')')
        match('A')
    elif lookahead.startswith('*'):
        match('*')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['!', '*']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['?']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('I'):
        match('I')
        match('v')
        match('0')
    elif lookahead.startswith('q'):
        match('q')
        parse_N()
        match('{')
        match('u')
    elif lookahead.startswith('m'):
        match('m')
        match(',')
    elif lookahead.startswith('a'):
        match('a')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['I', 'q', 'm', 'a']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_B()
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