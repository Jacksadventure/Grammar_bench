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
    if lookahead == '{':
        parse_<b>()
        match('<b>')
    elif lookahead == 'y':
        match('{')
    else:
        error("Unexpected token " + lookahead + " in <a>, expected one of: " + ", ".join(['{', 'y']))

def parse_<b>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <b>")
    lookahead = tokens[pos]
    if lookahead == 'y':
        parse_<a>()
        match('<a>')
    elif lookahead == '{':
        parse_<b>()
        match('y')
    else:
        error("Unexpected token " + lookahead + " in <b>, expected one of: " + ", ".join(['y', '{', '']))

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