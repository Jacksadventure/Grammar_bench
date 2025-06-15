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

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('?'):
        match('?')
        match('h')
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('?'):
            match('?')
            match('h')
            parse_P()
            match('W')
            parse_P()
        elif lookahead.startswith('d'):
            match('d')
            parse_C()
            parse_J()
        else:
            error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['?', '', 'd']))
        match('W')

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('x'):
        match('x')
        match('G')

def parse_J():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('k'):
        match('k')
        match('!')
        match('[')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_P()
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