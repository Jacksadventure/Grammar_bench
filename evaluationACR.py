#!/usr/bin/env python3
"""
Verify repaired_generated_parser.py for each case using
test_cases stored in parser_cases.db.

Run:  python verify_repairs_db.py
"""

import json
import subprocess
from pathlib import Path
from sqlite3 import connect
import os
from typing import List

DB_PATH     = Path("parser_cases.db")
REPOS_ROOT  = Path("repos")
PYTHON_BIN  = "python"      # or full path to your interpreter


# ------------------------------------------------------------- #
# helpers
# ------------------------------------------------------------- #
def run_parser(parser: Path, sample: str) -> bool:
    """Return True if parser exits 0 on sample."""
    proc = subprocess.run([PYTHON_BIN, str(parser), sample],
                          stdout=subprocess.PIPE)
    return proc.returncode == 0

def find_repaired(case_id: str) -> Path | None:
    """Recursive search for repaired_generated_parser.py under repo."""
    repo_root = REPOS_ROOT / case_id
    matches = list(repo_root.rglob("repaired_generated_parser.py"))
    return matches[0] if matches else None


# ------------------------------------------------------------- #
# main logic
# ------------------------------------------------------------- #
def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit(f"{DB_PATH} not found")

    conn = connect(DB_PATH)
    cur  = conn.cursor()

    total_cases, total_passed = 0, 0

    for row in cur.execute("SELECT id, test_cases FROM cases"):
        db_id, tc_json = row
        case_id = f"case-{db_id:05d}"

        repaired = find_repaired(case_id)
        if not repaired:
            print(f"[!] {case_id}: repaired parser not found – skip")
            continue

        try:
            test_cases: List[str] = json.loads(tc_json)
        except json.JSONDecodeError:
            print(f"[!] {case_id}: malformed test_cases JSON – skip")
            continue

        # run all samples
        total_cases += 1
        failures = [s for s in test_cases if not run_parser(repaired, s)]

        if not failures:
            total_passed += 1
            print(f"[✓] {case_id}: {len(test_cases)} / {len(test_cases)} passed")
        else:
            print(f"[✗] {case_id}: {len(failures)} / {len(test_cases)} failed")
            for s in failures[:5]:
                short = s[:60] + ("…" if len(s) > 60 else "")
                print("    -", short)

    conn.close()

    # summary
    print("\n=== SUMMARY ===")
    print(f"verified {total_cases} cases  |  "
          f"{total_passed} fully passed  |  "
          f"{total_cases - total_passed} had failures")


if __name__ == "__main__":
    main()