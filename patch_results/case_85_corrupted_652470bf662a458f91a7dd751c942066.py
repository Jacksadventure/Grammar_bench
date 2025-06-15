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

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('#'):
        match('#')
        while pos < len(tokens) and tokens[pos].startswith('b'):
            match('b')
            match('8')
            match('.')
            match('b')
    elif lookahead.startswith('T'):
        while pos < len(tokens) and tokens[pos].startswith('b'):
            match('b')
            match('8')
            match('.')
            match('b')
        while pos < len(tokens) and tokens[pos].startswith('b'):
            match('b')
            match('8')
            match('.')
            match('b')
    elif lookahead.startswith('9'):
        match('9')
        if pos >= len(tokens):
            error("Unexpected end of input in N")
        lookahead = tokens[pos]
        if lookahead.startswith('#'):
            match('#')
            parse_T()
        elif lookahead.startswith('T'):
            parse_T()
            parse_T()
        elif lookahead.startswith('9'):
            match('9')
            parse_N()
            parse_F()
        elif lookahead.startswith('5'):
            match('5')
            parse_T()
            parse_O()
            parse_T()
        elif lookahead.startswith('e'):
            match('e')
        else:
            error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['#', 'T', '9', '5', 'e']))
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('|'):
            match('|')
            match('j')
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['|', '']))
    elif lookahead.startswith('5'):
        match('5')
        while pos < len(tokens) and tokens[pos].startswith('b'):
            match('b')
            match('8')
            match('.')
            match('b')
        while pos < len(tokens) and tokens[pos].startswith('+'):
            match('+')
            parse_F()
            parse_F()
            match('d')
        while pos < len(tokens) and tokens[pos].startswith('b'):
            match('b')
            match('8')
            match('.')
            match('b')
    elif lookahead.startswith('e'):
        match('e')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['#', 'T', '9', '5', 'e']))

def parse_T():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('b'):
        match('b')
        match('8')
        match('.')
        match('b')

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('+'):
        match('+')
        parse_F()
        parse_F()
        match('d')

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('|'):
        match('|')
        match('j')
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['|', '']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_N()
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