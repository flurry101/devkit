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

from . import workspace
from . import logs as log_analyzer

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
# Project Workspace Commands
# ============================================================================

@cli.command()
@click.option('--force', is_flag=True, help='Reinitialize if .devkit already exists')
def init(force):
    """Initialize DevKit project workspace
    
    Creates .devkit/ directory with project-specific config and snippets.
    """
    try:
        project_root = workspace.find_project_root()
        
        if not project_root:
            project_root = Path.cwd()
            click.echo(f"{Fore.YELLOW}⚠️  No project markers found. Using current directory.{Style.RESET_ALL}")
        
        config = workspace.init_project_workspace(project_root, force=force)
        
        click.echo(f"\n{Fore.GREEN}✅ Initialized DevKit workspace!{Style.RESET_ALL}\n")
        click.echo(f"Project: {config['project_name']}")
        click.echo(f"Type: {config['project_type']}")
        click.echo(f"Location: {project_root}/.devkit/\n")
    
    except FileExistsError as e:
        click.echo(f"{Fore.YELLOW}⚠️  {e}{Style.RESET_ALL}")
        click.echo(f"Use {Fore.CYAN}devkit init --force{Style.RESET_ALL} to reinitialize.")


# ============================================================================
# Log Analysis Commands
# ============================================================================

@cli.group()
def logs():
    """AI-powered log analysis and debugging"""
    pass


@logs.command('analyze')
@click.argument('logfile', required=False)
def logs_analyze(logfile):
    """Analyze log file for errors and crashes
    
    Examples:
      devkit logs analyze app.log
      cat error.log | devkit logs analyze
    """
    try:
        if logfile:
            click.echo(f"{Fore.CYAN}📄 Reading: {logfile}{Style.RESET_ALL}\n")
            log_content = log_analyzer.read_log_file(logfile)
        else:
            click.echo(f"{Fore.CYAN}📄 Reading from stdin...{Style.RESET_ALL}\n")
            log_content = log_analyzer.read_stdin()
        
        if not log_content.strip():
            click.echo(f"{Fore.RED}❌ Empty log{Style.RESET_ALL}")
            return
        
        patterns = log_analyzer.extract_error_patterns(log_content)
        context = workspace.get_project_context()
        
        click.echo(f"{Fore.CYAN}🤖 Analyzing with AI...{Style.RESET_ALL}\n")
        analysis = log_analyzer.analyze_log_with_ai(log_content, context)
        
        output = log_analyzer.format_analysis_output(analysis, patterns)
        click.echo(output)
    
    except RuntimeError as e:
        click.echo(f"{Fore.RED}❌ {e}{Style.RESET_ALL}")
    except Exception as e:
        click.echo(f"{Fore.RED}❌ Analysis failed: {e}{Style.RESET_ALL}")
        
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
@click.option('--ai', 'ai_mode', is_flag=True, help='Use AI to generate commit message')
@click.option('--edit', '-e', is_flag=True, help='Edit message before committing')
def commit(ai_mode, edit):
    """Create a conventional commit message with preview
    
    Examples:
      devkit commit          # Interactive
      devkit commit --ai     # AI-generated  
      devkit commit --ai -e  # AI + edit
    """
    import tempfile
    
    # Check git repo
    try:
        subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        click.echo(f"{Fore.RED}❌ Not in a git repository!{Style.RESET_ALL}")
        return
    
    # Get staged files for preview
    result = subprocess.run(["git", "diff", "--staged", "--name-status"], 
                          capture_output=True, text=True)
    staged_files = result.stdout.strip()
    
    if not staged_files:
        click.echo(f"{Fore.YELLOW}⚠️  No staged changes.{Style.RESET_ALL}")
        click.echo("Run 'git add <files>' first.\n")
        return
    
    # Generate commit message
    commit_msg = None
    
    if ai_mode:
        click.echo(f"\n{Fore.CYAN}🤖 Generating commit message...{Style.RESET_ALL}\n")
        
        result = subprocess.run(["git", "diff", "--staged"], 
                              capture_output=True, text=True, check=True)
        diff = result.stdout
        
        if not diff:
            click.echo(f"{Fore.RED}❌ No diff{Style.RESET_ALL}")
            return
        
        commit_msg = ai.generate_commit_message(diff)
        
        if commit_msg.startswith("❌"):
            click.echo(commit_msg)
            return
    else:
        # Interactive mode
        click.echo(f"\n{Fore.CYAN}📝 Conventional Commit Helper{Style.RESET_ALL}\n")
        
        types = {
            '1': ('feat', '✨ New feature'),
            '2': ('fix', '🐛 Bug fix'),
            '3': ('docs', '📝 Documentation'),
            '4': ('style', '💄 Code style'),
            '5': ('refactor', '♻️  Refactoring'),
            '6': ('test', '✅ Tests'),
            '7': ('chore', '🔧 Maintenance')
        }
        
        click.echo("Select type:")
        for key, (value, desc) in types.items():
            click.echo(f"  {key}. {value:10} - {desc}")
        
        type_choice = click.prompt("\nType", default='1')
        commit_type = types.get(type_choice, types['1'])[0]
        
        scope = click.prompt("Scope (optional)", default="", show_default=False)
        description = click.prompt("Description", type=str)
        
        commit_msg = f"{commit_type}({scope}): {description}" if scope else f"{commit_type}: {description}"
    
    # Preview
    click.echo(f"\n{Fore.CYAN}📋 Preview:{Style.RESET_ALL}")
    click.echo("=" * 70)
    click.echo(f"{Fore.WHITE}Message: {commit_msg}{Style.RESET_ALL}\n")
    click.echo(f"{Fore.YELLOW}Staged files:{Style.RESET_ALL}")
    for line in staged_files.split('\n'):
        if line:
            parts = line.split('\t')
            status = parts[0]
            file = '\t'.join(parts[1:])
            color = Fore.GREEN if status == 'A' else Fore.YELLOW if status == 'M' else Fore.RED
            click.echo(f"  {color}{status}{Style.RESET_ALL} {file}")
    click.echo("=" * 70 + "\n")
    
    # Edit option
    if edit or click.confirm("Edit message?", default=False):
        import os
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as f:
            f.write(commit_msg)
            temp_path = f.name
        
        editor = os.environ.get('EDITOR', 'nano')
        subprocess.run([editor, temp_path])
        
        with open(temp_path) as f:
            commit_msg = f.read().strip()
        
        os.unlink(temp_path)
        
        if not commit_msg:
            click.echo(f"{Fore.RED}❌ Empty message{Style.RESET_ALL}")
            return
        
        click.echo(f"\n{Fore.CYAN}Updated: {commit_msg}{Style.RESET_ALL}\n")
    
    # Confirm and commit
    if click.confirm(f"{Fore.GREEN}Proceed?{Style.RESET_ALL}", default=True):
        try:
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            click.echo(f"\n{Fore.GREEN}✅ Committed!{Style.RESET_ALL}")
            storage.log_command(f"git commit -m \"{commit_msg}\"", "Committed", 0)
        except subprocess.CalledProcessError as e:
            click.echo(f"{Fore.RED}❌ Failed: {e}{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.YELLOW}❌ Cancelled{Style.RESET_ALL}")

'''@cli.command()
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
        click.echo("❌ Commit cancelled")'''


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