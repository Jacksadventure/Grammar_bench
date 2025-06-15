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

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith(':'):
        match(':')
        match('a')
        match('N')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('1'):
            match('1')
            match('p')
            parse_W()
            match('-')
            parse_V()
        elif lookahead.startswith('7'):
            match('7')
        elif lookahead.startswith('g'):
            match('g')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['1', '7', 'g']))
    elif lookahead.startswith('}'):
        match('}')
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith(':'):
            match(':')
            match('a')
            match('N')
            parse_I()
        elif lookahead.startswith('}'):
            match('}')
            parse_W()
        elif lookahead.startswith('m'):
            match('m')
            match(']')
            match('.')
            match('_')
        elif lookahead.startswith('w'):
            match('w')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join([':', '}', 'm', 'w']))
    elif lookahead.startswith('m'):
        match('m')
        match(']')
        match('.')
        match('_')
    elif lookahead.startswith('w'):
        match('w')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join([':', '}', 'm', 'w']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('1'):
        match('1')
        match('p')
        parse_W()
        match('-')
        parse_V()
    elif lookahead.startswith('7'):
        match('7')
    elif lookahead.startswith('g'):
        match('g')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['1', '7', 'g']))

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('M'):
        match('M')
        parse_W()
        match('^')
        match('v')
        match('b')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_W()
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