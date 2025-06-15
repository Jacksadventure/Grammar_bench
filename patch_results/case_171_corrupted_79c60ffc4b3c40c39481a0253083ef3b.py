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
    while pos < len(tokens) and tokens[pos].startswith('7'):
        match('7')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('R'):
            match('R')
            match('c')
            match('R')
            match('a')
            parse_V()
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['R', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('7'):
            match('7')
            parse_V()
            parse_O()
            match('b')
            parse_O()
        elif lookahead.startswith('A'):
            match('A')
            parse_I()
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['7', '', 'A']))
        match('b')

def parse_I():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('N'):
        match('N')
        parse_V()
        parse_I()
        parse_I()
        parse_O()

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('R'):
        match('R')
        match('c')
        match('R')
        match('a')

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