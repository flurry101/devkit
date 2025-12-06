"""
Integration tests for DevKit CLI
"""

import pytest
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_cli_help():
    """Test that CLI help command works"""
    import sys
    python_cmd = sys.executable
    result = subprocess.run(
        [python_cmd, '-m', 'devkit.main', '--help'],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    assert result.returncode == 0
    assert 'DevKit' in result.stdout or 'devkit' in result.stdout.lower()


def test_cli_version():
    """Test that CLI version command works"""
    import sys
    python_cmd = sys.executable
    result = subprocess.run(
        [python_cmd, '-m', 'devkit.main', '--version'],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    assert result.returncode == 0
    assert '0.1.0' in result.stdout or 'version' in result.stdout.lower()


def test_cli_status():
    """Test that status command works"""
    import sys
    python_cmd = sys.executable
    result = subprocess.run(
        [python_cmd, '-m', 'devkit.main', 'status'],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    # Status should work even if it shows empty stats
    assert result.returncode == 0 or 'Status' in result.stdout


def test_cli_about():
    """Test that about command works"""
    import sys
    python_cmd = sys.executable
    result = subprocess.run(
        [python_cmd, '-m', 'devkit.main', 'about'],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    # About should work
    assert result.returncode == 0 or 'DevKit' in result.stdout


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

