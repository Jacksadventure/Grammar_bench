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

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('7'):
        match('7')
        while pos < len(tokens) and tokens[pos].startswith('-'):
            match('-')
            match('6')
            parse_X()
            parse_L()
            parse_D()
        while pos < len(tokens) and tokens[pos].startswith('1'):
            match('1')
            match('>')
        while pos < len(tokens) and tokens[pos].startswith('!'):
            match('!')
            match('q')
            match("'")
            parse_L()
            match('G')
        match('w')
    elif lookahead.startswith('8'):
        match('8')
        while pos < len(tokens) and tokens[pos].startswith('*'):
            match('*')
            parse_T()
            parse_X()
            match('j')
            parse_V()
        while pos < len(tokens) and tokens[pos].startswith('*'):
            match('*')
            parse_T()
            parse_X()
            match('j')
            parse_V()
        while pos < len(tokens) and tokens[pos].startswith(';'):
            match(';')
            match("'")
    elif lookahead.startswith('>'):
        match('>')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['7', '8', '>']))

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('w'):
        match('w')
        match('3')
        match('6')

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(';'):
        match(';')
        match("'")

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('1'):
        match('1')
        match('>')

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('-'):
        match('-')
        match('6')
        parse_X()
        parse_L()
        parse_D()

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('A'):
        match('A')
        parse_U()
        match('R')
        match('v')

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        match(']')
        parse_C()
        parse_X()
        match('P')
    elif lookahead.startswith("'"):
        match("'")
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join([']', "'"]))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith(')'):
        match(')')
        match('r')
        match('5')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join([')', '']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_K()
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