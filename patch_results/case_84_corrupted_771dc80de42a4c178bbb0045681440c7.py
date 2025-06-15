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

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('*'):
        match('*')
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('p'):
            match('p')
            parse_K()
        elif lookahead.startswith('l'):
            match('l')
            match('.')
            match('-')
        elif lookahead.startswith('p'):
            match('p')
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['p', 'l', 'p']))

def parse_K():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in K")
    lookahead = tokens[pos]
    if lookahead.startswith('C'):
        match('C')
        match('F')
    else:
        error("Unexpected token " + lookahead + " in K, expected one of: " + ", ".join(['C', '']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('}'):
        match('}')
    elif lookahead.startswith('x'):
        match('x')
        parse_B()
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['}', 'x']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_A()
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