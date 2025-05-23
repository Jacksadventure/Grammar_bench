import sys

tokens = []
pos = 0

def error(msg):
    print("Parse error:", msg)
    sys.exit(1)

def match(expected):
    global pos, tokens
    # Accept prefixes: if no more tokens, consider match successful
    if pos >= len(tokens):
        return
    if tokens[pos].startswith(expected):
        pos += 1
    else:
        # Only error on true mismatch
        error("Expected " + expected + ", got " + tokens[pos])

def parse_a():
    global pos, tokens
    # If no more tokens, accept prefix and return
    if pos >= len(tokens):
        return
    lookahead = tokens[pos]
    if lookahead.startswith('y'):
        match('y')
        parse_b()
        parse_b()
        match('j')
        match('j')
        match('y')
        match('y')
    elif lookahead.startswith('y'):
        match('y')
    else:
        error("Unexpected token " + lookahead + " in a, expected one of: " + ", ".join(['y', 'y']))

def parse_b():
    global pos, tokens
    # If no more tokens, accept prefix and return
    if pos >= len(tokens):
        return
    lookahead = tokens[pos]
    if lookahead.startswith('y'):
        match('y')
        match('y')
        match('y')
        match('j')
        match('j')
        match('j')
    elif lookahead.startswith('j'):
        match('j')
    else:
        error("Unexpected token " + lookahead + " in b, expected one of: " + ", ".join(['y', 'j']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_a()
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