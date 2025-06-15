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

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('p'):
        match('p')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('p'):
            match('p')
            parse_J()
        elif lookahead.startswith("'"):
            match("'")
            match('j')
            match('&')
            parse_Z()
        elif lookahead.startswith('3'):
            match('3')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['p', "'", '3']))
    elif lookahead.startswith("'"):
        match("'")
        match('j')
        match('&')
        if pos >= len(tokens):
            error("Unexpected end of input in Z")
        lookahead = tokens[pos]
        if lookahead.startswith('r'):
            match('r')
            match('^')
            match('{')
            match('b')
            match('|')
            match('<')
        else:
            error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['r', '']))
    elif lookahead.startswith('3'):
        match('3')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['p', "'", '3']))

def parse_Z():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Z")
    lookahead = tokens[pos]
    if lookahead.startswith('r'):
        match('r')
        match('^')
        match('{')
        match('b')
        match('|')
        match('<')
    else:
        error("Unexpected token " + lookahead + " in Z, expected one of: " + ", ".join(['r', '']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_J()
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