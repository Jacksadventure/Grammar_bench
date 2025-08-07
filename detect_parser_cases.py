import sqlite3
import json
import tempfile
import subprocess
import os
import sys

def write_parser(code, suffix):
    """Write parser code to a temp file, return file path."""
    fd, path = tempfile.mkstemp(suffix=suffix, text=True)
    with os.fdopen(fd, 'w') as f:
        f.write(code)
    return path

def check_parse(parser_path, test_input):
    """Run parser as subprocess, return True if accepted, False if rejected."""
    try:
        result = subprocess.run(
            [sys.executable, parser_path, test_input],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        output = result.stdout.decode(errors='ignore')
        return "Input accepted." in output
    except Exception as e:
        return False

def main(db_path="targets13.db", output_path="detect_results.csv"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, failing_test_cases, passing_test_cases, original_parser, corrupted_parser FROM cases")
    rows = c.fetchall()

    with open(output_path, "w") as out:
        out.write("case_id,failing_total,failing_ok_original,failing_ok_corrupted,passing_total,passing_ok_original,passing_ok_corrupted\n")
        for row in rows:
            case_id, failing_json, passing_json, orig_code, corr_code = row
            try:
                failing_cases = json.loads(failing_json)
                passing_cases = json.loads(passing_json)
            except Exception as e:
                print(f"Error parsing test cases for case {case_id}: {e}")
                continue

            orig_path = write_parser(orig_code, "_orig.py")
            corr_path = write_parser(corr_code, "_corr.py")

            # Failing cases
            fail_total = len(failing_cases)
            fail_ok_orig = 0
            fail_ok_corr = 0
            for s in failing_cases:
                if check_parse(orig_path, s):
                    fail_ok_orig += 1
                if check_parse(corr_path, s):
                    fail_ok_corr += 1

            # Passing cases
            pass_total = len(passing_cases)
            pass_ok_orig = 0
            pass_ok_corr = 0
            for s in passing_cases:
                if check_parse(orig_path, s):
                    pass_ok_orig += 1
                if check_parse(corr_path, s):
                    pass_ok_corr += 1

            out.write(f"{case_id},{fail_total},{fail_ok_orig},{fail_ok_corr},{pass_total},{pass_ok_orig},{pass_ok_corr}\n")

            # Clean up temp files
            os.remove(orig_path)
            os.remove(corr_path)

    print(f"Detection complete. Results saved to {output_path}")

if __name__ == "__main__":
    main()
