#!/bin/bash
# Setup script for DevKit autocomplete
# Run this script to enable tab completion for devkit commands

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DEVKIT_DIR="$SCRIPT_DIR/devkit"

# Detect shell
if [ -n "$ZSH_VERSION" ]; then
    SHELL_TYPE="zsh"
    COMPLETION_FILE="$HOME/.zsh_completion_devkit"
    RC_FILE="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_TYPE="bash"
    COMPLETION_FILE="$HOME/.bash_completion_devkit"
    RC_FILE="$HOME/.bashrc"
else
    echo "Unsupported shell. Please use bash or zsh."
    exit 1
fi

echo "Setting up DevKit autocomplete for $SHELL_TYPE..."

# Copy completion script
if [ "$SHELL_TYPE" == "zsh" ]; then
    cp "$DEVKIT_DIR/_zsh_completion.sh" "$COMPLETION_FILE"
    chmod +x "$COMPLETION_FILE"
    echo "Copied zsh completion script to $COMPLETION_FILE"
else
    cp "$DEVKIT_DIR/_bash_completion.sh" "$COMPLETION_FILE"
    chmod +x "$COMPLETION_FILE"
    echo "Copied bash completion script to $COMPLETION_FILE"
fi

# Add to shell RC file if not already present
if ! grep -q "devkit.*completion" "$RC_FILE" 2>/dev/null; then
    echo "" >> "$RC_FILE"
    echo "# DevKit autocomplete" >> "$RC_FILE"
    echo "source $COMPLETION_FILE" >> "$RC_FILE"
    echo "Added autocomplete to $RC_FILE"
else
    echo "Autocomplete already configured in $RC_FILE"
fi

echo ""
echo "✅ DevKit autocomplete setup complete!"
echo "Please run: source $RC_FILE"
echo "Or restart your terminal to enable tab completion."