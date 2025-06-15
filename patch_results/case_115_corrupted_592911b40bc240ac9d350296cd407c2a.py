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

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('V'):
        match('V')
        match('%')
        match('+')
        match('#')
        match('V')
    elif lookahead.startswith('L'):
        match('L')
        if pos >= len(tokens):
            error("Unexpected end of input in C")
        lookahead = tokens[pos]
        if lookahead.startswith('s'):
            match('s')
        elif lookahead.startswith('q'):
            match('q')
            match('z')
            match('s')
            parse_Q()
            parse_Q()
        elif lookahead.startswith('}'):
            match('}')
            match("'")
            match('t')
        else:
            error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['s', 'q', '}']))
        match('u')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('<'):
            match('<')
            match('>')
            parse_O()
        elif lookahead.startswith('n'):
            match('n')
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['<', 'n']))
    elif lookahead.startswith('='):
        match('=')
    elif lookahead.startswith('W'):
        match('W')
        match('|')
        match('U')
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('z'):
            match('z')
            match('.')
        elif lookahead.startswith('j'):
            match('j')
        else:
            error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['z', 'j']))
        match('I')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['V', 'L', '=', 'W']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('6'):
        match('6')
        parse_O()
    elif lookahead.startswith(';'):
        match(';')
        match('K')
        match(')')
        match('s')
    elif lookahead.startswith('{'):
        match('{')
        match('>')
        match('[')
    elif lookahead.startswith('.'):
        match('.')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['6', ';', '{', '.']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('z'):
        match('z')
        parse_Q()
        match(':')
        match('<')
        match('4')
    elif lookahead.startswith('1'):
        match('1')
    elif lookahead.startswith('U'):
        match('U')
        parse_B()
        match('y')
        parse_Q()
        match('0')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['z', '1', 'U']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('#'):
        match('#')
        match(']')
        match('S')
    elif lookahead.startswith('?'):
        match('?')
        match('|')
        match('g')
        match('c')
    elif lookahead.startswith('F'):
        match('F')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['#', '?', 'F']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_T()
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