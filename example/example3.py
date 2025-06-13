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

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
    elif lookahead.startswith('_'):
        match('_')
        match('9')
        while pos < len(tokens) and tokens[pos].startswith('('):
            match('(')
            match('S')
            match('Y')
        match('M')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: '+', '_'")

def parse_input(input_str):
    global pos, tokens
    tokens = list(input_str)
    pos = 0
    parse_Z()
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