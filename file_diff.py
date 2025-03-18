import difflib
import re
import ast
def diff(file1, file2, method="unified"):
    """
    Compare two text files and print their differences.

    :param file1: Path to the first file.
    :param file2: Path to the second file.
    :param method: "unified" for diff-like output, "differ" for detailed line-by-line comparison.
    """
    try:
        # Read file contents
        with open(file1, 'r', encoding='utf-8') as f1:
            file1_lines = f1.readlines()
        
        with open(file2, 'r', encoding='utf-8') as f2:
            file2_lines = f2.readlines()

        if method == "unified":
            # Use unified_diff for a diff-like output
            diff = difflib.unified_diff(file1_lines, file2_lines, 
                                        fromfile=file1, tofile=file2, lineterm='')
        elif method == "differ":
            # Use Differ for a more detailed line-by-line comparison
            d = difflib.Differ()
            diff = d.compare(file1_lines, file2_lines)
        else:
            raise ValueError("Invalid method. Choose 'unified' or 'differ'.")

        # Print the differences
        print("\n".join(diff))

    except FileNotFoundError as e:
        print(f"Error: {e}")

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
            # Estimate the function's end line by taking the maximum line number among all nodes in the function.
            end = max((getattr(n, 'lineno', start) for n in ast.walk(node)), default=start)
            funcs.append((node.name, start, end))
    return funcs

def parse_diff(file1, file2):
    """
    Generate a unified diff between two files and return:
      - diff_lines: the full diff output as a list of strings.
      - changed_lines: a list of line numbers in file2 that have changes (additions or modifications).
    """
    with open(file1, 'r', encoding='utf-8') as f:
        f1_lines = f.readlines()
    with open(file2, 'r', encoding='utf-8') as f:
        f2_lines = f.readlines()
    
    diff_lines = list(difflib.unified_diff(f1_lines, f2_lines,
                                             fromfile=file1,
                                             tofile=file2,
                                             lineterm=''))
    changed_lines = []  # To store changed line numbers in file2
    file1_line = None
    file2_line = None

    for line in diff_lines:
        if line.startswith('@@'):
            # Parse the hunk header: format @@ -a,b +c,d @@
            m = re.search(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', line)
            if m:
                file1_line = int(m.group(1))
                file2_line = int(m.group(3))
        else:
            if line.startswith(' '):
                # Context lines: increment both file counters
                file1_line += 1
                file2_line += 1
            elif line.startswith('-'):
                # Removed line from file1: increment file1 counter only
                file1_line += 1
            elif line.startswith('+'):
                # Added line in file2: record the line number and increment file2 counter
                changed_lines.append(file2_line)
                file2_line += 1
    return diff_lines, changed_lines

def locate_changes(changed_lines, function_ranges):
    """
    Match each changed line number with the function it falls in.
    Returns a dictionary mapping function names (or 'Global') to lists of changed line numbers.
    """
    locations = {}
    for lineno in changed_lines:
        found = False
        for func_name, start, end in function_ranges:
            if start <= lineno <= end:
                locations.setdefault(func_name, []).append(lineno)
                found = True
                break
        if not found:
            locations.setdefault('Global', []).append(lineno)
    return locations

def get_diff_function(file1, file2):
    """
    Accept two Python files and return a dictionary mapping the functions in file2
    that have changes (compared to file1) to the list of changed line numbers.
    If changes occur outside any function, they are categorized under 'Global'.
    """
    # 1. Parse file2 to get function definitions and their line ranges.
    function_ranges = get_function_ranges(file2)
    # 2. Generate the diff and extract the changed line numbers in file2.
    _, changed_lines = parse_diff(file1, file2)
    # 3. Determine which functions contain the changes.
    diff_functions = locate_changes(changed_lines, function_ranges)
    return diff_functions[0]
