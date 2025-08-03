import os
import json
import textwrap
from sqlite3 import connect
from pathlib import Path
from ultility import creat_repo   # make sure ultility.py is on PYTHONPATH

# --------------------------------------------------------------------------- #
# Workspace preparation
# --------------------------------------------------------------------------- #
ROOT_DIR = "repos"

os.makedirs(ROOT_DIR, exist_ok=True)
os.chdir(ROOT_DIR)

# --------------------------------------------------------------------------- #
# Database connection
# --------------------------------------------------------------------------- #
db_path = "../parser_cases.db"           # adjust if the DB lives elsewhere
conn = connect(db_path)
cursor = conn.cursor()

# Ensure the expected table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cases'")
if not cursor.fetchone():
    raise RuntimeError(f"No table named 'cases' found in {db_path}")

# --------------------------------------------------------------------------- #
# Main export loop
# --------------------------------------------------------------------------- #
query = """
SELECT id,
       original_grammar,
       corrupted_grammar,
       corrupted_parser,
       test_cases,
       num_nonterminals,
       nonterminal_prob,
       loop_prob,
       mutation_depth
FROM   cases
"""
for (
    case_id,
    original_grammar,
    corrupted_grammar,
    corrupted_parser,
    test_cases,
    num_nonterminals,
    nonterminal_prob,
    loop_prob,
    mutation_depth,
) in cursor.execute(query):

    repo_name = f"case-{case_id:05d}"
    if os.path.exists(repo_name):
        print(f"[⚠] {repo_name} already exists – skipping")
        continue

    # --------------------------------------------------------------------- #
    # Build an issue description
    # --------------------------------------------------------------------- #
    issue_body = textwrap.dedent(
        f"""
        ### Original grammar
        ```json
        {json.dumps(json.loads(original_grammar), indent=2, ensure_ascii=False)}
        ```

        ### Corrupted grammar
        ```json
        {json.dumps(json.loads(corrupted_grammar), indent=2, ensure_ascii=False)}
        ```

        ### Failing test cases
        ```json
        {json.dumps(json.loads(test_cases[:3]), indent=2, ensure_ascii=False)}
        ```

        The parser in `corrupted_generated_parser.py` should accept the
        original language but rejects the above *failing* inputs; repairing it
        so that all test cases are accepted (exit code 0) will resolve this
        issue.
        """
    ).strip()

    # --------------------------------------------------------------------- #
    # Create the repository and save parser and mutated grammar
    # --------------------------------------------------------------------- #
    repo_sub = Path(f"{repo_name}/{repo_name}")
    repo_sub.mkdir(parents=True, exist_ok=True)
    # write corrupted grammar JSON to file
    try:
        grammar_obj = json.loads(corrupted_grammar)
    except Exception:
        grammar_obj = None
    if grammar_obj is not None:
        with open(repo_sub / "corrupted_grammar.json", "w", encoding="utf-8") as gf:
            json.dump(grammar_obj, gf, ensure_ascii=False, indent=2)
    # create repo with parser code and issue description
    creat_repo(
        repo_name=repo_name,
        code=corrupted_parser,
        issue=issue_body,
    )
    print(f"[✓] Exported {repo_name}")

conn.close()
print("\nAll repositories exported successfully.")
