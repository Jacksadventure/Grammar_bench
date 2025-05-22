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
    if lookahead == 'f':
        parse_<b>()
        parse_<b>()
        match('<b>')
    elif lookahead == 'y':
        match('y')
    elif lookahead == 'O':
        parse_<c>()
        match('<c>')
    else:
        error("Unexpected token " + lookahead + " in <a>, expected one of: " + ", ".join(['f', 'y', 'O']))

def parse_<b>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <b>")
    lookahead = tokens[pos]
    if lookahead == 'O':
        match('y')
    elif lookahead == 'y':
        match('O')
    elif lookahead == 'f':
        match('f')
    else:
        error("Unexpected token " + lookahead + " in <b>, expected one of: " + ", ".join(['O', 'y', 'f']))

def parse_<c>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <c>")
    lookahead = tokens[pos]
    if lookahead == 'y':
        parse_<a>()
        match('f')
    elif lookahead == 'O':
        match('O')
    else:
        error("Unexpected token " + lookahead + " in <c>, expected one of: " + ", ".join(['y', 'O']))

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