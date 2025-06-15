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
    if lookahead.startswith('b'):
        match('b')
        while pos < len(tokens) and tokens[pos].startswith('0'):
            match('0')
            parse_K()
            match('N')
            match('e')
            match(':')
        match('%')
        match(')')
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith('b'):
            match('b')
            parse_M()
            match('%')
            match(')')
            parse_D()
        elif lookahead.startswith('B'):
            match('B')
            parse_O()
            match('<')
            parse_O()
            parse_M()
        elif lookahead.startswith('Q'):
            match('Q')
            match('s')
            parse_K()
        elif lookahead.startswith('`'):
            match('`')
        else:
            error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['b', 'B', 'Q', '`']))
    elif lookahead.startswith('B'):
        match('B')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('5'):
            match('5')
        elif lookahead.startswith('_'):
            match('_')
            match('[')
            parse_O()
            parse_M()
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['5', '_']))
        match('<')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('5'):
            match('5')
        elif lookahead.startswith('_'):
            match('_')
            match('[')
            parse_O()
            parse_M()
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['5', '_']))
        while pos < len(tokens) and tokens[pos].startswith('0'):
            match('0')
            parse_K()
            match('N')
            match('e')
            match(':')
    elif lookahead.startswith('Q'):
        match('Q')
        match('s')
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith('%'):
            match('%')
            parse_O()
            parse_H()
            match('n')
            parse_X()
        elif lookahead.startswith('j'):
            match('j')
            match("'")
            match('>')
            match('#')
        elif lookahead.startswith('G'):
            match('G')
            match('9')
            match('+')
            parse_M()
            match('q')
        elif lookahead.startswith('*'):
            match('*')
        elif lookahead.startswith('N'):
            match('N')
            parse_M()
            match('e')
            match('!')
            parse_K()
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['%', 'j', 'G', '*', 'N']))
    elif lookahead.startswith('`'):
        match('`')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['b', 'B', 'Q', '`']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('5'):
        match('5')
    elif lookahead.startswith('_'):
        match('_')
        match('[')
        parse_O()
        parse_M()
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['5', '_']))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('3'):
        match('3')
        match('_')
        match('0')
        match('<')
        parse_K()

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('%'):
        match('%')
        parse_O()
        parse_H()
        match('n')
        parse_X()
    elif lookahead.startswith('j'):
        match('j')
        match("'")
        match('>')
        match('#')
    elif lookahead.startswith('G'):
        match('G')
        match('9')
        match('+')
        parse_M()
        match('q')
    elif lookahead.startswith('*'):
        match('*')
    elif lookahead.startswith('N'):
        match('N')
        parse_M()
        match('e')
        match('!')
        parse_K()
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['%', 'j', 'G', '*', 'N']))

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('0'):
        match('0')
        parse_K()
        match('N')
        match('e')
        match(':')

def parse_X():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('^'):
        match('^')
        match('g')
        match(']')
        match('k')
        match(':')

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