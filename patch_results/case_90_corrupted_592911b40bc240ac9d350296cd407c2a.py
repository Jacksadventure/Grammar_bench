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

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('>'):
        match('>')
        if pos >= len(tokens):
            error("Unexpected end of input in F")
        lookahead = tokens[pos]
        if lookahead.startswith('['):
            match('[')
            parse_S()
            match('0')
            match('G')
        elif lookahead.startswith('z'):
            match('z')
            match('%')
            match('>')
            parse_F()
            parse_A()
        elif lookahead.startswith('{'):
            match('{')
            match('V')
        elif lookahead.startswith('s'):
            match('s')
            parse_S()
            parse_S()
            match('%')
            match('$')
        elif lookahead.startswith('M'):
            match('M')
            match('Z')
            match('O')
            parse_E()
        elif lookahead.startswith('A'):
            parse_A()
            parse_F()
        else:
            error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['[', 'z', '{', 's', 'M', 'A']))
        match('C')
        match('&')
    elif lookahead.startswith('l'):
        match('l')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['>', 'l']))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in F")
    lookahead = tokens[pos]
    if lookahead.startswith('['):
        match('[')
        parse_S()
        match('0')
        match('G')
    elif lookahead.startswith('z'):
        match('z')
        match('%')
        match('>')
        parse_F()
        parse_A()
    elif lookahead.startswith('{'):
        match('{')
        match('V')
    elif lookahead.startswith('s'):
        match('s')
        parse_S()
        parse_S()
        match('%')
        match('$')
    elif lookahead.startswith('M'):
        match('M')
        match('Z')
        match('O')
        parse_E()
    elif lookahead.startswith('A'):
        parse_A()
        parse_F()
    else:
        error("Unexpected token " + lookahead + " in F, expected one of: " + ", ".join(['[', 'z', '{', 's', 'M', 'A']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('c'):
        match('c')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['c']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('B'):
        parse_B()
        match('1')
        match(';')
        parse_F()
        match("'")
    elif lookahead.startswith('h'):
        match('h')
        match('%')
        match('$')
        match("'")
        match('.')
    elif lookahead.startswith("'"):
        match("'")
    elif lookahead.startswith('~'):
        match('~')
        parse_B()
        match("'")
        match('Z')
        match('I')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['B', 'h', "'", '~']))

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('A'):
        parse_A()
        match('}')
    elif lookahead.startswith('O'):
        match('O')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: " + ", ".join(['A', 'O']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_B()
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