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
    if lookahead.startswith('g'):
        match('g')
        match('T')
        match('[')
        match('p')
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith('g'):
            match('g')
            match('T')
            match('[')
            match('p')
            parse_L()
        elif lookahead.startswith('A'):
            match('A')
            match('Y')
            match('9')
            match('m')
            match(',')
        elif lookahead.startswith('#'):
            match('#')
            parse_H()
            parse_W()
        elif lookahead.startswith('}'):
            match('}')
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['g', 'A', '#', '}']))
    elif lookahead.startswith('A'):
        match('A')
        match('Y')
        match('9')
        match('m')
        match(',')
    elif lookahead.startswith('#'):
        match('#')
        while pos < len(tokens) and tokens[pos].startswith('6'):
            match('6')
            parse_L()
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith('.'):
            match('.')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['.']))
    elif lookahead.startswith('}'):
        match('}')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['g', 'A', '#', '}']))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('6'):
        match('6')
        parse_L()

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('.'):
        match('.')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['.']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('4'):
        match('4')
        match('?')
        match('x')
    elif lookahead.startswith('~'):
        match('~')
        match('#')
        match('n')
    elif lookahead.startswith('A'):
        match('A')
        parse_W()
    elif lookahead.startswith('T'):
        match('T')
        parse_M()
        match("'")
        parse_H()
    elif lookahead.startswith('X'):
        match('X')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['4', '~', 'A', 'T', 'X']))

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