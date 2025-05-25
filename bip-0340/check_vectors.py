import os
import sys
import subprocess


def main():
    script_dir = os.path.dirname(__file__)
    test_vectors_py = os.path.join(script_dir, "test-vectors.py")
    csv_path = os.path.join(script_dir, "test-vectors.csv")

    result = subprocess.run([sys.executable, test_vectors_py], capture_output=True, text=True, check=True)
    generated_lines = [line.rstrip() for line in result.stdout.splitlines()]
    with open(csv_path, "r") as f:
        existing_lines = [line.rstrip() for line in f.readlines()]

    if generated_lines != existing_lines:
        sys.stderr.write("test-vectors.csv is out of date. Run test-vectors.py to regenerate.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
