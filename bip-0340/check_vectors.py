import difflib
import os
import subprocess
import sys


def main() -> None:
    script_dir = os.path.dirname(__file__)
    test_vectors_py = os.path.join(script_dir, "test-vectors.py")
    csv_path = os.path.join(script_dir, "test-vectors.csv")

    result = subprocess.run(
        [sys.executable, test_vectors_py], capture_output=True, text=True, check=True
    )
    generated_lines = result.stdout.splitlines()
    with open(csv_path, "r", newline="") as f:
        existing_lines = f.read().splitlines()

    if generated_lines != existing_lines:
        diff = difflib.unified_diff(
            existing_lines,
            generated_lines,
            fromfile="test-vectors.csv",
            tofile="generated",
            lineterm="",
        )
        sys.stderr.write("\n".join(diff) + "\n")
        sys.stderr.write(
            "test-vectors.csv is out of date. Run test-vectors.py to regenerate.\n"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()

