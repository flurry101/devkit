import pytest
from click.testing import CliRunner
from pathlib import Path
import json
import shutil

from devkit.main import cli
from devkit.storage import DEVKIT_DIR, SNIPPETS_FILE

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def clean_devkit_dir():
    # Remove test devkit directory if it exists
    if DEVKIT_DIR.exists():
        shutil.rmtree(DEVKIT_DIR)
    
    # Create fresh directory
    DEVKIT_DIR.mkdir(exist_ok=True)
    
    # Create snippets file with empty dict
    with open(SNIPPETS_FILE, 'w') as f:
        json.dump({}, f)
    
    yield
    
    # Cleanup after tests
    if DEVKIT_DIR.exists():
        shutil.rmtree(DEVKIT_DIR)

def test_save_snippet(runner, clean_devkit_dir):
    # Test saving a snippet
    result = runner.invoke(cli, ['snippet', 'save', 'test', 'echo "test"'])
    assert result.exit_code == 0
    
    # Verify snippet was saved with new format
    with open(SNIPPETS_FILE, 'r') as f:
        snippets = json.load(f)
        assert 'test' in snippets
        assert snippets['test']['command'] == 'echo "test"'
        assert 'tags' in snippets['test']
        assert 'created' in snippets['test']

def test_list_snippets(runner, clean_devkit_dir):
    # Save a test snippet first
    runner.invoke(cli, ['snippet', 'save', 'test1', 'echo "test1"'])
    runner.invoke(cli, ['snippet', 'save', 'test2', 'echo "test2"'])
    
    # Test listing snippets
    result = runner.invoke(cli, ['snippet', 'list'])
    assert result.exit_code == 0
    assert 'test1' in result.output
    assert 'test2' in result.output

def test_delete_snippet(runner, clean_devkit_dir):
    # Save a test snippet
    save_result = runner.invoke(cli, ['snippet', 'save', 'test', 'echo "test"'])
    assert save_result.exit_code == 0
    
    # Verify it was saved
    with open(SNIPPETS_FILE, 'r') as f:
        snippets = json.load(f)
        assert 'test' in snippets
    
    # Delete it (need to confirm)
    result = runner.invoke(cli, ['snippet', 'delete', 'test'], input='y\n')
    assert result.exit_code == 0
    
    # Verify it's gone
    with open(SNIPPETS_FILE, 'r') as f:
        snippets = json.load(f)
        assert 'test' not in snippets

def test_no_ai_graceful_fallback(runner):
    # Test that AI commands fail gracefully when API key is not configured
    result = runner.invoke(cli, ['ask', 'how to list files'])
    assert result.exit_code == 0
    assert 'API key not configured' in result.output