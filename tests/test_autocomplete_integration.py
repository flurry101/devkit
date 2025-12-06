"""
Integration test for autocomplete functionality
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from devkit import autocomplete


def test_autocomplete_available():
    """Test that autocomplete module is importable"""
    assert autocomplete is not None
    assert hasattr(autocomplete, 'DEVKIT_COMMANDS')
    assert hasattr(autocomplete, 'create_completer')
    assert hasattr(autocomplete, 'get_snippet_completions')


def test_autocomplete_commands():
    """Test that autocomplete includes all main commands"""
    commands = autocomplete.DEVKIT_COMMANDS
    assert 'ask' in commands
    assert 'explain' in commands
    assert 'status' in commands
    assert 'about' in commands
    assert 'snippet' in commands


def test_autocomplete_snippet_context():
    """Test autocomplete in snippet context"""
    completer = autocomplete.create_completer("snippet")
    if autocomplete.PROMPT_TOOLKIT_AVAILABLE:
        assert completer is not None
    # If prompt_toolkit not available, completer will be None, which is fine


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

