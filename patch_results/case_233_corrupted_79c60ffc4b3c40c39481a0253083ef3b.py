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
    while pos < len(tokens) and tokens[pos].startswith('@'):
        match('@')
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith('a'):
            match('a')
            match('}')
            parse_V()
        elif lookahead.startswith(':'):
            match(':')
            parse_Y()
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join(['a', '', ':']))

def parse_V():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('a'):
        match('a')
        match('}')

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith('i'):
        match('i')
        match('|')
    elif lookahead.startswith('*'):
        match('*')
        match('-')
        match('D')
        parse_Y()
    elif lookahead.startswith('T'):
        match('T')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join(['i', '*', 'T']))

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