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

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('V'):
        match('V')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('c'):
            match('c')
        elif lookahead.startswith('<'):
            match('<')
            match('L')
            parse_O()
            parse_I()
            parse_C()
        elif lookahead.startswith('&'):
            match('&')
            parse_D()
        elif lookahead.startswith('y'):
            match('y')
            parse_K()
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['c', '<', '&', 'y']))
        match('s')
        while pos < len(tokens) and tokens[pos].startswith('*'):
            match('*')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('<'):
            match('<')
            match('c')
            match('q')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['<', '']))
    elif lookahead.startswith('G'):
        while pos < len(tokens) and tokens[pos].startswith('R'):
            match('R')
            match('9')
            match('1')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['V', 'G']))

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('*'):
        match('*')

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('E'):
        match('E')
        match('*')
        parse_H()
        match('A')

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(':'):
        match(':')
        match('s')
        parse_I()
        match('6')

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('k'):
        match('k')
        match('+')
        match('+')

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('C'):
        parse_C()
        match('9')

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('<'):
        match('<')
        match('c')
        match('q')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['<', '']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_P()
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