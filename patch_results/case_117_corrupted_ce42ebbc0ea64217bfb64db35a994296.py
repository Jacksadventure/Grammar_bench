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

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('{'):
        match('{')
        match('b')
        match('<')
        match('g')
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('Y'):
            match('Y')
            match('9')
            parse_W()
            match('s')
        elif lookahead.startswith('7'):
            match('7')
        elif lookahead.startswith('.'):
            match('.')
            match("'")
            match('7')
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['Y', '7', '.']))
    elif lookahead.startswith('J'):
        match('J')
        match('@')
        match('J')
        match('n')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('I'):
            match('I')
            parse_C()
            parse_H()
            parse_G()
            match('w')
        elif lookahead.startswith(';'):
            match(';')
            match('*')
        elif lookahead.startswith('&'):
            match('&')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['I', ';', '&']))
    elif lookahead.startswith('Z'):
        match('Z')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['{', 'J', 'Z']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('I'):
        match('I')
        parse_C()
        parse_H()
        parse_G()
        match('w')
    elif lookahead.startswith(';'):
        match(';')
        match('*')
    elif lookahead.startswith('&'):
        match('&')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['I', ';', '&']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('t'):
        match('t')
        parse_C()
        match('`')
        match('d')
        parse_K()
    elif lookahead.startswith('5'):
        match('5')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['t', '5']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('{'):
        match('{')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['{']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('G'):
        parse_G()
        match('<')
        match('E')
        match('Y')
        parse_G()
    elif lookahead.startswith('9'):
        match('9')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['G', '9']))

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        match('y')
        match('t')
    elif lookahead.startswith('}'):
        match('}')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(["'", '}']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Q()
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