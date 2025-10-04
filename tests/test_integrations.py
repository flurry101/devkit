"""Integration tests covering all demo commands"""
import pytest
from click.testing import CliRunner
from devkit.main import cli

@pytest.fixture
def runner():
    return CliRunner()

def test_full_workflow(runner):
    """Test complete user workflow"""
    
    # 1. Save snippet
    result = runner.invoke(cli, ['snippet', 'save', 'test-cmd', 'echo "test"', '--tags', 'demo,test'])
    assert result.exit_code == 0
    assert "Saved snippet" in result.output
    
    # 2. List snippets
    result = runner.invoke(cli, ['snippet', 'list'])
    assert result.exit_code == 0
    assert "test-cmd" in result.output
    
    # 3. Search snippets
    result = runner.invoke(cli, ['snippet', 'search', 'test'])
    assert result.exit_code == 0
    assert "test-cmd" in result.output
    
    # 4. Get snippet
    result = runner.invoke(cli, ['snippet', 'get', 'test-cmd'])
    assert result.exit_code == 0
    assert "echo" in result.output
    
    # 5. Export snippets
    result = runner.invoke(cli, ['snippet', 'export', 'test_export.json'])
    assert result.exit_code == 0
    
    # 6. Delete snippet
    result = runner.invoke(cli, ['snippet', 'delete', 'test-cmd'], input='y\n')
    assert result.exit_code == 0

def test_workspace_init(runner):
    """Test workspace initialization"""
    result = runner.invoke(cli, ['init'])
    assert result.exit_code == 0 or "already exists" in result.output

def test_status_command(runner):
    """Test status display"""
    result = runner.invoke(cli, ['status'])
    assert result.exit_code == 0
    assert "DevKit Status" in result.output