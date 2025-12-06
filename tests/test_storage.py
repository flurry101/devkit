"""
Unit tests for storage module
"""

import pytest
import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from devkit import storage


def test_load_snippets_empty():
    """Test loading snippets when file doesn't exist"""
    # This will use the default empty dict
    snippets = storage.load_snippets()
    assert isinstance(snippets, dict)


def test_save_and_load_snippets():
    """Test saving and loading snippets"""
    # Ensure directory exists
    storage.DEVKIT_DIR.mkdir(exist_ok=True)
    
    test_snippets = {
        'test1': {
            'command': 'echo hello',
            'tags': ['test'],
            'created': '2024-01-01T00:00:00'
        }
    }
    
    storage.save_snippets(test_snippets)
    loaded = storage.load_snippets()
    
    assert 'test1' in loaded
    assert loaded['test1']['command'] == 'echo hello'


def test_load_config():
    """Test loading configuration"""
    config = storage.load_config()
    assert isinstance(config, dict)
    assert 'api_key' in config or 'time_travel_enabled' in config


def test_save_config():
    """Test saving configuration"""
    # Ensure directory exists
    storage.DEVKIT_DIR.mkdir(exist_ok=True)
    
    config = storage.load_config()
    config['test_key'] = 'test_value'
    storage.save_config(config)
    
    loaded = storage.load_config()
    assert loaded.get('test_key') == 'test_value'


def test_log_command():
    """Test logging a command"""
    # Ensure directory exists
    storage.DEVKIT_DIR.mkdir(exist_ok=True)
    
    storage.log_command("test command", "test output", 0)
    history = storage.load_history()
    
    assert len(history) > 0
    assert history[-1]['command'] == "test command"
    assert history[-1]['exit_code'] == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

