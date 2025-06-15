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

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('H'):
        match('H')
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('#'):
            match('#')
            match('0')
            parse_K()
        elif lookahead.startswith('o'):
            match('o')
            match('4')
            match('b')
        elif lookahead.startswith('7'):
            match('7')
            parse_S()
            match('v')
        elif lookahead.startswith('d'):
            match('d')
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['#', 'o', '7', 'd']))
    elif lookahead.startswith('_'):
        match('_')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['H', '_']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('c'):
        match('c')
        parse_M()
        match('b')
        match('v')
    elif lookahead.startswith('+'):
        match('+')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['c', '+']))

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        match('n')
        match('b')
        match(',')
        parse_G()
    elif lookahead.startswith('g'):
        match('g')
    elif lookahead.startswith('v'):
        match('v')
        match('(')
        match('}')
        match('P')
        match('&')
    elif lookahead.startswith('H'):
        match('H')
        match('J')
        match('Z')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['w', 'g', 'v', 'H']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('O'):
        match('O')
    elif lookahead.startswith('A'):
        match('A')
    elif lookahead.startswith('*'):
        match('*')
        match('y')
        match('J')
        parse_K()
        match('@')
    elif lookahead.startswith('y'):
        match('y')
    elif lookahead.startswith('#'):
        match('#')
        parse_D()
        parse_R()
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['O', 'A', '*', 'y', '#']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('#'):
        match('#')
        match('0')
        parse_K()
    elif lookahead.startswith('o'):
        match('o')
        match('4')
        match('b')
    elif lookahead.startswith('7'):
        match('7')
        parse_S()
        match('v')
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['#', 'o', '7', 'd']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('e'):
        match('e')
    elif lookahead.startswith('J'):
        match('J')
        match('_')
        match("'")
        match('a')
        parse_D()
    elif lookahead.startswith('O'):
        match('O')
        match('0')
        parse_M()
        match('H')
    elif lookahead.startswith("'"):
        match("'")
        parse_V()
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['e', 'J', 'O', "'"]))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('~'):
        match('~')
        match('~')
        parse_Y()
    elif lookahead.startswith('C'):
        match('C')
        match('$')
    elif lookahead.startswith('0'):
        match('0')
        parse_G()
        parse_D()
    elif lookahead.startswith('$'):
        match('$')
        match('/')
        match('&')
    elif lookahead.startswith('O'):
        match('O')
        match('#')
        match('O')
        parse_R()
        match('w')
    elif lookahead.startswith('h'):
        match('h')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['~', 'C', '0', '$', 'O', 'h']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('k'):
        match('k')
        match('r')
        parse_D()
    elif lookahead.startswith('!'):
        match('!')
        match('1')
        parse_R()
        match(',')
    elif lookahead.startswith('e'):
        match('e')
        match('}')
        parse_R()
    elif lookahead.startswith('g'):
        match('g')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['k', '!', 'e', 'g']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('U'):
        match('U')
        parse_F()
    elif lookahead.startswith(')'):
        match(')')
        match('&')
        match('n')
        match('P')
    elif lookahead.startswith('E'):
        match('E')
    elif lookahead.startswith('W'):
        match('W')
        parse_K()
        parse_N()
        match('n')
        match('8')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['U', ')', 'E', 'W']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('~'):
        match('~')
        parse_K()
        match('H')
    elif lookahead.startswith(','):
        match(',')
        match('x')
        parse_F()
        parse_S()
    elif lookahead.startswith(']'):
        match(']')
        match(';')
        match("'")
        match('@')
    elif lookahead.startswith('x'):
        match('x')
        match('6')
    elif lookahead.startswith('A'):
        match('A')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['~', ',', ']', 'x', 'A']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_R()
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