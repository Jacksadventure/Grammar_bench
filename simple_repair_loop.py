"""
A lightweight, single-threaded repair driver derived from benchmark.py.

Key constraints
---------------
1. Runs sequentially – no multiprocessing/futures.
2. Does **not** write to any database; results are printed.
3. Stores every produced file (corrupted parser, patch, repaired parser)
   in a user-supplied output directory.
4. Performs up to N (default 5) refinement loops.  
   Each new localisation prompt receives:
   • the previous patch text (if any) and  
   • any tests that were still failing.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import uuid
from pathlib import Path
from typing import List, Tuple

from localisation import localise_program

# --------------------------------------------------------------------------- #
# Utility helpers                                                             #
# --------------------------------------------------------------------------- #
def _robust_json(text: str):
    """Load JSON, fixing single-quote strings occasionally stored in DB."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(text.replace("'", '"'))


def _write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _apply_patch(target: Path, patch_text: str) -> bool:
    """
    Apply unified diff *patch_text* in-place to *target*.

    Returns True iff patch applied cleanly.
    """
    patch_file = target.with_suffix(".diff")
    _write(patch_file, patch_text)

    try:
        subprocess.run(
            ["patch", "-t", "-s", target, "-i", patch_file],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        patch_file.unlink(missing_ok=True)
        return True
    except subprocess.CalledProcessError:
        return False


# --------------------------------------------------------------------------- #
# Core logic                                                                  #
# --------------------------------------------------------------------------- #
def _generate_patch(
    parser_code: str,
    failing_tests: List[str],
    backend: str,
    model: str,
    previous_patch: str | None,
):
    """
    Call localisation.localise_program but prepend the previous patch
    (when available) to the prompt so the LLM can refine its answer.
    """
    # Manually craft the prompt because original helper lacks this feature.
    annotated = [f"{i} {ln}" for i, ln in enumerate(parser_code.splitlines(), 1)]
    prompt = (
        "parser code with line numbers:\n"
        + "\n".join(annotated)
    )
    if previous_patch:
        prompt += "\nPrevious patch:\n" + previous_patch
    prompt += "\nThis parser failed in these testcases:\n" + "\n".join(failing_tests)

    from ai_interface import AIInterface  # local import to avoid unused errors
    ai = AIInterface(backend, model)
    resp = ai.get_response(
        "You are a patch generator. Given the corrupted parser code annotated with "
        "line numbers, a previous patch (optional) and some failing tests, produce "
        "a unified diff that fixes the parser. Only output the diff.",  # short system prompt
        prompt,
    )
    return resp.response_text, resp  # patch, full resp (token counts etc.)


def _run_on_case(
    row: Tuple,
    backend: str,
    model: str,
    out_dir: Path,
    max_loops: int = 5,
):
    (
        case_id,
        _num_nt,
        _nt_prob,
        _loop_prob,
        _depth,
        _orig_grammar,
        _orig_parser,
        _corr_grammar,
        corr_parser,
        failing_json,
        passing_json,
    ) = row

    failing_tests: List[str] = _robust_json(failing_json)
    passing_tests: List[str] = _robust_json(passing_json)

    case_dir = out_dir / f"case_{case_id}"
    case_dir.mkdir(parents=True, exist_ok=True)

    # save corrupted parser
    run_id = uuid.uuid4().hex[:8]
    corrupted_file = case_dir / f"corrupted_{run_id}.py"
    _write(corrupted_file, corr_parser)

    previous_patch: str | None = None
    still_failing = list(failing_tests)  # start with provided failing tests

    for loop in range(1, max_loops + 1):
        if not still_failing:
            print(f"[Case {case_id}] All tests pass – stopping after loop {loop-1}.")
            break

        print(f"[Case {case_id}] Refinement loop {loop}: {len(still_failing)} failing tests")

        # Generate patch
        patch_text, resp = _generate_patch(
            corr_parser if loop == 1 else repaired_code,
            still_failing,
            backend,
            model,
            previous_patch,
        )
        patch_file = case_dir / f"patch_L{loop}_{run_id}.diff"
        _write(patch_file, patch_text)
        previous_patch = patch_text

        # Apply patch to a fresh copy of the corrupted parser (or last repaired)
        repaired_file = case_dir / f"repaired_L{loop}_{run_id}.py"
        if loop == 1:
            shutil.copy(corrupted_file, repaired_file)
        else:
            _write(repaired_file, repaired_code)

        if not _apply_patch(repaired_file, patch_text):
            print(f"[Case {case_id}] Patch failed to apply at loop {loop}.")
            break

        repaired_code = repaired_file.read_text(encoding="utf-8")

        # Execute tests
        def _run_tests(tests: List[str]) -> List[str]:
            failures = []
            for inp in tests:
                proc = subprocess.run(
                    [sys.executable, str(repaired_file), inp],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                if proc.returncode != 0:
                    failures.append(inp)
            return failures

        still_failing = _run_tests(still_failing)
        passing_failures = _run_tests(passing_tests)

        print(
            f"[Case {case_id}] Loop {loop} results – "
            f"original failing passed: {len(failing_tests)-len(still_failing)}/{len(failing_tests)}, "
            f"regressions: {len(passing_failures)}"
        )

        if passing_failures:
            # Regression => treat them as failing for the next loop.
            still_failing.extend(passing_failures)

    print(f"[Case {case_id}] Completed.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", type=str, default="openai")
    ap.add_argument("--model", type=str, default="o1-mini-2024-09-12")
    ap.add_argument("--db-path", type=str, default="parser_cases.db")
    ap.add_argument("--out-dir", type=str, default="simple_loop_outputs")
    ap.add_argument("--max-loops", type=int, default=5)
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(args.db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, num_nonterminals, nonterminal_prob, loop_prob, mutation_depth, "
        "       original_grammar, original_parser, corrupted_grammar, corrupted_parser, "
        "       failing_test_cases, passing_test_cases "
        "FROM cases"
    )
    rows = cur.fetchall()
    conn.close()

    print(f"Processing {len(rows)} parser cases sequentially…")
    for row in rows:
        _run_on_case(row, args.backend, args.model, out_dir, args.max_loops)


if __name__ == "__main__":
    main()
