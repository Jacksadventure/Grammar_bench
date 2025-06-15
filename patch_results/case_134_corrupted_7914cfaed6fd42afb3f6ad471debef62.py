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

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        match('v')
        match('(')
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith('w'):
            match('w')
            parse_P()
            parse_K()
            parse_Q()
        elif lookahead.startswith('H'):
            match('H')
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['w', 'H']))
        while pos < len(tokens) and tokens[pos].startswith('>'):
            match('>')
            match('8')
            parse_J()
    elif lookahead.startswith('['):
        match('[')
        while pos < len(tokens) and tokens[pos].startswith('W'):
            match('W')
    elif lookahead.startswith('v'):
        match('v')
        match(';')
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith('w'):
            match('w')
            parse_P()
            parse_K()
            parse_Q()
        elif lookahead.startswith('H'):
            match('H')
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['w', 'H']))
        match('W')
    elif lookahead.startswith('B'):
        match('B')
        while pos < len(tokens) and tokens[pos].startswith('W'):
            match('W')
    elif lookahead.startswith('k'):
        match('k')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['o', '[', 'v', 'B', 'k']))

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('U'):
        match('U')
        match('D')
        match('+')
        parse_J()

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('e'):
        match('e')
        match('z')
        match('u')
        match(',')
        parse_J()

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        parse_P()
        parse_K()
        parse_Q()
    elif lookahead.startswith('H'):
        match('H')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['w', 'H']))

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('C'):
        match('C')
        match('A')

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('>'):
        match('>')
        match('8')
        parse_J()

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('W'):
        match('W')

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        match('G')
        parse_I()
    elif lookahead.startswith('h'):
        match('h')
        parse_F()
        parse_J()
    elif lookahead.startswith('B'):
        match('B')
        parse_F()
        match('y')
        parse_M()
        match('*')
    elif lookahead.startswith('$'):
        match('$')
        match('0')
        parse_Q()
        match('1')
        parse_S()
    elif lookahead.startswith('{'):
        match('{')
        match('G')
    elif lookahead.startswith('c'):
        match('c')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join([',', 'h', 'B', '$', '{', 'c']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_J()
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