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
    if lookahead.startswith(')'):
        match(')')
        while pos < len(tokens) and tokens[pos].startswith(';'):
            match(';')
            match('J')
            parse_Y()
    elif lookahead.startswith('.'):
        match('.')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join([')', '.']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('C'):
        match('C')
        match('d')
        parse_B()
        match('5')
        parse_T()
    elif lookahead.startswith('l'):
        match('l')
        parse_F()
    elif lookahead.startswith('A'):
        match('A')
        match('D')
        parse_F()
        parse_F()
        match('a')
    elif lookahead.startswith('1'):
        match('1')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['C', 'l', 'A', '1']))

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(';'):
        match(';')
        match('J')
        parse_Y()

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('S'):
        match('S')
        parse_B()
        match('8')
    elif lookahead.startswith('_'):
        match('_')
        match('&')
        parse_H()
        parse_H()
    elif lookahead.startswith(';'):
        match(';')
    elif lookahead.startswith('d'):
        match('d')
    elif lookahead.startswith('N'):
        match('N')
        match('s')
        parse_K()
        parse_O()
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['S', '_', ';', 'd', 'N']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('2'):
        match('2')
        parse_T()
        match('N')
        match(']')
        match('9')
    elif lookahead.startswith('-'):
        match('-')
    elif lookahead.startswith('{'):
        match('{')
    elif lookahead.startswith('O'):
        parse_O()
        match('@')
        match('!')
        match('>')
        match('L')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['2', '-', '{', 'O']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('0'):
        match('0')
        parse_O()
    elif lookahead.startswith('$'):
        match('$')
        match('S')
        match('+')
    elif lookahead.startswith("'"):
        match("'")
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['0', '$', "'"]))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('b'):
        match('b')

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        parse_K()
        match('y')
        match('e')
    elif lookahead.startswith('q'):
        match('q')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['/', 'q']))

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