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

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('K'):
        match('K')
        while pos < len(tokens) and tokens[pos].startswith('j'):
            match('j')
            parse_F()
            parse_P()
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('K'):
            match('K')
            parse_O()
            parse_F()
        elif lookahead.startswith('c'):
            match('c')
            parse_H()
        elif lookahead.startswith('f'):
            match('f')
            parse_O()
            parse_F()
            parse_O()
        elif lookahead.startswith('s'):
            match('s')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['K', 'c', 'f', 's']))
    elif lookahead.startswith('c'):
        match('c')
        while pos < len(tokens) and tokens[pos].startswith('A'):
            match('A')
            parse_O()
            parse_P()
    elif lookahead.startswith('f'):
        match('f')
        while pos < len(tokens) and tokens[pos].startswith('j'):
            match('j')
            parse_F()
            parse_P()
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('K'):
            match('K')
            parse_O()
            parse_F()
        elif lookahead.startswith('c'):
            match('c')
            parse_H()
        elif lookahead.startswith('f'):
            match('f')
            parse_O()
            parse_F()
            parse_O()
        elif lookahead.startswith('s'):
            match('s')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['K', 'c', 'f', 's']))
        while pos < len(tokens) and tokens[pos].startswith('j'):
            match('j')
            parse_F()
            parse_P()
    elif lookahead.startswith('s'):
        match('s')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['K', 'c', 'f', 's']))

def parse_P():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('b'):
        match('b')
        parse_F()
        match('6')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['b', '']))

def parse_H():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('A'):
        match('A')
        parse_O()
        parse_P()

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('j'):
        match('j')
        parse_F()
        parse_P()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_F()
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