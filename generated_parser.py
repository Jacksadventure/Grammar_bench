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
        if la == '=':
            match('=')
            # Standard rule set for <B>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF in <B>')
            else:
                la = tokens[pos]
                if la == 'R':
                    match('R')
                    # Standard rule set for <D>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <D>')
                    else:
                        la = tokens[pos]
                        if la == 'k':
                            match('k')
                        elif la == '8':
                            match('8')
                            match('t')
                            # Standard rule set for <J>
                            if pos >= len(tokens):
                                raise ParseError('Unexpected EOF in <J>')
                            else:
                                la = tokens[pos]
                                if la == 'g':
                                    match('g')
                                    match('P')
                                    match('V')
                                    match('W')
                                elif la == 'h':
                                    match('h')
                                    match('6')
                                elif la == ']':
                                    match(']')
                                    match('q')
                                else:
                                    raise ParseError(f'Unexpected token {la!r} in <J>')
                            # Standard rule set for <K>
                            if pos >= len(tokens):
                                raise ParseError('Unexpected EOF in <K>')
                            else:
                                la = tokens[pos]
                                if la == '?':
                                    match('?')
                                else:
                                    raise ParseError(f'Unexpected token {la!r} in <K>')
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <D>')
                    match('U')
                elif la == 'e':
                    match('e')
                    # Standard rule set for <E>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <E>')
                    else:
                        la = tokens[pos]
                        if la == 'j':
                            match('j')
                            match('%')
                            match('d')
                        elif la == 'l':
                            match('l')
                            match('i')
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <E>')
                    match('}')
                elif la == 'f':
                    match('f')
                    # Standard rule set for <F>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <F>')
                    else:
                        la = tokens[pos]
                        if la == '!':
                            match('!')
                            match('4')
                            match('u')
                            match('i')
                        elif la == 'o':
                            match('o')
                            # Standard rule set for <L>
                            if pos >= len(tokens):
                                raise ParseError('Unexpected EOF in <L>')
                            else:
                                la = tokens[pos]
                                if la == '4':
                                    match('4')
                                    match('q')
                                elif la == '7':
                                    match('7')
                                    match('U')
                                else:
                                    raise ParseError(f'Unexpected token {la!r} in <L>')
                            # Standard rule set for <M>
                            if pos >= len(tokens):
                                raise ParseError('Unexpected EOF in <M>')
                            else:
                                la = tokens[pos]
                                if la == ',':
                                    match(',')
                                    match('P')
                                else:
                                    raise ParseError(f'Unexpected token {la!r} in <M>')
                        elif la == '`':
                            match('`')
                            match('&')
                            # Standard rule set for <N>
                            if pos >= len(tokens):
                                raise ParseError('Unexpected EOF in <N>')
                            else:
                                la = tokens[pos]
                                if la == '+':
                                    match('+')
                                    match('y')
                                    match('6')
                                    match(';')
                                else:
                                    raise ParseError(f'Unexpected token {la!r} in <N>')
                            # Standard rule set for <O>
                            if pos >= len(tokens):
                                raise ParseError('Unexpected EOF in <O>')
                            else:
                                la = tokens[pos]
                                if la == '5':
                                    match('5')
                                    match('P')
                                    match('[')
                                    match('P')
                                elif la == '0':
                                    match('0')
                                    match('z')
                                    match('z')
                                elif la == '}':
                                    match('}')
                                    match('Q')
                                    match('{')
                                    match('#')
                                else:
                                    raise ParseError(f'Unexpected token {la!r} in <O>')
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <F>')
                else:
                    raise ParseError(f'Unexpected token {la!r} in <B>')
            # Standard rule set for <C>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF in <C>')
            else:
                la = tokens[pos]
                if la == '9':
                    match('9')
                    # Standard rule set for <G>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <G>')
                    else:
                        la = tokens[pos]
                        if la == 'Z':
                            match('Z')
                            match('d')
                            match('q')
                            match('$')
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <G>')
                    # Standard rule set for <H>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <H>')
                    else:
                        la = tokens[pos]
                        if la == 'Y':
                            match('Y')
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <H>')
                elif la == '2':
                    match('2')
                    match('/')
                    # Standard rule set for <I>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <I>')
                    else:
                        la = tokens[pos]
                        if la == '-':
                            match('-')
                            match('#')
                            match('}')
                        elif la == 'p':
                            match('p')
                            match('.')
                            match('d')
                            match('w')
                        elif la == ')':
                            match(')')
                            match('V')
                            match('*')
                            match('6')
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <I>')
                elif la == 'T':
                    match('T')
                else:
                    raise ParseError(f'Unexpected token {la!r} in <C>')
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