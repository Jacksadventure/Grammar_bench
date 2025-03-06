import difflib

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