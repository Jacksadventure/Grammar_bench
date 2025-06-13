"""
<S> : s | <A> | <B>
<A> : a <B> | epsilon
<B> : b <A> | epsilon
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
    if lookahead.startswith('s'):
        match('s')
    elif lookahead.startswith('A'):
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('a'):
            match('a')
            if pos >= len(tokens):
                error("Unexpected end of input in B")
            lookahead = tokens[pos]
            if lookahead.startswith('b'):
                match('b')
                parse_A()
            else:
                error("Unexpected token " + lookahead + " in B, expected one of: 'b'")
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: 'a'")
    elif lookahead.startswith('B'):
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('b'):
            match('b')
            if pos >= len(tokens):
                error("Unexpected end of input in A")
            lookahead = tokens[pos]
            if lookahead.startswith('a'):
                match('a')
                parse_B()
            else:
                error("Unexpected token " + lookahead + " in A, expected one of: 'a'")
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: 'b'")
    else:
        error("Unexpected token " + lookahead + " in S, expected one of: 's', 'A', 'B'")

def parse_A():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in A")
    lookahead = tokens[pos]
    if lookahead.startswith('a'):
        match('a')
        if pos >= len(tokens):
            error("Unexpected end of input in B")
        lookahead = tokens[pos]
        if lookahead.startswith('b'):
            match('b')
            parse_A()
        else:
            error("Unexpected token " + lookahead + " in B, expected one of: 'b'")
    else:
        error("Unexpected token " + lookahead + " in A, expected one of: 'a'")

def parse_B():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in B")
    lookahead = tokens[pos]
    if lookahead.startswith('b'):
        match('b')
        if pos >= len(tokens):
            error("Unexpected end of input in A")
        lookahead = tokens[pos]
        if lookahead.startswith('a'):
            match('a')
            parse_B()
        else:
            error("Unexpected token " + lookahead + " in A, expected one of: 'a'")
    else:
        error("Unexpected token " + lookahead + " in B, expected one of: 'b'")

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