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

def parse_L():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in L")
    lookahead = tokens[pos]
    if lookahead.startswith('q'):
        match('q')
        match('R')
    elif lookahead.startswith('M'):
        match('M')
        match('j')
        match('|')
        match('%')
        match('o')
    elif lookahead.startswith('!'):
        match('!')
        match('0')
        match("'")
    elif lookahead.startswith('D'):
        match('D')
        if pos >= len(tokens):
            error("Unexpected end of input in J")
        lookahead = tokens[pos]
        if lookahead.startswith('+'):
            match('+')
            match('v')
            match('_')
            parse_T()
        elif lookahead.startswith('s'):
            match('s')
            match('M')
            match('q')
            parse_E()
        elif lookahead.startswith('p'):
            match('p')
            match('n')
            parse_O()
            match('s')
            parse_E()
        elif lookahead.startswith('o'):
            match('o')
        else:
            error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['+', 's', 'p', 'o']))
        match('M')
        if pos >= len(tokens):
            error("Unexpected end of input in E")
        lookahead = tokens[pos]
        if lookahead.startswith('_'):
            match('_')
            match('i')
        elif lookahead.startswith('J'):
            parse_J()
        elif lookahead.startswith('`'):
            match('`')
            parse_A()
            match('>')
            match('R')
        elif lookahead.startswith(','):
            match(',')
            match('j')
            match(')')
            match('H')
            match(':')
        else:
            error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['_', 'J', '`', ',']))
        if pos >= len(tokens):
            error("Unexpected end of input in O")
        lookahead = tokens[pos]
        if lookahead.startswith('>'):
            match('>')
            parse_G()
            match('t')
            parse_B()
            parse_B()
        elif lookahead.startswith('w'):
            match('w')
        elif lookahead.startswith('='):
            match('=')
            parse_O()
            match('j')
            match('{')
            parse_E()
        elif lookahead.startswith(']'):
            match(']')
            parse_O()
        elif lookahead.startswith('W'):
            match('W')
            parse_U()
        else:
            error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['>', 'w', '=', ']', 'W']))
    elif lookahead.startswith('H'):
        match('H')
    else:
        error("Unexpected token " + lookahead + " in L, expected one of: " + ", ".join(['q', 'M', '!', 'D', 'H']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('['):
        match('[')
        parse_L()
        match('C')
    elif lookahead.startswith('$'):
        match('$')
        match('|')
        match('!')
    elif lookahead.startswith('A'):
        parse_A()
    elif lookahead.startswith('g'):
        match('g')
    elif lookahead.startswith('.'):
        match('.')
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: " + ", ".join(['[', '$', 'A', 'g', '.']))

def parse_O():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in O")
    lookahead = tokens[pos]
    if lookahead.startswith('>'):
        match('>')
        parse_G()
        match('t')
        parse_B()
        parse_B()
    elif lookahead.startswith('w'):
        match('w')
    elif lookahead.startswith('='):
        match('=')
        parse_O()
        match('j')
        match('{')
        parse_E()
    elif lookahead.startswith(']'):
        match(']')
        parse_O()
    elif lookahead.startswith('W'):
        match('W')
        parse_U()
    else:
        error("Unexpected token " + lookahead + " in O, expected one of: " + ", ".join(['>', 'w', '=', ']', 'W']))

def parse_T():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in T")
    lookahead = tokens[pos]
    if lookahead.startswith('<'):
        match('<')
        match('.')
    elif lookahead.startswith('7'):
        match('7')
    elif lookahead.startswith('Z'):
        match('Z')
        match('i')
        parse_J()
        match('Y')
    else:
        error("Unexpected token " + lookahead + " in T, expected one of: " + ", ".join(['<', '7', 'Z']))

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('B'):
        parse_B()
    elif lookahead.startswith(','):
        match(',')
        match('/')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: " + ", ".join(['B', ',']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in E")
    lookahead = tokens[pos]
    if lookahead.startswith('_'):
        match('_')
        match('i')
    elif lookahead.startswith('J'):
        parse_J()
    elif lookahead.startswith('`'):
        match('`')
        parse_A()
        match('>')
        match('R')
    elif lookahead.startswith(','):
        match(',')
        match('j')
        match(')')
        match('H')
        match(':')
    else:
        error("Unexpected token " + lookahead + " in E, expected one of: " + ", ".join(['_', 'J', '`', ',']))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('>'):
        match('>')
        match(',')
    elif lookahead.startswith('/'):
        match('/')
        match('Q')
        parse_A()
        match('Q')
    elif lookahead.startswith('k'):
        match('k')
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: " + ", ".join(['>', '/', 'k']))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in J")
    lookahead = tokens[pos]
    if lookahead.startswith('+'):
        match('+')
        match('v')
        match('_')
        parse_T()
    elif lookahead.startswith('s'):
        match('s')
        match('M')
        match('q')
        parse_E()
    elif lookahead.startswith('p'):
        match('p')
        match('n')
        parse_O()
        match('s')
        parse_E()
    elif lookahead.startswith('o'):
        match('o')
    else:
        error("Unexpected token " + lookahead + " in J, expected one of: " + ", ".join(['+', 's', 'p', 'o']))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in G")
    lookahead = tokens[pos]
    if lookahead.startswith('W'):
        match('W')
        match('_')
        match('0')
    elif lookahead.startswith('?'):
        match('?')
        match('W')
    elif lookahead.startswith('?'):
        match('?')
    else:
        error("Unexpected token " + lookahead + " in G, expected one of: " + ", ".join(['W', '?', '?']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_L()
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