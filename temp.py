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
        if la == ')':
            match(')')
            # α* loop for <B>
            while pos < len(tokens) and (tokens[pos] == 'd'):
                match('d')
                match('w')
            # other alts of <B>
            if pos < len(tokens):
                la = tokens[pos]
                if la == '6':
                    match('6')
                    # α* loop for <G>
                    while pos < len(tokens) and (tokens[pos] == '('):
                        match('(')
                        match('3')
                    # other alts of <G>
                    if pos < len(tokens):
                        la = tokens[pos]
                        if la == 'a':
                            match('a')
                            # standard alts for <P>
                            if pos >= len(tokens):
                                raise ParseError('Unexpected EOF in <P>')
                            else:
                                la = tokens[pos]
                                if la == '~':
                                    match('~')
                                else:
                                    raise ParseError(f'Unexpected token {la!r} in <P>')
                        elif True:  # ε
                            pass
                elif la == '>':
                    match('>')
                    # α* loop for <H>
                    while pos < len(tokens) and (tokens[pos] == 'c'):
                        match('c')
                    # other alts of <H>
                    if pos < len(tokens):
                        la = tokens[pos]
                        if la == 'e':
                            match('e')
                            # α* loop for <Q>
                            while pos < len(tokens) and (tokens[pos] == 'w'):
                                match('w')
                            # other alts of <Q>
                            if pos < len(tokens):
                                la = tokens[pos]
                                if la == 'j':
                                    match('j')
                                elif True:  # ε
                                    pass
                        elif True:  # ε
                            pass
                elif la == '$':
                    match('$')
                    # standard alts for <I>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <I>')
                    else:
                        la = tokens[pos]
                        if la == '*':
                            match('*')
                            # α* loop for <R>
                            while pos < len(tokens) and (tokens[pos] == '&'):
                                match('&')
                                match('r')
                            # other alts of <R>
                            if pos < len(tokens):
                                la = tokens[pos]
                                if la == 'b':
                                    match('b')
                                    match('+')
                                    match('#')
                                elif la == 'k':
                                    match('k')
                                elif True:  # ε
                                    pass
                            match('n')
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <I>')
                elif True:  # ε
                    pass
        elif la == '.':
            match('.')
            # standard alts for <C>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF in <C>')
            else:
                la = tokens[pos]
                if la == 'm':
                    match('m')
                    # standard alts for <J>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <J>')
                    else:
                        la = tokens[pos]
                        if la == '%':
                            match('%')
                            # α* loop for <S>
                            while pos < len(tokens) and (tokens[pos] == '3'):
                                match('3')
                                match('{')
                            # other alts of <S>
                            if pos < len(tokens):
                                la = tokens[pos]
                                if la == 't':
                                    match('t')
                                elif True:  # ε
                                    pass
                        elif la == '!':
                            match('!')
                            # standard alts for <T>
                            if pos >= len(tokens):
                                raise ParseError('Unexpected EOF in <T>')
                            else:
                                la = tokens[pos]
                                if la == 'p':
                                    match('p')
                                    match('v')
                                    match('l')
                                else:
                                    raise ParseError(f'Unexpected token {la!r} in <T>')
                        elif la == 'h':
                            match('h')
                            # α* loop for <U>
                            while pos < len(tokens) and (tokens[pos] == '|'):
                                match('|')
                                match('n')
                            # other alts of <U>
                            if pos < len(tokens):
                                la = tokens[pos]
                                if la == '5':
                                    match('5')
                                elif la == '':
                                    match('')
                                    match('7')
                                    match('{')
                                elif True:  # ε
                                    pass
                            # α* loop for <V>
                            while pos < len(tokens) and (tokens[pos] == 'r'):
                                match('r')
                                match('_')
                            # other alts of <V>
                            if pos < len(tokens):
                                la = tokens[pos]
                                if la == '2':
                                    match('2')
                                    match('[')
                                    match('{')
                                elif la == '{':
                                    match('{')
                                elif True:  # ε
                                    pass
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <J>')
                elif la == 'q':
                    match('q')
                    # α* loop for <K>
                    while pos < len(tokens) and (tokens[pos] == '4'):
                        match('4')
                    # other alts of <K>
                    if pos < len(tokens):
                        la = tokens[pos]
                        if la == '=':
                            match('=')
                            # standard alts for <W>
                            if pos >= len(tokens):
                                raise ParseError('Unexpected EOF in <W>')
                            else:
                                la = tokens[pos]
                                if la == '+':
                                    match('+')
                                    match('l')
                                    match('7')
                                else:
                                    raise ParseError(f'Unexpected token {la!r} in <W>')
                        elif True:  # ε
                            pass
                elif la == 'f':
                    match('f')
                    # standard alts for <L>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <L>')
                    else:
                        la = tokens[pos]
                        if la == 's':
                            match('s')
                            # standard alts for <X>
                            if pos >= len(tokens):
                                raise ParseError('Unexpected EOF in <X>')
                            else:
                                la = tokens[pos]
                                if la == 'l':
                                    match('l')
                                    match('i')
                                    match('@')
                                else:
                                    raise ParseError(f'Unexpected token {la!r} in <X>')
                            # α* loop for <Y>
                            while pos < len(tokens) and (tokens[pos] == '8'):
                                match('8')
                            # other alts of <Y>
                            if pos < len(tokens):
                                la = tokens[pos]
                                if la == '^':
                                    match('^')
                                    match('7')
                                    match(']')
                                elif True:  # ε
                                    pass
                        elif la == 'y':
                            match('y')
                            # standard alts for <Z>
                            if pos >= len(tokens):
                                raise ParseError('Unexpected EOF in <Z>')
                            else:
                                la = tokens[pos]
                                if la == '[':
                                    match('[')
                                else:
                                    raise ParseError(f'Unexpected token {la!r} in <Z>')
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <L>')
                else:
                    raise ParseError(f'Unexpected token {la!r} in <C>')
            # standard alts for <D>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF in <D>')
            else:
                la = tokens[pos]
                if la == '-':
                    match('-')
                    # standard alts for <M>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <M>')
                    else:
                        la = tokens[pos]
                        if la == ':':
                            match(':')
                            # α* loop for <AA>
                            while pos < len(tokens) and (tokens[pos] == '7'):
                                match('7')
                                match('n')
                            # other alts of <AA>
                            if pos < len(tokens):
                                la = tokens[pos]
                                if la == '#':
                                    match('#')
                                    match('n')
                                elif la == '1':
                                    match('1')
                                    match(']')
                                    match('i')
                                elif True:  # ε
                                    pass
                        elif la == '0':
                            match('0')
                            # standard alts for <AB>
                            if pos >= len(tokens):
                                raise ParseError('Unexpected EOF in <AB>')
                            else:
                                la = tokens[pos]
                                if la == ',':
                                    match(',')
                                    match(']')
                                    match('`')
                                elif la == ';':
                                    match(';')
                                    match('o')
                                else:
                                    raise ParseError(f'Unexpected token {la!r} in <AB>')
                        elif la == 'z':
                            match('z')
                            # standard alts for <AC>
                            if pos >= len(tokens):
                                raise ParseError('Unexpected EOF in <AC>')
                            else:
                                la = tokens[pos]
                                if la == 'n':
                                    match('n')
                                    match('@')
                                else:
                                    raise ParseError(f'Unexpected token {la!r} in <AC>')
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <M>')
                else:
                    raise ParseError(f'Unexpected token {la!r} in <D>')
        elif la == '/':
            match('/')
            # standard alts for <E>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF in <E>')
            else:
                la = tokens[pos]
                if la == 'u':
                    match('u')
                    # standard alts for <N>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <N>')
                    else:
                        la = tokens[pos]
                        if la == '9':
                            match('9')
                            # standard alts for <AD>
                            if pos >= len(tokens):
                                raise ParseError('Unexpected EOF in <AD>')
                            else:
                                la = tokens[pos]
                                if la == 'p':
                                    match('p')
                                else:
                                    raise ParseError(f'Unexpected token {la!r} in <AD>')
                            match('r')
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <N>')
                else:
                    raise ParseError(f'Unexpected token {la!r} in <E>')
            # α* loop for <F>
            while pos < len(tokens) and (tokens[pos] == 'g'):
                match('g')
            # other alts of <F>
            if pos < len(tokens):
                la = tokens[pos]
                if la == '?':
                    match('?')
                    # standard alts for <O>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF in <O>')
                    else:
                        la = tokens[pos]
                        if la == '}':
                            match('}')
                            match('b')
                            match(';')
                        elif la == 'x':
                            match('x')
                            match('r')
                        else:
                            raise ParseError(f'Unexpected token {la!r} in <O>')
                elif True:  # ε
                    pass
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