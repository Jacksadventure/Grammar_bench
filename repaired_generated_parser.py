import sys
tokens = []
pos = 0

def error(msg):
    print('Parse error:', msg)
    sys.exit(1)

def match(expected):
    global pos, tokens
    if pos < len(tokens) and tokens[pos] == expected:
        pos += 1
    else:
        error('Expected ' + expected + ', got ' + (tokens[pos] if pos < len(tokens) else 'EOF'))

def parse_A():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'd':
        match('d')
        parse_A()
        parse_C()

def parse_B():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'c':
        match('c')
        parse_E()

def parse_C():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'b':
        match('b')

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        return
    lookahead = tokens[pos]
    if lookahead == 'a':
        match('a')
        match('e')
        parse_D()
    elif lookahead == 'e':
        match('e')
        parse_D()
    else:
        error('Unexpected token ' + lookahead + ' in D, expected one of: ' + ', '.join(['a', 'e']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in E')
    lookahead = tokens[pos]
    if lookahead == 'a':
        match('a')
    elif lookahead == 'b':
        match('b')
        parse_D()
        parse_A()
    else:
        error('Unexpected token ' + lookahead + ' in E, expected one of: ' + ', '.join(['a', 'b']))

def parse_input(input_str):
    global tokens, pos
    tokens = list(input_str)
    pos = 0
    parse_A()
    if pos != len(tokens):
        error('Extra tokens after parsing: ' + ' '.join(tokens[pos:]))
    print('Input accepted.')

def main():
    import sys
    if len(sys.argv) > 1:
        input_str = sys.argv[1]
        parse_input(input_str)
if __name__ == '__main__':
    main()