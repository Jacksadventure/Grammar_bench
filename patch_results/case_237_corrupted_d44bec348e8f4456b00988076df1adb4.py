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

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('3'):
        match('3')
        match('@')
        while pos < len(tokens) and tokens[pos].startswith('#'):
            match('#')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('3'):
            match('3')
            match('@')
            parse_F()
            parse_U()
            parse_U()
        elif lookahead.startswith('m'):
            match('m')
            parse_M()
            match('}')
            parse_U()
        elif lookahead.startswith('9'):
            match('9')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['3', 'm', '9']))
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('3'):
            match('3')
            match('@')
            parse_F()
            parse_U()
            parse_U()
        elif lookahead.startswith('m'):
            match('m')
            parse_M()
            match('}')
            parse_U()
        elif lookahead.startswith('9'):
            match('9')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['3', 'm', '9']))
    elif lookahead.startswith('m'):
        match('m')
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('Q'):
            match('Q')
            match('>')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['Q', '']))
        match('}')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('3'):
            match('3')
            match('@')
            parse_F()
            parse_U()
            parse_U()
        elif lookahead.startswith('m'):
            match('m')
            parse_M()
            match('}')
            parse_U()
        elif lookahead.startswith('9'):
            match('9')
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['3', 'm', '9']))
    elif lookahead.startswith('9'):
        match('9')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['3', 'm', '9']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('Q'):
        match('Q')
        match('>')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['Q', '']))

def parse_F():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('#'):
        match('#')

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_U()
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