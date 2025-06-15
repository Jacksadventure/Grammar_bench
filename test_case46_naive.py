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
    if lookahead.startswith('^'):
        match('^')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('T'):
            match('T')
            parse_S()
        elif lookahead.startswith('!'):
            match('!')
            match('U')
        elif lookahead.startswith('G'):
            match('G')
            match('M')
            match('=')
            parse_H()
            parse_H()
        elif lookahead.startswith('Y'):
            match('Y')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['T', '!', 'G', 'Y']))
    elif lookahead.startswith('T'):
        match('T')
        match('a')
        match('3')
    elif lookahead.startswith('`'):
        match('`')
    else:
        error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['^', 'T', '`']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('g'):
        match('g')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['g']))

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