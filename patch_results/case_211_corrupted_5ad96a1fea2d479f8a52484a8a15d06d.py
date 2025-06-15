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
    while pos < len(tokens) and tokens[pos].startswith('l'):
        match('l')
        match('|')
        if pos >= len(tokens):
            error("Unexpected end of input in W")
        lookahead = tokens[pos]
        if lookahead.startswith('{'):
            match('{')
            parse_L()
            parse_G()
            match('{')
            parse_I()
        elif lookahead.startswith(']'):
            match(']')
            match("'")
        elif lookahead.startswith('<'):
            match('<')
            parse_B()
            parse_L()
        elif lookahead.startswith('e'):
            match('e')
            parse_G()
            match(':')
            match('(')
            match('8')
        elif lookahead.startswith('|'):
            match('|')
            parse_W()
            parse_B()
        elif lookahead.startswith('l'):
            match('l')
        else:
            error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['{', ']', '<', 'e', '|', 'l']))
        match('h')

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('q'):
        match('q')
        match('(')

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('!'):
        match('!')

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('%'):
        match('%')
        parse_G()
        match('U')

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith("'"):
        match("'")

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('{'):
        match('{')
        parse_L()
        parse_G()
        match('{')
        parse_I()
    elif lookahead.startswith(']'):
        match(']')
        match("'")
    elif lookahead.startswith('<'):
        match('<')
        parse_B()
        parse_L()
    elif lookahead.startswith('e'):
        match('e')
        parse_G()
        match(':')
        match('(')
        match('8')
    elif lookahead.startswith('|'):
        match('|')
        parse_W()
        parse_B()
    elif lookahead.startswith('l'):
        match('l')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['{', ']', '<', 'e', '|', 'l']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
    elif lookahead.startswith('6'):
        match('6')
        parse_C()
        parse_O()
    elif lookahead.startswith('?'):
        match('?')
        parse_T()
        parse_S()
        parse_W()
        match('.')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join([',', '6', '?']))

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('T'):
        parse_T()

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('^'):
        match('^')
        match('b')

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