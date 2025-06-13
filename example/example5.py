"""
<S> : s | <A> | <B>
<A> : a <B>
<B> : c <A>
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

def parse_s():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in s")
    lookahead = tokens[pos]
    if lookahead.startswith('s'):
        parse_s()
    elif lookahead.startswith('a'):
        if pos >= len(tokens):
            error("Unexpected end of input in a")
        lookahead = tokens[pos]
        if lookahead.startswith('a'):
            parse_a()
            if pos >= len(tokens):
                error("Unexpected end of input in b")
            lookahead = tokens[pos]
            if lookahead.startswith('c'):
                match('c')
                parse_a()
            else:
                error("Unexpected token " + lookahead + " in b, expected one of: 'c'")
        else:
            error("Unexpected token " + lookahead + " in a, expected one of: 'a'")
    elif lookahead.startswith('b'):
        if pos >= len(tokens):
            error("Unexpected end of input in b")
        lookahead = tokens[pos]
        if lookahead.startswith('c'):
            match('c')
            if pos >= len(tokens):
                error("Unexpected end of input in a")
            lookahead = tokens[pos]
            if lookahead.startswith('a'):
                parse_a()
                parse_b()
            else:
                error("Unexpected token " + lookahead + " in a, expected one of: 'a'")
        else:
            error("Unexpected token " + lookahead + " in b, expected one of: 'c'")
    else:
        error("Unexpected token " + lookahead + " in s, expected one of: 's', 'a', 'b'")

def parse_a():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in a")
    lookahead = tokens[pos]
    if lookahead.startswith('a'):
        parse_a()
        if pos >= len(tokens):
            error("Unexpected end of input in b")
        lookahead = tokens[pos]
        if lookahead.startswith('c'):
            match('c')
            parse_a()
        else:
            error("Unexpected token " + lookahead + " in b, expected one of: 'c'")
    else:
        error("Unexpected token " + lookahead + " in a, expected one of: 'a'")

def parse_b():
    global pos, tokens
    if pos >= len(tokens):
        error("Unexpected end of input in b")
    lookahead = tokens[pos]
    if lookahead.startswith('c'):
        match('c')
        if pos >= len(tokens):
            error("Unexpected end of input in a")
        lookahead = tokens[pos]
        if lookahead.startswith('a'):
            parse_a()
            parse_b()
        else:
            error("Unexpected token " + lookahead + " in a, expected one of: 'a'")
    else:
        error("Unexpected token " + lookahead + " in b, expected one of: 'c'")

def parse_input(input_str):
    global pos, tokens
    tokens = list(input_str)
    pos = 0
    parse_s()
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