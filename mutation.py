import copy
import random

def mutate_grammar(grammar, nonterminals, terminals):
    """
    Applies a single random mutation to the given grammar, ensuring the mutated grammar is different from the original.
    
    Parameters:
      grammar: dict, mapping nonterminal -> list of productions, where each production is a list of symbols.
      nonterminals: list, e.g. ['A', 'B', 'C', ...]
      terminals: list, e.g. ['a', 'b', 'c', ...]
    
    Returns:
      mutated_grammar: A new grammar with one mutation applied (deep copied so as not to modify the original).
    """
    # Create a deep copy to avoid modifying the original grammar
    mutated_grammar = copy.deepcopy(grammar)
    # Select a nonterminal from the deepest nonterminals in the original grammar
    def compute_depths(g, start):
        # longest acyclic path depth for each nonterminal
        depths = {}
        visiting = set()
        def dfs(symbol):
            if symbol in depths:
                return depths[symbol]
            if symbol in visiting:
                # cycle: treat as depth 0
                return 0
            visiting.add(symbol)
            max_child = 0
            for prod in g.get(symbol, []):
                for sym in prod:
                    if sym in g:
                        d = dfs(sym)
                        if d > max_child:
                            max_child = d
            visiting.remove(symbol)
            depths[symbol] = 1 + max_child
            return depths[symbol]
        # compute from start and all others
        dfs(start)
        for s in g:
            dfs(s)
        return depths

    # assume first in nonterminals is the start symbol
    start_nt = nonterminals[0] if nonterminals else next(iter(grammar))
    depths = compute_depths(grammar, start_nt)
    max_depth = max(depths.values()) if depths else 0
    deepest = [nt for nt, d in depths.items() if d == max_depth]
    nt = random.choice(deepest) if deepest else random.choice(list(mutated_grammar.keys()))
    
    # Randomly select one production of that nonterminal, amd make sure that productions are not empty
    productions = mutated_grammar[nt]
    productions = [p for p in productions if len(p) > 0]
    prod_index = random.randrange(len(productions))
    production = productions[prod_index]
    
    # Randomly choose a position in the production to mutate
    pos = random.randrange(len(production))
    original_symbol = production[pos]
    
    # Decide the replacement choices based on the position:
    # If it's the first symbol, choose a different terminal (to maintain LL(1) constraint)
    if pos == 0:
        choices = [t for t in terminals if t != original_symbol]
        # If no alternative is available and the production has more symbols, try mutating a later position
        if not choices and len(production) > 1:
            pos = 1
            original_symbol = production[pos]
            choices = [s for s in (terminals + nonterminals) if s != original_symbol]
    else:
        # For non-first positions, the replacement can be any terminal or nonterminal
        choices = [s for s in (terminals + nonterminals) if s != original_symbol]
    
    # If no alternative is available (very unlikely), return the grammar unchanged with metadata
    if not choices:
        return (mutated_grammar, nonterminals, terminals, nt, prod_index)
    
    new_symbol = random.choice(choices)
    production[pos] = new_symbol
    
    # Update the mutated production
    mutated_grammar[nt][prod_index] = production
    
    return (mutated_grammar,nonterminals,terminals,nt,prod_index)