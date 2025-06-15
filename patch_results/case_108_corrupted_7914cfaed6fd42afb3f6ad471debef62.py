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

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('#'):
        match('#')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('@'):
            match('@')
            match('%')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['@', '']))
    elif lookahead.startswith('g'):
        match('g')
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('1'):
            match('1')
        elif lookahead.startswith('f'):
            match('f')
        else:
            error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['1', 'f']))
    elif lookahead.startswith('f'):
        match('f')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith(']'):
            match(']')
            parse_W()
            parse_P()
            parse_J()
            match('7')
        elif lookahead.startswith('.'):
            match('.')
            parse_W()
            parse_W()
            parse_F()
            parse_P()
        elif lookahead.startswith('N'):
            match('N')
        elif lookahead.startswith('}'):
            match('}')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join([']', '.', 'N', '}']))
        match('E')
    elif lookahead.startswith("'"):
        match("'")
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('1'):
            match('1')
        elif lookahead.startswith('f'):
            match('f')
        else:
            error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['1', 'f']))
    elif lookahead.startswith('0'):
        match('0')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['#', 'g', 'f', "'", '0']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        parse_J()
        parse_F()
    elif lookahead.startswith('t'):
        match('t')
        parse_J()
        match('(')
        parse_F()
        match("'")
    elif lookahead.startswith('b'):
        match('b')
        match('y')
        parse_F()
        parse_J()
    elif lookahead.startswith('{'):
        match('{')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['o', 't', 'b', '{']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        match(']')
        parse_W()
        parse_P()
        parse_J()
        match('7')
    elif lookahead.startswith('.'):
        match('.')
        parse_W()
        parse_W()
        parse_F()
        parse_P()
    elif lookahead.startswith('N'):
        match('N')
    elif lookahead.startswith('}'):
        match('}')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join([']', '.', 'N', '}']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('@'):
        match('@')
        match('%')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['@', '']))

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('J'):
        parse_J()
        match('<')
        match('A')
        match('V')
        parse_H()

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('1'):
        match('1')
    elif lookahead.startswith('f'):
        match('f')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['1', 'f']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_C()
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