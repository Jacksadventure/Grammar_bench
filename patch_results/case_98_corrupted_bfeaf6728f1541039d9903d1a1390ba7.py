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

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('k'):
        match('k')
        match('%')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('u'):
            match('u')
            parse_L()
            match('P')
        elif lookahead.startswith('I'):
            match('I')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['u', 'I']))
    elif lookahead.startswith('E'):
        match('E')
        match('E')
    elif lookahead.startswith('v'):
        match('v')
        match(')')
    elif lookahead.startswith('>'):
        match('>')
        if pos >= len(tokens):
            error("Unexpected end of input in K")
        lookahead = tokens[pos]
        if lookahead.startswith('1'):
            match('1')
            parse_K()
            match('&')
            match('+')
            parse_S()
        elif lookahead.startswith('d'):
            match('d')
        else:
            error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['1', 'd']))
        match('h')
        match('B')
    elif lookahead.startswith(','):
        match(',')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['k', 'E', 'v', '>', ',']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('r'):
        match('r')
        match('3')
        parse_L()
    elif lookahead.startswith('+'):
        match('+')
        parse_R()
        parse_L()
    elif lookahead.startswith('8'):
        match('8')
        match('[')
        match('d')
        match('-')
        parse_S()
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['r', '+', '8', 'd']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('1'):
        match('1')
        parse_K()
        match('&')
        match('+')
        parse_S()
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['1', 'd']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('u'):
        match('u')
        parse_L()
        match('P')
    elif lookahead.startswith('I'):
        match('I')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['u', 'I']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_L()
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