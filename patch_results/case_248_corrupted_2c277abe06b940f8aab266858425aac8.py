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

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('>'):
        match('>')
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('}'):
            match('}')
            parse_D()
            parse_P()
            parse_V()
            parse_M()
        elif lookahead.startswith('M'):
            parse_M()
            match('o')
        elif lookahead.startswith('7'):
            match('7')
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['}', 'M', '7']))

def parse_D():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('B'):
        match('B')
        parse_R()
        parse_V()

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('W'):
        match('W')
        parse_P()
        parse_M()
        match('.')
        parse_Z()

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('J'):
        match('J')
        parse_Z()
        parse_Z()

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('}'):
        match('}')
        parse_D()
        parse_P()
        parse_V()
        parse_M()
    elif lookahead.startswith('M'):
        parse_M()
        match('o')
    elif lookahead.startswith('7'):
        match('7')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['}', 'M', '7']))

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('<'):
        match('<')
        parse_L()
        parse_M()
        parse_Q()
        match('0')

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('t'):
        match('t')
        parse_D()
        match('v')
        parse_M()
        parse_V()

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('l'):
        match('l')
        parse_S()
        parse_L()
        parse_S()
        parse_Z()

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        match('|')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['o', '']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_R()
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