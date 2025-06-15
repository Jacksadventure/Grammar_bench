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

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('P'):
        match('P')
        match('!')
        while pos < len(tokens) and tokens[pos].startswith('L'):
            match('L')
            match('`')
            match('^')
            parse_K()
    elif lookahead.startswith('Q'):
        match('Q')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['P', 'Q']))

def parse_K():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('L'):
        match('L')
        match('`')
        match('^')
        parse_K()

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_I()
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