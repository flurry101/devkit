"""
Workspace module for DevKit
Handles project-aware features and context detection
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


PROJECT_CONFIG_FILE = ".devkit/config.json"
PROJECT_SNIPPETS_FILE = ".devkit/snippets.json"


def find_project_root() -> Optional[Path]:
    """Find project root by looking for markers like .git, package.json, etc."""
    current = Path.cwd()
    
    # Look for common project markers
    markers = [
        '.git',
        'package.json',
        'setup.py',
        'pyproject.toml',
        'Cargo.toml',
        'go.mod',
        'pom.xml',
        'build.gradle',
        '.devkit'
    ]
    
    # Walk up the directory tree
    for parent in [current] + list(current.parents):
        for marker in markers:
            if (parent / marker).exists():
                return parent
    
    return None


def detect_project_type(project_root: Path) -> str:
    """Detect project type based on files present"""
    if (project_root / "package.json").exists():
        return "nodejs"
    elif (project_root / "setup.py").exists() or (project_root / "pyproject.toml").exists():
        return "python"
    elif (project_root / "Cargo.toml").exists():
        return "rust"
    elif (project_root / "go.mod").exists():
        return "go"
    elif (project_root / "pom.xml").exists():
        return "java-maven"
    elif (project_root / "build.gradle").exists():
        return "java-gradle"
    elif (project_root / ".git").exists():
        return "git-repo"
    else:
        return "unknown"


def get_project_name(project_root: Path, project_type: str) -> str:
    """Extract project name from project files"""
    try:
        if project_type == "nodejs":
            with open(project_root / "package.json") as f:
                data = json.load(f)
                return data.get("name", project_root.name)
        
        elif project_type == "python":
            if (project_root / "pyproject.toml").exists():
                import toml
                with open(project_root / "pyproject.toml") as f:
                    data = toml.load(f)
                    return data.get("project", {}).get("name", project_root.name)
            elif (project_root / "setup.py").exists():
                # Try to extract from setup.py (basic parsing)
                return project_root.name
        
        elif project_type == "rust":
            import toml
            with open(project_root / "Cargo.toml") as f:
                data = toml.load(f)
                return data.get("package", {}).get("name", project_root.name)
    
    except Exception:
        pass
    
    return project_root.name


def init_project_workspace(project_root: Path, force: bool = False) -> Dict[str, Any]:
    """Initialize .devkit directory in project root"""
    devkit_dir = project_root / ".devkit"
    
    if devkit_dir.exists() and not force:
        raise FileExistsError(f".devkit already exists in {project_root}")
    
    # Create .devkit directory
    devkit_dir.mkdir(exist_ok=True)
    
    # Detect project info
    project_type = detect_project_type(project_root)
    project_name = get_project_name(project_root, project_type)
    
    # Create project config
    config = {
        "project_name": project_name,
        "project_type": project_type,
        "project_root": str(project_root),
        "initialized_at": __import__('datetime').datetime.now().isoformat(),
        "settings": {
            "auto_stage": False,
            "commit_template": None
        }
    }
    
    config_file = devkit_dir / "config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    # Create empty snippets file
    snippets_file = devkit_dir / "snippets.json"
    if not snippets_file.exists():
        with open(snippets_file, 'w') as f:
            json.dump({}, f)
    
    # Add .devkit to .gitignore if in git repo
    gitignore = project_root / ".gitignore"
    if (project_root / ".git").exists():
        gitignore_content = ""
        if gitignore.exists():
            gitignore_content = gitignore.read_text()
        
        if ".devkit/" not in gitignore_content:
            with open(gitignore, 'a') as f:
                f.write("\n# DevKit project workspace\n.devkit/\n")
    
    return config


def load_project_config() -> Optional[Dict[str, Any]]:
    """Load project config if in a project workspace"""
    project_root = find_project_root()
    
    if not project_root:
        return None
    
    config_file = project_root / ".devkit" / "config.json"
    
    if not config_file.exists():
        return None
    
    try:
        with open(config_file) as f:
            return json.load(f)
    except Exception:
        return None


def get_project_context() -> str:
    """Get project context string for AI prompts"""
    config = load_project_config()
    
    if not config:
        return ""
    
    project_name = config.get("project_name", "unknown")
    project_type = config.get("project_type", "unknown")
    
    context = f"\nProject Context:\n- Name: {project_name}\n- Type: {project_type}\n"
    
    return context


def load_project_snippets() -> Dict[str, Any]:
    """Load project-specific snippets"""
    project_root = find_project_root()
    
    if not project_root:
        return {}
    
    snippets_file = project_root / ".devkit" / "snippets.json"
    
    if not snippets_file.exists():
        return {}
    
    try:
        with open(snippets_file) as f:
            return json.load(f)
    except Exception:
        return {}


def save_project_snippets(snippets: Dict[str, Any]):
    """Save project-specific snippets"""
    project_root = find_project_root()
    
    if not project_root:
        raise RuntimeError("Not in a project workspace")
    
    devkit_dir = project_root / ".devkit"
    devkit_dir.mkdir(exist_ok=True)
    
    snippets_file = devkit_dir / "snippets.json"
    
    with open(snippets_file, 'w') as f:
        json.dump(snippets, f, indent=2)


def is_in_project_workspace() -> bool:
    """Check if currently in a project workspace"""
    project_root = find_project_root()
    if not project_root:
        return False
    
    return (project_root / ".devkit").exists()