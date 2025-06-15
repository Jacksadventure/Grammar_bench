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

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        match('<')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('w'):
            match('w')
            match('<')
            parse_U()
        elif lookahead.startswith('Z'):
            match('Z')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['w', 'Z']))
    elif lookahead.startswith('Z'):
        match('Z')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['w', 'Z']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_U()
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