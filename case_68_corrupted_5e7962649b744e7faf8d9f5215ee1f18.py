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
    while pos < len(tokens) and tokens[pos] == '^':
        match('^')
        parse_<a>()
        match('K')
        match('K')
        match('^')
        match('K')
        match('K')

def parse_<b>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <b>")
    lookahead = tokens[pos]
    if lookahead == '^':
        parse_<a>()
        parse_<a>()
        parse_<a>()
        match('<a>')
    elif lookahead == '<a>':
        parse_<a>()
        parse_<b>()
        parse_<a>()
        parse_<c>()
        parse_<a>()
        match('<a>')
    else:
        error("Unexpected token " + lookahead + " in <b>, expected one of: " + ", ".join(['^', '<a>', '']))

def parse_<c>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <c>")
    lookahead = tokens[pos]
    if lookahead == '^':
        match('K')
    elif lookahead == 'K':
        parse_<a>()
        parse_<c>()
        parse_<a>()
        match('<a>')
    elif lookahead == '<a>':
        parse_<a>()
        parse_<b>()
        parse_<a>()
        parse_<a>()
        parse_<a>()
        match('K')
    else:
        error("Unexpected token " + lookahead + " in <c>, expected one of: " + ", ".join(['^', 'K', '<a>', '']))

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