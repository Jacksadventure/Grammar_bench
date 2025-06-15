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

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('!'):
        match('!')
        match('#')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('!'):
            match('!')
            match('#')
            parse_A()
            parse_A()
        elif lookahead.startswith('9'):
            match('9')
            parse_L()
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['!', '', '9']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('@'):
        match('@')
        match('t')
        parse_T()
        match('Z')
        match('/')
    elif lookahead.startswith('('):
        match('(')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['@', '(']))

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith(')'):
        match(')')
        parse_B()
        parse_L()
        parse_R()
        match('&')

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('Y'):
        match('Y')
        match('%')
        match('8')
        match('e')

def parse_L():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('!'):
        match('!')
        parse_R()

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('<'):
        match('<')
        match('v')
        parse_E()
        parse_T()
        parse_Q()
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['<', 'd']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        parse_T()
    elif lookahead.startswith('G'):
        match('G')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(["'", 'G']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_A()
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