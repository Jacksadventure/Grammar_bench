"""
<S> ::= w <Q> <Q> <Q>
      | 4 <Q> <Q> <Q>
      | p

<Q> ::= X <Q>
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

def parse_S():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in S")
    lookahead = tokens[pos]
    if lookahead.startswith('w'):
        match('w')
        while pos < len(tokens) and tokens[pos].startswith('X'):
            match('X')
        while pos < len(tokens) and tokens[pos].startswith('X'):
            match('X')
        while pos < len(tokens) and tokens[pos].startswith('X'):
            match('X')
    elif lookahead.startswith('4'):
        match('4')
        while pos < len(tokens) and tokens[pos].startswith('X'):
            match('X')
        while pos < len(tokens) and tokens[pos].startswith('X'):
            match('X')
        while pos < len(tokens) and tokens[pos].startswith('X'):
            match('X')
    elif lookahead.startswith('p'):
        match('p')
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: 'w', '4', 'p'")

def parse_Q():
    global pos, tokens
    while pos < len(tokens) and tokens[pos].startswith('X'):
        match('X')

def parse_input(input_str):
    global pos, tokens
    tokens = list(input_str)
    pos = 0
    parse_S()
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