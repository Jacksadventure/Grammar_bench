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
    if lookahead.startswith('R'):
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('x'):
            match('x')
            parse_R()
            match('V')
            match('c')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['x', '']))
        while pos < len(tokens) and tokens[pos].startswith('K'):
            match('K')
            parse_G()
            parse_S()
            match('P')
            match('?')
        match('6')
    elif lookahead.startswith('K'):
        match('K')
        match("'")
    elif lookahead.startswith('['):
        match('[')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('R'):
            parse_R()
            parse_M()
            match('6')
        elif lookahead.startswith('K'):
            match('K')
            match("'")
        elif lookahead.startswith('['):
            match('[')
            parse_E()
            match('D')
            match('q')
            parse_N()
            parse_M()
        elif lookahead.startswith('%'):
            match('%')
            parse_M()
            parse_M()
            parse_M()
            parse_N()
        elif lookahead.startswith('0'):
            match('0')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['R', 'K', '[', '%', '0']))
        match('D')
        match('q')
        while pos < len(tokens) and tokens[pos].startswith('m'):
            match('m')
            match('s')
            parse_C()
            match('O')
            match('v')
        while pos < len(tokens) and tokens[pos].startswith('K'):
            match('K')
            parse_G()
            parse_S()
            match('P')
            match('?')
    elif lookahead.startswith('%'):
        match('%')
        while pos < len(tokens) and tokens[pos].startswith('K'):
            match('K')
            parse_G()
            parse_S()
            match('P')
            match('?')
        while pos < len(tokens) and tokens[pos].startswith('K'):
            match('K')
            parse_G()
            parse_S()
            match('P')
            match('?')
        while pos < len(tokens) and tokens[pos].startswith('K'):
            match('K')
            parse_G()
            parse_S()
            match('P')
            match('?')
        while pos < len(tokens) and tokens[pos].startswith('m'):
            match('m')
            match('s')
            parse_C()
            match('O')
            match('v')
    elif lookahead.startswith('0'):
        match('0')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['R', 'K', '[', '%', '0']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('x'):
        match('x')
        parse_R()
        match('V')
        match('c')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['x', '']))

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('K'):
        match('K')
        parse_G()
        parse_S()
        match('P')
        match('?')

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('H'):
        match('H')
        parse_R()
        match('&')

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('m'):
        match('m')
        match('s')
        parse_C()
        match('O')
        match('v')

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('<'):
        match('<')
        match('@')
        match('s')
        parse_S()

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('U'):
        match('U')
        match('o')

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