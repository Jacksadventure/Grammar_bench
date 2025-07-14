import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
import tempfile
import pytest

from new_grammar_gen import generate_grammar
from new_fuzzer import convert_ebnf
from new_codegen import read_grammar, generate_parser
from ultility import compile_parser


@pytest.mark.parametrize("seed, num_nt", [
    (42, 3),
    (7, 4),
    (123, 5),
])
def test_generated_parser_executes(seed, num_nt):
    # Generate random EBNF grammar
    random.seed(seed)
    ebnf = generate_grammar(num_nt)

    # Write EBNF to temp file and read into AST
    tmp = tempfile.NamedTemporaryFile("w+", delete=False, suffix=".ebnf")
    tmp.write(ebnf)
    tmp.flush()
    tmp.close()
    rules = read_grammar(tmp.name)

    # Generate recursive-descent parser code
    src = generate_parser(rules)

    # Ensure the generated code compiles
    namespace = {}
    exec(src, namespace)

    # Invoke the parse entrypoint; SyntaxError is acceptable
    parse_fn = namespace.get("parse")
    assert callable(parse_fn)
    try:
        parse_fn("")
    except SyntaxError:
        pass