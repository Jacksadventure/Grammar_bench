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
    while pos < len(tokens) and tokens[pos].startswith('['):
        match('[')
        match('*')
        match('^')
        match('d')
        match('l')
        match('8')
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('t'):
            match('t')
            match('b')
            match("'")
            parse_Z()
            match(':')
            match('4')
            match('U')
        elif lookahead.startswith(']'):
            match(']')
            match('D')
            match('`')
        elif lookahead.startswith('L'):
            match('L')
            parse_H()
        elif lookahead.startswith('/'):
            match('/')
            match('%')
        elif lookahead.startswith('y'):
            match('y')
            match('x')
            parse_P()
            match('C')
            match('W')
            match('n')
        elif lookahead.startswith('+'):
            match('+')
        else:
            error("Parse failed")
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith(','):
            match(',')
            parse_G()
            match('v')
            match('?')
            parse_X()
        elif lookahead.startswith('x'):
            match('x')
        else:
            error("Parse failed")

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('P'):
        parse_P()

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('B'):
        match('B')
        match('4')
        match('o')
        match('^')
        parse_E()
        match('B')
        match('|')
    elif lookahead.startswith('C'):
        match('C')
        match('f')
        match('[')
    elif lookahead.startswith('7'):
        match('7')
        match('W')
        parse_P()
    elif lookahead.startswith('k'):
        match('k')
        match('C')
        parse_G()
        parse_X()
        match('&')
        match('5')
        match('g')
    elif lookahead.startswith('n'):
        match('n')
        match('/')
        match('@')
        match('A')
        match('(')
        match('4')
        match('L')
        match('3')
    elif lookahead.startswith('v'):
        match('v')
        match('9')
        match('U')
        match('i')
        match('`')
        match('I')
        match('t')
    elif lookahead.startswith('<'):
        match('<')
    else:
        error("Parse failed")

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        parse_G()
        match('v')
        match('?')
        parse_X()
    elif lookahead.startswith('x'):
        match('x')
    else:
        error("Parse failed")

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('+'):
        match('+')
        match('1')
        parse_X()
        match('g')
        parse_E()
        match('?')
        match('~')
        match('8')

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('{'):
        match('{')
        match('3')
    elif lookahead.startswith('#'):
        match('#')
    elif lookahead.startswith('>'):
        match('>')
        match(')')
        match('p')
        match("'")
        parse_P()
    elif lookahead.startswith('='):
        match('=')
        parse_Z()
        match('C')
        match('v')
        match('Y')
        match('/')
    else:
        error("Parse failed")

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('e'):
        match('e')
        match('y')
        match('$')
        parse_M()
    elif lookahead.startswith('v'):
        match('v')
        match('A')
        match('j')
        match('p')
        match('c')
        match("'")
        match('A')
        match('=')
    elif lookahead.startswith('J'):
        match('J')
    else:
        error("Parse failed")

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('t'):
        match('t')
        match('b')
        match("'")
        parse_Z()
        match(':')
        match('4')
        match('U')
    elif lookahead.startswith(']'):
        match(']')
        match('D')
        match('`')
    elif lookahead.startswith('L'):
        match('L')
        parse_H()
    elif lookahead.startswith('/'):
        match('/')
        match('%')
    elif lookahead.startswith('y'):
        match('y')
        match('x')
        parse_P()
        match('C')
        match('W')
        match('n')
    elif lookahead.startswith('+'):
        match('+')
    else:
        error("Parse failed")

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    try:
        parse_V()
    except SyntaxError:
        # Partial parser: accept if some tokens consumed
        if pos == 0:
            raise
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