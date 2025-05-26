#!/usr/bin/env python3
import subprocess
import os
import sys
import difflib

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    # Run test-vectors.py and capture its CSV output
    proc = subprocess.run(
        [sys.executable, 'test-vectors.py'],
        cwd=here,
        capture_output=True,
        text=True,
        check=True,
    )
    generated = proc.stdout.replace('\r\n', '\n')
    with open(os.path.join(here, 'test-vectors.csv'), 'r') as f:
        expected = f.read().replace('\r\n', '\n')
    if generated != expected:
        diff = difflib.unified_diff(
            expected.splitlines(),
            generated.splitlines(),
            fromfile='test-vectors.csv',
            tofile='generated',
            lineterm='' 
        )
        for line in diff:
            print(line)
        sys.exit(1)

if __name__ == '__main__':
    main()
