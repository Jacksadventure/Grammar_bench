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

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('['):
        match('[')
        match('c')
        match('8')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('q'):
            match('q')
            parse_G()
        elif lookahead.startswith("'"):
            match("'")
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['q', "'"]))
    elif lookahead.startswith('/'):
        match('/')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('g'):
            match('g')
            match('U')
            parse_B()
            parse_A()
        elif lookahead.startswith('!'):
            match('!')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['g', '!']))
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('['):
            match('[')
            match('c')
            match('8')
            parse_J()
        elif lookahead.startswith('/'):
            match('/')
            parse_T()
            parse_N()
            match('u')
            parse_N()
        elif lookahead.startswith('3'):
            match('3')
            match('9')
            match(',')
            parse_B()
        elif lookahead.startswith('8'):
            match('8')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['[', '/', '3', '8']))
        match('u')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('['):
            match('[')
            match('c')
            match('8')
            parse_J()
        elif lookahead.startswith('/'):
            match('/')
            parse_T()
            parse_N()
            match('u')
            parse_N()
        elif lookahead.startswith('3'):
            match('3')
            match('9')
            match(',')
            parse_B()
        elif lookahead.startswith('8'):
            match('8')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['[', '/', '3', '8']))
    elif lookahead.startswith('3'):
        match('3')
        match('9')
        match(',')
        while pos < len(tokens) and tokens[pos].startswith('y'):
            match('y')
            parse_C()
            parse_T()
    elif lookahead.startswith('8'):
        match('8')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['[', '/', '3', '8']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('8'):
        match('8')
        match('v')
    elif lookahead.startswith('m'):
        match('m')
        match("'")
        parse_G()
        parse_C()
        match('V')
    elif lookahead.startswith('!'):
        match('!')
        parse_T()
    elif lookahead.startswith('R'):
        match('R')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['8', 'm', '!', 'R']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('q'):
        match('q')
        parse_G()
    elif lookahead.startswith("'"):
        match("'")
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['q', "'"]))

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('y'):
        match('y')
        parse_C()
        parse_T()

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('>'):
        match('>')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['>']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('g'):
        match('g')
        match('U')
        parse_B()
        parse_A()
    elif lookahead.startswith('!'):
        match('!')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['g', '!']))

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('y'):
        match('y')
        parse_C()
        match('n')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_N()
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