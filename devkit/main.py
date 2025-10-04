"""
DevKit - AI-Powered Terminal Assistant
Main CLI entry point with all commands
"""

import click
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Import colorama for colored output
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    # Fallback if colorama is not available
    class Fore:
        GREEN = RED = YELLOW = BLUE = CYAN = MAGENTA = WHITE = ""
    class Style:
        RESET_ALL = BRIGHT = DIM = ""
    COLORS_AVAILABLE = False

# Import our modules
from . import storage
from . import time_travel
from . import rollback

# Optional AI module
try:
    from . import ai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# Main CLI Group
@click.group()
@click.version_option(version="0.1.0")
def cli():
    """DevKit - AI-powered terminal assistant for developers
    
    Your companion for terminal operations:
    - Save and run code snippets
    - Get AI command suggestions
    - Write better git commits
    - Time-travel debugging
    - Emergency rollback assistance
    
    Get started: devkit --help
    """
    pass

# ============================================================================
# Snippet Commands
# ============================================================================

@cli.group()
def snippet():
    """Manage code snippets
    
    Save and run frequently used commands.
    Example: devkit snippet save docker-clean "docker system prune -a"
    """
    pass

@snippet.command('save')
@click.argument('name')
@click.argument('command')
@click.option('--tags', help='Comma-separated tags for the snippet')
def snippet_save(name: str, command: str, tags: str):
    """Save a new snippet with optional tags"""
    snippets = storage.load_snippets()
    
    # Check if snippet already exists
    if name in snippets:
        if not click.confirm(f"Snippet {name} already exists. Overwrite?"):
            return
    
    # Parse tags
    tag_list = []
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
    
    # Save snippet with metadata
    snippets[name] = {
        'command': command,
        'tags': tag_list,
        'created': datetime.now().isoformat()
    }
    storage.save_snippets(snippets)
    
    tag_info = f" (tags: {', '.join(tag_list)})" if tag_list else ""
    click.echo(f"{Fore.GREEN}✅ Saved snippet: {name}{tag_info}{Style.RESET_ALL}")

@snippet.command('list')
@click.option('--tag', help='Filter snippets by tag')
def snippet_list(tag: str):
    """List all saved snippets, optionally filtered by tag"""
    snippets = storage.load_snippets()
    
    if not snippets:
        click.echo("No snippets saved yet!")
        return
    
    # Filter by tag if specified
    if tag:
        filtered_snippets = {}
        for name, data in snippets.items():
            if tag.lower() in [t.lower() for t in data.get('tags', [])]:
                filtered_snippets[name] = data
        snippets = filtered_snippets
        
        if not snippets:
            click.echo(f"No snippets found with tag '{tag}'")
            return
    
    click.echo(f"\n📋 Saved Snippets ({len(snippets)} total):")
    click.echo("=" * 70)
    
    for name, data in snippets.items():
        command = data.get('command', '')
        tags = data.get('tags', [])
        
        click.echo(f"\n{Fore.CYAN}{name}{Style.RESET_ALL}")
        click.echo(f"  {Fore.WHITE}{command}{Style.RESET_ALL}")
        
        if tags:
            tag_str = ', '.join(tags)
            click.echo(f"  {Fore.YELLOW}Tags: {tag_str}{Style.RESET_ALL}")
    
    click.echo()

@snippet.command('search')
@click.argument('query')
def snippet_search(query: str):
    """Search snippets by name, command content, or tags"""
    snippets = storage.load_snippets()
    
    if not snippets:
        click.echo(f"{Fore.YELLOW}No snippets to search.{Style.RESET_ALL}")
        return
    
    # Search in name, command content, and tags
    results = {}
    for name, data in snippets.items():
        command = data.get('command', '')
        tags = data.get('tags', [])
        tag_str = ' '.join(tags)
        
        if (query.lower() in name.lower() or 
            query.lower() in command.lower() or
            query.lower() in tag_str.lower()):
            results[name] = data
    
    if not results:
        click.echo(f"{Fore.YELLOW}No snippets found matching '{query}'.{Style.RESET_ALL}")
        return
    
    click.echo(f"\n🔍 Search results for '{query}' ({len(results)} found):")
    click.echo("=" * 70)
    
    for name, data in results.items():
        command = data.get('command', '')
        tags = data.get('tags', [])
        
        click.echo(f"\n{Fore.CYAN}{name}{Style.RESET_ALL}")
        click.echo(f"  {Fore.WHITE}{command}{Style.RESET_ALL}")
        
        if tags:
            tag_str = ', '.join(tags)
            click.echo(f"  {Fore.YELLOW}Tags: {tag_str}{Style.RESET_ALL}")
    
    click.echo("\n" + "=" * 70)

@snippet.command('export')
@click.argument('filename')
@click.option('--format', 'export_format', type=click.Choice(['json', 'txt']), default='json', help='Export format')
def snippet_export(filename: str, export_format: str):
    """Export snippets to a file"""
    import json
    snippets = storage.load_snippets()
    
    if not snippets:
        click.echo(f"{Fore.YELLOW}No snippets to export.{Style.RESET_ALL}")
        return
    
    try:
        if export_format == 'json':
            with open(filename, 'w') as f:
                json.dump(snippets, f, indent=2)
        else:  # txt format
            with open(filename, 'w') as f:
                for name, data in snippets.items():
                    command = data.get('command', '')
                    tags = data.get('tags', [])
                    f.write(f"# {name}\n")
                    if tags:
                        f.write(f"# Tags: {', '.join(tags)}\n")
                    f.write(f"{command}\n\n")
        
        click.echo(f"{Fore.GREEN}✅ Exported {len(snippets)} snippets to {filename}{Style.RESET_ALL}")
    except Exception as e:
        click.echo(f"{Fore.RED}❌ Export failed: {str(e)}{Style.RESET_ALL}")

@snippet.command('import')
@click.argument('filename')
@click.option('--overwrite', is_flag=True, help='Overwrite existing snippets with same names')
def snippet_import(filename: str, overwrite: bool):
    """Import snippets from a file"""
    import json
    import os
    
    if not os.path.exists(filename):
        click.echo(f"{Fore.RED}❌ File {filename} not found.{Style.RESET_ALL}")
        return
    
    try:
        with open(filename, 'r') as f:
            if filename.endswith('.json'):
                imported_snippets = json.load(f)
            else:  # txt format
                imported_snippets = {}
                content = f.read()
                # Simple parsing for txt format
                lines = content.split('\n')
                current_name = None
                current_command = []
                
                for line in lines:
                    if line.startswith('# '):
                        if current_name and current_command:
                            imported_snippets[current_name] = '\n'.join(current_command)
                        current_name = line[2:].strip()
                        current_command = []
                    elif line.strip() and current_name:
                        current_command.append(line)
                
                if current_name and current_command:
                    imported_snippets[current_name] = '\n'.join(current_command)
        
        # Load existing snippets
        existing_snippets = storage.load_snippets()
        
        # Check for conflicts
        conflicts = []
        for name in imported_snippets:
            if name in existing_snippets and not overwrite:
                conflicts.append(name)
        
        if conflicts:
            click.echo(f"{Fore.YELLOW}⚠️  Found {len(conflicts)} conflicting snippets:{Style.RESET_ALL}")
            for name in conflicts:
                click.echo(f"  - {name}")
            if not click.confirm("Use --overwrite to replace them, or skip?"):
                return
        
        # Import snippets
        imported_count = 0
        for name, command in imported_snippets.items():
            if name not in existing_snippets or overwrite:
                existing_snippets[name] = command
                imported_count += 1
        
        storage.save_snippets(existing_snippets)
        click.echo(f"{Fore.GREEN}✅ Imported {imported_count} snippets from {filename}{Style.RESET_ALL}")
        
    except Exception as e:
        click.echo(f"{Fore.RED}❌ Import failed: {str(e)}{Style.RESET_ALL}")

@snippet.command('delete')
@click.argument('name')
def snippet_delete(name: str):
    """Delete a saved snippet"""
    try:
        snippets = storage.load_snippets()
        
        if name not in snippets:
            click.echo(f"{Fore.RED}❌ Snippet {name} not found!{Style.RESET_ALL}")
            return
        
        del snippets[name]
        storage.save_snippets(snippets)
        click.echo(f"{Fore.GREEN}✅ Deleted snippet: {name}{Style.RESET_ALL}")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        sys.exit(1)

@snippet.command('get')
@click.argument('name')
def snippet_get(name: str):
    """Show a specific snippet"""
    snippets = storage.load_snippets()
    
    if name not in snippets:
        click.echo(f"{Fore.RED}❌ Snippet {name} not found!{Style.RESET_ALL}")
        
        # Suggest similar names
        similar = [n for n in snippets.keys() if name.lower() in n.lower()]
        if similar:
            click.echo(f"\n{Fore.YELLOW}Did you mean: {', '.join(similar)}{Style.RESET_ALL}")
        
        return
    
    data = snippets[name]
    command = data.get('command', '')
    tags = data.get('tags', [])
    created = data.get('created', '')
    
    click.echo(f"\n{Fore.CYAN}📝 Snippet: {name}{Style.RESET_ALL}")
    click.echo(f"{Fore.WHITE}Command: {command}{Style.RESET_ALL}")
    
    if tags:
        tag_str = ', '.join(tags)
        click.echo(f"{Fore.YELLOW}Tags: {tag_str}{Style.RESET_ALL}")
    
    if created:
        try:
            dt = datetime.fromisoformat(created)
            created_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            click.echo(f"{Fore.BLUE}Created: {created_str}{Style.RESET_ALL}")
        except:
            pass
    
    click.echo()

@snippet.command('run')
@click.argument('name')
def snippet_run(name: str):
    """Run a saved snippet"""
    snippets = storage.load_snippets()
    
    if name not in snippets:
        click.echo(f"{Fore.RED}❌ Snippet {name} not found!{Style.RESET_ALL}")
        return
        
    data = snippets[name]
    command = data.get('command', '')
    click.echo(f"{Fore.BLUE}🚀 Running: {command}{Style.RESET_ALL}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout + result.stderr # Log to History
    storage.log_command(command, output, result.returncode)
    
    if result.returncode != 0:
        click.echo(f"{Fore.RED}❌ Command failed with exit code {result.returncode}{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.GREEN}✅ Command completed successfully{Style.RESET_ALL}")

# ============================================================================
# AI Commands
# ============================================================================

@cli.command()
@click.argument('query', nargs=-1, required=True)
def ask(query):
    """Ask AI for a command suggestion
    
    Example: devkit ask how do I find large files
    """
    if not AI_AVAILABLE:
        click.echo("❌ AI features are not available - google-generativeai package not installed")
        return
        
    query_str = ' '.join(query)
    click.echo(f"\n🤖 Finding command for: {query_str}\n")
    
    response = ai.ask_command(query_str)
    click.echo(response)
    
    # Parse response to extract command if possible
    if "COMMAND:" in response:
        lines = response.split('\n')
        for line in lines:
            if line.startswith("COMMAND:"):
                command = line.replace("COMMAND:", "").strip()
                if click.confirm(f"\n💾 Save this as a snippet?", default=False):
                    name = click.prompt("Snippet name", type=str)
                    snippets = storage.load_snippets()
                    snippets[name] = command
                    storage.save_snippets(snippets)
                    click.echo(f"Saved as '{name}'")
                break
    
    click.echo()


@cli.command()
@click.argument('command', nargs=-1, required=True)
def explain(command):
    """Explain what a command does

    Example: devkit explain docker run -p 8080:80 nginx
    """
    if not AI_AVAILABLE:
        click.echo("❌ AI features are not available - google-generativeai package not installed")
        return
        
    command_str = ' '.join(command)
    click.echo(f"\n🔍 Explaining: {command_str}\n")
    
    explanation = ai.explain_command(command_str)
    
    click.echo("=" * 70)
    click.echo(explanation)
    click.echo("=" * 70)
    click.echo()


# ============================================================================
# Commit Commands
# ============================================================================

@cli.command()
@click.option('--ai', 'ai_mode', is_flag=True, help='Use AI to generate commit message from diff')
def commit(ai_mode):
    """Create a conventional commit message
    
    Interactive mode (default): Prompts for type, scope, description
    AI mode (--ai): Analyzes git diff and generates message
    
    Example: devkit commit
    Example: devkit commit --ai
    """
    # Check if we're in a git repo
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError:
        click.echo("❌ Not in a git repository!")
        return
    
    if ai_mode:
        # AI-powered commit
        click.echo("\n🤖 Generating commit message from your changes...\n")
        
        # Get git diff
        try:
            result = subprocess.run(
                ["git", "diff", "--staged"],
                capture_output=True,
                text=True,
                check=True
            )
            diff = result.stdout
            if not diff:
                click.echo("❌ No staged changes found.")
                click.echo("Run 'git add <files>' first, then try again.\n")
                return
            
            # Generate commit message with AI
            commit_msg = ai.generate_commit_message(diff)
            
            if commit_msg.startswith("❌"):
                click.echo(commit_msg)
                return
            
            click.echo("📋 AI-generated commit message:")
            click.echo(f"   {commit_msg}\n")
            
            if click.confirm("Use this commit message?", default=True):
                try:
                    subprocess.run(
                        ["git", "commit", "-m", commit_msg],
                        check=True
                    )
                    click.echo("✅ Commit created successfully!")
                    storage.log_command(f"git commit -m \"{commit_msg}\"", "Commit created", 0)
                except subprocess.CalledProcessError as e:
                    click.echo(f"❌ Git commit failed: {e}")
            else:
                click.echo("❌ Commit cancelled")
        
        except Exception as e:
            click.echo(f"❌ Error: {e}")
        
        return
    
    # Interactive mode (original)
    click.echo("\n📝 Conventional Commit Helper\n")
    
    # Commit type
    click.echo("Select commit type:")
    types = {
        '1': 'feat',
        '2': 'fix',
        '3': 'docs',
        '4': 'style',
        '5': 'refactor',
        '6': 'test',
        '7': 'chore'
    }
    
    for key, value in types.items():
        descriptions = {
            'feat': '✨ New feature',
            'fix': '🐛 Bug fix',
            'docs': '📝 Documentation',
            'style': '💄 Code style/formatting',
            'refactor': '♻️  Code refactoring',
            'test': '✅ Tests',
            'chore': '🔧 Maintenance'
        }
        click.echo(f"  {key}. {value:10} - {descriptions[value]}")
    
    type_choice = click.prompt("\nType", type=str, default='1')
    commit_type = types.get(type_choice, 'feat')
    
    # Scope (optional)
    scope = click.prompt("Scope (optional, press Enter to skip)", default="", show_default=False)
    
    # Description
    description = click.prompt("Short description", type=str)
    
    # Build commit message
    if scope:
        commit_msg = f"{commit_type}({scope}): {description}"
    else:
        commit_msg = f"{commit_type}: {description}"
    
    # Preview
    click.echo(f"\n📋 Commit message:")
    click.echo(f"   {commit_msg}\n")
    
    # Confirm
    if click.confirm("Create this commit?", default=True):
        try:
            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                check=True
            )
            click.echo("✅ Commit created successfully!")
            storage.log_command(f"git commit -m \"{commit_msg}\"", "Commit created", 0)
        except subprocess.CalledProcessError as e:
            click.echo(f"❌ Git commit failed: {e}")
    else:
        click.echo("❌ Commit cancelled")


# ============================================================================
# Time-Travel Debugging Commands
# ============================================================================

@cli.command()
@click.option('--limit', '-n', default=10, help='Number of commands to show')
@click.option('--analyze', is_flag=True, help='Analyze history with AI')
@click.option('--failures', is_flag=True, help='Show only failed commands')
def rewind(limit, analyze, failures):
    """Time-travel debugging - view and analyze command history
    
    Examples:
      devkit rewind              Show last 10 commands
      devkit rewind -n 20        Show last 20 commands
      devkit rewind --analyze    AI analysis of recent commands
      devkit rewind --failures   Show only failed commands
    """
    if analyze:
        time_travel.analyze_recent_history()
    elif failures:
        time_travel.show_failures()
    else:
        time_travel.show_history(limit)


@cli.command()
@click.option('--stats', is_flag=True, help='Show dangerous command statistics')
def panic(stats):
    """🚨 Emergency rollback assistant
    
    Detects recent dangerous commands and suggests rollback steps.
    Use this when you just deployed something and it broke!
    
    Examples:
      devkit panic         Get rollback suggestions
      devkit panic --stats Show dangerous command statistics
    """
    if stats:
        rollback.show_dangerous_patterns()
    else:
        rollback.show_panic_mode()


# ============================================================================
# Configuration Commands
# ============================================================================

@cli.command()
@click.option('--api-key', help='Set Gemini API key')
def config(api_key):
    """Configure DevKit settings
    
    Example: devkit config --api-key AIza...
    """
    if api_key:
        config_data = storage.load_config()
        config_data['api_key'] = api_key
        storage.save_config(config_data)
        click.echo("✅ API key saved to ~/.devkit/config.json")
    else:
        click.echo("\n⚙️  Current Configuration:")
        click.echo("=" * 50)
        
        config_data = storage.load_config()
        api_key_stored = config_data.get('api_key')
        
        if api_key_stored:
            click.echo(f"API Key: {api_key_stored[:20]}... (stored)")
        else:
            import os
            env_key = os.getenv("GEMINI_API_KEY")
            if env_key:
                click.echo(f"API Key: {env_key[:20]}... (from environment)")
            else:
                click.echo("API Key: Not configured")
        
        click.echo(f"\nHistory logging: {'Enabled' if config_data.get('time_travel_enabled', True) else 'Disabled'}")
        click.echo(f"Max history: {config_data.get('max_history', 100)} commands")
        click.echo("\n" + "=" * 50)
        click.echo("\nTo set API key: devkit config --api-key <your-key>")
        click.echo("Or set environment variable: export GEMINI_API_KEY=<your-key>\n")


@cli.command()
def status():
    """Show DevKit status and statistics"""
    click.echo("\n📊 DevKit Status")
    click.echo("=" * 70)
    
    # Snippets
    snippets = storage.load_snippets()
    click.echo(f"\n📝 Snippets: {len(snippets)} saved")
    
    # History
    history = storage.load_history()
    click.echo(f"⏰ Command History: {len(history)} commands logged")
    
    if history:
        failures = [h for h in history if h['exit_code'] != 0]
        click.echo(f"   - Successful: {len(history) - len(failures)}")
        click.echo(f"   - Failed: {len(failures)}")
    
    # Dangerous commands
    dangerous = rollback.find_recent_dangerous_commands()
    click.echo(f"⚠️  Recent Dangerous Commands: {len(dangerous)}")
    
    # API status
    api_key = storage.get_api_key()
    if api_key:
        click.echo(f"🤖 AI Features: ✅ Enabled (API key configured)")
    else:
        click.echo(f"🤖 AI Features: ❌ Disabled (no API key)")
        click.echo("   Set API key: devkit config --api-key <key>")
    
    click.echo("\n" + "=" * 70 + "\n")


# ============================================================================
# Utility Commands
# ============================================================================

@cli.command()
@click.confirmation_option(prompt='Clear all command history?')
def clear():
    """Clear command history (use with caution!)"""
    storage.clear_history()
    click.echo("✅ Command history cleared")


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == '__main__':
    cli()
    
# ============================================================================
#