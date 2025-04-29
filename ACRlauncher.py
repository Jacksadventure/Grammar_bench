#!/usr/bin/env python3
"""
Batch-run Auto-Code-Rover (ACR) in local-issue mode
and immediately apply its generated patch.

Directory layout (example):
  Grammar_bench/
  ├── run_acr_local.py            ← this script
  ├── repos/                      ← case-* repos (input)
  └── auto-code-rover/            ← ACR source tree
      └── acr_output/             ← will be filled by this script
"""

from pathlib import Path
import subprocess
import shlex
import os
import shutil
import sys

# --------------------------------------------------------------------------- #
# CONFIG – adjust these paths / parameters as you need
# --------------------------------------------------------------------------- #
ACR_ROOT   = Path("auto-code-rover")        # Auto-Code-Rover checkout
REPOS_ROOT = Path("repos")                  # where case-* repos live
OUTPUT_ROOT= ACR_ROOT / "acr_output"        # ACR's default output folder
MODEL      = "gpt-4o-2024-05-13"
TEMP       = "0.2"

# --------------------------------------------------------------------------- #
# HELPER: run a command and return CompletedProcess
# --------------------------------------------------------------------------- #
def run(cmd, cwd=None, env=None):
    print("[+] Running:", " ".join(shlex.quote(x) for x in cmd))
    cp = subprocess.run(cmd, cwd=cwd, env=env,
                        capture_output=True, text=True)
    return cp

# --------------------------------------------------------------------------- #
# HELPER: locate first extracted_patch_*.diff under an output tree
# --------------------------------------------------------------------------- #
def find_patch(out_dir: Path) -> Path | None:
    return next(out_dir.rglob("extracted_patch_*.diff"), None)

# --------------------------------------------------------------------------- #
# HELPER: apply a diff to corrupted_generated_parser.py
# --------------------------------------------------------------------------- #

def apply_patch(case_id: str, patch_path: Path,
                repos_root: Path = Path("repos")) -> None:
    """
    Copy corrupted_generated_parser.py → repaired_generated_parser.py
    then apply unified diff `patch_path` to the repaired copy.

    Success:  repaired_generated_parser.py written, prints ✓
    Failure:  repaired copy removed, prints ✗
    """
    # ------------------------------------------------------------------ #
    # 1. locate original file (recursive search, supports nested folders)
    # ------------------------------------------------------------------ #
    repo_root = repos_root / case_id
    matches = list(repo_root.rglob("corrupted_generated_parser.py"))
    if not matches:
        print(f"[!] corrupted_generated_parser.py not found under {case_id}")
        return
    src_file = matches[0]

    # ------------------------------------------------------------------ #
    # 2. create repaired copy
    # ------------------------------------------------------------------ #
    repaired = src_file.with_name("repaired_generated_parser.py")
    shutil.copy2(src_file, repaired)

    # ------------------------------------------------------------------ #
    # 3. apply patch in-place
    # ------------------------------------------------------------------ #
    proc = subprocess.run(
        ["patch", str(repaired), "-i", str(patch_path)],
        capture_output=True, text=True
    )

    if proc.returncode != 0:
        print(f"[✗] Patch failed for {case_id}\n{proc.stderr.strip()}")
        repaired.unlink(missing_ok=True)
        return

    rel_path = os.path.relpath(repaired.resolve(), Path.cwd())
    print(f"[✓] Patched {case_id}: {rel_path}")
# --------------------------------------------------------------------------- #
# MAIN
# --------------------------------------------------------------------------- #
def main() -> None:
    # Basic checks
    if not ACR_ROOT.exists():
        sys.exit(f"ACR_ROOT {ACR_ROOT} not found; edit script.")
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    # Iterate all case repos
    for repo_dir in sorted(REPOS_ROOT.glob("case-*")):
        issue_file = repo_dir / "issue.txt"
        if not issue_file.exists():
            print(f"[!] {issue_file} missing – skip {repo_dir.name}")
            continue

        case_id = repo_dir.name
        out_dir = OUTPUT_ROOT / case_id
        out_dir.mkdir(exist_ok=True)

        # --- build ACR command --------------------------------------------
        cmd = [
            "python", "-m", "app.main", "local-issue",
            "--output-dir", str(out_dir),
            "--model", MODEL,
            "--model-temperature", TEMP,
            "--task-id", case_id,
            "--local-repo", str(repo_dir.resolve()),
            "--issue-file", str(issue_file.resolve()),
        ]

        env = os.environ.copy()
        env["PYTHONPATH"] = str(ACR_ROOT)  # critical for 'import app ...'

        cp = run(cmd, cwd=ACR_ROOT, env=env)
        # store log no matter success or not
        (out_dir / "acr_stdout.log").write_text(
            cp.stdout + "\n--- STDERR ---\n" + cp.stderr
        )
        if cp.returncode != 0:
            print(f"[✗] ACR failed for {case_id} (code {cp.returncode})")
            continue

        # --- locate and copy patch ----------------------------------------
        patch_path = find_patch(out_dir)
        if patch_path is None:
            print(f"[!] No diff produced for {case_id}")
            continue

        # Copy patch to out_dir root if not already there
        dest_patch = out_dir / patch_path.name
        if not dest_patch.exists():
            shutil.copy2(patch_path, dest_patch)

        # --- apply patch ---------------------------------------------------
        apply_patch(case_id, dest_patch)

    print("\nAll cases processed.")

if __name__ == "__main__":
    main()
