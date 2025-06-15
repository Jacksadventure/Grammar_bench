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
    if pos >= len(tokens):
        error("Unexpected end of input in P")
    lookahead = tokens[pos]
    if lookahead.startswith('u'):
        match('u')
        if pos >= len(tokens):
            error("Unexpected end of input in P")
        lookahead = tokens[pos]
        if lookahead.startswith('u'):
            match('u')
            parse_P()
            match('#')
            match('p')
            parse_S()
        elif lookahead.startswith(']'):
            match(']')
        else:
            error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['u', ']']))
        match('#')
        match('p')
        if pos >= len(tokens):
            error("Unexpected end of input in S")
        lookahead = tokens[pos]
        if lookahead.startswith('N'):
            match('N')
            parse_P()
        elif lookahead.startswith('7'):
            match('7')
            match('&')
            match('b')
            match('+')
        elif lookahead.startswith('B'):
            match('B')
        else:
            error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['N', '7', 'B']))
    elif lookahead.startswith(']'):
        match(']')
    else:
        error("Unexpected token " + lookahead + " in P, expected one of: " + ", ".join(['u', ']']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('N'):
        match('N')
        parse_P()
    elif lookahead.startswith('7'):
        match('7')
        match('&')
        match('b')
        match('+')
    elif lookahead.startswith('B'):
        match('B')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['N', '7', 'B']))

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