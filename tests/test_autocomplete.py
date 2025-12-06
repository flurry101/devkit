"""
Unit tests for autocomplete module
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from devkit import autocomplete


def test_get_snippet_completions():
    """Test getting snippet completions"""
    completions = autocomplete.get_snippet_completions()
    assert isinstance(completions, list)


def test_create_completer():
    """Test creating a completer"""
    completer = autocomplete.create_completer("")
    if autocomplete.PROMPT_TOOLKIT_AVAILABLE:
        assert completer is not None
    else:
        assert completer is None


def test_devkit_commands_list():
    """Test that DevKit commands are in the list"""
    assert 'ask' in autocomplete.DEVKIT_COMMANDS
    assert 'explain' in autocomplete.DEVKIT_COMMANDS
    assert 'status' in autocomplete.DEVKIT_COMMANDS


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

