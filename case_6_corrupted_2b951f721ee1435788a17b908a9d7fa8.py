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
    if lookahead.startswith('7'):
        match('7')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('['):
            match('[')
            match('5')
            match('y')
            parse_G()
        elif lookahead.startswith("'"):
            match("'")
            parse_D()
            match('c')
            parse_Y()
            match('~')
        elif lookahead.startswith('V'):
            match('V')
            match('S')
        elif lookahead.startswith('?'):
            match('?')
        else:
            error("Parse failed")
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('7'):
            match('7')
            parse_Z()
            parse_I()
            match('0')
            match('c')
        elif lookahead.startswith('&'):
            match('&')
            match('z')
            match('5')
            match('1')
        elif lookahead.startswith('S'):
            match('S')
        else:
            error("Parse failed")
        match('0')
        match('c')
    elif lookahead.startswith('&'):
        match('&')
        match('z')
        match('5')
        match('1')
    elif lookahead.startswith('S'):
        match('S')
    else:
        error("Parse failed")

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('{'):
        match('{')
        match('h')
        match('&')
        match('.')
    elif lookahead.startswith('>'):
        match('>')
        match('T')
        match('~')
        match('m')
        parse_U()
    elif lookahead.startswith('7'):
        match('7')
    else:
        error("Parse failed")

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('['):
        match('[')
        match('5')
        match('y')
        parse_G()
    elif lookahead.startswith("'"):
        match("'")
        parse_D()
        match('c')
        parse_Y()
        match('~')
    elif lookahead.startswith('V'):
        match('V')
        match('S')
    elif lookahead.startswith('?'):
        match('?')
    else:
        error("Parse failed")

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('n'):
        match('n')
        match('V')
        parse_W()
        match('t')
        match("'")
    elif lookahead.startswith('2'):
        match('2')
        parse_U()
        match('a')
        parse_O()
    elif lookahead.startswith('D'):
        parse_D()
    else:
        error("Parse failed")

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('Y'):
        parse_Y()
        match("'")
        match('7')
    elif lookahead.startswith('c'):
        match('c')
    else:
        error("Parse failed")

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        match('X')
        match('v')
        match('$')
        match('=')
    elif lookahead.startswith('H'):
        match('H')
    else:
        error("Parse failed")

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('q'):
        match('q')
        match('1')
        match('S')
        match('s')
        match('8')
    elif lookahead.startswith('7'):
        match('7')
        match('z')
        parse_F()
    elif lookahead.startswith('p'):
        match('p')
        match('}')
    elif lookahead.startswith('k'):
        match('k')
    else:
        error("Parse failed")

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('&'):
        match('&')
        parse_J()
        parse_Q()
    elif lookahead.startswith('T'):
        match('T')
    else:
        error("Parse failed")

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('e'):
        match('e')
        match('P')
        match('n')
        match(')')
    elif lookahead.startswith('5'):
        match('5')
    elif lookahead.startswith('u'):
        match('u')
        match('?')
    elif lookahead.startswith(','):
        match(',')
        parse_W()
        match('n')
        match('P')
    elif lookahead.startswith('D'):
        parse_D()
        match('r')
        parse_J()
        match('i')
        match('N')
    else:
        error("Parse failed")

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('g'):
        match('g')
        match('N')
        match('V')
        match('S')
    elif lookahead.startswith('*'):
        match('*')
        match('/')
        match('S')
        match('+')
        match('X')
    elif lookahead.startswith('R'):
        match('R')
        match(':')
        parse_W()
        match('}')
    elif lookahead.startswith('f'):
        match('f')
        match('|')
        match('@')
    elif lookahead.startswith('a'):
        match('a')
    else:
        error("Parse failed")

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        match(']')
    elif lookahead.startswith('e'):
        match('e')
        match('8')
    elif lookahead.startswith('q'):
        match('q')
        parse_G()
        match('S')
        parse_J()
        match('0')
    elif lookahead.startswith(','):
        match(',')
        match('}')
        match(')')
        match(':')
    elif lookahead.startswith('2'):
        match('2')
    else:
        error("Parse failed")

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