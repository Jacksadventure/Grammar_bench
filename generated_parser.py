import sys

tokens = []
pos = 0

class ParseError(Exception):
    pass

def match(expected):
    global pos
    if pos < len(tokens) and tokens[pos] == expected:
        pos += 1
    else:
        got = tokens[pos] if pos < len(tokens) else 'EOF'
        raise ParseError(f'Expected {expected!r}, got {got!r}')

def parse(inp):
    global tokens, pos
    tokens = list(inp.strip())
    pos = 0
    # standard alts for <A>
    if pos >= len(tokens):
        raise ParseError('Unexpected EOF in <A>')
    else:
        la = tokens[pos]
        if la == 'w':
            match('w')
            match('H')
            match('-')
        else:
            raise ParseError(f'Unexpected token {la!r} in <A>')
    if pos < len(tokens):
        raise ParseError(f'Extra input at end: {"".join(tokens[pos:])}')
    print("Input accepted.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python generated_parser.py <string>")
        sys.exit(1)
    try:
        parse(sys.argv[1])
    except ParseError as err:
        print("Input rejected.")
        print(err)