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

def parse_W():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in W")
    lookahead = tokens[pos]
    if lookahead.startswith('?'):
        match('?')
        if pos >= len(tokens):
            error("Unexpected end of input in Q")
        lookahead = tokens[pos]
        if lookahead.startswith('%'):
            match('%')
            parse_W()
            match('|')
        elif lookahead.startswith('C'):
            match('C')
        else:
            error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['%', 'C']))
    elif lookahead.startswith('8'):
        match('8')
        match('j')
        match("'")
    elif lookahead.startswith('('):
        match('(')
    else:
        error("Unexpected token " + lookahead + " in W, expected one of: " + ", ".join(['?', '8', '(']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_W()
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