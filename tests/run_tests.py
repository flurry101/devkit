#!/usr/bin/env python3
"""
Test runner for DevKit
Run all tests: python tests/run_tests.py
Run specific test: python tests/run_tests.py test_display
"""

import sys
import subprocess
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_tests(test_module=None):
    """Run pytest tests"""
    test_dir = Path(__file__).parent
    
    if test_module:
        test_file = test_dir / f"test_{test_module}.py"
        if test_file.exists():
            cmd = ['pytest', str(test_file), '-v']
        else:
            print(f"Test file {test_file} not found")
            return 1
    else:
        cmd = ['pytest', str(test_dir), '-v', '--tb=short']
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    return result.returncode


if __name__ == '__main__':
    test_module = sys.argv[1] if len(sys.argv) > 1 else None
    exit_code = run_tests(test_module)
    sys.exit(exit_code)

