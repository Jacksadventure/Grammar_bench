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

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('O'):
        match('O')
    elif lookahead.startswith('o'):
        match('o')
        while pos < len(tokens) and tokens[pos].startswith('R'):
            match('R')
            parse_S()
            parse_L()
            match('W')
    elif lookahead.startswith('7'):
        match('7')
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith('$'):
            match('$')
            parse_S()
            parse_B()
        elif lookahead.startswith('j'):
            match('j')
            parse_L()
        elif lookahead.startswith('/'):
            match('/')
            parse_M()
        elif lookahead.startswith('A'):
            match('A')
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['$', 'j', '/', 'A']))
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['O', 'o', '7']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('$'):
        match('$')
        parse_S()
        parse_B()
    elif lookahead.startswith('j'):
        match('j')
        parse_L()
    elif lookahead.startswith('/'):
        match('/')
        parse_M()
    elif lookahead.startswith('A'):
        match('A')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['$', 'j', '/', 'A']))

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('v'):
        match('v')
        parse_G()

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['w']))

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('?'):
        match('?')
        match('%')
        match('O')
        match('m')

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('R'):
        match('R')
        parse_S()
        parse_L()
        match('W')

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        parse_V()
        match('u')
        match(':')
        parse_M()
    elif lookahead.startswith('4'):
        match('4')
    elif lookahead.startswith('J'):
        match('J')
        match('Z')
        parse_V()
        parse_G()
    elif lookahead.startswith('f'):
        match('f')
        parse_C()
        parse_G()
        match('w')
    elif lookahead.startswith('Q'):
        match('Q')
        parse_G()
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join([',', '4', 'J', 'f', 'Q']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('P'):
        match('P')
        parse_C()
        parse_S()
        match('`')
    elif lookahead.startswith('j'):
        match('j')
        parse_M()
        parse_S()
        parse_G()
    elif lookahead.startswith('l'):
        match('l')
        match('Q')
        parse_G()
    elif lookahead.startswith('f'):
        match('f')
    elif lookahead.startswith('/'):
        match('/')
        parse_M()
        parse_F()
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['P', 'j', 'l', 'f', '/']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_F()
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