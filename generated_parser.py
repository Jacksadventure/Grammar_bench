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
        if la == '+':
            match('+')
            # standard alts for <B>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF in <B>')
            else:
                la = tokens[pos]
                if la == '^':
                    match('^')
                    match('`')
                elif la == '%':
                    match('%')
                    match(']')
                    match('@')
                    match('?')
                    match('2')
                    match('f')
                    match('W')
                    match('a')
                    match('(')
                    match('#')
                elif la == 'v':
                    match('v')
                    match('P')
                    match('U')
                    match('-')
                    match('Y')
                    match('@')
                    match('?')
                    match(')')
                elif la == 'Q':
                    match('Q')
                    match('-')
                    match('7')
                    match(')')
                elif la == '}':
                    match('}')
                    match('(')
                    match('R')
                    match('8')
                    match('6')
                    match('{')
                else:
                    raise ParseError(f'Unexpected token {la!r} in <B>')
            match('6')
            match('m')
            # standard alts for <C>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF in <C>')
            else:
                la = tokens[pos]
                if la == 'q':
                    match('q')
                    match(',')
                    match('7')
                elif la == 'k':
                    match('k')
                    match('(')
                    match('L')
                elif la == '@':
                    match('@')
                    match('P')
                    match('>')
                elif la == '>':
                    match('>')
                    match(';')
                    match('0')
                    match('j')
                    match('3')
                    match('`')
                elif la == '=':
                    match('=')
                    match('6')
                    match('3')
                    match('$')
                elif la == ')':
                    match(')')
                    match('N')
                    match('0')
                else:
                    raise ParseError(f'Unexpected token {la!r} in <C>')
            # standard alts for <D>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF in <D>')
            else:
                la = tokens[pos]
                if la == '{':
                    match('{')
                    match('6')
                    match('N')
                    match('~')
                    match('X')
                    match('3')
                    match('f')
                elif la == '8':
                    match('8')
                    match('n')
                elif la == '1':
                    match('1')
                    match('-')
                elif la == 'Z':
                    match('Z')
                    match('t')
                    match('a')
                    match('U')
                elif la == 'W':
                    match('W')
                elif la == '5':
                    match('5')
                    match('a')
                    match('2')
                    match('&')
                    match('0')
                elif la == '[':
                    match('[')
                    match('P')
                    match('|')
                    match('u')
                    match('w')
                    match('O')
                    match('i')
                    match('U')
                elif la == ';':
                    match(';')
                    match(',')
                    match('a')
                elif la == 'K':
                    match('K')
                    match('n')
                    match('$')
                    match('h')
                    match('!')
                    match('6')
                    match(',')
                    match('X')
                    match('j')
                    match('w')
                else:
                    raise ParseError(f'Unexpected token {la!r} in <D>')
            # α* loop for <E>
            while pos < len(tokens) and (tokens[pos] == 'R'):
                match('R')
                match('X')
                match('n')
                match('/')
                match('3')
                match('n')
                match(']')
            # other alts of <E>
            if pos < len(tokens):
                la = tokens[pos]
                if la == 'Y':
                    match('Y')
                    match('6')
                    match('_')
                    match('3')
                    match('/')
                    match('0')
                    match('|')
                    match('j')
                    match('w')
                elif la == 's':
                    match('s')
                elif la == 'U':
                    match('U')
                    match('e')
                    match('u')
                    match('?')
                    match('n')
                    match(':')
                    match('6')
                    match('(')
                    match('X')
                elif la == '/':
                    match('/')
                    match('?')
                elif True:  # ε
                    pass
            # α* loop for <F>
            while pos < len(tokens) and (tokens[pos] == 'u'):
                match('u')
            # other alts of <F>
            if pos < len(tokens):
                la = tokens[pos]
                if la == 'X':
                    match('X')
                    match('y')
                elif True:  # ε
                    pass
            match(')')
        elif la == 'r':
            match('r')
            # standard alts for <G>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF in <G>')
            else:
                la = tokens[pos]
                if la == '$':
                    match('$')
                    match('d')
                    match('3')
                    match('i')
                elif la == 'x':
                    match('x')
                    match('e')
                    match('h')
                    match(']')
                    match('?')
                elif la == ':':
                    match(':')
                    match('M')
                    match('a')
                    match('t')
                    match('f')
                    match('i')
                    match('#')
                    match('|')
                elif la == '3':
                    match('3')
                    match('P')
                    match('l')
                    match('!')
                elif la == '?':
                    match('?')
                    match('g')
                    match('|')
                    match('t')
                    match('P')
                    match('')
                    match('6')
                    match('f')
                elif la == 'P':
                    match('P')
                    match('*')
                    match('~')
                    match('7')
                    match('b')
                else:
                    raise ParseError(f'Unexpected token {la!r} in <G>')
        elif la == 'o':
            match('o')
            # α* loop for <H>
            while pos < len(tokens) and (tokens[pos] == 'S'):
                match('S')
                match('t')
                match('y')
                match('p')
                match('t')
                match('')
                match('t')
                match('*')
            # other alts of <H>
            if pos < len(tokens):
                la = tokens[pos]
                if la == 'j':
                    match('j')
                    match('w')
                elif la == '`':
                    match('`')
                    match('|')
                    match('i')
                elif la == 'g':
                    match('g')
                    match('0')
                    match('f')
                    match('7')
                    match('7')
                    match('b')
                    match('(')
                    match('e')
                elif la == 'O':
                    match('O')
                    match(']')
                    match('N')
                elif la == 'd':
                    match('d')
                    match('6')
                    match('6')
                    match(',')
                    match('l')
                    match('b')
                    match('.')
                    match('&')
                    match('a')
                elif la == '(':
                    match('(')
                    match('p')
                    match('f')
                    match('a')
                    match('i')
                    match('&')
                    match('f')
                    match('N')
                    match('!')
                elif True:  # ε
                    pass
            match('W')
            # standard alts for <I>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF in <I>')
            else:
                la = tokens[pos]
                if la == '6':
                    match('6')
                    match('')
                    match('a')
                    match('')
                elif la == '':
                    match('')
                    match('t')
                    match(']')
                    match('.')
                    match('b')
                else:
                    raise ParseError(f'Unexpected token {la!r} in <I>')
        elif la == 'm':
            match('m')
            # α* loop for <J>
            while pos < len(tokens) and (tokens[pos] == ']'):
                match(']')
                match('0')
            # other alts of <J>
            if pos < len(tokens):
                la = tokens[pos]
                if la == '_':
                    match('_')
                    match('a')
                    match('*')
                    match('n')
                    match('N')
                elif True:  # ε
                    pass
            match('K')
        elif la == '4':
            match('4')
            match('n')
            match('[')
            match('s')
            match('$')
            match('N')
            match('c')
        elif la == 'V':
            match('V')
            match('L')
            match(';')
            match('x')
            match('2')
        elif la == 'T':
            match('T')
            match('^')
            match('~')
        elif la == '9':
            match('9')
            match('W')
            match('6')
            match(',')
            match('Y')
            match('|')
            match('5')
            match('p')
        elif la == 'z':
            match('z')
            match('O')
            match('3')
            match('h')
            match('%')
            match('{')
            match('Q')
            match('n')
            match('Y')
            match('Z')
        elif la == 'c':
            match('c')
            match('5')
            match('O')
            match('l')
            match('e')
            match('3')
            match('7')
            match('|')
            match('~')
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