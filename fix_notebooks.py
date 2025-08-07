#!/usr/bin/env python3
"""
Utility to clean up Jupyter notebooks with trailing commas or other JSON5 features.
Reads one or more .ipynb files and rewrites them as strict JSON (no trailing commas).

Usage:
    python fix_notebooks.py notebook1.ipynb [notebook2.ipynb ...]
"""
import sys

try:
    import json5
except ImportError:
    sys.exit('Error: json5 package is required. Install with `pip install json5`.')
import json

def fix_notebook(path):
    """Load notebook using JSON5 tolerant parser and write back as strict JSON."""
    with open(path, 'r', encoding='utf-8') as fp:
        data = json5.load(fp)
    with open(path, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, indent=1)
    print(f'Rewritten {path}')

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for nb in sys.argv[1:]:
        fix_notebook(nb)

if __name__ == '__main__':
    main()
