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
    while pos < len(tokens) and tokens[pos].startswith('o'):
        match('o')
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith('@'):
            match('@')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['@']))
        match('&')
        match('9')

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('l'):
        match('l')
        parse_M()
        match('x')
    elif lookahead.startswith('m'):
        match('m')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['l', 'm']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('='):
        match('=')
    elif lookahead.startswith('O'):
        match('O')
    elif lookahead.startswith('_'):
        match('_')
    elif lookahead.startswith('R'):
        match('R')
        match('t')
        parse_M()
        match('`')
        parse_W()
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['=', 'O', '_', 'R']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        parse_L()
        parse_M()
        match('9')
        parse_T()
    elif lookahead.startswith('@'):
        match('@')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join([',', '@']))

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('L'):
        parse_L()
        parse_E()
        match('3')
        match('s')
        match('}')

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('@'):
        match('@')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['@']))

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