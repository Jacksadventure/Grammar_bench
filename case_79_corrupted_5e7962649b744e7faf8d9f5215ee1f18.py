import sys

tokens = []
pos = 0

def error(msg):
    print("Parse error:", msg)
    sys.exit(1)

def match(expected):
    global pos, tokens
    if pos < len(tokens) and tokens[pos] == expected:
        pos += 1
    else:
        error("Expected " + expected + ", got " + (tokens[pos] if pos < len(tokens) else "EOF"))

def parse_<a>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <a>")
    lookahead = tokens[pos]
    if lookahead == '7':
        parse_<a>()
        parse_<c>()
        parse_<a>()
        match('7')
    else:
        error("Unexpected token " + lookahead + " in <a>, expected one of: " + ", ".join(['7', '']))

def parse_<b>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '7':
        match('7')
        match('w')
        match('w')
        parse_<b>()
        match('6')
        match('6')
        parse_<c>()
        parse_<c>()
        match('6')

def parse_<c>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <c>")
    lookahead = tokens[pos]
    if lookahead == '6':
        parse_<b>()
        match('6')
    elif lookahead == '7':
        match('w')
    else:
        error("Unexpected token " + lookahead + " in <c>, expected one of: " + ", ".join(['6', '7']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_<a>()
    if pos != len(tokens):
        error("Extra tokens after parsing: " + " ".join(tokens[pos:]))
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