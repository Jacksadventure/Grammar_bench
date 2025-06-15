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

def parse_R():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in R")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith("'"):
            match("'")
            parse_R()
            parse_V()
            parse_R()
        elif lookahead.startswith(','):
            match(',')
            match('T')
        elif lookahead.startswith('-'):
            match('-')
            match('7')
            parse_R()
            parse_M()
            parse_M()
        elif lookahead.startswith('A'):
            match('A')
            parse_S()
            parse_M()
        elif lookahead.startswith('&'):
            match('&')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(["'", ',', '-', 'A', '&']))
        if pos >= len(tokens):
            error("Unexpected end of input in V")
        lookahead = tokens[pos]
        if lookahead.startswith(','):
            match(',')
        elif lookahead.startswith('W'):
            match('W')
            parse_S()
            parse_V()
        elif lookahead.startswith('G'):
            match('G')
            parse_V()
            parse_R()
        elif lookahead.startswith('P'):
            match('P')
        else:
            error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join([',', 'W', 'G', 'P']))
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith("'"):
            match("'")
            parse_R()
            parse_V()
            parse_R()
        elif lookahead.startswith(','):
            match(',')
            match('T')
        elif lookahead.startswith('-'):
            match('-')
            match('7')
            parse_R()
            parse_M()
            parse_M()
        elif lookahead.startswith('A'):
            match('A')
            parse_S()
            parse_M()
        elif lookahead.startswith('&'):
            match('&')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(["'", ',', '-', 'A', '&']))
    elif lookahead.startswith(','):
        match(',')
        match('T')
    elif lookahead.startswith('-'):
        match('-')
        match('7')
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith("'"):
            match("'")
            parse_R()
            parse_V()
            parse_R()
        elif lookahead.startswith(','):
            match(',')
            match('T')
        elif lookahead.startswith('-'):
            match('-')
            match('7')
            parse_R()
            parse_M()
            parse_M()
        elif lookahead.startswith('A'):
            match('A')
            parse_S()
            parse_M()
        elif lookahead.startswith('&'):
            match('&')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(["'", ',', '-', 'A', '&']))
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('@'):
            match('@')
            parse_V()
            parse_R()
        elif lookahead.startswith('}'):
            match('}')
            parse_M()
        elif lookahead.startswith('4'):
            match('4')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['@', '}', '4']))
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('@'):
            match('@')
            parse_V()
            parse_R()
        elif lookahead.startswith('}'):
            match('}')
            parse_M()
        elif lookahead.startswith('4'):
            match('4')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['@', '}', '4']))
    elif lookahead.startswith('A'):
        match('A')
        while pos < len(tokens) and tokens[pos].startswith('v'):
            match('v')
            parse_M()
        if pos >= len(tokens):
            error("Unexpected end of input in M")
        lookahead = tokens[pos]
        if lookahead.startswith('@'):
            match('@')
            parse_V()
            parse_R()
        elif lookahead.startswith('}'):
            match('}')
            parse_M()
        elif lookahead.startswith('4'):
            match('4')
        else:
            error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['@', '}', '4']))
    elif lookahead.startswith('&'):
        match('&')
    else:
        error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(["'", ',', '-', 'A', '&']))

def parse_M():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in M")
    lookahead = tokens[pos]
    if lookahead.startswith('@'):
        match('@')
        parse_V()
        parse_R()
    elif lookahead.startswith('}'):
        match('}')
        parse_M()
    elif lookahead.startswith('4'):
        match('4')
    else:
        error("Unexpected token " + lookahead + " in M, expected one of: " + ", ".join(['@', '}', '4']))

def parse_S():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('v'):
        match('v')
        parse_M()

def parse_V():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in V")
    lookahead = tokens[pos]
    if lookahead.startswith(','):
        match(',')
    elif lookahead.startswith('W'):
        match('W')
        parse_S()
        parse_V()
    elif lookahead.startswith('G'):
        match('G')
        parse_V()
        parse_R()
    elif lookahead.startswith('P'):
        match('P')
    else:
        error("Unexpected token " + lookahead + " in V, expected one of: " + ", ".join([',', 'W', 'G', 'P']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_R()
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