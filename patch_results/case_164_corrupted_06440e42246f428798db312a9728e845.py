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

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('<'):
        match('<')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('e'):
            match('e')
            match('=')
            match('P')
        elif lookahead.startswith('E'):
            match('E')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['e', 'E']))
        match('U')
        if pos >= len(tokens):
            error("Unexpected end of input in Q")
        lookahead = tokens[pos]
        if lookahead.startswith('<'):
            match('<')
            parse_R()
            match('U')
            parse_Q()
            parse_R()
            parse_Q()
        elif lookahead.startswith('|'):
            match('|')
            parse_L()
        else:
            error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['<', '', '|']))
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('e'):
            match('e')
            match('=')
            match('P')
        elif lookahead.startswith('E'):
            match('E')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['e', 'E']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('e'):
        match('e')
        match('=')
        match('P')
    elif lookahead.startswith('E'):
        match('E')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['e', 'E']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('1'):
        match('1')
        parse_L()
        match('I')
        match('p')
    elif lookahead.startswith('I'):
        match('I')
        parse_L()
        match('@')
        match('m')
    elif lookahead.startswith(';'):
        match(';')
        match('Z')
    elif lookahead.startswith('h'):
        match('h')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['1', 'I', ';', 'h']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Q()
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