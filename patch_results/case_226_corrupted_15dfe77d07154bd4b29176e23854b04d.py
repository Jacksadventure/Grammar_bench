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
    if lookahead.startswith("'"):
        match("'")
        match('z')
        match('n')
        match('Q')
    elif lookahead.startswith('C'):
        match('C')
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith('S'):
            parse_S()
            parse_S()
            match('k')
        elif lookahead.startswith('s'):
            match('s')
            match(']')
            parse_D()
            match('^')
        elif lookahead.startswith('R'):
            match('R')
        elif lookahead.startswith('6'):
            match('6')
            parse_S()
            match('`')
        else:
            error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['S', 's', 'R', '6']))
        if pos >= len(tokens):
            error("Unexpected end of input in X")
        lookahead = tokens[pos]
        if lookahead.startswith('>'):
            match('>')
            parse_O()
            parse_O()
        elif lookahead.startswith('M'):
            match('M')
        else:
            error("Unexpected token " + lookahead + " in X, expected one of: " + ", ".join(['>', 'M']))
        match('v')
    elif lookahead.startswith(')'):
        match(')')
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(["'", 'C', ')']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('S'):
        parse_S()
        parse_S()
        match('k')
    elif lookahead.startswith('s'):
        match('s')
        match(']')
        parse_D()
        match('^')
    elif lookahead.startswith('R'):
        match('R')
    elif lookahead.startswith('6'):
        match('6')
        parse_S()
        match('`')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['S', 's', 'R', '6']))

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('5'):
        match('5')
        parse_S()
        match("'")

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