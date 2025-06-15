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
    if lookahead.startswith('v'):
        match('v')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('t'):
            match('t')
            parse_A()
            parse_Q()
            parse_W()
        elif lookahead.startswith('q'):
            match('q')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['t', 'q']))
        match('S')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('v'):
            match('v')
            parse_J()
            match('S')
            parse_I()
            parse_I()
        elif lookahead.startswith('~'):
            match('~')
            match('H')
            match('m')
        elif lookahead.startswith('<'):
            match('<')
            match('k')
            match('/')
            match('2')
        elif lookahead.startswith('T'):
            match('T')
            match('`')
        elif lookahead.startswith('>'):
            match('>')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['v', '~', '<', 'T', '>']))
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('v'):
            match('v')
            parse_J()
            match('S')
            parse_I()
            parse_I()
        elif lookahead.startswith('~'):
            match('~')
            match('H')
            match('m')
        elif lookahead.startswith('<'):
            match('<')
            match('k')
            match('/')
            match('2')
        elif lookahead.startswith('T'):
            match('T')
            match('`')
        elif lookahead.startswith('>'):
            match('>')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['v', '~', '<', 'T', '>']))
    elif lookahead.startswith('~'):
        match('~')
        match('H')
        match('m')
    elif lookahead.startswith('<'):
        match('<')
        match('k')
        match('/')
        match('2')
    elif lookahead.startswith('T'):
        match('T')
        match('`')
    elif lookahead.startswith('>'):
        match('>')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['v', '~', '<', 'T', '>']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('.'):
        match('.')
        parse_G()
        match('8')
        match('t')
    elif lookahead.startswith('~'):
        match('~')
    elif lookahead.startswith('C'):
        match('C')
        parse_N()
        parse_Q()
        parse_F()
        match('n')
    elif lookahead.startswith('h'):
        match('h')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['.', '~', 'C', 'h']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('Y'):
        match('Y')
        match('!')
        parse_W()
    elif lookahead.startswith('j'):
        match('j')
        match('j')
        match('!')
        parse_Q()
        parse_O()
    elif lookahead.startswith('R'):
        parse_R()
    elif lookahead.startswith(','):
        match(',')
        parse_G()
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['Y', 'j', 'R', ',']))

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('F'):
        parse_F()
        parse_W()

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('t'):
        match('t')
        parse_A()
        parse_Q()
        parse_W()
    elif lookahead.startswith('q'):
        match('q')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['t', 'q']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        match('l')
        match('K')
        match('V')
        match('*')
    elif lookahead.startswith(':'):
        match(':')
        match('6')
    elif lookahead.startswith(';'):
        match(';')
    elif lookahead.startswith('m'):
        match('m')
        parse_J()
    elif lookahead.startswith('y'):
        match('y')
        match('!')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join([',', ':', ';', 'm', 'y']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('P'):
        match('P')
        match('_')
        parse_I()
    elif lookahead.startswith('y'):
        match('y')
        parse_J()
        match('E')
        parse_N()
        parse_N()
    elif lookahead.startswith('.'):
        match('.')
        parse_J()
        match('y')
    elif lookahead.startswith('b'):
        match('b')
        parse_Q()
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['P', 'y', '.', 'b', 'd']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('n'):
        match('n')
        match(']')
        match('n')
    elif lookahead.startswith('e'):
        match('e')
        match('$')
    elif lookahead.startswith('4'):
        match('4')
        parse_G()
    elif lookahead.startswith('m'):
        match('m')
        match('_')
        parse_R()
    elif lookahead.startswith('$'):
        match('$')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['n', 'e', '4', 'm', '$']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('1'):
        match('1')
    elif lookahead.startswith('X'):
        match('X')
        parse_N()
        match('|')
        match('-')
        match('p')
    elif lookahead.startswith('Y'):
        match('Y')
        match("'")
        parse_F()
        parse_A()
        parse_G()
    elif lookahead.startswith('v'):
        match('v')
        parse_N()
        parse_J()
        parse_G()
        parse_F()
    elif lookahead.startswith('6'):
        match('6')
        match(')')
        parse_O()
        parse_J()
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['1', 'X', 'Y', 'v', '6']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('E'):
        match('E')
        parse_A()
        match('V')
        parse_R()
        match('_')
    elif lookahead.startswith(','):
        match(',')
        parse_G()
    elif lookahead.startswith(':'):
        match(':')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['E', ',', ':']))

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