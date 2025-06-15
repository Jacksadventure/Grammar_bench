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
    if lookahead.startswith('L'):
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith('m'):
            match('m')
            parse_E()
        elif lookahead.startswith('I'):
            match('I')
            match('N')
            match('0')
            match('R')
        elif lookahead.startswith(';'):
            match(';')
            match('K')
            parse_L()
            match('7')
        elif lookahead.startswith('*'):
            match('*')
        elif lookahead.startswith('/'):
            match('/')
            parse_L()
            parse_L()
            parse_U()
            match('4')
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['m', 'I', ';', '*', '/']))
        match('.')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('Z'):
            match('Z')
            match('^')
            match('g')
            match('v')
        elif lookahead.startswith('p'):
            match('p')
            parse_A()
            parse_A()
            parse_U()
        elif lookahead.startswith('{'):
            match('{')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['Z', 'p', '{']))
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith(','):
            match(',')
            match(',')
            match('w')
            match('7')
        elif lookahead.startswith('5'):
            match('5')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join([',', '5']))
    elif lookahead.startswith('u'):
        match('u')
        match('+')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('.'):
            match('.')
            match('q')
            match('q')
            match('V')
        elif lookahead.startswith('K'):
            match('K')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['.', 'K']))
    elif lookahead.startswith(','):
        match(',')
        match("'")
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith('m'):
            match('m')
            parse_E()
        elif lookahead.startswith('I'):
            match('I')
            match('N')
            match('0')
            match('R')
        elif lookahead.startswith(';'):
            match(';')
            match('K')
            parse_L()
            match('7')
        elif lookahead.startswith('*'):
            match('*')
        elif lookahead.startswith('/'):
            match('/')
            parse_L()
            parse_L()
            parse_U()
            match('4')
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['m', 'I', ';', '*', '/']))
        match('<')
        match('m')
    elif lookahead.startswith('}'):
        match('}')
        match('h')
        match('9')
        match('m')
        match('M')
    elif lookahead.startswith('9'):
        match('9')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['L', 'u', ',', '}', '9']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('.'):
        match('.')
        match('q')
        match('q')
        match('V')
    elif lookahead.startswith('K'):
        match('K')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['.', 'K']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('m'):
        match('m')
        parse_E()
    elif lookahead.startswith('I'):
        match('I')
        match('N')
        match('0')
        match('R')
    elif lookahead.startswith(';'):
        match(';')
        match('K')
        parse_L()
        match('7')
    elif lookahead.startswith('*'):
        match('*')
    elif lookahead.startswith('/'):
        match('/')
        parse_L()
        parse_L()
        parse_U()
        match('4')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['m', 'I', ';', '*', '/']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('Z'):
        match('Z')
        match('^')
        match('g')
        match('v')
    elif lookahead.startswith('p'):
        match('p')
        parse_A()
        parse_A()
        parse_U()
    elif lookahead.startswith('{'):
        match('{')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['Z', 'p', '{']))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        match(',')
        match('w')
        match('7')
    elif lookahead.startswith('5'):
        match('5')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join([',', '5']))

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