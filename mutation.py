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
    # Randomly select a nonterminal
    nt = random.choice(list(mutated_grammar.keys()))
    
    # Randomly select one production of that nonterminal
    productions = mutated_grammar[nt]
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
    
    # If no alternative is available (very unlikely), return the grammar as is
    if not choices:
        return mutated_grammar
    
    new_symbol = random.choice(choices)
    production[pos] = new_symbol
    
    # Update the mutated production
    mutated_grammar[nt][prod_index] = production
    
    return (mutated_grammar,nonterminals,terminals)