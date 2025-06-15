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

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('/'):
        match('/')
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith("'"):
            match("'")
            match('E')
            parse_K()
        elif lookahead.startswith('~'):
            match('~')
            parse_C()
        elif lookahead.startswith('@'):
            match('@')
            match('^')
            parse_U()
            match('j')
            match('N')
        elif lookahead.startswith('N'):
            match('N')
            match('9')
            match('R')
            match("'")
        elif lookahead.startswith('b'):
            match('b')
            match('?')
        elif lookahead.startswith('m'):
            match('m')
            parse_L()
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(["'", '~', '@', 'N', 'b', 'm']))
        match('~')
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith("'"):
            match("'")
            match('E')
            parse_K()
        elif lookahead.startswith('~'):
            match('~')
            parse_C()
        elif lookahead.startswith('@'):
            match('@')
            match('^')
            parse_U()
            match('j')
            match('N')
        elif lookahead.startswith('N'):
            match('N')
            match('9')
            match('R')
            match("'")
        elif lookahead.startswith('b'):
            match('b')
            match('?')
        elif lookahead.startswith('m'):
            match('m')
            parse_L()
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(["'", '~', '@', 'N', 'b', 'm']))
        match('#')
    elif lookahead.startswith('w'):
        match('w')
        match('8')
    elif lookahead.startswith('0'):
        match('0')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['/', 'w', '0']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('0'):
        match('0')
        match('O')
    elif lookahead.startswith('k'):
        match('k')
        parse_C()
        match('y')
        match('u')
    elif lookahead.startswith('/'):
        match('/')
    elif lookahead.startswith('['):
        match('[')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['0', 'k', '/', '[']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('D'):
        match('D')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['D']))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('R'):
        match('R')
        parse_U()
    elif lookahead.startswith('w'):
        match('w')
        match('2')
        parse_Y()
    elif lookahead.startswith('7'):
        match('7')
        parse_U()
        parse_U()
        parse_C()
    elif lookahead.startswith('E'):
        match('E')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['R', 'w', '7', 'E']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('6'):
        match('6')
        match('v')
        match(':')
        match('p')
        match('1')
    elif lookahead.startswith("'"):
        match("'")
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['6', "'"]))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        parse_W()
    elif lookahead.startswith('J'):
        match('J')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(["'", 'J']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        match('E')
        parse_K()
    elif lookahead.startswith('~'):
        match('~')
        parse_C()
    elif lookahead.startswith('@'):
        match('@')
        match('^')
        parse_U()
        match('j')
        match('N')
    elif lookahead.startswith('N'):
        match('N')
        match('9')
        match('R')
        match("'")
    elif lookahead.startswith('b'):
        match('b')
        match('?')
    elif lookahead.startswith('m'):
        match('m')
        parse_L()
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(["'", '~', '@', 'N', 'b', 'm']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_S()
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