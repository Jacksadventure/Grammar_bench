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
    # Standard rule set for <A>
    if pos >= len(tokens):
        raise ParseError('Unexpected EOF in <A>')
    else:
        la = tokens[pos]
        if la == 'p':
            match('p')
            # Standard rule set for <B>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF in <B>')
            else:
                la = tokens[pos]
                if la == 'o':
                    match('o')
                elif la == 'M':
                    match('M')
                    match('f')
                else:
                    raise ParseError(f'Unexpected token {la!r} in <B>')
            match('4')
        elif la == 'V':
            match('V')
        elif la == 's':
            match('s')
            # Iterative rule for <C> → ['N', '+', 'i']*
            while pos < len(tokens) and (tokens[pos] == 'N'):
                match('N')
                match('+')
                match('i')
        elif la == '4':
            match('4')
            # Standard rule set for <D>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF in <D>')
            else:
                la = tokens[pos]
                if la == 'x':
                    match('x')
                    # Standard rule set for <E>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <E>')
                    else:
                        la = tokens[pos]
                        if la == 'S':
                            match('S')
                            match('3')
                        elif la == '?':
                            match('?')
                        elif la == 'd':
                            match('d')
                            match('g')
                            match('=')
                            match('%')
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <E>')
                elif la == '*':
                    match('*')
                    match('~')
                    match('$')
                    match('-')
                else:
                    raise ParseError(f'Unexpected token {la!r} in <D>')
        else:
            raise ParseError(f'Unexpected token {la!r} in <A>')
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