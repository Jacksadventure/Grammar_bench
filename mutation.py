import random
from ultility import get_path

def mutate_grammar(grammar, nonterminals, terminals):
    """
    Applies a single mutation to the given grammar by replacing the last symbol
    of the last nonterminal (a terminal) with a different terminal.

    Parameters:
      grammar: dict mapping nonterminals to lists of productions (each a list of symbols).
      nonterminals: list of nonterminal symbols.
      terminals: list of terminal symbols.

    Returns:
      A tuple (mutated_grammar, nonterminals, terminals, nt, prod_index), where mutated_grammar
      is a new grammar with one mutation applied, nt is the nonterminal mutated (last),
      and prod_index is the index of the production mutated (last).
    """
    # Create a shallow copy of the grammar mapping;
    # we will copy only the mutated nonterminal's productions list below.
    mutated_grammar = grammar.copy()
    # Set mutation point to the last symbol of the last nonterminal (guaranteed to be a terminal)
    nt = nonterminals[-1]
    # Copy productions list and inner lists for chosen nonterminal before mutation
    mutated_grammar[nt] = [prod.copy() for prod in grammar[nt]]
    
    # Find the index of the last non-empty production
    prod_index = -1
    for i in range(len(mutated_grammar[nt]) - 1, -1, -1):
        if mutated_grammar[nt][i]:
            prod_index = i
            break
    
    # If no non-empty production is found, return the original grammar
    if prod_index == -1:
        return (mutated_grammar, nonterminals, terminals, nt, None)

    production = mutated_grammar[nt][prod_index]

    # Mutate the last symbol of the production
    pos = len(production) - 1
    original_symbol = production[pos]
    choices = [t for t in terminals if t != original_symbol]
    if not choices:
        return (mutated_grammar, nonterminals, terminals, nt, prod_index)

    new_symbol = random.choice(choices)
    production[pos] = new_symbol

    return (mutated_grammar, nonterminals, terminals, nt, prod_index)
