"""
Storage module for DevKit
Handles all data persistence (snippets, history, config)
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Configuration
DEVKIT_DIR = Path.home() / ".devkit"
SNIPPETS_FILE = DEVKIT_DIR / "snippets.json"
HISTORY_FILE = DEVKIT_DIR / "history.json"
CONFIG_FILE = DEVKIT_DIR / "config.json"

# Ensure devkit directory exists
DEVKIT_DIR.mkdir(exist_ok=True)


# ============================================================================
# Snippet Storage
# ============================================================================

def load_snippets() -> Dict[str, Dict[str, Any]]:
    """Load snippets from JSON file with support for tags"""
    if not SNIPPETS_FILE.exists():
        return {}
    
    try:
        with open(SNIPPETS_FILE, 'r') as f:
            data = json.load(f)
            
            # Handle legacy format (string values) and new format (dict values)
            converted_data = {}
            for name, value in data.items():
                if isinstance(value, str):
                    # Legacy format: convert to new format
                    converted_data[name] = {
                        'command': value,
                        'tags': [],
                        'created': datetime.now().isoformat()
                    }
                else:
                    # New format: ensure all required fields exist
                    converted_data[name] = {
                        'command': value.get('command', ''),
                        'tags': value.get('tags', []),
                        'created': value.get('created', datetime.now().isoformat())
                    }
            
            return converted_data
    except json.JSONDecodeError:
        return {}


def save_snippets(snippets: Dict[str, Dict[str, Any]]) -> None:
    """Save snippets to JSON file"""
    with open(SNIPPETS_FILE, 'w') as f:
        json.dump(snippets, f, indent=2)


def load_snippets_legacy() -> Dict[str, str]:
    """Load snippets in legacy format (for backward compatibility)"""
    snippets = load_snippets()
    return {name: data['command'] for name, data in snippets.items()}


def save_snippets_legacy(snippets: Dict[str, str]) -> None:
    """Save snippets in legacy format (for backward compatibility)"""
    converted_snippets = {}
    for name, command in snippets.items():
        converted_snippets[name] = {
            'command': command,
            'tags': [],
            'created': datetime.now().isoformat()
        }
    save_snippets(converted_snippets)


# ============================================================================
# Command History Storage (for time-travel debugging)
# ============================================================================

def log_command(command: str, output: str = "", exit_code: int = 0) -> None:
    """Log a command to history for time-travel debugging"""
    history = load_history()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "output": output[:1000],  # Limit output size
        "exit_code": exit_code
    }
    
    history.append(entry)
    
    # Keep only last 100 commands to avoid huge files
    if len(history) > 100:
        history = history[-100:]
    
    save_history(history)


def load_history() -> List[Dict[str, Any]]:
    """Load command history"""
    if not HISTORY_FILE.exists():
        return []
    
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_history(history: List[Dict[str, Any]]) -> None:
    """Save command history"""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)


def clear_history() -> None:
    """Clear command history"""
    save_history([])


# ============================================================================
# Config Storage
# ============================================================================

def load_config() -> Dict[str, Any]:
    """Load configuration"""
    if not CONFIG_FILE.exists():
        return {
            "api_key": None,
            "time_travel_enabled": True,
            "max_history": 100
        }
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def get_api_key() -> str | None:
    """Get API key from config or environment"""
    import os
    
    # Try environment variable first
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key
    
    # Try config file
    config = load_config()
    return config.get("api_key")