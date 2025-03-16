import subprocess

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

def get_path(grammar,start,nonterminal):
    """Get the path to a nonterminal in the grammar.
    From target nonterminal to start nonterminal,then reverse the path
    """
    path = []
    visited = set()
    while nonterminal != start:
        for nt in grammar:
            for i,prod in enumerate(grammar[nt]):
                if nonterminal in prod:
                    if (nt,i) in visited:
                        print("Loop detected")
                        return None 
                    visited.add((nt,i))
                    path.append((nt,i))
                    nonterminal = nt
                    break
    return path[::-1]

    
    