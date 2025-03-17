import subprocess
from collections import deque
def validation_check(input,parser):
    command = ['python3', parser, input]
    result = subprocess.run(command, stdout=subprocess.PIPE).returncode
    if(result == 0):
        return True
    else:
        return False

def levenshtein_distance(a: str, b: str) -> int:
    """Calculate the Levenshtein distance between two strings."""
    if not a: return len(b)
    if not b: return len(a)

    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]

    for i in range(len(a) + 1):
        dp[i][0] = i
    for j in range(len(b) + 1):
        dp[0][j] = j

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,       # Deletion
                dp[i][j - 1] + 1,       # Insertion
                dp[i - 1][j - 1] + cost # Substitution
            )
    return dp[-1][-1]

def get_path(grammar, start, target):
    """
    Finds a derivation path from the start nonterminal to the target nonterminal using BFS.
    
    This function traverses the grammar starting from 'start'. Since the first symbol
    of every production is guaranteed to be a terminal (by construction), we only inspect
    symbols from index 1 onward. For every encountered nonterminal (child), we store its
    parent nonterminal and the production index that led to its discovery.
    
    Parameters:
      grammar: dict
          A dictionary mapping nonterminals to a list of productions. Each production is a list of symbols.
      start: str
          The starting nonterminal symbol.
      target: str
          The target nonterminal symbol for which we want to find a derivation path.
          
    Returns:
      A list of tuples (parent, production_index) representing the derivation steps from start to target.
      Each tuple indicates that the target nonterminal was reached from 'parent' using production at index 'production_index'.
      If the start is the target, an empty list is returned.
      If no path exists, returns None.
    """
    if start == target:
        return []
    
    # Use BFS to traverse reachable nonterminals and record how we reached them.
    queue = deque([start])
    # parent[symbol] will store the nonterminal from which 'symbol' was reached.
    parent = {start: None}
    # prod_used[symbol] stores the production index (and parent) used to derive this symbol.
    prod_used = {}

    while queue:
        cur = queue.popleft()
        # Traverse each production of the current nonterminal.
        for i, prod in enumerate(grammar[cur]):
            # Only consider symbols beyond the first, since the first is a terminal.
            for symbol in prod[1:]:
                # Only process nonterminals (keys in grammar) not already visited.
                if symbol in grammar and symbol not in parent:
                    parent[symbol] = cur
                    prod_used[symbol] = (cur, i)
                    if symbol == target:
                        # Reconstruct the path from target back to start.
                        path = []
                        s = target
                        while s != start:
                            path.append(prod_used[s])
                            s = parent[s]
                        return path[::-1]  # reverse the path to get start-to-target order.
                    queue.append(symbol)
    # If BFS finishes without reaching the target, no derivation path exists.
    return None

    
    