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
    while pos < len(tokens) and tokens[pos].startswith('U'):
        match('U')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('i'):
            match('i')
            parse_T()
        elif lookahead.startswith('C'):
            match('C')
            parse_T()
        elif lookahead.startswith('#'):
            match('#')
            parse_R()
            parse_S()
            parse_J()
            match('!')
        elif lookahead.startswith('Z'):
            match('Z')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['i', 'C', '#', 'Z']))
        if pos >= len(tokens):
            error("Unexpected end of input in Q")
        lookahead = tokens[pos]
        if lookahead.startswith('k'):
            match('k')
            parse_T()
            parse_S()
            parse_Q()
        elif lookahead.startswith('7'):
            match('7')
            parse_T()
            parse_T()
        elif lookahead.startswith('d'):
            match('d')
        else:
            error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['k', '7', 'd']))
        match('O')

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('S'):
        parse_S()
        parse_R()
        parse_S()
        parse_I()

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('i'):
        match('i')
        parse_T()
    elif lookahead.startswith('C'):
        match('C')
        parse_T()
    elif lookahead.startswith('#'):
        match('#')
        parse_R()
        parse_S()
        parse_J()
        match('!')
    elif lookahead.startswith('Z'):
        match('Z')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['i', 'C', '#', 'Z']))

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('D'):
        match('D')

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('k'):
        match('k')
        parse_T()
        parse_S()
        parse_Q()
    elif lookahead.startswith('7'):
        match('7')
        parse_T()
        parse_T()
    elif lookahead.startswith('d'):
        match('d')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['k', '7', 'd']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('Y'):
        match('Y')
        parse_T()
        parse_T()
    elif lookahead.startswith('%'):
        match('%')
        match('K')
        parse_Q()
    elif lookahead.startswith('W'):
        match('W')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['Y', '%', 'W']))

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('-'):
        match('-')
        parse_T()
        parse_J()

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