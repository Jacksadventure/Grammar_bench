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
    if lookahead.startswith(';'):
        match(';')
        match('y')
        match('t')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('9'):
            match('9')
            match('F')
            match(';')
            parse_A()
            parse_U()
            match('b')
            match('{')
            parse_N()
            parse_Y()
        elif lookahead.startswith('u'):
            match('u')
            match('i')
            match('b')
            match('T')
            match('2')
            match('S')
            match("'")
        elif lookahead.startswith('L'):
            match('L')
            match('l')
        elif lookahead.startswith('p'):
            match('p')
            parse_V()
            parse_N()
            match('^')
            match('*')
            match(',')
            match('h')
        elif lookahead.startswith('h'):
            match('h')
        elif lookahead.startswith('o'):
            match('o')
            parse_E()
            match('2')
            match('S')
            parse_D()
        elif lookahead.startswith('J'):
            parse_J()
            parse_N()
            match('H')
            match('k')
            match('}')
            match('x')
            match('T')
        elif lookahead.startswith('l'):
            match('l')
            match('-')
            parse_U()
            parse_J()
            match('R')
        else:
            error("Parse failed")
        match("'")
        while pos < len(tokens) and tokens[pos].startswith('o'):
            match('o')
            parse_V()
        match(',')
        match('p')
    elif lookahead.startswith('<'):
        match('<')
        match(']')
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith(';'):
            match(';')
            match('y')
            match('t')
            parse_O()
            match("'")
            parse_U()
            match(',')
            match('p')
        elif lookahead.startswith('<'):
            match('<')
            match(']')
            parse_D()
            parse_U()
            match(')')
            match('6')
            parse_A()
            match('-')
            match('o')
            match('%')
        elif lookahead.startswith('J'):
            parse_J()
            match(';')
            parse_E()
            parse_E()
        elif lookahead.startswith('j'):
            match('j')
            parse_V()
        elif lookahead.startswith('6'):
            match('6')
            parse_U()
        elif lookahead.startswith("'"):
            match("'")
            match(':')
            match('?')
            match('w')
            match(',')
            parse_I()
        elif lookahead.startswith('1'):
            match('1')
            parse_O()
            match('k')
            match('%')
            parse_A()
            parse_D()
        elif lookahead.startswith('['):
            match('[')
            parse_U()
            parse_D()
            match('1')
            parse_V()
            match(',')
            parse_N()
            match('i')
            parse_I()
        elif lookahead.startswith('='):
            match('=')
            match('h')
            parse_A()
        elif lookahead.startswith('N'):
            parse_N()
        else:
            error("Parse failed")
        while pos < len(tokens) and tokens[pos].startswith('o'):
            match('o')
            parse_V()
        match(')')
        match('6')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('x'):
            match('x')
            match('n')
        elif lookahead.startswith('n'):
            match('n')
            parse_V()
            match('@')
            match("'")
            parse_D()
            parse_A()
            match('v')
            parse_E()
            match('/')
            match('2')
        elif lookahead.startswith('F'):
            match('F')
        else:
            error("Parse failed")
        match('-')
        match('o')
        match('%')
    elif lookahead.startswith('J'):
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('0'):
            match('0')
            match("'")
            match('T')
            parse_I()
            parse_E()
            match(';')
            parse_U()
            match('6')
            match('u')
        elif lookahead.startswith('['):
            match('[')
            match('+')
            parse_I()
            match('K')
            parse_O()
            parse_D()
            match('5')
            parse_J()
            match('[')
            parse_O()
        elif lookahead.startswith('*'):
            match('*')
            match('~')
            match(':')
            match('2')
            match(':')
            match(')')
            parse_J()
            match(';')
            match('%')
        elif lookahead.startswith("'"):
            match("'")
            match('w')
        elif lookahead.startswith('~'):
            match('~')
            parse_A()
            parse_O()
            match('r')
            match("'")
            parse_J()
            match('Q')
        elif lookahead.startswith('T'):
            match('T')
        else:
            error("Parse failed")
        match(';')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('0'):
            match('0')
            match('o')
            match('L')
            parse_I()
            match(',')
            match('B')
            match('_')
            match('<')
            parse_E()
        elif lookahead.startswith('2'):
            match('2')
            parse_V()
            match('o')
            match('_')
        elif lookahead.startswith('&'):
            match('&')
            match('Z')
        elif lookahead.startswith('K'):
            match('K')
            parse_A()
        elif lookahead.startswith('Z'):
            match('Z')
            parse_N()
            parse_A()
        elif lookahead.startswith('X'):
            match('X')
        elif lookahead.startswith("'"):
            match("'")
        elif lookahead.startswith('w'):
            match('w')
            match('K')
            match(')')
            match('R')
            match('M')
            parse_O()
            parse_V()
        elif lookahead.startswith('`'):
            match('`')
            match(')')
            match('t')
            parse_O()
            parse_D()
            match('=')
            parse_D()
        elif lookahead.startswith('M'):
            match('M')
            match('R')
            match('d')
            parse_E()
            match('b')
        else:
            error("Parse failed")
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('0'):
            match('0')
            match('o')
            match('L')
            parse_I()
            match(',')
            match('B')
            match('_')
            match('<')
            parse_E()
        elif lookahead.startswith('2'):
            match('2')
            parse_V()
            match('o')
            match('_')
        elif lookahead.startswith('&'):
            match('&')
            match('Z')
        elif lookahead.startswith('K'):
            match('K')
            parse_A()
        elif lookahead.startswith('Z'):
            match('Z')
            parse_N()
            parse_A()
        elif lookahead.startswith('X'):
            match('X')
        elif lookahead.startswith("'"):
            match("'")
        elif lookahead.startswith('w'):
            match('w')
            match('K')
            match(')')
            match('R')
            match('M')
            parse_O()
            parse_V()
        elif lookahead.startswith('`'):
            match('`')
            match(')')
            match('t')
            parse_O()
            parse_D()
            match('=')
            parse_D()
        elif lookahead.startswith('M'):
            match('M')
            match('R')
            match('d')
            parse_E()
            match('b')
        else:
            error("Parse failed")
    elif lookahead.startswith('j'):
        match('j')
        while pos < len(tokens) and tokens[pos].startswith('v'):
            match('v')
            parse_E()
            parse_V()
            match('x')
            match('^')
            parse_D()
            match('-')
            match('<')
            match('~')
            match(')')
    elif lookahead.startswith('6'):
        match('6')
        while pos < len(tokens) and tokens[pos].startswith('o'):
            match('o')
            parse_V()
    elif lookahead.startswith("'"):
        match("'")
        match(':')
        match('?')
        match('w')
        match(',')
        while pos < len(tokens) and tokens[pos].startswith('1'):
            match('1')
            match('^')
            parse_D()
            match('%')
            parse_V()
            parse_U()
            match('H')
            match('i')
            match('r')
    elif lookahead.startswith('1'):
        match('1')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('9'):
            match('9')
            match('F')
            match(';')
            parse_A()
            parse_U()
            match('b')
            match('{')
            parse_N()
            parse_Y()
        elif lookahead.startswith('u'):
            match('u')
            match('i')
            match('b')
            match('T')
            match('2')
            match('S')
            match("'")
        elif lookahead.startswith('L'):
            match('L')
            match('l')
        elif lookahead.startswith('p'):
            match('p')
            parse_V()
            parse_N()
            match('^')
            match('*')
            match(',')
            match('h')
        elif lookahead.startswith('h'):
            match('h')
        elif lookahead.startswith('o'):
            match('o')
            parse_E()
            match('2')
            match('S')
            parse_D()
        elif lookahead.startswith('J'):
            parse_J()
            parse_N()
            match('H')
            match('k')
            match('}')
            match('x')
            match('T')
        elif lookahead.startswith('l'):
            match('l')
            match('-')
            parse_U()
            parse_J()
            match('R')
        else:
            error("Parse failed")
        match('k')
        match('%')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('x'):
            match('x')
            match('n')
        elif lookahead.startswith('n'):
            match('n')
            parse_V()
            match('@')
            match("'")
            parse_D()
            parse_A()
            match('v')
            parse_E()
            match('/')
            match('2')
        elif lookahead.startswith('F'):
            match('F')
        else:
            error("Parse failed")
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith(';'):
            match(';')
            match('y')
            match('t')
            parse_O()
            match("'")
            parse_U()
            match(',')
            match('p')
        elif lookahead.startswith('<'):
            match('<')
            match(']')
            parse_D()
            parse_U()
            match(')')
            match('6')
            parse_A()
            match('-')
            match('o')
            match('%')
        elif lookahead.startswith('J'):
            parse_J()
            match(';')
            parse_E()
            parse_E()
        elif lookahead.startswith('j'):
            match('j')
            parse_V()
        elif lookahead.startswith('6'):
            match('6')
            parse_U()
        elif lookahead.startswith("'"):
            match("'")
            match(':')
            match('?')
            match('w')
            match(',')
            parse_I()
        elif lookahead.startswith('1'):
            match('1')
            parse_O()
            match('k')
            match('%')
            parse_A()
            parse_D()
        elif lookahead.startswith('['):
            match('[')
            parse_U()
            parse_D()
            match('1')
            parse_V()
            match(',')
            parse_N()
            match('i')
            parse_I()
        elif lookahead.startswith('='):
            match('=')
            match('h')
            parse_A()
        elif lookahead.startswith('N'):
            parse_N()
        else:
            error("Parse failed")
    elif lookahead.startswith('['):
        match('[')
        while pos < len(tokens) and tokens[pos].startswith('o'):
            match('o')
            parse_V()
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith(';'):
            match(';')
            match('y')
            match('t')
            parse_O()
            match("'")
            parse_U()
            match(',')
            match('p')
        elif lookahead.startswith('<'):
            match('<')
            match(']')
            parse_D()
            parse_U()
            match(')')
            match('6')
            parse_A()
            match('-')
            match('o')
            match('%')
        elif lookahead.startswith('J'):
            parse_J()
            match(';')
            parse_E()
            parse_E()
        elif lookahead.startswith('j'):
            match('j')
            parse_V()
        elif lookahead.startswith('6'):
            match('6')
            parse_U()
        elif lookahead.startswith("'"):
            match("'")
            match(':')
            match('?')
            match('w')
            match(',')
            parse_I()
        elif lookahead.startswith('1'):
            match('1')
            parse_O()
            match('k')
            match('%')
            parse_A()
            parse_D()
        elif lookahead.startswith('['):
            match('[')
            parse_U()
            parse_D()
            match('1')
            parse_V()
            match(',')
            parse_N()
            match('i')
            parse_I()
        elif lookahead.startswith('='):
            match('=')
            match('h')
            parse_A()
        elif lookahead.startswith('N'):
            parse_N()
        else:
            error("Parse failed")
        match('1')
        while pos < len(tokens) and tokens[pos].startswith('v'):
            match('v')
            parse_E()
            parse_V()
            match('x')
            match('^')
            parse_D()
            match('-')
            match('<')
            match('~')
            match(')')
        match(',')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('m'):
            match('m')
        elif lookahead.startswith('$'):
            match('$')
            parse_J()
            match('R')
            parse_E()
        elif lookahead.startswith('0'):
            match('0')
            match("'")
            match('<')
            match('}')
            match("'")
        elif lookahead.startswith('a'):
            match('a')
            parse_A()
        elif lookahead.startswith('6'):
            match('6')
            parse_E()
        elif lookahead.startswith('<'):
            match('<')
        elif lookahead.startswith('O'):
            parse_O()
            parse_J()
            match('d')
            match('[')
            match('i')
        else:
            error("Parse failed")
        match('i')
        while pos < len(tokens) and tokens[pos].startswith('1'):
            match('1')
            match('^')
            parse_D()
            match('%')
            parse_V()
            parse_U()
            match('H')
            match('i')
            match('r')
    elif lookahead.startswith('='):
        match('=')
        match('h')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('x'):
            match('x')
            match('n')
        elif lookahead.startswith('n'):
            match('n')
            parse_V()
            match('@')
            match("'")
            parse_D()
            parse_A()
            match('v')
            parse_E()
            match('/')
            match('2')
        elif lookahead.startswith('F'):
            match('F')
        else:
            error("Parse failed")
    elif lookahead.startswith('N'):
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('m'):
            match('m')
        elif lookahead.startswith('$'):
            match('$')
            parse_J()
            match('R')
            parse_E()
        elif lookahead.startswith('0'):
            match('0')
            match("'")
            match('<')
            match('}')
            match("'")
        elif lookahead.startswith('a'):
            match('a')
            parse_A()
        elif lookahead.startswith('6'):
            match('6')
            parse_E()
        elif lookahead.startswith('<'):
            match('<')
        elif lookahead.startswith('O'):
            parse_O()
            parse_J()
            match('d')
            match('[')
            match('i')
        else:
            error("Parse failed")
    else:
        error("Parse failed")

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('m'):
        match('m')
    elif lookahead.startswith('$'):
        match('$')
        parse_J()
        match('R')
        parse_E()
    elif lookahead.startswith('0'):
        match('0')
        match("'")
        match('<')
        match('}')
        match("'")
    elif lookahead.startswith('a'):
        match('a')
        parse_A()
    elif lookahead.startswith('6'):
        match('6')
        parse_E()
    elif lookahead.startswith('<'):
        match('<')
    elif lookahead.startswith('O'):
        parse_O()
        parse_J()
        match('d')
        match('[')
        match('i')
    else:
        error("Parse failed")

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('x'):
        match('x')
        match('n')
    elif lookahead.startswith('n'):
        match('n')
        parse_V()
        match('@')
        match("'")
        parse_D()
        parse_A()
        match('v')
        parse_E()
        match('/')
        match('2')
    elif lookahead.startswith('F'):
        match('F')
    else:
        error("Parse failed")

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('v'):
        match('v')
        parse_E()
        parse_V()
        match('x')
        match('^')
        parse_D()
        match('-')
        match('<')
        match('~')
        match(')')

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('o'):
        match('o')
        parse_V()

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('0'):
        match('0')
        match("'")
        match('T')
        parse_I()
        parse_E()
        match(';')
        parse_U()
        match('6')
        match('u')
    elif lookahead.startswith('['):
        match('[')
        match('+')
        parse_I()
        match('K')
        parse_O()
        parse_D()
        match('5')
        parse_J()
        match('[')
        parse_O()
    elif lookahead.startswith('*'):
        match('*')
        match('~')
        match(':')
        match('2')
        match(':')
        match(')')
        parse_J()
        match(';')
        match('%')
    elif lookahead.startswith("'"):
        match("'")
        match('w')
    elif lookahead.startswith('~'):
        match('~')
        parse_A()
        parse_O()
        match('r')
        match("'")
        parse_J()
        match('Q')
    elif lookahead.startswith('T'):
        match('T')
    else:
        error("Parse failed")

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('|'):
        match('|')
        parse_U()
        match('b')
        parse_O()
        parse_J()
        parse_V()
        parse_J()
        parse_J()
    elif lookahead.startswith('b'):
        match('b')
        match('B')
        match('Z')
        match('=')
        parse_J()
        parse_U()
        parse_N()
        match('K')
    elif lookahead.startswith('6'):
        match('6')
    elif lookahead.startswith('*'):
        match('*')
        match('a')
        parse_D()
        match('`')
    elif lookahead.startswith("'"):
        match("'")
        match(',')
        match('K')
    elif lookahead.startswith('C'):
        match('C')
    elif lookahead.startswith('R'):
        match('R')
        parse_Y()
        match('~')
        parse_D()
        match("'")
        match('/')
    elif lookahead.startswith('<'):
        match('<')
        match(']')
        match('H')
        match('3')
        parse_J()
        parse_N()
        match('W')
        match('C')
        parse_Y()
        match(']')
    elif lookahead.startswith('p'):
        match('p')
        match('P')
        parse_A()
        match('?')
        match('H')
        match('g')
        match('u')
        match('P')
        parse_I()
        match(',')
    elif lookahead.startswith('s'):
        match('s')
        parse_J()
        match('%')
        match('W')
    else:
        error("Parse failed")

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('9'):
        match('9')
        match('F')
        match(';')
        parse_A()
        parse_U()
        match('b')
        match('{')
        parse_N()
        parse_Y()
    elif lookahead.startswith('u'):
        match('u')
        match('i')
        match('b')
        match('T')
        match('2')
        match('S')
        match("'")
    elif lookahead.startswith('L'):
        match('L')
        match('l')
    elif lookahead.startswith('p'):
        match('p')
        parse_V()
        parse_N()
        match('^')
        match('*')
        match(',')
        match('h')
    elif lookahead.startswith('h'):
        match('h')
    elif lookahead.startswith('o'):
        match('o')
        parse_E()
        match('2')
        match('S')
        parse_D()
    elif lookahead.startswith('J'):
        parse_J()
        parse_N()
        match('H')
        match('k')
        match('}')
        match('x')
        match('T')
    elif lookahead.startswith('l'):
        match('l')
        match('-')
        parse_U()
        parse_J()
        match('R')
    else:
        error("Parse failed")

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('0'):
        match('0')
        match('o')
        match('L')
        parse_I()
        match(',')
        match('B')
        match('_')
        match('<')
        parse_E()
    elif lookahead.startswith('2'):
        match('2')
        parse_V()
        match('o')
        match('_')
    elif lookahead.startswith('&'):
        match('&')
        match('Z')
    elif lookahead.startswith('K'):
        match('K')
        parse_A()
    elif lookahead.startswith('Z'):
        match('Z')
        parse_N()
        parse_A()
    elif lookahead.startswith('X'):
        match('X')
    elif lookahead.startswith("'"):
        match("'")
    elif lookahead.startswith('w'):
        match('w')
        match('K')
        match(')')
        match('R')
        match('M')
        parse_O()
        parse_V()
    elif lookahead.startswith('`'):
        match('`')
        match(')')
        match('t')
        parse_O()
        parse_D()
        match('=')
        parse_D()
    elif lookahead.startswith('M'):
        match('M')
        match('R')
        match('d')
        parse_E()
        match('b')
    else:
        error("Parse failed")

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('1'):
        match('1')
        match('^')
        parse_D()
        match('%')
        parse_V()
        parse_U()
        match('H')
        match('i')
        match('r')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    try:
        parse_D()
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