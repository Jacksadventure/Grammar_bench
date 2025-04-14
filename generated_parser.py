import sys

# --- Token and Lexer Classes ---
class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({{self.type}}, {{self.value}})"

class Lexer:
    def __init__(self, token_rules):
        # token_rules is a list of tuples (token_type, pattern)
        # If the pattern ends with '+', we treat it as a repeat-match pattern
        self.token_rules = []
        for token_type, pattern in token_rules:
            if pattern.endswith('+'):
                # For repeat-match, store the literal and mark as 'repeat'
                self.token_rules.append((token_type, pattern[:-1], 'repeat'))
            else:
                # Exact match
                self.token_rules.append((token_type, pattern, 'exact'))

    def tokenize(self, text):
        pos = 0
        tokens = []
        while pos < len(text):
            # Skip whitespace
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
                else:  # match_type == 'repeat'
                    if text[pos] == literal:
                        start = pos
                        while pos < len(text) and text[pos] == literal:
                            pos += 1
                        tokens.append(Token(token_type, text[start:pos]))
                        match_found = True
                        break
            if not match_found:
                error("Lexer error: Unexpected character '{}' at position {}".format(text[pos], pos))
        return tokens

# --- Randomly Generated Token Rules ---
token_rules = [('a', 'a+'), ('b', 'b+'), ('c', 'c'), ('d', 'd'), ('e', 'e+'), ('f', 'f+'), ('g', 'g'), ('h', 'h'), ('i', 'i'), ('j', 'j')]
lexer = Lexer(token_rules)

# Global token list and position index
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
    if lookahead == "h":
        match("h")
        parse_G()
        parse_I()
    elif lookahead == "g":
        match("g")
        match("j")
    else:
        error("Unexpected token " + tokens[pos].value + " in A, expected one of: " + ", ".join(["h", "g"]))

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in B')
    lookahead = tokens[pos].type
    if lookahead == "c":
        match("c")
    elif lookahead == "b":
        match("b")
        parse_G()
    else:
        error("Unexpected token " + tokens[pos].value + " in B, expected one of: " + ", ".join(["c", "b"]))

def parse_C():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in C')
    lookahead = tokens[pos].type
    if lookahead == "b":
        match("b")
        parse_E()
    elif lookahead == "g":
        match("g")
        match("g")
        parse_D()
    else:
        error("Unexpected token " + tokens[pos].value + " in C, expected one of: " + ", ".join(["b", "g"]))

def parse_D():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in D')
    lookahead = tokens[pos].type
    if lookahead == "h":
        match("h")
        parse_B()
    elif lookahead == "e":
        match("e")
        match("e")
    elif lookahead == "b":
        match("b")
        parse_D()
    elif lookahead == "i":
        match("i")
    else:
        error("Unexpected token " + tokens[pos].value + " in D, expected one of: " + ", ".join(["h", "e", "b", "i"]))

def parse_E():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in E')
    lookahead = tokens[pos].type
    if lookahead == "i":
        match("i")
        parse_C()
    elif lookahead == "g":
        match("g")
    elif lookahead == "c":
        match("c")
    else:
        error("Unexpected token " + tokens[pos].value + " in E, expected one of: " + ", ".join(["i", "g", "c"]))

def parse_F():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in F')
    lookahead = tokens[pos].type
    if lookahead == "b":
        match("b")
        parse_J()
        parse_C()
    elif lookahead == "e":
        match("e")
    elif lookahead == "i":
        match("i")
        parse_D()
    elif lookahead == "d":
        match("d")
        match("d")
        match("f")
    else:
        error("Unexpected token " + tokens[pos].value + " in F, expected one of: " + ", ".join(["b", "e", "i", "d"]))

def parse_G():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in G')
    lookahead = tokens[pos].type
    if lookahead == "j":
        match("j")
    elif lookahead == "e":
        match("e")
        match("c")
        match("e")
    elif lookahead == "h":
        match("h")
        parse_H()
    elif lookahead == "i":
        match("i")
    else:
        error("Unexpected token " + tokens[pos].value + " in G, expected one of: " + ", ".join(["j", "e", "h", "i"]))

def parse_H():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in H')
    lookahead = tokens[pos].type
    if lookahead == "g":
        match("g")
    elif lookahead == "c":
        match("c")
        parse_F()
        parse_H()
    elif lookahead == "h":
        match("h")
        parse_A()
    elif lookahead == "e":
        match("e")
    elif lookahead == "d":
        match("d")
    else:
        error("Unexpected token " + tokens[pos].value + " in H, expected one of: " + ", ".join(["g", "c", "h", "e", "d"]))

def parse_I():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in I')
    lookahead = tokens[pos].type
    if lookahead == "i":
        match("i")
    elif lookahead == "h":
        match("h")
        parse_E()
    elif lookahead == "c":
        match("c")
        parse_H()
    elif lookahead == "e":
        match("e")
        parse_D()
    elif lookahead == "j":
        match("j")
    else:
        error("Unexpected token " + tokens[pos].value + " in I, expected one of: " + ", ".join(["i", "h", "c", "e", "j"]))

def parse_J():
    global pos, tokens
    if pos >= len(tokens):
        error('Unexpected end of input in J')
    lookahead = tokens[pos].type
    if lookahead == "h":
        match("h")
        match("f")
    elif lookahead == "g":
        match("g")
        match("e")
    elif lookahead == "d":
        match("d")
    else:
        error("Unexpected token " + tokens[pos].value + " in J, expected one of: " + ", ".join(["h", "g", "d"]))

def parse_input(input_str):
    global tokens, pos
    try:
        tokens = lexer.tokenize(input_str)
    except Exception as e:
        error(str(e))
    pos = 0
    parse_A()
    if pos != len(tokens):
        error('Extra tokens after parsing: ' + ' '.join(token.value for token in tokens[pos:]))
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