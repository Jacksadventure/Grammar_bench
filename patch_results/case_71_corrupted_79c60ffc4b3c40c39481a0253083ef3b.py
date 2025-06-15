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

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
        match('Q')
    elif lookahead.startswith('!'):
        match('!')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('j'):
            match('j')
            match('Q')
        elif lookahead.startswith('!'):
            match('!')
            parse_O()
            parse_X()
            match('P')
            parse_L()
        elif lookahead.startswith('0'):
            match('0')
            parse_T()
            parse_X()
            match('^')
            parse_L()
        elif lookahead.startswith('}'):
            match('}')
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['j', '!', '0', '}']))
        while pos < len(tokens) and tokens[pos].startswith('B'):
            match('B')
        match('P')
        while pos < len(tokens) and tokens[pos].startswith('>'):
            match('>')
            parse_X()
    elif lookahead.startswith('0'):
        match('0')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith(']'):
            match(']')
            match('q')
            parse_T()
            match('x')
        elif lookahead.startswith('w'):
            match('w')
            match('@')
            parse_T()
            match('^')
        elif lookahead.startswith(')'):
            match(')')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join([']', 'w', ')']))
        while pos < len(tokens) and tokens[pos].startswith('B'):
            match('B')
        match('^')
        while pos < len(tokens) and tokens[pos].startswith('>'):
            match('>')
            parse_X()
    elif lookahead.startswith('}'):
        match('}')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['j', '!', '0', '}']))

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('>'):
        match('>')
        parse_X()

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        match(']')
        match('q')
        parse_T()
        match('x')
    elif lookahead.startswith('w'):
        match('w')
        match('@')
        parse_T()
        match('^')
    elif lookahead.startswith(')'):
        match(')')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join([']', 'w', ')']))

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('B'):
        match('B')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_O()
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