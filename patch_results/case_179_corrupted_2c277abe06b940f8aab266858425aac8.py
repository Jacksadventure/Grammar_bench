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

def parse_M():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('2'):
        match('2')
        match('?')
        match('}')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('v'):
            match('v')
            match('J')
            match('b')
            parse_E()
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['v', '']))

def parse_N():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in N")
    lookahead = tokens[pos]
    if lookahead.startswith('o'):
        match('o')
        parse_M()
        parse_N()
    elif lookahead.startswith('*'):
        match('*')
    elif lookahead.startswith('b'):
        match('b')
        parse_E()
        match('#')
    else:
        error("Unexpected token " + lookahead + " in N, expected one of: " + ", ".join(['o', '*', 'b']))

def parse_E():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('v'):
        match('v')
        match('J')
        match('b')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_M()
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