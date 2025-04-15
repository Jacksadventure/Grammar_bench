import sys

class Token:

    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f'Token({{self.type}}, {{self.value}})'

class Lexer:

    def __init__(self, token_rules):
        self.token_rules = []
        for token_type, pattern in token_rules:
            if pattern.endswith('+'):
                self.token_rules.append((token_type, pattern[:-1], 'repeat'))
            else:
                self.token_rules.append((token_type, pattern, 'exact'))

    def tokenize(self, text):
        pos = 0
        tokens = []
        while pos < len(text):
            if text[pos].isspace():
                pos += 1
                continue
            match_found = False
            for token_type, literal, match_type in self.token_rules:
                if match_type == 'exact':
                    if text.startswith(literal, pos):
                        tokens.append(Token(token_type, literal))
                        pos += len(literal)
                        match_found = True
                        break
                elif text[pos] == literal:
                    start = pos
                    while pos < len(text) and text[pos] == literal:
                        pos += 1
                    tokens.append(Token(token_type, text[start:pos]))
                    match_found = True
                    break
            if not match_found:
                error("Lexer error: Unexpected character '{}' at position {}".format(text[pos], pos))
        return tokens
token_rules = [('a', 'a+'), ('b', 'b+'), ('c', 'c'), ('d', 'd+'), ('e', 'e+')]
lexer = Lexer(token_rules)
tokens = []
pos = 0

def error(msg):
    print('Parse error:', msg)
    sys.exit(1)

def match(expected):
    global pos, tokens
    if pos < len(tokens) and tokens[pos].type == expected:
        pos += 1
    else:
        current = tokens[pos].value if pos < len(tokens) else 'EOF'
        error(f"Expected token type '{expected}', got {current}")

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in A')
    lookahead = tokens[pos].type
    if lookahead == 'e':
        match('e')
        parse_C()
        parse_E()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in A, expected one of: ' + ', '.join(['e']))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in B')
    lookahead = tokens[pos].type
    if lookahead == 'c':
        match('c')
        match('a')
        match('e')
    elif lookahead == 'e':
        match('e')
        match('d')
        parse_D()
    elif lookahead == 'b':
        match('b')
        parse_C()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in B, expected one of: ' + ', '.join(['c', 'e', 'b']))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in C')
    lookahead = tokens[pos].type
    if lookahead == 'c':
        match('c')
        match('b')
        match('e')
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'e':
        match('e')
        parse_A()
        match('d')
    elif lookahead == 'a':
        match('a')
        match('e')
        parse_C()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in C, expected one of: ' + ', '.join(['c', 'b', 'e', 'a']))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in D')
    lookahead = tokens[pos].type
    if lookahead == 'a':
        match('a')
        match('a')
    elif lookahead == 'b':
        match('b')
    elif lookahead == 'd':
        match('d')
    elif lookahead == 'c':
        match('c')
    elif lookahead == 'e':
        match('e')
        parse_B()
        parse_B()
    else:
        error('Unexpected token ' + tokens[pos].value + ' in D, expected one of: ' + ', '.join(['a', 'b', 'd', 'c', 'e']))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in E')
    lookahead = tokens[pos].type
    if lookahead == 'd':
        match('d')
        match('c')
    elif lookahead == 'c':
        match('c')
    else:
        error('Unexpected token ' + tokens[pos].value + ' in E, expected one of: ' + ', '.join(['d', 'c']))

def parse_input(input_str):
    global tokens, pos
    try:
        tokens = lexer.tokenize(input_str)
    except Exception as e:
        error(str(e))
    pos = 0
    parse_A()
    if pos != len(tokens):
        error('Extra tokens after parsing: ' + ' '.join((token.value for token in tokens[pos:])))
    print('Input accepted.')

def main():
    import sys
    if len(sys.argv) > 1:
        input_str = sys.argv[1]
        parse_input(input_str)
    else:
        print('Usage: python generated_parser.py <input_string>')
if __name__ == '__main__':
    main()