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

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('C'):
        match('C')
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith(']'):
            match(']')
            match(':')
            match('C')
        elif lookahead.startswith('W'):
            match('W')
            parse_Y()
            match('v')
            match('N')
            parse_M()
        elif lookahead.startswith('e'):
            match('e')
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join([']', 'W', 'e']))
        match('3')
    elif lookahead.startswith('$'):
        match('$')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['C', '$']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        match('x')
        match('#')
        match('+')
    elif lookahead.startswith('a'):
        match('a')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join([',', 'a']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('C'):
        match('C')
        parse_P()
        match('@')
        match('z')
        parse_Y()
    elif lookahead.startswith(':'):
        match(':')
        match('_')
        parse_S()
        match('_')
        parse_D()
    elif lookahead.startswith(']'):
        match(']')
        match('B')
        match('$')
        parse_M()
    elif lookahead.startswith('!'):
        match('!')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['C', ':', ']', '!']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('p'):
        match('p')
        parse_Y()
        parse_P()
        parse_P()
        match('Q')
        parse_F()
    elif lookahead.startswith('T'):
        match('T')
        parse_Y()
    elif lookahead.startswith('!'):
        match('!')
        parse_S()
    elif lookahead.startswith('E'):
        match('E')
        match('g')
        parse_M()
        match('V')
        match('6')
    elif lookahead.startswith('V'):
        match('V')
        match('f')
        match('N')
        parse_P()
    elif lookahead.startswith('G'):
        match('G')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['p', 'T', '!', 'E', 'V', 'G']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('='):
        match('=')
    elif lookahead.startswith('i'):
        match('i')
        match('^')
        match('2')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['=', 'i']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        match(']')
        match(':')
        match('C')
    elif lookahead.startswith('W'):
        match('W')
        parse_Y()
        match('v')
        match('N')
        parse_M()
    elif lookahead.startswith('e'):
        match('e')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join([']', 'W', 'e']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('Q'):
        match('Q')
        parse_P()
        match('B')
        match('-')
    elif lookahead.startswith('1'):
        match('1')
        parse_J()
    elif lookahead.startswith('w'):
        match('w')
        parse_S()
    elif lookahead.startswith('t'):
        match('t')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['Q', '1', 'w', 't']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_D()
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