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

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('}'):
        match('}')
        match('~')
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith(','):
            match(',')
            match('d')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join([',', '']))
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('}'):
            match('}')
            match('~')
            parse_Y()
            parse_E()
            parse_Y()
        elif lookahead.startswith('A'):
            match('A')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['}', 'A']))
        if pos >= len(tokens):
            error("Unexpected end of input in Y")
        lookahead = tokens[pos]
        if lookahead.startswith(','):
            match(',')
            match('d')
        else:
            error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join([',', '']))
    elif lookahead.startswith('A'):
        match('A')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['}', 'A']))

def parse_Y():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in Y")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
        match('d')
    else:
        error("Unexpected token " + lookahead + " in Y, expected one of: " + ", ".join([',', '']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_E()
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