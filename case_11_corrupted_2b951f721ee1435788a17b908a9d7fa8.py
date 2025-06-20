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

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('i'):
        match('i')
        match('b')
        match('E')
    elif lookahead.startswith('9'):
        match('9')
        match('5')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('p'):
            match('p')
        elif lookahead.startswith('i'):
            match('i')
        elif lookahead.startswith(':'):
            match(':')
            match("'")
            match('t')
        elif lookahead.startswith('&'):
            match('&')
            match("'")
            parse_D()
        elif lookahead.startswith('9'):
            match('9')
            parse_I()
        else:
            error("Parse failed")
    elif lookahead.startswith('i'):
        match('i')
    else:
        error("Parse failed")

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('W'):
        parse_W()
        match('8')

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('4'):
        match('4')
        match('u')
    elif lookahead.startswith('G'):
        match('G')
        parse_K()
        parse_K()
        match('^')
    elif lookahead.startswith('a'):
        match('a')
        parse_F()
        match('3')
        match('7')
        parse_B()
    elif lookahead.startswith('-'):
        match('-')
        match('i')
        match('$')
        match('5')
        parse_I()
    elif lookahead.startswith('_'):
        match('_')
        parse_W()
    elif lookahead.startswith('2'):
        match('2')
    else:
        error("Parse failed")

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('T'):
        parse_T()
        match(',')
    elif lookahead.startswith('X'):
        parse_X()
    elif lookahead.startswith('m'):
        match('m')
        match('|')
    elif lookahead.startswith('J'):
        match('J')
    elif lookahead.startswith('^'):
        match('^')
        match('v')
        match('4')
        match('S')
        parse_T()
    else:
        error("Parse failed")

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('j'):
        match('j')

def parse_X():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in X")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        match('G')
    elif lookahead.startswith('#'):
        match('#')
        match('<')
        match('$')
        match('.')
        match('Z')
    elif lookahead.startswith('|'):
        match('|')
        parse_V()
    elif lookahead.startswith('6'):
        match('6')
    else:
        error("Parse failed")

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('w'):
        match('w')
        match('4')
        match('e')

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('u'):
        match('u')
        parse_F()
        parse_V()
        match('t')
    elif lookahead.startswith('g'):
        match('g')
        parse_I()
        match('@')
        match('i')
        parse_B()
    elif lookahead.startswith("'"):
        match("'")
        match('/')
        parse_T()
        parse_T()
        match("'")
    elif lookahead.startswith('Q'):
        match('Q')
        parse_P()
        match('&')
        parse_D()
        match('a')
    elif lookahead.startswith('T'):
        parse_T()
        match('=')
        parse_V()
        match('[')
        match('{')
    elif lookahead.startswith('q'):
        match('q')
    else:
        error("Parse failed")

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('L'):
        match('L')
        match('Q')
    else:
        error("Parse failed")

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('z'):
        match('z')
        parse_K()
        match('G')
        parse_V()
        match('E')
    elif lookahead.startswith('N'):
        match('N')
    else:
        error("Parse failed")

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_B()
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