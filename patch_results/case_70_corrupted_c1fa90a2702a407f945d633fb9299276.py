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
    while pos < len(tokens) and tokens[pos].startswith('H'):
        match('H')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('z'):
            match('z')
            parse_B()
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['z', '']))
        match('w')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('.'):
            match('.')
            parse_O()
        elif lookahead.startswith('P'):
            match('P')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['.', 'P']))

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('z'):
        match('z')

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('&'):
        match('&')
        match('X')
        match('n')
        parse_O()

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