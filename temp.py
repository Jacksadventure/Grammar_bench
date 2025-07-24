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
    # α* loop for <A>
    while pos < len(tokens) and (tokens[pos] == ','):
        match(',')
    # other alts of <A>
    if pos < len(tokens):
        la = tokens[pos]
        if la == 's':
            match('s')
            # α* loop for <B>
            while pos < len(tokens) and (tokens[pos] == ']'):
                match(']')
            # other alts of <B>
            if pos < len(tokens):
                la = tokens[pos]
                if la == 'Z':
                    match('Z')
                    # α* loop for <D>
                    while pos < len(tokens) and (tokens[pos] == '6'):
                        match('6')
                        match(')')
                    # other alts of <D>
                    if pos < len(tokens):
                        la = tokens[pos]
                        if la == '=':
                            match('=')
                            # standard alts for <J>
                            if pos >= len(tokens):
                                raise ParseError('Unexpected EOF in <J>')
                            else:
                                la = tokens[pos]
                                if la == 'K':
                                    match('K')
                                else:
                                    raise ParseError(f'Unexpected token {la!r} in <J>')
                        elif la == 'c':
                            match('c')
                        elif True:  # ε
                            pass
                elif True:  # ε
                    pass
            # α* loop for <C>
            while pos < len(tokens) and (tokens[pos] == 'N'):
                match('N')
                match('j')
            # other alts of <C>
            if pos < len(tokens):
                la = tokens[pos]
                if la == 'k':
                    match('k')
                    # standard alts for <E>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <E>')
                    else:
                        la = tokens[pos]
                        if la == '9':
                            match('9')
                            match('?')
                            match('O')
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <E>')
                elif la == 'r':
                    match('r')
                    # standard alts for <F>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <F>')
                    else:
                        la = tokens[pos]
                        if la == '-':
                            match('-')
                        elif la == 't':
                            match('t')
                            match('i')
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <F>')
                    # standard alts for <G>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <G>')
                    else:
                        la = tokens[pos]
                        if la == 'h':
                            match('h')
                        elif la == '4':
                            match('4')
                            match('n')
                            match('8')
                        elif la == 'v':
                            match('v')
                            match('$')
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <G>')
                elif la == '+':
                    match('+')
                    # α* loop for <H>
                    while pos < len(tokens) and (tokens[pos] == '#'):
                        match('#')
                    # other alts of <H>
                    if pos < len(tokens):
                        la = tokens[pos]
                        if la == 'z':
                            match('z')
                            match('U')
                        elif True:  # ε
                            pass
                    # α* loop for <I>
                    while pos < len(tokens) and (tokens[pos] == '7'):
                        match('7')
                        match('*')
                    # other alts of <I>
                    if pos < len(tokens):
                        la = tokens[pos]
                        if la == 'x':
                            match('x')
                            match('%')
                        elif True:  # ε
                            pass
                elif True:  # ε
                    pass
        elif True:  # ε
            pass
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