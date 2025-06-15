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

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        if pos >= len(tokens):
            error("Unexpected end of input in D")
        lookahead = tokens[pos]
        if lookahead.startswith('p'):
            match('p')
            match('}')
            match('}')
            parse_T()
        elif lookahead.startswith('/'):
            match('/')
            match('S')
            match('1')
            match('L')
        elif lookahead.startswith('Z'):
            match('Z')
            match('W')
        elif lookahead.startswith('7'):
            match('7')
        else:
            error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['p', '/', 'Z', '7']))
    elif lookahead.startswith('C'):
        match('C')
        match('a')
        match('`')
        match('n')
        match('6')
    elif lookahead.startswith('~'):
        match('~')
        match('r')
    elif lookahead.startswith('M'):
        match('M')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['o', 'C', '~', 'M']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('['):
        match('[')
        match('}')
        match('0')
        match('B')
    elif lookahead.startswith(']'):
        match(']')
        match('`')
        match('k')
        match("'")
        match('v')
    elif lookahead.startswith('v'):
        match('v')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['[', ']', 'v']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in D")
    lookahead = tokens[pos]
    if lookahead.startswith('p'):
        match('p')
        match('}')
        match('}')
        parse_T()
    elif lookahead.startswith('/'):
        match('/')
        match('S')
        match('1')
        match('L')
    elif lookahead.startswith('Z'):
        match('Z')
        match('W')
    elif lookahead.startswith('7'):
        match('7')
    else:
        error("Unexpected token " + lookahead + " in D, expected one of: " + ", ".join(['p', '/', 'Z', '7']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('s'):
        match('s')
        match(':')
        match('l')
        parse_D()
        parse_E()
    elif lookahead.startswith('_'):
        match('_')
        parse_T()
        parse_T()
        match('Q')
    elif lookahead.startswith('h'):
        match('h')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['s', '_', 'h']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_R()
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