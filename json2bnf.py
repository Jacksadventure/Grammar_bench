import json

def json_to_bnf(grammar_json: str) -> str:
    grammar = json.loads(grammar_json)
    bnf_lines = []

    for nonterminal, productions in grammar.items():
        bnf_rule = f"{nonterminal} ::= "
        prod_strs = []
        for prod in productions:
            if not prod:
                prod_strs.append('epsilon')
            else:
                prod_strs.append(' '.join(prod))
        bnf_rule += '\n      | '.join(prod_strs)
        bnf_lines.append(bnf_rule)

    return '\n\n'.join(bnf_lines)

example_input = '''
{"<U>": [["p"], ["g", "<A>"]], "<M>": [["T", "<M>"], []], "<A>": [[".", "<M>"], ["f", "<M>"], ["(", "<U>", "<U>", "<A>"], ["q", "<N>", "<M>"], ["<"]], "<N>": [["/", "0", "!", "<N>"], []]}'''
bnf_output = json_to_bnf(example_input)
print(bnf_output)