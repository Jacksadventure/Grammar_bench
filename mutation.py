import random
from ultility import get_path

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
    # Create a shallow copy of the grammar mapping;
    # we will copy only the mutated nonterminal's productions list below.
    mutated_grammar = grammar.copy()
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

    # Choose a nonterminal to mutate: pick from those with the longest path from the start (deepest in the tree)
    start_nt = nonterminals[0] if nonterminals else next(iter(grammar))
    # Compute longest acyclic path lengths from start_nt to each reachable nonterminal
    longest_dist = {}
    def dfs(sym, dist, visited):
        # Record only if this path is longer than any seen before
        if dist > longest_dist.get(sym, -1):
            longest_dist[sym] = dist
        else:
            return
        for prod in mutated_grammar.get(sym, []):
            for child in prod:
                if child in mutated_grammar and child not in visited:
                    visited.add(child)
                    dfs(child, dist + 1, visited)
                    visited.remove(child)
    dfs(start_nt, 0, {start_nt})
    # Select among nonterminals with maximal longest path distance
    if longest_dist:
        max_dist = max(longest_dist.values())
        candidates = [nt for nt, d in longest_dist.items() if d == max_dist]
        nt = random.choice(candidates)
    else:
        # Fallback: random nonterminal if no reachable distances
        nt = random.choice(list(mutated_grammar.keys()))
    
    # Copy productions list and inner lists for chosen nonterminal before mutation
    mutated_grammar[nt] = [prod.copy() for prod in grammar[nt]]
    productions = [p for p in mutated_grammar[nt] if len(p) > 0]
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
            choices = [s for s in terminals  if s != original_symbol]
    else:
        # For non-first positions, the replacement can be any terminal or nonterminal
        choices = [s for s in terminals  if s != original_symbol]
    
    # If no alternative is available (very unlikely), return the grammar unchanged with metadata
    if not choices:
        return (mutated_grammar, nonterminals, terminals, nt, prod_index)
    
    new_symbol = random.choice(choices)
    production[pos] = new_symbol
    
    # Update the mutated production
    mutated_grammar[nt][prod_index] = production
    
    return (mutated_grammar,nonterminals,terminals,nt,prod_index)