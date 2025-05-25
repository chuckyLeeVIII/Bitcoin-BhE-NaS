#!/usr/bin/env python3
"""Simple check script to verify BIP340 test vectors.

This runs ``test-vectors.py`` to regenerate the CSV data and compares the
result with ``test-vectors.csv``. The script exits with a non-zero status if
the files differ.
"""

import subprocess
import sys
import difflib
from pathlib import Path

# Paths relative to repository root
BASE_DIR = Path(__file__).resolve().parent
TEST_VECTOR_SCRIPT = BASE_DIR / "test-vectors.py"
EXPECTED_CSV = BASE_DIR / "test-vectors.csv"

# Run the generator script and capture its CSV output
result = subprocess.run(
    [sys.executable, str(TEST_VECTOR_SCRIPT)],
    capture_output=True,
    text=True,
)

if result.returncode != 0:
    print(result.stdout)
    print(result.stderr, file=sys.stderr)
    sys.exit(result.returncode)

# Normalize line endings and strip trailing whitespace
output = result.stdout.strip().splitlines()
expected = EXPECTED_CSV.read_text().strip().splitlines()

if output != expected:
    print("Generated test vectors do not match test-vectors.csv", file=sys.stderr)
    diff = difflib.unified_diff(
        expected,
        output,
        fromfile="test-vectors.csv",
        tofile="generated",
        lineterm="",
    )
    for line in diff:
        print(line)
    sys.exit(1)

print("Test vectors match." )

