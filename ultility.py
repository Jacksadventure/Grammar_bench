import subprocess
import ast
from collections import deque
import re
import os
from pathlib import Path
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

def get_shortcut(grammar):
    """
    Computes the shortcut string for each symbol in the given grammar.

    Grammar format:
      grammar: dict, where keys are nonterminals (e.g., "A", "B", ...),
               and values are lists of productions, where each production is a list of symbols.

    - Terminals: Symbols that do not appear as keys in grammar. Their shortcut is themselves.
    - Nonterminals:
      - If a production consists of a single symbol, and that symbol already has a shortcut,
        the nonterminal takes that shortcut.
      - If a production consists of multiple symbols, and all of them have shortcuts,
        the nonterminal's shortcut is the concatenation of those shortcuts.

    The algorithm first assigns shortcuts to all terminal symbols.
    It then iterates over the grammar to propagate shortcuts to nonterminals.
    The process continues until no new shortcuts are discovered.

    Returns:
      A dictionary `shortcut` where keys are symbols (both terminals and nonterminals),
      and values are their corresponding shortcut strings.
    """
    shortcut = {}

    # Collect all symbols that appear in any production
    all_symbols = set()
    for nt, prods in grammar.items():
        for prod in prods:
            for sym in prod:
                all_symbols.add(sym)

    # Identify terminal symbols (those that are not in grammar.keys())
    terminals = {sym for sym in all_symbols if sym not in grammar}

    # Assign shortcuts for terminal symbols
    for t in terminals:
        shortcut[t] = t

    # Iteratively update shortcuts for nonterminals
    while True:
        flag = False  # Indicates whether a new shortcut was assigned in this iteration
        for nt in grammar.keys():
            # Skip if this nonterminal already has a shortcut
            if nt in shortcut:
                continue
            # Try to derive the shortcut from its productions
            for prod in grammar[nt]:
                # Case 1: Production has a single symbol (similar to "non_terminal" type in C++)
                if len(prod) == 1:
                    sym = prod[0]
                    if sym in shortcut:
                        shortcut[nt] = shortcut[sym]
                        flag = True
                        break
                else:
                    # Case 2: Production has multiple symbols (similar to "expression" type in C++)
                    combination = ""
                    all_found = True
                    for sym in prod:
                        if sym in shortcut:
                            combination += shortcut[sym]
                        else:
                            all_found = False
                            break
                    if all_found:
                        shortcut[nt] = combination
                        flag = True
                        break
        # Stop when no new shortcuts are assigned
        if not flag:
            break
    return shortcut

def get_function_ranges(filename):
    """
    Parse the given Python file and return a list of tuples.
    Each tuple contains (function name, start line, estimated end line).
    """
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()
    tree = ast.parse(source, filename)
    funcs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno
            # Estimate the function's end line by taking the maximum line number of all nodes inside it.
            end = max((getattr(n, 'lineno', start) for n in ast.walk(node)), default=start)
            funcs.append((node.name, start, end))
    return funcs

def remove_think_tags(text):
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)

def remove_markdown_tags(text:str):
    pattern = r'^```json\s*([\s\S]*?)\s*```$'
    match = re.search(pattern, text.strip())
    if match:
        return match.group(1)
    else:
        raise ValueError("Input format is not valid. Could not extract content.")

def creat_repo(repo_name:str,code:str,issue:str):
    folder_path = Path(f"{repo_name}/{repo_name}")
    folder_path.mkdir(parents=True, exist_ok=True)
    with open(folder_path / "corrupted_generated_parser.py", "w") as f:
        f.write(code)
    with open(Path(f"{repo_name}") / "issue.txt", "w") as f:
        f.write(issue)
    # Initialize a git repository
    subprocess.run(["git", "init"], cwd=repo_name)
    # Add all files to the repository
    subprocess.run(["git", "add", "."], cwd=repo_name)
    # Commit the changes
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_name)

def grammar_printer(nonterminals, grammar):
    """
    Prints the grammar in a readable format.
    """
    for nt in nonterminals:
        for prod in grammar[nt]:
            print(f"  {nt} -> {' '.join(prod)}")