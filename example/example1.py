"""
<U> ::= p
      | g <A>

<M> ::= T <M>
      | epsilon

<A> ::= . <M>
      | f <M>
      | ( <U> <U> <A>
      | q <N> <M>
      | <

<N> ::= / 0 ! <N>
      | epsilon
"""
import sys

tokens = []
pos = 0

def error(msg):
    print("Parse error:", msg)
    sys.exit(1)

def match(expected):
    global pos, tokens
    if pos < len(tokens) and tokens[pos].startswith(expected):
        pos += 1
    else:
        error("Expected " + expected + ", got " + (tokens[pos] if pos < len(tokens) else "EOF"))

def parse_U():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in U")
    lookahead = tokens[pos]
    if lookahead.startswith('p'):
        match('p')
    elif lookahead.startswith('g'):
        match('g')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('.'):
            match('.')
            while pos < len(tokens) and tokens[pos].startswith('T'):
                match('T')
        elif lookahead.startswith('f'):
            match('f')
            while pos < len(tokens) and tokens[pos].startswith('T'):
                match('T')
        elif lookahead.startswith('('):
            match('(')
            parse_U()
            parse_U()
            parse_A()
        elif lookahead.startswith('q'):
            match('q')
            while pos < len(tokens) and tokens[pos].startswith('/'):
                match('/')
                match('0')
                match('[')
            while pos < len(tokens) and tokens[pos].startswith('T'):
                match('T')
        elif lookahead.startswith('<'):
            match('<')
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: '.', 'f', '(', 'q', '<'")
    else:
        error("Unexpected token " + lookahead + " in U, expected one of: 'p', 'g'")

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('.'):
        match('.')
        while pos < len(tokens) and tokens[pos].startswith('T'):
            match('T')
    elif lookahead.startswith('f'):
        match('f')
        while pos < len(tokens) and tokens[pos].startswith('T'):
            match('T')
    elif lookahead.startswith('('):
        match('(')
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('p'):
            match('p')
        elif lookahead.startswith('g'):
            match('g')
            parse_A()
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: 'p', 'g'")
        if pos >= len(tokens):
            error("Unexpected end of input in U")
        lookahead = tokens[pos]
        if lookahead.startswith('p'):
            match('p')
        elif lookahead.startswith('g'):
            match('g')
            parse_A()
        else:
            error("Unexpected token " + lookahead + " in U, expected one of: 'p', 'g'")
        parse_A()
    elif lookahead.startswith('q'):
        match('q')
        while pos < len(tokens) and tokens[pos].startswith('/'):
            match('/')
            match('0')
            match('[')
        while pos < len(tokens) and tokens[pos].startswith('T'):
            match('T')
    elif lookahead.startswith('<'):
        match('<')
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: '.', 'f', '(', 'q', '<'")

def parse_input(input_str):
    global pos, tokens
    tokens = list(input_str)
    pos = 0
    parse_U()
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