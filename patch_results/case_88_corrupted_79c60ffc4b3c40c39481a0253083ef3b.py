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

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith("'"):
        match("'")
        match('@')
        if pos >= len(tokens):
            error("Unexpected end of input in H")
        lookahead = tokens[pos]
        if lookahead.startswith('h'):
            match('h')
        elif lookahead.startswith('O'):
            parse_O()
            match('D')
            match('g')
        elif lookahead.startswith('.'):
            match('.')
        elif lookahead.startswith('b'):
            match('b')
        else:
            error("Unexpected token " + lookahead + " in H, expected one of: " + ", ".join(['h', 'O', '.', 'b']))
        if pos >= len(tokens):
            error("Unexpected end of input in R")
        lookahead = tokens[pos]
        if lookahead.startswith('n'):
            match('n')
            parse_I()
            match('*')
            match('e')
            match('{')
        elif lookahead.startswith(')'):
            match(')')
            parse_I()
            match('#')
            match('z')
        elif lookahead.startswith('}'):
            match('}')
        else:
            error("Unexpected token " + lookahead + " in R, expected one of: " + ", ".join(['n', ')', '}']))
        while pos < len(tokens) and tokens[pos].startswith('?'):
            match('?')
            parse_J()
            match('@')
    elif lookahead.startswith('r'):
        match('r')
        match('P')
        match('(')
    elif lookahead.startswith('?'):
        match('?')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(["'", 'r', '?']))

def parse_O():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('?'):
        match('?')
        parse_J()
        match('@')

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in I")
    lookahead = tokens[pos]
    if lookahead.startswith('p'):
        match('p')
        match('n')
    elif lookahead.startswith('>'):
        match('>')
        match('?')
        match('}')
    elif lookahead.startswith('g'):
        match('g')
    else:
        error("Unexpected token " + lookahead + " in I, expected one of: " + ", ".join(['p', '>', 'g']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_J()
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