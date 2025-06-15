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
    if lookahead.startswith('c'):
        match('c')
        while pos < len(tokens) and tokens[pos].startswith('#'):
            match('#')
            match('m')
            match('3')
            match('L')
            match('P')
        match('3')
        while pos < len(tokens) and tokens[pos].startswith('F'):
            match('F')
            match('s')
            match('`')
        match('|')
    elif lookahead.startswith('['):
        match('[')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['c', '[']))

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