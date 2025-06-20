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

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('F'):
        match('F')
        match('0')
        while pos < len(tokens) and tokens[pos].startswith('('):
            match('(')
            parse_B()
            parse_G()
        match('q')
        match('D')
    elif lookahead.startswith('~'):
        match('~')
        match('m')
        match('z')
    elif lookahead.startswith('p'):
        match('p')
        match('1')
        match('n')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith(')'):
            match(')')
            match('a')
            match('3')
            match('r')
        elif lookahead.startswith('s'):
            match('s')
            parse_P()
            match('?')
            match('L')
            match('b')
        elif lookahead.startswith('$'):
            match('$')
            parse_R()
            match('m')
            match('/')
        elif lookahead.startswith('^'):
            match('^')
        else:
            error("Parse failed")
        match('t')
    elif lookahead.startswith('J'):
        match('J')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('%'):
            match('%')
            match('{')
        elif lookahead.startswith('`'):
            match('`')
            parse_V()
            match('Z')
            match('`')
        elif lookahead.startswith('f'):
            match('f')
            match('j')
            match('y')
        elif lookahead.startswith('6'):
            match('6')
            match('j')
            match('4')
            match(']')
            match('5')
        elif lookahead.startswith('h'):
            match('h')
        else:
            error("Parse failed")
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('T'):
            match('T')
            match('0')
            parse_S()
        elif lookahead.startswith('X'):
            match('X')
            match('+')
            parse_E()
        elif lookahead.startswith('['):
            match('[')
            match('`')
            match('0')
            parse_R()
        elif lookahead.startswith('}'):
            match('}')
            match('x')
            match('Y')
            parse_H()
        elif lookahead.startswith('P'):
            parse_P()
        else:
            error("Parse failed")
        match('s')
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('J'):
            match('J')
        elif lookahead.startswith('8'):
            match('8')
            match('o')
            match("'")
        elif lookahead.startswith('}'):
            match('}')
            match('h')
        elif lookahead.startswith('L'):
            match('L')
            parse_C()
            match('X')
            match("'")
            match('?')
        else:
            error("Parse failed")
    elif lookahead.startswith('+'):
        match('+')
    else:
        error("Parse failed")

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        match('{')
    elif lookahead.startswith('V'):
        parse_V()
        match('#')
        parse_V()
        match('q')
    elif lookahead.startswith("'"):
        match("'")
        parse_H()
        parse_O()
        parse_G()
    elif lookahead.startswith('2'):
        match('2')
        match('s')
        parse_G()
    elif lookahead.startswith('+'):
        match('+')
    else:
        error("Parse failed")

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('T'):
        match('T')
        match('0')
        parse_S()
    elif lookahead.startswith('X'):
        match('X')
        match('+')
        parse_E()
    elif lookahead.startswith('['):
        match('[')
        match('`')
        match('0')
        parse_R()
    elif lookahead.startswith('}'):
        match('}')
        match('x')
        match('Y')
        parse_H()
    elif lookahead.startswith('P'):
        parse_P()
    else:
        error("Parse failed")

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('%'):
        match('%')
        match('{')
    elif lookahead.startswith('`'):
        match('`')
        parse_V()
        match('Z')
        match('`')
    elif lookahead.startswith('f'):
        match('f')
        match('j')
        match('y')
    elif lookahead.startswith('6'):
        match('6')
        match('j')
        match('4')
        match(']')
        match('5')
    elif lookahead.startswith('h'):
        match('h')
    else:
        error("Parse failed")

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('`'):
        match('`')
        match('[')
    elif lookahead.startswith('+'):
        match('+')
        match('-')
        parse_P()
    elif lookahead.startswith('r'):
        match('r')
        match('X')
        match(']')
        match('d')
        parse_N()
    elif lookahead.startswith('J'):
        match('J')
    else:
        error("Parse failed")

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('J'):
        match('J')
    elif lookahead.startswith('8'):
        match('8')
        match('o')
        match("'")
    elif lookahead.startswith('}'):
        match('}')
        match('h')
    elif lookahead.startswith('L'):
        match('L')
        parse_C()
        match('X')
        match("'")
        match('?')
    else:
        error("Parse failed")

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('9'):
        match('9')
        match('a')
        match('|')
        parse_E()
        match('b')
    elif lookahead.startswith('y'):
        match('y')
    else:
        error("Parse failed")

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('('):
        match('(')
        parse_B()
        parse_G()

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('_'):
        match('_')
        match('v')
        parse_H()
        match('M')
    elif lookahead.startswith('R'):
        parse_R()
    else:
        error("Parse failed")

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('*'):
        match('*')

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith(')'):
        match(')')
        match('a')
        match('3')
        match('r')
    elif lookahead.startswith('s'):
        match('s')
        parse_P()
        match('?')
        match('L')
        match('b')
    elif lookahead.startswith('$'):
        match('$')
        parse_R()
        match('m')
        match('/')
    elif lookahead.startswith('^'):
        match('^')
    else:
        error("Parse failed")

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_P()
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