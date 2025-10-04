"""
Emergency rollback module
Detects dangerous commands and suggests rollback
"""

from typing import List, Dict, Any
from .storage import load_history
import click

# Optional AI features
try:
    from .ai import suggest_rollback
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


# Keywords that indicate potentially dangerous operations
DANGEROUS_KEYWORDS = [
    'deploy', 'push', 'delete', 'drop', 'rm', 'remove',
    'prune', 'migrate', 'rollout', 'apply', 'destroy',
    'shutdown', 'reboot', 'kill', 'force', 'production',
    'prod', 'master', 'main'
]


def is_dangerous_command(command: str) -> bool:
    """Check if a command is potentially dangerous"""
    command_lower = command.lower()
    return any(keyword in command_lower for keyword in DANGEROUS_KEYWORDS)


def find_recent_dangerous_commands(limit: int = 10) -> List[Dict[str, Any]]:
    """Find recent dangerous commands in history"""
    history = load_history()
    
    if not history:
        return []
    
    recent = history[-limit:]
    dangerous = [entry for entry in recent if is_dangerous_command(entry['command'])]
    
    return dangerous


def show_panic_mode() -> None:
    """Emergency rollback mode - show recent dangerous commands and suggest rollback"""
    click.echo("\n🚨 PANIC MODE - Emergency Rollback Assistant\n")
    
    dangerous = find_recent_dangerous_commands(limit=20)
    
    if not dangerous:
        click.echo("✅ No recent dangerous commands detected.")
        click.echo("You're probably fine! 😅\n")
        return
    
    click.echo("⚠️  Recent potentially dangerous commands:")
    click.echo("=" * 70)
    
    for i, entry in enumerate(dangerous, 1):
        click.echo(f"\n{i}. {entry['command']}")
        click.echo(f"   Time: {entry['timestamp']}")
        click.echo(f"   Status: {'✅ Success' if entry['exit_code'] == 0 else '❌ Failed'}")
    
    click.echo("\n" + "=" * 70)
    
    # Ask AI for rollback suggestions if available
    if AI_AVAILABLE and click.confirm("\n🤖 Get AI-powered rollback suggestions?", default=True):
        click.echo("\n🔍 Analyzing and generating rollback steps...\n")
        
        suggestions = suggest_rollback(dangerous)
        
        click.echo("=" * 70)
        click.echo(suggestions)
        click.echo("=" * 70)
        
        click.echo("\n⚠️  WARNING: Review these suggestions carefully before running!")
        click.echo("Always test rollback in staging first if possible.\n")
    else:
        click.echo("\nℹ️  AI-powered analysis not available. Using built-in patterns:")
        for entry in dangerous:
            quick_rollback_suggestions(entry['command'])


def quick_rollback_suggestions(command: str) -> None:
    """Give quick rollback suggestions for a specific command"""
    click.echo(f"\n🔄 Quick rollback suggestions for: {command}\n")
    
    # Common rollback patterns
    if 'git push' in command:
        click.echo("Git Push Rollback:")
        click.echo("  1. git revert HEAD")
        click.echo("  2. git push origin <branch>")
        click.echo("  Or: git reset --hard HEAD~1 && git push --force (dangerous!)")
    
    elif 'docker' in command and 'deploy' in command:
        click.echo("Docker Deploy Rollback:")
        click.echo("  1. docker ps -a  # Find container ID")
        click.echo("  2. docker stop <container-id>")
        click.echo("  3. docker start <previous-container-id>")
    
    elif 'kubectl' in command:
        click.echo("Kubernetes Rollback:")
        click.echo("  kubectl rollout undo deployment/<name>")
        click.echo("  kubectl rollout status deployment/<name>")
    
    elif 'npm' in command and 'publish' in command:
        click.echo("NPM Publish Rollback:")
        click.echo("  npm unpublish <package>@<version>")
        click.echo("  (Note: Only works within 72 hours)")
    
    elif 'migrate' in command:
        click.echo("Database Migration Rollback:")
        click.echo("  Check your migration tool's documentation")
        click.echo("  Common: npm run migrate:down or rake db:rollback")
    
    else:
        click.echo("No specific rollback pattern found.")
        click.echo("Use 'devkit panic' for AI-powered suggestions!")
    
    click.echo()


def show_dangerous_patterns() -> None:
    """Show patterns of dangerous commands in history"""
    history = load_history()
    
    if not history:
        click.echo("No history available.")
        return
    
    # Count dangerous commands
    dangerous_count = sum(1 for entry in history if is_dangerous_command(entry['command']))
    total_count = len(history)
    
    percentage = (dangerous_count / total_count * 100) if total_count > 0 else 0
    
    click.echo(f"\n📊 Dangerous Command Statistics:")
    click.echo("=" * 70)
    click.echo(f"Total commands: {total_count}")
    click.echo(f"Dangerous commands: {dangerous_count} ({percentage:.1f}%)")
    
    # Most common dangerous keywords
    keyword_counts = {}
    for entry in history:
        if is_dangerous_command(entry['command']):
            for keyword in DANGEROUS_KEYWORDS:
                if keyword in entry['command'].lower():
                    keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
    
    if keyword_counts:
        click.echo("\nMost common risky operations:")
        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        for keyword, count in sorted_keywords[:5]:
            click.echo(f"  - {keyword}: {count} times")
    
    click.echo()