"""
Unit tests for display module
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from devkit import display
from devkit import storage


def test_show_intro_once():
    """Test that intro shows only once"""
    # Reset intro state
    config = storage.load_config()
    config['intro_shown'] = False
    storage.save_config(config)
    
    # First call should show intro
    display.show_intro_once()
    
    # Check that it's marked as shown
    config = storage.load_config()
    assert config.get('intro_shown', False) == True
    
    # Second call should not show intro again
    # (We can't easily test the actual display, but we can test the state)
    display.show_intro_once()
    config = storage.load_config()
    assert config.get('intro_shown', False) == True


def test_format_numbered_lists():
    """Test numbered list formatting"""
    text = "1. First item\n2. Second item\n3. Third item"
    formatted = display.format_numbered_lists(text)
    assert "1. " in formatted
    assert "2. " in formatted
    assert "3. " in formatted


def test_format_ai_response():
    """Test AI response formatting"""
    response = """COMMAND: find . -name "*.py"
EXPLANATION: This command finds all Python files
DETAILED_NOTES: Useful for searching codebases
CITATIONS: man find"""
    
    formatted = display.format_ai_response(response, "test query")
    assert "COMMAND:" not in formatted  # Should be formatted
    assert "find . -name" in formatted
    assert "CITATIONS" in formatted or "Official Documentation" in formatted


def test_get_console():
    """Test console instance creation"""
    console = display.get_console()
    assert console is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

