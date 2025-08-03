import random
from ultility import get_path, charset, grammar_printer

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
          for symbol in range(len(mutated_grammar[nt][i])-1,-1,-1):
            if mutated_grammar[nt][i][symbol] != '' and mutated_grammar[nt][i][symbol] not in nonterminals:
                prod_index = i
                # Skip empty productions when gathering leading terminals to avoid IndexError
                candidate = random.choice(
                    [
                        s
                        for s in charset().chars
                        if s not in [x[0] for x in mutated_grammar[nt] if x]  # ignore ε-productions
                        and s not in nonterminals
                    ]
                )
                mutated_grammar[nt][i][symbol] = candidate
                # grammar_printer(nonterminals,mutated_grammar)
                return (mutated_grammar, nonterminals, terminals, nt, prod_index)
