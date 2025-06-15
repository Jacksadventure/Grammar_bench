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
    if lookahead.startswith('d'):
        match('d')
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('j'):
            match('j')
            parse_O()
            match('B')
            match('A')
            match('U')
        elif lookahead.startswith('e'):
            match('e')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['j', 'e']))
        if pos >= len(tokens):
            error("Unexpected end of input in I")
        lookahead = tokens[pos]
        if lookahead.startswith('j'):
            match('j')
            parse_O()
            match('B')
            match('A')
            match('U')
        elif lookahead.startswith('e'):
            match('e')
        else:
            error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['j', 'e']))
    elif lookahead.startswith('o'):
        match('o')
        match('|')
    elif lookahead.startswith('i'):
        match('i')
        match('m')
        match('g')
        match('i')
        match('%')
    elif lookahead.startswith('p'):
        match('p')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['d', 'o', 'i', 'p']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('6'):
        match('6')
    elif lookahead.startswith('j'):
        match('j')
        match('?')
        match('9')
        parse_S()
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['6', 'j']))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('j'):
        match('j')
        parse_O()
        match('B')
        match('A')
        match('U')
    elif lookahead.startswith('e'):
        match('e')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['j', 'e']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('O'):
        parse_O()
        parse_O()
        match(',')
        match('Q')
    elif lookahead.startswith('_'):
        match('_')
        match('[')
        match('{')
    elif lookahead.startswith(','):
        match(',')
        match('U')
        parse_O()
        parse_I()
    elif lookahead.startswith('E'):
        match('E')
        match('J')
        match('|')
        match('1')
    elif lookahead.startswith('m'):
        match('m')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['O', '_', ',', 'E', 'm']))

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