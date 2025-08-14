import sys

NONTERMINALS = ['A', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
TERMINALS = ['', '!', '#', '$', '%', '&', '(', ')', '+', ',', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '=', '>', '?', '@', '[', ']', '^', '_', '`', 'a', 'b', 'c', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'y', 'z', '{', '|', '}', '~']
START = 'A'

# DECISIONS: for each nonterminal, a list of (lookahead set, production).
# Special lookahead {'__EPS__'} means epsilon (empty production).
DECISIONS = {
    'A': [
        ({'f'}, ['f', 'B', 'C']),
        ({'e'}, ['e', 'D', 'E']),
        ({'h'}, ['h', 'F']),
    ],
    'B': [
        ({'v'}, ['v', 'G']),
    ],
    'C': [
        ({'s'}, ['s', 'z', 'C']),
        ({'__EPS__'}, []),
        ({'e', 'f', 'h'}, ['A', 'H']),
    ],
    'D': [
        ({'@'}, ['@', 'I']),
        ({'_'}, ['_', 'J']),
    ],
    'E': [
        ({'5', ':', ';', '@', ']', 'q', '}'}, ['G', 'E']),
        ({'__EPS__'}, []),
        ({'5'}, ['5', 'K']),
        ({':'}, [':', 'L', 'M']),
        ({']'}, [']', 'N', '_']),
    ],
    'F': [
        ({'{'}, ['{', 'O']),
        ({'s'}, ['s', 'P']),
    ],
    'G': [
        ({'}'}, ['}', 'G']),
        ({'__EPS__'}, []),
        ({'5', ':', ';', '@', ']', 'q', '}'}, ['E', 'Q', 'A']),
    ],
    'H': [
        ({'#'}, ['#', 'R']),
        ({'m'}, ['m', 'S']),
        ({'h'}, ['h', 'T']),
    ],
    'I': [
        ({'g'}, ['g', 'I']),
        ({'__EPS__'}, []),
        ({'$'}, ['$', 'U', 'V']),
        ({'>'}, ['>', 'W']),
        ({'6'}, ['6', 'X']),
    ],
    'J': [
        ({'#', '$', '&', 'c', 'h', 'm', 's'}, ['R', 'J']),
        ({'__EPS__'}, []),
        ({'c'}, ['c', 'Y']),
        ({'#', 'h', 'm'}, ['H', 'Z']),
        ({'$'}, ['$', 'AA']),
    ],
    'K': [
        ({'s', '{'}, ['F', 'AB', 'AC']),
    ],
    'L': [
        ({'k'}, ['k', 'AD']),
    ],
    'M': [
        ({'j'}, ['j', 'AE']),
        ({'8'}, ['8', 'AF']),
        ({'1'}, ['1', 'AG']),
    ],
    'N': [
        ({'4'}, ['4', 'AH', 'AI']),
        ({'('}, ['(', 'AJ']),
        ({'k'}, ['k', 'AK']),
    ],
    'O': [
        ({'='}, ['=', 'AL']),
        ({']'}, [']', 'AM']),
        ({'e', 'f', 'h'}, ['A', 'AN']),
    ],
    'P': [
        ({'.'}, ['.', '+', 'P']),
        ({'__EPS__'}, []),
        ({'6'}, ['6']),
        ({'#', ')', 'n', 'u', 'v'}, ['V', 'W', '(']),
        ({'7'}, ['7', '0', 'W']),
    ],
    'Q': [
        ({'@'}, ['@', '!']),
        ({';'}, [';']),
        ({'q'}, ['q', ':', 'M']),
    ],
    'R': [
        ({'&'}, ['&', 'R']),
        ({'__EPS__'}, []),
        ({'h'}, ['h']),
        ({'#', 'h', 'm'}, ['H', 'z', '6']),
        ({'s'}, ['s', ',', 'e']),
    ],
    'S': [
        ({'`'}, ['`', '(', 'A']),
        ({'@', '_'}, ['D', '2']),
    ],
    'T': [
        ({'g'}, ['g', '_']),
        ({'!'}, ['!', '', 'm']),
        ({':'}, [':']),
    ],
    'U': [
        ({'('}, ['(', 'Z']),
        ({'!'}, ['!', 'j', 'C']),
        ({'|'}, ['|', '$']),
    ],
    'V': [
        ({'v'}, ['v', '_', 'V']),
        ({'__EPS__'}, []),
        ({'n'}, ['n', '!']),
        ({'#'}, ['#', 'S', '&']),
        ({'u'}, ['u', 'X']),
    ],
    'W': [
        ({')'}, [')', 'b', 'W']),
        ({'v'}, ['v', 'y', 'b']),
    ],
    'X': [
        ({'/'}, ['/', '7', 'r']),
    ],
    'Y': [
        ({'c'}, ['c', 'j']),
        ({'b'}, ['b']),
        ({'s', '{'}, ['K', 'M', '%']),
    ],
    'Z': [
        ({'s', '{'}, ['K', 'Y']),
        ({'=', ']', 'e', 'f', 'h'}, ['O']),
        ({'#', '&', '^', 'h', 'm', 's'}, ['R', '^', 'f']),
    ],
    'AA': [
        ({'y'}, ['y', 'AA']),
        ({'__EPS__'}, []),
        ({';', '@', 'q'}, ['Q']),
        ({'t'}, ['t']),
    ],
    'AB': [
        ({'c'}, ['c', 'p', 'AB']),
        ({'__EPS__'}, []),
        ({'4'}, ['4', '+']),
        ({'`', 'e', 'f', 'h', 's'}, ['C', '`']),
    ],
    'AC': [
        ({'v'}, ['B']),
    ],
    'AD': [
        ({'$'}, ['$', 'i', 'AD']),
        ({'__EPS__'}, []),
        ({'a'}, ['a']),
        ({'m'}, ['m', 'N', '8']),
        ({'`'}, ['`']),
    ],
    'AE': [
        ({'a'}, ['a']),
    ],
    'AF': [
        ({'@', '_'}, ['D']),
    ],
    'AG': [
        ({'3'}, ['3', 'S', '|']),
        ({'~'}, ['~', 'b', '?']),
        ({'v'}, ['v']),
    ],
    'AH': [
        ({'#', 'h', 'm'}, ['H']),
    ],
    'AI': [
        ({'/'}, ['X', 'e']),
        ({'9'}, ['9']),
    ],
    'AJ': [
        ({'~'}, ['~']),
    ],
    'AK': [
        ({'b', 'c', 's', '{'}, ['Y', 'S', 'AK']),
        ({'__EPS__'}, []),
        ({';', '@', 'q'}, ['Q', 'B', 'k']),
        ({'('}, ['(', '_']),
        ({':'}, [':', 'j', 'I']),
    ],
    'AL': [
        ({'s'}, ['s', 'AL']),
        ({'__EPS__'}, []),
        ({'e', 'f', 'h', 's'}, ['C']),
        ({'a'}, ['a', 'G']),
    ],
    'AM': [
        ({'5', ':', ';', '@', ']', 'n', 'q', '}'}, ['E', 'n', 'AM']),
        ({'__EPS__'}, []),
        ({'h'}, ['h', 'P']),
        ({'['}, ['[']),
        ({'e', 'f', 'h'}, ['A', 'G']),
    ],
    'AN': [
        ({'5', ':', ';', '@', ']', 'q', '}'}, ['G']),
        ({'__EPS__'}, []),
        ({':'}, [':', 'S']),
        ({'e', 'f', 'h'}, ['A', '}', '6']),
    ],
}

class ParseError(Exception):
    pass

def parse(inp):
    tokens = list(inp.strip())
    pos = 0
    stack = [START]

    def peek_la():
        return tokens[pos] if pos < len(tokens) else None

    while stack:
        top = stack.pop()
        la = peek_la()

        if top not in NONTERMINALS:
            # Terminal: must match exactly
            if la == top:
                pos += 1
            else:
                got = la if la is not None else 'EOF'
                raise ParseError(f"Expected {top!r}, got {got!r}")
            continue

        # Nonterminal: choose a production based on lookahead
        chosen = None
        cases = DECISIONS.get(top, [])
        for look, prod in cases:
            if '__EPS__' in look:
                if chosen is None:
                    chosen = prod  # Save epsilon as fallback
                continue
            if la in look:
                chosen = prod
                break

        if chosen is None:
            got = la if la is not None else 'EOF'
            raise ParseError(f"Unexpected token {got!r} in <{top}>")

        # Push production symbols in reverse order (so first symbol is on top)
        for sym in reversed(chosen):
            stack.append(sym)

    # If parsing finishes but tokens remain, it's an error
    if pos < len(tokens):
        tail = ''.join(tokens[pos:])
        raise ParseError(f"Extra input at end: {tail}")
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