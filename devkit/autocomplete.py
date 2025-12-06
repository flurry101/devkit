"""
Autocomplete support for DevKit commands
"""

try:
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.styles import Style
    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:
    PROMPT_TOOLKIT_AVAILABLE = False

from . import storage

# DevKit commands for autocomplete
DEVKIT_COMMANDS = [
    'ask', 'explain', 'commit', 'rewind', 'panic', 'status', 'config', 'about',
    'snippet', 'snippet save', 'snippet list', 'snippet search', 'snippet run',
    'snippet delete', 'snippet get', 'snippet export', 'snippet import',
    'logs', 'logs analyze', 'init', 'clear'
]

# Snippet names for autocomplete
def get_snippet_completions():
    """Get snippet names for autocomplete"""
    try:
        snippets = storage.load_snippets()
        return list(snippets.keys())
    except:
        return []


def create_completer(context=""):
    """Create a completer based on context"""
    if not PROMPT_TOOLKIT_AVAILABLE:
        return None
    
    # Base commands
    completions = DEVKIT_COMMANDS.copy()
    
    # Add snippet names if in snippet context
    if 'snippet' in context.lower():
        completions.extend(get_snippet_completions())
    
    return WordCompleter(completions, ignore_case=True)


def get_user_input(prompt_text="> ", context=""):
    """Get user input with autocomplete"""
    if not PROMPT_TOOLKIT_AVAILABLE:
        return input(prompt_text)
    
    completer = create_completer(context)
    
    # Create style for better appearance
    style = Style.from_dict({
        'completion-menu.completion': 'bg:#008888 #ffffff',
        'completion-menu.completion.current': 'bg:#00aaaa #000000',
        'scrollbar.background': 'bg:#88aaaa',
        'scrollbar.button': 'bg:#222222',
    })
    
    try:
        user_input = prompt(
            prompt_text,
            completer=completer,
            style=style,
            auto_suggest=AutoSuggestFromHistory(),
            history=FileHistory(str(storage.DEVKIT_DIR / '.devkit_history')),
        )
        return user_input
    except (EOFError, KeyboardInterrupt):
        return None


