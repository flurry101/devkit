"""
Automatic completion installation for DevKit
This runs automatically after package installation
"""

import os
import sys
import shutil
from pathlib import Path


def get_shell_rc_file():
    """Detect shell and return RC file path"""
    shell = os.environ.get('SHELL', '')
    home = Path.home()
    
    if 'zsh' in shell:
        return home / '.zshrc'
    elif 'bash' in shell:
        # Check for .bash_profile first (macOS)
        bash_profile = home / '.bash_profile'
        if bash_profile.exists():
            return bash_profile
        return home / '.bashrc'
    return None


def install_completion():
    """Install completion scripts automatically"""
    try:
        # Get package directory (where completion scripts are installed)
        try:
            import devkit
            package_dir = Path(devkit.__file__).parent
        except:
            # Fallback to current file's directory
            package_dir = Path(__file__).parent
        completion_dir = package_dir
        
        # Detect shell
        shell_rc = get_shell_rc_file()
        if not shell_rc:
            # Can't detect shell, skip installation
            return False
        
        # Determine which completion script to use
        if 'zsh' in os.environ.get('SHELL', ''):
            completion_script = completion_dir / '_zsh_completion.sh'
            completion_name = '_devkit'
        else:
            completion_script = completion_dir / '_bash_completion.sh'
            completion_name = 'devkit_completion'
        
        if not completion_script.exists():
            return False
        
        # For zsh, install to fpath
        if 'zsh' in os.environ.get('SHELL', ''):
            fpath_dir = Path.home() / '.zsh' / 'completions'
            fpath_dir.mkdir(parents=True, exist_ok=True)
            target_file = fpath_dir / '_devkit'
            shutil.copy(completion_script, target_file)
            target_file.chmod(0o644)
            
            # Add fpath to .zshrc if not present
            if shell_rc.exists():
                with open(shell_rc, 'r') as f:
                    content = f.read()
                if 'fpath=(' not in content or '.zsh/completions' not in content:
                    with open(shell_rc, 'a') as f:
                        f.write('\n# DevKit autocomplete\n')
                        f.write('fpath=($HOME/.zsh/completions $fpath)\n')
                        f.write('autoload -Uz compinit && compinit\n')
        else:
            # For bash, source the completion script
            completion_target = Path.home() / f'.{completion_name}'
            shutil.copy(completion_script, completion_target)
            completion_target.chmod(0o644)
            
            # Add source line to .bashrc if not present
            if shell_rc.exists():
                with open(shell_rc, 'r') as f:
                    content = f.read()
                source_line = f'source {completion_target}'
                if source_line not in content and 'devkit.*completion' not in content:
                    with open(shell_rc, 'a') as f:
                        f.write(f'\n# DevKit autocomplete\n')
                        f.write(f'{source_line}\n')
        
        return True
    except Exception as e:
        # Silently fail - don't break installation
        return False


if __name__ == '__main__':
    # This can be called during installation
    install_completion()

