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

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('m'):
        match('m')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('3'):
            match('3')
            match('E')
            match('E')
        elif lookahead.startswith('u'):
            match('u')
        elif lookahead.startswith('1'):
            match('1')
            parse_A()
            match('0')
            match('Q')
            match('$')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['3', 'u', '1']))
    elif lookahead.startswith('4'):
        match('4')
        match('#')
        match('l')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('G'):
            match('G')
            match('j')
            match("'")
        elif lookahead.startswith("'"):
            match("'")
            parse_R()
            parse_R()
            parse_V()
        elif lookahead.startswith('%'):
            match('%')
            match('7')
            match('6')
            match('s')
            match(')')
        elif lookahead.startswith('.'):
            match('.')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['G', "'", '%', '.']))
    elif lookahead.startswith('^'):
        match('^')
        match('c')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('m'):
            match('m')
            parse_H()
        elif lookahead.startswith('4'):
            match('4')
            match('#')
            match('l')
            parse_A()
        elif lookahead.startswith('^'):
            match('^')
            match('c')
            parse_V()
            parse_R()
        elif lookahead.startswith('l'):
            match('l')
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['m', '4', '^', 'l']))
        while pos < len(tokens) and tokens[pos].startswith('O'):
            match('O')
    elif lookahead.startswith('l'):
        match('l')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['m', '4', '^', 'l']))

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('O'):
        match('O')

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('G'):
        match('G')
        match('j')
        match("'")
    elif lookahead.startswith("'"):
        match("'")
        parse_R()
        parse_R()
        parse_V()
    elif lookahead.startswith('%'):
        match('%')
        match('7')
        match('6')
        match('s')
        match(')')
    elif lookahead.startswith('.'):
        match('.')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['G', "'", '%', '.']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('3'):
        match('3')
        match('E')
        match('E')
    elif lookahead.startswith('u'):
        match('u')
    elif lookahead.startswith('1'):
        match('1')
        parse_A()
        match('0')
        match('Q')
        match('$')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['3', 'u', '1']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_V()
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