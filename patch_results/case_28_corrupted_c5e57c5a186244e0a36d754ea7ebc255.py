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

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('~'):
        match('~')
        if pos >= len(tokens):
            error("Unexpected end of input in G")
        lookahead = tokens[pos]
        if lookahead.startswith('y'):
            match('y')
            match('>')
            match('&')
            match('*')
        elif lookahead.startswith('6'):
            match('6')
        else:
            error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['y', '6']))
    elif lookahead.startswith('`'):
        match('`')
        match('c')
    elif lookahead.startswith('l'):
        match('l')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['~', '`', 'l']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_B()
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