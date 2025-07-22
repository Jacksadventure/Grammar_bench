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
        got = tokens[pos] if pos < len(tokens) else "EOF"
        raise ParseError(f"Expected {expected!r}, got {got!r}")

def parse(inp):
    global tokens, pos
    tokens = list(inp.strip())
    pos = 0
    # Iterative rule for <A> → ['H']*
    while pos < len(tokens) and (tokens[pos] == 'H'):
        match('H')
    # After loop: choose the rest of <A>
    if pos < len(tokens):
        la = tokens[pos]
        if la == 'w':
            match('w')
            # Standard rule set for <B>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF in <B>')
            else:
                la = tokens[pos]
                if la == 'x':
                    match('x')
                else:
                    raise ParseError(f'Unexpected token {la!r} in <B>')
        elif True:  # ε
            pass
    if pos < len(tokens):
        raise ParseError(f"Extra input at end: {''.join(tokens[pos:])}")
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