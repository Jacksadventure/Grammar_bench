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

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('9'):
        match('9')
        match('x')
        while pos < len(tokens) and tokens[pos].startswith('D'):
            match('D')
            parse_P()
            parse_A()
            parse_P()
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('9'):
            match('9')
            match('x')
            parse_A()
            parse_H()
            parse_H()
        elif lookahead.startswith('o'):
            match('o')
            parse_L()
        elif lookahead.startswith('5'):
            match('5')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['9', 'o', '5']))
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('9'):
            match('9')
            match('x')
            parse_A()
            parse_H()
            parse_H()
        elif lookahead.startswith('o'):
            match('o')
            parse_L()
        elif lookahead.startswith('5'):
            match('5')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['9', 'o', '5']))
    elif lookahead.startswith('o'):
        match('o')
        if pos >= len(tokens):
            error("Unexpected end of input in L")
        lookahead = tokens[pos]
        if lookahead.startswith('%'):
            match('%')
        elif lookahead.startswith("'"):
            match("'")
            parse_K()
            parse_K()
            parse_K()
            parse_L()
        elif lookahead.startswith('Z'):
            match('Z')
            parse_P()
            match('G')
            parse_P()
            parse_Q()
        else:
            error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['%', "'", 'Z']))
    elif lookahead.startswith('5'):
        match('5')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['9', 'o', '5']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('u'):
        match('u')
    elif lookahead.startswith("'"):
        match("'")
        parse_Q()
        parse_H()
    elif lookahead.startswith('P'):
        parse_P()
        match('r')
        match('.')
        parse_Q()
    elif lookahead.startswith("'"):
        match("'")
        parse_K()
        parse_H()
        match('6')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['u', "'", 'P', "'"]))

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('o'):
        match('o')

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('i'):
        match('i')
        match('Z')

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('%'):
        match('%')
    elif lookahead.startswith("'"):
        match("'")
        parse_K()
        parse_K()
        parse_K()
        parse_L()
    elif lookahead.startswith('Z'):
        match('Z')
        parse_P()
        match('G')
        parse_P()
        parse_Q()
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['%', "'", 'Z']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_H()
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