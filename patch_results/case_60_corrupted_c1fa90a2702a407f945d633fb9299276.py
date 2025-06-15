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

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('#'):
        match('#')
        match('8')
        match('v')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('x'):
            match('x')
        elif lookahead.startswith('@'):
            match('@')
        elif lookahead.startswith('W'):
            match('W')
            parse_I()
            parse_P()
            parse_P()
            match('_')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['x', '@', 'W']))
    elif lookahead.startswith('F'):
        match('F')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['#', 'F']))

def parse_P():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('.'):
        match('.')
        match('M')
        match('g')
        match('K')

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('x'):
        match('x')
    elif lookahead.startswith('@'):
        match('@')
    elif lookahead.startswith('W'):
        match('W')
        parse_I()
        parse_P()
        parse_P()
        match('_')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['x', '@', 'W']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_Q()
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