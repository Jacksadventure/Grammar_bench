import random
from ultility import get_shortcut

MAX_TEMP = 500

class StopGeneration(Exception):
    """Internal exception to stop generation once mutation point is reached."""
    def __init__(self, result: str):
        self.result = result

def generate_biased_example(grammar, symbol, path, shortcut, max_depth=100):
    """
    Recursively generate a derivation string from the given nonterminal symbol.
    
    The function follows a given biased path—provided as a list of tuples (nonterminal, production_index)
    that must be used in order. For the branch corresponding to this path, the derivation will strictly
    use the specified production indices until the path is exhausted. Other branches are derived randomly.
    
    Parameters:
      grammar: dict
          A dictionary mapping nonterminals to lists of productions (each production is a list of symbols).
      symbol: str
          The current nonterminal (or symbol) to expand.
      path: list of tuples
          A list representing the forced derivation path. Each tuple is (nonterminal, production_index).
          If the current symbol matches the first element of the path, that production index is used.
      max_depth: int
          Maximum recursion depth to avoid infinite recursion.
          
    Returns:
      A derivation string generated from the grammar.
    """
    if max_depth <= 0:
        return shortcut.get(symbol,"")
    
    # Check if we should follow the biased path for this nonterminal.
    if path and path[0][0] == symbol:
        # Use the specified production index from the path (mutation point).
        _, prod_index = path[0]
        prod = grammar[symbol][prod_index]
        next_path = path[1:]
        mutation_hit = True
    else:
        prod = random.choice(grammar[symbol])
        next_path = path
        mutation_hit = False
    
    result = ""
    for s in prod:
        if s in grammar:
            try:
                out = generate_biased_example(grammar, s, next_path, shortcut, max_depth-1)
            except StopGeneration:
                # Propagate early termination once mutation point reached.
                raise
        else:
            out = s
        result += out
        if len(result) > MAX_TEMP:
            return result
    if mutation_hit:
        # Stop generation immediately after mutation point.
        raise StopGeneration(result)
    return result

def generate_biased_example_wrapper(grammar, symbol, path, max_depth=60):
    """
    Wrapper function to generate biased examples with a given path.
    
    This function generates a biased example using the provided path and prints the result.
    """
    shortcut = get_shortcut(grammar)
    try:
        example = generate_biased_example(grammar, symbol, path, shortcut, max_depth)
    except StopGeneration as e:
        example = e.result
    return example
    