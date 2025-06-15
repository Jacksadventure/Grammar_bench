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
    if lookahead.startswith('1'):
        match('1')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('j'):
            match('j')
            match('#')
        elif lookahead.startswith('3'):
            match('3')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['j', '3']))
        match('v')
    elif lookahead.startswith('#'):
        match('#')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('t'):
            match('t')
            match('=')
            parse_L()
        elif lookahead.startswith('o'):
            match('o')
        elif lookahead.startswith('G'):
            match('G')
            match('j')
            parse_L()
            match('d')
            parse_L()
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['t', 'o', 'G']))
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith('1'):
            match('1')
            parse_A()
            match('v')
        elif lookahead.startswith('#'):
            match('#')
            parse_T()
            parse_L()
        elif lookahead.startswith('}'):
            match('}')
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['1', '#', '}']))
    elif lookahead.startswith('}'):
        match('}')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['1', '#', '}']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
        match('#')
    elif lookahead.startswith('3'):
        match('3')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['j', '3']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('t'):
        match('t')
        match('=')
        parse_L()
    elif lookahead.startswith('o'):
        match('o')
    elif lookahead.startswith('G'):
        match('G')
        match('j')
        parse_L()
        match('d')
        parse_L()
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['t', 'o', 'G']))

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