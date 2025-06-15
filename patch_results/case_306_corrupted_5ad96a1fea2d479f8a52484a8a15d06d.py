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

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('h'):
        match('h')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('2'):
            match('2')
            match('V')
            match('l')
            parse_N()
        elif lookahead.startswith(','):
            match(',')
            parse_O()
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['2', '', ',']))
        match('2')
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith('_'):
            match('_')
            parse_W()
            match('S')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['_', '']))
        match(',')

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('_'):
        match('_')
        parse_W()
        match('S')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['_', '']))

def parse_N():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('2'):
        match('2')
        match('V')
        match('l')

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('$'):
        match('$')

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('M'):
        parse_M()
        match('z')
        parse_W()
        match('$')

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('&'):
        match('&')
        parse_M()
        parse_W()

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Y'):
        match('Y')
        match('K')
        parse_J()

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith(')'):
        match(')')
        parse_X()
        parse_Q()
        parse_X()
        match('v')
    elif lookahead.startswith('q'):
        match('q')
        parse_F()
    elif lookahead.startswith('.'):
        match('.')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join([')', 'q', '.']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_M()
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