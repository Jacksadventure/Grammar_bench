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
    if lookahead.startswith('i'):
        match('i')
        while pos < len(tokens) and tokens[pos].startswith('-'):
            match('-')
    elif lookahead.startswith('&'):
        match('&')
        while pos < len(tokens) and tokens[pos].startswith('&'):
            match('&')
            parse_F()
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('G'):
            parse_G()
            parse_W()
            parse_H()
            match('-')
            match("'")
        elif lookahead.startswith('?'):
            match('?')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['G', '?']))
        match('(')
    elif lookahead.startswith('Q'):
        match('Q')
        match('A')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('N'):
            match('N')
            parse_B()
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['N', '']))
        match("'")
        match('>')
    elif lookahead.startswith('!'):
        match('!')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['i', '&', 'Q', '!']))

def parse_W():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('^'):
        match('^')

def parse_G():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('-'):
        match('-')

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('&'):
        match('&')
        parse_F()

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('N'):
        match('N')
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['N', '']))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('M'):
        match('M')
        parse_U()
        parse_G()
        parse_D()

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('D'):
        parse_D()
        parse_F()
    elif lookahead.startswith('Q'):
        match('Q')
        parse_E()
        parse_W()
        match('@')
        parse_H()
    elif lookahead.startswith('H'):
        parse_H()
        match('+')
        parse_U()
    elif lookahead.startswith('s'):
        match('s')
        parse_H()
    elif lookahead.startswith('*'):
        match('*')
        parse_U()
        match('y')
    elif lookahead.startswith(']'):
        match(']')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['D', 'Q', 'H', 's', '*', ']']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('G'):
        parse_G()
        parse_W()
        parse_H()
        match('-')
        match("'")
    elif lookahead.startswith('?'):
        match('?')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['G', '?']))

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