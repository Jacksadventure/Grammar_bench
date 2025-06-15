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
    if lookahead.startswith('8'):
        match('8')
        while pos < len(tokens) and tokens[pos].startswith('4'):
            match('4')
        while pos < len(tokens) and tokens[pos].startswith('4'):
            match('4')
            match('d')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('}'):
            match('}')
            parse_Q()
        elif lookahead.startswith('U'):
            parse_U()
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['}', 'U']))
        while pos < len(tokens) and tokens[pos].startswith('4'):
            match('4')
    elif lookahead.startswith(']'):
        match(']')
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith('8'):
            match('8')
            parse_Q()
            parse_U()
            parse_A()
            parse_Q()
        elif lookahead.startswith(']'):
            match(']')
            parse_D()
        elif lookahead.startswith('m'):
            match('m')
            parse_D()
        elif lookahead.startswith('j'):
            match('j')
            parse_A()
            parse_A()
            parse_C()
            parse_D()
        elif lookahead.startswith('d'):
            match('d')
        else:
            error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['8', ']', 'm', 'j', 'd']))
    elif lookahead.startswith('m'):
        match('m')
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith('8'):
            match('8')
            parse_Q()
            parse_U()
            parse_A()
            parse_Q()
        elif lookahead.startswith(']'):
            match(']')
            parse_D()
        elif lookahead.startswith('m'):
            match('m')
            parse_D()
        elif lookahead.startswith('j'):
            match('j')
            parse_A()
            parse_A()
            parse_C()
            parse_D()
        elif lookahead.startswith('d'):
            match('d')
        else:
            error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['8', ']', 'm', 'j', 'd']))
    elif lookahead.startswith('j'):
        match('j')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('}'):
            match('}')
            parse_Q()
        elif lookahead.startswith('U'):
            parse_U()
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['}', 'U']))
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('}'):
            match('}')
            parse_Q()
        elif lookahead.startswith('U'):
            parse_U()
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['}', 'U']))
        if pos >= len(tokens):
            error("Unexpected end of input in C")
        lookahead = tokens[pos]
        if lookahead.startswith('l'):
            match('l')
            parse_D()
        elif lookahead.startswith(')'):
            match(')')
            parse_C()
            parse_U()
        elif lookahead.startswith('Q'):
            parse_Q()
            parse_C()
            parse_D()
            parse_D()
            parse_C()
        elif lookahead.startswith(';'):
            match(';')
            parse_B()
            parse_C()
            parse_D()
            parse_A()
        elif lookahead.startswith('5'):
            match('5')
        else:
            error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['l', ')', 'Q', ';', '5']))
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith('8'):
            match('8')
            parse_Q()
            parse_U()
            parse_A()
            parse_Q()
        elif lookahead.startswith(']'):
            match(']')
            parse_D()
        elif lookahead.startswith('m'):
            match('m')
            parse_D()
        elif lookahead.startswith('j'):
            match('j')
            parse_A()
            parse_A()
            parse_C()
            parse_D()
        elif lookahead.startswith('d'):
            match('d')
        else:
            error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['8', ']', 'm', 'j', 'd']))
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['8', ']', 'm', 'j', 'd']))

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('4'):
        match('4')
        match('d')

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in C")
    lookahead = tokens[pos]
    if lookahead.startswith('l'):
        match('l')
        parse_D()
    elif lookahead.startswith(')'):
        match(')')
        parse_C()
        parse_U()
    elif lookahead.startswith('Q'):
        parse_Q()
        parse_C()
        parse_D()
        parse_D()
        parse_C()
    elif lookahead.startswith(';'):
        match(';')
        parse_B()
        parse_C()
        parse_D()
        parse_A()
    elif lookahead.startswith('5'):
        match('5')
    else:
        error("Unexpected token " + lookahead + " in C, expected one of: " + ", ".join(['l', ')', 'Q', ';', '5']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('}'):
        match('}')
        parse_Q()
    elif lookahead.startswith('U'):
        parse_U()
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['}', 'U']))

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('X'):
        match('X')
        parse_U()

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('4'):
        match('4')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_D()
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