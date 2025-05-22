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
    if lookahead == 'h':
        parse_<b>()
        parse_<a>()
        match('0')
    elif lookahead == 'h':
        parse_<c>()
        match('0')
    elif lookahead == '5':
        match('0')
    else:
        error("Unexpected token " + lookahead + " in <a>, expected one of: " + ", ".join(['h', 'h', '5', '']))

def parse_<b>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '0':
        match('0')
        parse_<c>()
        parse_<b>()
        match('5')
        match('h')

def parse_<c>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <c>")
    lookahead = tokens[pos]
    if lookahead == 'h':
        parse_<a>()
        match('<a>')
    elif lookahead == '5':
        parse_<b>()
        parse_<b>()
        parse_<a>()
        parse_<a>()
        match('<a>')
    else:
        error("Unexpected token " + lookahead + " in <c>, expected one of: " + ", ".join(['h', '5']))

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