import sys
tokens = []
pos = 0
class ParseError(Exception): pass

def match(expected):
    global pos
    if pos < len(tokens) and tokens[pos] == expected:
        pos += 1
    else:
        got = tokens[pos] if pos < len(tokens) else 'EOF'
        raise ParseError(f"Expected {expected!r}, got {got!r}")

def parse(input_str):
    global tokens, pos
    tokens = list(input_str.strip())
    pos = 0
    # Standard logic for <N>
    if pos >= len(tokens):
        raise ParseError('Unexpected EOF parsing <N>')
    else:
        la = tokens[pos]
        if la == '':
            match('')
            match('3')
            # Iterative rule for <Y>: while ['=', '3', 'I']
            while pos < len(tokens) and (tokens[pos] == '='):
                match('=')
                match('3')
                match('I')
            match('3')
        elif la == 'I':
            match('I')
        elif la == 'f':
            match('f')
            match('{')
            # Standard logic for <G>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF parsing <G>')
            else:
                la = tokens[pos]
                if la == '':
                    match('')
                    # Iterative rule for <Y>: while ['=', '3', 'I']
                    while pos < len(tokens) and (tokens[pos] == '='):
                        match('=')
                        match('3')
                        match('I')
                    match('')
                    # Standard logic for <Z>
                    if pos >= len(tokens):
                        raise ParseError('Unexpected EOF parsing <Z>')
                    else:
                        la = tokens[pos]
                        if la == '=':
                            match('=')
                            match('f')
                            # Iterative rule for <R>: while [')', 'o']
                            while pos < len(tokens) and (tokens[pos] == ')'):
                                match(')')
                                match('o')
                            # Iterative rule for <X>: while ['f', 'I']
                            while pos < len(tokens) and (tokens[pos] == 'f'):
                                match('f')
                                match('I')
                            # Iterative rule for <J>: while ['=', 'Y']
                            while pos < len(tokens) and (tokens[pos] == '='):
                                match('=')
                                # Iterative rule for <Y>: while ['=', '3', 'I']
                                while pos < len(tokens) and (tokens[pos] == '='):
                                    match('=')
                                    match('3')
                                    match('I')
                        elif la == '':
                            match('')
                        else:
                            raise ParseError(f"Unexpected token {la!r} parsing <Z>")
                elif la == '=':
                    match('=')
                else:
                    raise ParseError(f"Unexpected token {la!r} parsing <G>")
            # Standard logic for <Z>
            if pos >= len(tokens):
                raise ParseError('Unexpected EOF parsing <Z>')
            else:
                la = tokens[pos]
                if la == '=':
                    match('=')
                    match('f')
                    # Iterative rule for <R>: while [')', 'o']
                    while pos < len(tokens) and (tokens[pos] == ')'):
                        match(')')
                        match('o')
                    # Iterative rule for <X>: while ['f', 'I']
                    while pos < len(tokens) and (tokens[pos] == 'f'):
                        match('f')
                        match('I')
                    # Iterative rule for <J>: while ['=', 'Y']
                    while pos < len(tokens) and (tokens[pos] == '='):
                        match('=')
                        # Iterative rule for <Y>: while ['=', '3', 'I']
                        while pos < len(tokens) and (tokens[pos] == '='):
                            match('=')
                            match('3')
                            match('I')
                elif la == '':
                    match('')
                else:
                    raise ParseError(f"Unexpected token {la!r} parsing <Z>")
        else:
            raise ParseError(f"Unexpected token {la!r} parsing <N>")
    if pos < len(tokens):
        raise ParseError(f"Extra characters at end: {''.join(tokens[pos:])}")
    print('Input accepted.')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            parse(sys.argv[1])
        except ParseError as e:
            print('Input rejected.')
            print(e)
    else:
        print('Usage: python generated_parser.py <string_to_parse>')