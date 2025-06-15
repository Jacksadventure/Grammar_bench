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

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in H")
    lookahead = tokens[pos]
    if lookahead.startswith('M'):
        match('M')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('9'):
            match('9')
            match('R')
            match('x')
            match('_')
            match('W')
        elif lookahead.startswith('&'):
            match('&')
            parse_Q()
        elif lookahead.startswith('V'):
            match('V')
            match('z')
        elif lookahead.startswith('8'):
            match('8')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['9', '&', 'V', '8']))
    elif lookahead.startswith('s'):
        match('s')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['M', 's']))

def parse_Q():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Q")
    lookahead = tokens[pos]
    if lookahead.startswith('R'):
        match('R')
        match(')')
    elif lookahead.startswith('8'):
        match('8')
        match(',')
        match('q')
        match('x')
        match('^')
    elif lookahead.startswith('A'):
        match('A')
        parse_H()
    elif lookahead.startswith('|'):
        match('|')
    else:
        error("Unexpected token " + lookahead + " in Q, expected one of: " + ", ".join(['R', '8', 'A', '|']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_H()
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