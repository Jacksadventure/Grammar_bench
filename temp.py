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
    while pos < len(tokens) and tokens[pos] == 'Z':
        match('Z')
        match("'")
        match('0')
        parse_<e>()

def parse_<b>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <b>")
    lookahead = tokens[pos]
    if lookahead == '-':
        parse_<y>()
        parse_<d>()
        parse_<l>()
        match('<l>')
    elif lookahead == '1':
        match('1')
    elif lookahead == '~':
        parse_<j>()
        match('?')
    elif lookahead == 'Z':
        parse_<q>()
        match('<q>')
    elif lookahead == ')':
        match('N')
    elif lookahead == '"':
        parse_<y>()
        parse_<m>()
        match('<m>')
    elif lookahead == "'":
        parse_<t>()
        parse_<i>()
        parse_<n>()
        parse_<n>()
        parse_<b>()
        match('#')
    elif lookahead == '<u>':
        parse_<u>()
        parse_<e>()
        match('<e>')
    elif lookahead == 'K':
        parse_<y>()
        parse_<m>()
        parse_<a>()
        parse_<m>()
        match("'")
    elif lookahead == '?':
        parse_<k>()
        match('<k>')
    elif lookahead == '<y>':
        parse_<y>()
        parse_<p>()
        match('M')
    elif lookahead == 'Y':
        parse_<n>()
        parse_<p>()
        match('<p>')
    elif lookahead == '6':
        parse_<e>()
        parse_<o>()
        parse_<o>()
        parse_<u>()
        parse_<a>()
        parse_<m>()
        match('<m>')
    elif lookahead == '#':
        parse_<u>()
        match('+')
    elif lookahead == '+':
        parse_<b>()
        parse_<k>()
        match('<k>')
    else:
        error("Unexpected token " + lookahead + " in <b>, expected one of: " + ", ".join(['-', '1', '~', 'Z', ')', '"', "'", '<u>', 'K', '?', '<y>', 'Y', '6', '#', '+', '']))

def parse_<c>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '~':
        match('~')
        parse_<c>()
        match('-')
        parse_<y>()
        match('@')
        match('Y')
        match('z')
        match('S')
        match("'")

def parse_<d>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '?':
        match('?')
        match(')')
        parse_<t>()
        match('-')
        match('?')
        match("'")
        match('z')
        match('z')
        parse_<i>()

def parse_<e>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <e>")
    lookahead = tokens[pos]
    if lookahead == 'M':
        parse_<m>()
        match('"')
    elif lookahead == '<':
        parse_<e>()
        match('Z')
    elif lookahead == '#':
        match('#')
    elif lookahead == '?':
        parse_<a>()
        match('<a>')
    elif lookahead == '-':
        parse_<a>()
        match('<a>')
    elif lookahead == '+':
        match('+')
    elif lookahead == 'N':
        match('N')
    elif lookahead == '<m>':
        parse_<m>()
        match('0')
    elif lookahead == '<u>':
        parse_<u>()
        match('<')
    elif lookahead == 'K':
        match('K')
    elif lookahead == '@':
        parse_<m>()
        parse_<o>()
        parse_<n>()
        match('?')
    elif lookahead == '<e>':
        parse_<e>()
        match('M')
    elif lookahead == 'S':
        match('@')
    else:
        error("Unexpected token " + lookahead + " in <e>, expected one of: " + ", ".join(['M', '<', '#', '?', '-', '+', 'N', '<m>', '<u>', 'K', '@', '<e>', 'S', '']))

def parse_<f>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <f>")
    lookahead = tokens[pos]
    if lookahead == '<m>':
        parse_<m>()
        parse_<y>()
        parse_<m>()
        parse_<e>()
        match('<e>')
    elif lookahead == 'M':
        match('M')
    elif lookahead == '0':
        parse_<o>()
        match('?')
    elif lookahead == '@':
        parse_<g>()
        parse_<o>()
        match('"')
    else:
        error("Unexpected token " + lookahead + " in <f>, expected one of: " + ", ".join(['<m>', 'M', '0', '@']))

def parse_<g>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <g>")
    lookahead = tokens[pos]
    if lookahead == '?':
        parse_<y>()
        parse_<k>()
        match('<k>')
    elif lookahead == 'Y':
        parse_<v>()
        parse_<p>()
        match('6')
    elif lookahead == '@':
        match(',')
    elif lookahead == '1':
        parse_<g>()
        match('"')
    elif lookahead == '<e>':
        parse_<e>()
        parse_<v>()
        parse_<e>()
        parse_<e>()
        parse_<t>()
        parse_<x>()
        match('z')
    elif lookahead == 'M':
        parse_<m>()
        parse_<i>()
        parse_<y>()
        match('"')
    elif lookahead == '0':
        parse_<y>()
        parse_<m>()
        match(')')
    elif lookahead == '#':
        parse_<u>()
        parse_<e>()
        parse_<a>()
        parse_<j>()
        match('z')
    elif lookahead == '<y>':
        parse_<y>()
        parse_<m>()
        parse_<k>()
        match('1')
    elif lookahead == '<m>':
        parse_<m>()
        parse_<i>()
        match('<i>')
    elif lookahead == '-':
        parse_<e>()
        parse_<y>()
        match('<y>')
    elif lookahead == "'":
        parse_<r>()
        match('<r>')
    elif lookahead == '6':
        parse_<j>()
        match('<j>')
    else:
        error("Unexpected token " + lookahead + " in <g>, expected one of: " + ", ".join(['?', 'Y', '@', '1', '<e>', 'M', '0', '#', '<y>', '<m>', '-', "'", '6', '']))

def parse_<h>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <h>")
    lookahead = tokens[pos]
    if lookahead == 'S':
        parse_<m>()
        match('K')
    elif lookahead == 'M':
        parse_<h>()
        parse_<f>()
        parse_<y>()
        parse_<p>()
        parse_<s>()
        match('6')
    elif lookahead == 'N':
        match('z')
    elif lookahead == '-':
        parse_<y>()
        parse_<h>()
        match('+')
    elif lookahead == '1':
        parse_<m>()
        match('z')
    elif lookahead == '0':
        parse_<a>()
        parse_<i>()
        parse_<i>()
        match('<i>')
    else:
        error("Unexpected token " + lookahead + " in <h>, expected one of: " + ", ".join(['S', 'M', 'N', '-', '1', '0', '']))

def parse_<i>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'S':
        match('S')
        match('<')
        match('+')
        match('"')
        match('M')

def parse_<j>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <j>")
    lookahead = tokens[pos]
    if lookahead == 'N':
        parse_<m>()
        parse_<u>()
        parse_<s>()
        parse_<l>()
        parse_<k>()
        match('<k>')
    elif lookahead == '<e>':
        parse_<e>()
        parse_<h>()
        parse_<m>()
        match(',')
    elif lookahead == '@':
        parse_<b>()
        match('<b>')
    elif lookahead == 'Y':
        parse_<u>()
        parse_<u>()
        match('<u>')
    elif lookahead == "'":
        parse_<l>()
        parse_<j>()
        parse_<k>()
        match('<k>')
    elif lookahead == ',':
        match(',')
    elif lookahead == 'M':
        parse_<v>()
        parse_<y>()
        match('<y>')
    else:
        error("Unexpected token " + lookahead + " in <j>, expected one of: " + ", ".join(['N', '<e>', '@', 'Y', "'", ',', 'M', '']))

def parse_<k>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '?':
        match('?')
        match('M')
        match("'")

def parse_<l>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '1':
        match('1')
        match('~')
        match(',')
        match(')')
        parse_<y>()
        parse_<m>()

def parse_<m>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <m>")
    lookahead = tokens[pos]
    if lookahead == 'N':
        match('N')
    elif lookahead == 'z':
        parse_<y>()
        parse_<m>()
        parse_<i>()
        match('S')
    else:
        error("Unexpected token " + lookahead + " in <m>, expected one of: " + ", ".join(['N', 'z', '']))

def parse_<n>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '+':
        match('+')
        match('N')
        match('"')

def parse_<o>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <o>")
    lookahead = tokens[pos]
    if lookahead == '?':
        parse_<x>()
        parse_<h>()
        parse_<u>()
        parse_<w>()
        match('<w>')
    elif lookahead == 'z':
        parse_<e>()
        match('<e>')
    elif lookahead == 'N':
        parse_<p>()
        parse_<v>()
        match('<v>')
    else:
        error("Unexpected token " + lookahead + " in <o>, expected one of: " + ", ".join(['?', 'z', 'N']))

def parse_<p>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '<e>':
        parse_<e>()
        match('-')
        parse_<e>()
        match('+')
        match('6')
        match('#')
        match(')')
        match('S')

def parse_<q>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '-':
        match('-')
        parse_<h>()
        parse_<w>()
        match('#')

def parse_<r>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'Y':
        match('Y')
        match('K')
        match('@')
        parse_<f>()
        match('"')
        match('Z')
        match('Y')
        match('K')

def parse_<s>():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in <s>")
    lookahead = tokens[pos]
    if lookahead == 'Y':
        match('0')
    elif lookahead == '<e>':
        parse_<e>()
        parse_<m>()
        parse_<j>()
        parse_<r>()
        parse_<s>()
        parse_<x>()
        parse_<h>()
        match('S')
    elif lookahead == '1':
        parse_<p>()
        parse_<q>()
        match('N')
    elif lookahead == ',':
        match('z')
    elif lookahead == '6':
        parse_<s>()
        parse_<i>()
        match('#')
    elif lookahead == '0':
        match('0')
    elif lookahead == '~':
        parse_<l>()
        parse_<r>()
        match('<r>')
    elif lookahead == '?':
        parse_<x>()
        parse_<a>()
        parse_<y>()
        match('<y>')
    elif lookahead == '"':
        parse_<u>()
        match(',')
    elif lookahead == "'":
        parse_<d>()
        parse_<a>()
        parse_<m>()
        parse_<r>()
        match('<r>')
    elif lookahead == 'S':
        parse_<d>()
        parse_<o>()
        match("'")
    elif lookahead == 'z':
        parse_<g>()
        parse_<x>()
        parse_<h>()
        match('<h>')
    elif lookahead == '<m>':
        parse_<m>()
        match('<m>')
    elif lookahead == 'N':
        parse_<d>()
        match(',')
    else:
        error("Unexpected token " + lookahead + " in <s>, expected one of: " + ", ".join(['Y', '<e>', '1', ',', '6', '0', '~', '?', '"', "'", 'S', 'z', '<m>', 'N', '']))

def parse_<t>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '?':
        match('?')
        match('z')
        match(',')

def parse_<u>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == ')':
        match(')')
        match(')')
        match('z')
        match('#')
        match('1')

def parse_<v>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == 'M':
        match('M')
        parse_<r>()
        match(',')
        match('Z')
        match('K')
        parse_<h>()
        match('-')
        match('S')
        match('?')
        match('-')

def parse_<w>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '?':
        match('?')
        match('0')
        match('M')

def parse_<x>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '<m>':
        parse_<m>()
        match('S')

def parse_<y>():
    global pos, tokens
    while pos < len(tokens) and tokens[pos] == '<u>':
        parse_<u>()
        parse_<u>()
        match(',')
        parse_<h>()
        match('?')

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