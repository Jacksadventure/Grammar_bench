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

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('8'):
        match('8')
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('8'):
            match('8')
            parse_T()
            parse_T()
            parse_T()
            parse_T()
        elif lookahead.startswith('y'):
            match('y')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['8', 'y']))
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('8'):
            match('8')
            parse_T()
            parse_T()
            parse_T()
            parse_T()
        elif lookahead.startswith('y'):
            match('y')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['8', 'y']))
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('8'):
            match('8')
            parse_T()
            parse_T()
            parse_T()
            parse_T()
        elif lookahead.startswith('y'):
            match('y')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['8', 'y']))
        if pos >= len(tokens):
            error("Unexpected end of input in T")
        lookahead = tokens[pos]
        if lookahead.startswith('8'):
            match('8')
            parse_T()
            parse_T()
            parse_T()
            parse_T()
        elif lookahead.startswith('y'):
            match('y')
        else:
            error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['8', 'y']))
    elif lookahead.startswith('y'):
        match('y')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['8', 'y']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_T()
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