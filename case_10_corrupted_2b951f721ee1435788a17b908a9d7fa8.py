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

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('&'):
        match('&')
        match("'")
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('i'):
            match('i')
            match('a')
            parse_S()
        elif lookahead.startswith('X'):
            match('X')
            match('W')
            match('k')
            match('3')
            match('n')
        elif lookahead.startswith('b'):
            match('b')
        else:
            error("Parse failed")
        match('5')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('!'):
            match('!')
            match('^')
        elif lookahead.startswith('U'):
            match('U')
            match('r')
        elif lookahead.startswith('+'):
            match('+')
        else:
            error("Parse failed")
    elif lookahead.startswith('p'):
        match('p')
        match('&')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('a'):
            match('a')
            match('x')
            parse_A()
        elif lookahead.startswith('G'):
            parse_G()
            match('Q')
            match('@')
        elif lookahead.startswith(','):
            match(',')
            match('?')
        elif lookahead.startswith('4'):
            match('4')
        elif lookahead.startswith('?'):
            match('?')
            parse_K()
            match('`')
            match('f')
        else:
            error("Parse failed")
        match('0')
        match('`')
    elif lookahead.startswith('('):
        match('(')
        match('e')
        match('5')
        match('h')
        match('t')
    elif lookahead.startswith('7'):
        match('7')
        match('4')
        match('V')
        match('z')
    elif lookahead.startswith('H'):
        match('H')
        match('{')
        match('O')
        match(':')
    elif lookahead.startswith('k'):
        match('k')
    else:
        error("Parse failed")

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('}'):
        match('}')
        match('^')
        parse_N()
    elif lookahead.startswith('k'):
        match('k')
        match('>')
        match('|')
        parse_E()
        match(',')
    elif lookahead.startswith('8'):
        match('8')
    else:
        error("Parse failed")

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('h'):
        match('h')
    else:
        error("Parse failed")

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('a'):
        match('a')
        match('x')
        parse_A()
    elif lookahead.startswith('G'):
        parse_G()
        match('Q')
        match('@')
    elif lookahead.startswith(','):
        match(',')
        match('?')
    elif lookahead.startswith('4'):
        match('4')
    elif lookahead.startswith('?'):
        match('?')
        parse_K()
        match('`')
        match('f')
    else:
        error("Parse failed")

def parse_Y():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('['):
        match('[')
        parse_T()
        parse_E()

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('b'):
        match('b')
        parse_A()
        parse_M()
    elif lookahead.startswith('V'):
        match('V')
        parse_A()
        match('t')
        match('u')
    elif lookahead.startswith('X'):
        match('X')
        match('a')
        match('h')
    elif lookahead.startswith('x'):
        match('x')
    elif lookahead.startswith('g'):
        match('g')
        match('X')
    else:
        error("Parse failed")

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('#'):
        match('#')
        match('>')
        parse_Y()
    elif lookahead.startswith('l'):
        match('l')
        match('[')
        match('4')
    elif lookahead.startswith('A'):
        parse_A()
        match('n')
        match('V')
        parse_T()
        parse_Y()
    elif lookahead.startswith('D'):
        match('D')
    else:
        error("Parse failed")

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('c'):
        match('c')
        match('h')
        parse_G()
        parse_B()
    elif lookahead.startswith('u'):
        match('u')
    elif lookahead.startswith('d'):
        match('d')
    elif lookahead.startswith('a'):
        match('a')
        parse_N()
    else:
        error("Parse failed")

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Q'):
        match('Q')
        parse_K()
        match('m')
        parse_K()

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('!'):
        match('!')
        match('^')
    elif lookahead.startswith('U'):
        match('U')
        match('r')
    elif lookahead.startswith('+'):
        match('+')
    else:
        error("Parse failed")

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_N()
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