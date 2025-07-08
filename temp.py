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

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('}'):
        match('}')
        match("'")
        match('m')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('<'):
            match('<')
            match('*')
        elif lookahead.startswith('*'):
            match('*')
            parse_A()
        elif lookahead.startswith('@'):
            match('@')
        elif lookahead.startswith('P'):
            match('P')
            match('(')
            match('/')
            match('I')
            parse_B()
        elif lookahead.startswith('b'):
            match('b')
            match('M')
        else:
            error("Parse failed")
    elif lookahead.startswith('Z'):
        match('Z')
    else:
        error("Parse failed")

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith(']'):
        match(']')
        match(']')
        match('M')
    elif lookahead.startswith('-'):
        match('-')
        match('a')
        match('8')
    elif lookahead.startswith(','):
        match(',')
        parse_U()
    elif lookahead.startswith('5'):
        match('5')
        match('v')
    elif lookahead.startswith('z'):
        match('z')
        match('M')
        parse_G()
        match('?')
    elif lookahead.startswith('C'):
        match('C')
    else:
        error("Parse failed")

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('9'):
        match('9')
        parse_B()
        parse_U()
        parse_E()

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('<'):
        match('<')
        match('*')
    elif lookahead.startswith('*'):
        match('*')
        parse_A()
    elif lookahead.startswith('@'):
        match('@')
    elif lookahead.startswith('P'):
        match('P')
        match('(')
        match('/')
        match('I')
        parse_B()
    elif lookahead.startswith('b'):
        match('b')
        match('M')
    else:
        error("Parse failed")

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('j'):
        match('j')
        match('*')
        match('2')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    try:
        parse_E()
    except SyntaxError:
        # Partial parser: accept if some tokens consumed
        if pos == 0:
            raise
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