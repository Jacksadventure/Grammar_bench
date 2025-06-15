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

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('}'):
        match('}')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('^'):
            match('^')
            parse_B()
            parse_P()
            parse_B()
            parse_P()
        elif lookahead.startswith('J'):
            match('J')
            parse_U()
            parse_Z()
            parse_S()
            parse_H()
        elif lookahead.startswith('v'):
            match('v')
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['^', 'J', 'v']))
    elif lookahead.startswith('?'):
        match('?')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['}', '?']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('r'):
        match('r')
        parse_S()
        parse_U()
        parse_Z()
        parse_Z()
    elif lookahead.startswith(']'):
        match(']')
        match('(')
    elif lookahead.startswith('^'):
        match('^')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['r', ']', '^']))

def parse_U():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('q'):
        match('q')
        match("'")
        match('I')

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('#'):
        match('#')
        match('%')
        match('j')
        match('<')
        parse_P()
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['#', '']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('^'):
        match('^')
        parse_B()
        parse_P()
        parse_B()
        parse_P()
    elif lookahead.startswith('J'):
        match('J')
        parse_U()
        parse_Z()
        parse_S()
        parse_H()
    elif lookahead.startswith('v'):
        match('v')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['^', 'J', 'v']))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('q'):
        match('q')
        parse_B()
        match('{')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Z()
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