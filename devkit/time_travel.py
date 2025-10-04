"""
Time-travel debugging module
Allows rewinding and analyzing command history
"""

from datetime import datetime
from typing import List, Dict, Any
from .storage import load_history, log_command
import click

# Optional AI features
try:
    from .ai import analyze_history
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


def show_history(limit: int = 10) -> None:
    """Display recent command history"""
    history = load_history()
    
    if not history:
        click.echo("No command history yet. Run some commands first!")
        return
    
    recent = history[-limit:]
    
    click.echo(f"\n⏰ Command History (last {len(recent)} commands):")
    click.echo("=" * 70)
    
    for i, entry in enumerate(recent, 1):
        timestamp = entry['timestamp']
        command = entry['command']
        exit_code = entry['exit_code']
        
        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%H:%M:%S")
        except:
            time_str = timestamp
        
        # Status indicator
        status = "✅" if exit_code == 0 else "❌"
        
        click.echo(f"\n{i}. [{time_str}] {status} {command}")
        
        if exit_code != 0:
            click.echo(f"   Exit code: {exit_code}")


def analyze_recent_history() -> None:
    """Analyze recent history with AI to find issues"""
    if not AI_AVAILABLE:
        click.echo("❌ AI features are not available - anthropic package not installed")
        return
        
    history = load_history()
    
    if not history:
        click.echo("No command history to analyze yet.")
        return
    
    click.echo("\n🔍 Analyzing recent commands with AI...\n")
    
    # Get AI analysis
    analysis = analyze_history(history)
    
    click.echo("=" * 70)
    click.echo(analysis)
    click.echo("=" * 70)


def find_failures() -> List[Dict[str, Any]]:
    """Find all failed commands in history"""
    history = load_history()
    failures = [entry for entry in history if entry['exit_code'] != 0]
    return failures


def show_failures() -> None:
    """Display all failed commands"""
    failures = find_failures()
    
    if not failures:
        click.echo("✅ No failed commands in history!")
        return
    
    click.echo(f"\n❌ Found {len(failures)} failed command(s):")
    click.echo("=" * 70)
    
    for i, entry in enumerate(failures, 1):
        timestamp = entry['timestamp']
        command = entry['command']
        exit_code = entry['exit_code']
        
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            time_str = timestamp
        
        click.echo(f"\n{i}. [{time_str}]")
        click.echo(f"   Command: {command}")
        click.echo(f"   Exit code: {exit_code}")
        
        if entry.get('output'):
            click.echo(f"   Output: {entry['output'][:200]}...")


def rewind_to_state(steps: int = 1) -> None:
    """Show what commands to run to rewind N steps"""
    history = load_history()
    
    if len(history) < steps:
        click.echo(f"Only {len(history)} commands in history, can't rewind {steps} steps.")
        return
    
    click.echo(f"\n⏪ To rewind {steps} step(s), you might need to:")
    click.echo("=" * 70)
    
    recent = history[-steps:]
    
    for entry in reversed(recent):
        command = entry['command']
        click.echo(f"\nUndo: {command}")
        click.echo("  (No automatic undo available - review and revert manually)")
    
    click.echo("\n💡 Use 'devkit panic' for AI-powered rollback suggestions!")