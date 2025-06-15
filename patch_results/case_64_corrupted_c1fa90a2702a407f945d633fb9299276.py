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
    if lookahead.startswith('l'):
        match('l')
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith('c'):
            match('c')
            match('/')
            match("'")
            match('G')
            parse_R()
        elif lookahead.startswith('b'):
            match('b')
            match('f')
            match('v')
            parse_E()
        elif lookahead.startswith('+'):
            match('+')
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['c', 'b', '+']))
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('l'):
            match('l')
            match('e')
            parse_F()
            match('J')
            match('V')
        elif lookahead.startswith('M'):
            match('M')
            match('_')
            parse_L()
        elif lookahead.startswith('j'):
            match('j')
        elif lookahead.startswith('S'):
            match('S')
            match('9')
            match('s')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['l', 'M', 'j', 'S']))
    elif lookahead.startswith('z'):
        match('z')
    elif lookahead.startswith('|'):
        match('|')
        match('|')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('l'):
            match('l')
            parse_L()
            parse_F()
        elif lookahead.startswith('z'):
            match('z')
        elif lookahead.startswith('|'):
            match('|')
            match('|')
            parse_E()
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['l', 'z', '|']))
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['l', 'z', '|']))

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('c'):
        match('c')
        match('/')
        match("'")
        match('G')
        parse_R()
    elif lookahead.startswith('b'):
        match('b')
        match('f')
        match('v')
        parse_E()
    elif lookahead.startswith('+'):
        match('+')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['c', 'b', '+']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('l'):
        match('l')
        match('e')
        parse_F()
        match('J')
        match('V')
    elif lookahead.startswith('M'):
        match('M')
        match('_')
        parse_L()
    elif lookahead.startswith('j'):
        match('j')
    elif lookahead.startswith('S'):
        match('S')
        match('9')
        match('s')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['l', 'M', 'j', 'S']))

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        match('H')
        match('=')
        parse_E()
    elif lookahead.startswith('F'):
        parse_F()
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(["'", 'F']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_E()
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