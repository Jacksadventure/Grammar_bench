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

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('G'):
        match('G')
        while pos < len(tokens) and tokens[pos].startswith('='):
            match('=')
            match('{')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('v'):
            match('v')
            parse_Z()
            parse_O()
            parse_O()
            parse_E()
        elif lookahead.startswith('h'):
            match('h')
            parse_N()
            match('s')
            parse_V()
            parse_P()
        elif lookahead.startswith('u'):
            match('u')
            parse_R()
        elif lookahead.startswith('4'):
            match('4')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['v', 'h', 'u', '4']))
    elif lookahead.startswith('4'):
        match('4')
    elif lookahead.startswith('C'):
        match('C')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('u'):
            match('u')
            parse_N()
            match('j')
            match('I')
        elif lookahead.startswith('|'):
            match('|')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['u', '|']))
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('['):
            match('[')
            parse_H()
            parse_T()
        elif lookahead.startswith('W'):
            parse_W()
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['[', 'W']))
        while pos < len(tokens) and tokens[pos].startswith('('):
            match('(')
            match('8')
            match('G')
            parse_T()
    elif lookahead.startswith('{'):
        match('{')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['G', '4', 'C', '{']))

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('='):
        match('=')
        match('{')

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('0'):
        match('0')
        match('K')
        match('x')
        match('&')

def parse_Z():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('>'):
        match('>')
        parse_E()
        match('l')
        parse_E()

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('I'):
        match('I')
        match('3')
        match('Y')
        match('{')

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('u'):
        match('u')
        parse_N()
        match('j')
        match('I')
    elif lookahead.startswith('|'):
        match('|')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['u', '|']))

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('('):
        match('(')
        match('8')
        match('G')
        parse_T()

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('r'):
        match('r')
        match('~')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['r', '']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('['):
        match('[')
        parse_H()
        parse_T()
    elif lookahead.startswith('W'):
        parse_W()
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['[', 'W']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('v'):
        match('v')
        parse_Z()
        parse_O()
        parse_O()
        parse_E()
    elif lookahead.startswith('h'):
        match('h')
        parse_N()
        match('s')
        parse_V()
        parse_P()
    elif lookahead.startswith('u'):
        match('u')
        parse_R()
    elif lookahead.startswith('4'):
        match('4')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['v', 'h', 'u', '4']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_W()
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