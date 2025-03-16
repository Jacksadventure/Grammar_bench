import random

MAX_TEMP = 1000

def generate_diff_example(grammar, symbol,mutate_point,prod_index, max_depth=10):
    """
    Recursively generate a derivation string from the given nonterminal symbol.
    Terminals are returned as is.
    """
    if symbol not in grammar or max_depth <= 0:
        return symbol
    elif symbol == mutate_point:
        prod = grammar[symbol][prod_index]
    else:
        prod = random.choice(grammar[symbol])
    result = []
    for s in prod:
        if s in grammar:
            result.append(generate_diff_example(grammar,s,mutate_point,prod,max_depth-1))
        else:
            result.append(s)
    return "".join(result)
