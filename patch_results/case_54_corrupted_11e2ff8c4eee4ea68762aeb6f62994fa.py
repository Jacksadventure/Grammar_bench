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
    if lookahead.startswith('M'):
        match('M')
        match('9')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('b'):
            match('b')
            match('W')
            parse_O()
        elif lookahead.startswith('|'):
            match('|')
            match('S')
        elif lookahead.startswith('*'):
            match('*')
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['b', '|', '*']))
        match('b')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('3'):
            match('3')
        elif lookahead.startswith(','):
            match(',')
            parse_V()
        elif lookahead.startswith('N'):
            match('N')
            match('o')
            parse_L()
            match('A')
            parse_O()
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['3', ',', 'N']))
    elif lookahead.startswith('s'):
        match('s')
    elif lookahead.startswith('z'):
        match('z')
        match('c')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['M', 's', 'z']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('b'):
        match('b')
        match('W')
        parse_O()
    elif lookahead.startswith('|'):
        match('|')
        match('S')
    elif lookahead.startswith('*'):
        match('*')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['b', '|', '*']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('3'):
        match('3')
    elif lookahead.startswith(','):
        match(',')
        parse_V()
    elif lookahead.startswith('N'):
        match('N')
        match('o')
        parse_L()
        match('A')
        parse_O()
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['3', ',', 'N']))

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