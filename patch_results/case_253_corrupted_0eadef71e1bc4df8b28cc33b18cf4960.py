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

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('i'):
        match('i')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('w'):
            match('w')
            parse_F()
        elif lookahead.startswith('B'):
            match('B')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['w', 'B']))
    elif lookahead.startswith('T'):
        match('T')
    elif lookahead.startswith('8'):
        match('8')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['i', 'T', '8']))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        parse_F()
    elif lookahead.startswith('B'):
        match('B')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['w', 'B']))

def parse_R():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('-'):
        match('-')
        parse_M()
        match('9')
        parse_M()

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('z'):
        match('z')
        match('S')
        match('4')
        parse_R()
    elif lookahead.startswith('G'):
        match('G')
        parse_R()
        parse_H()
    elif lookahead.startswith('$'):
        match('$')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['z', 'G', '$']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        match('b')
    elif lookahead.startswith('X'):
        match('X')
    elif lookahead.startswith('a'):
        match('a')
        parse_M()
        parse_O()
        parse_O()
        match('w')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['o', 'X', 'a']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_O()
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