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

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('B'):
        match('B')
        match('>')
        match('d')
        while pos < len(tokens) and tokens[pos].startswith('|'):
            match('|')
            match('?')
            match('a')
            match('5')
            match('u')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('-'):
            match('-')
            parse_E()
            match('+')
        elif lookahead.startswith('0'):
            match('0')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['-', '0']))
    elif lookahead.startswith('%'):
        match('%')
        while pos < len(tokens) and tokens[pos].startswith('C'):
            match('C')
            parse_E()
            parse_G()
            match('z')
        match('r')
        match('&')
    elif lookahead.startswith('$'):
        match('$')
        match('N')
        match('K')
        match('S')
    elif lookahead.startswith('g'):
        match('g')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['B', '%', '$', 'g']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('-'):
        match('-')
        parse_E()
        match('+')
    elif lookahead.startswith('0'):
        match('0')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['-', '0']))

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('C'):
        match('C')
        parse_E()
        parse_G()
        match('z')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_I()
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