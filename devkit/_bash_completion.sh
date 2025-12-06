# Bash completion for DevKit
# Auto-installed by devkit-cli package
# Supports partial matching: typing "g" suggests "get"

_devkit_completion() {
    local cur prev words cword
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    words=("${COMP_WORDS[@]}")
    cword=$COMP_CWORD

    # Main commands
    local commands="ask explain commit rewind panic status config about init clear"
    local snippet_commands="save list search run delete get export import"
    local logs_commands="analyze"
    
    # Handle subcommands with partial matching
    if [[ ${prev} == "snippet" ]]; then
        # Partial matching: "g" will suggest "get", "s" will suggest "save", "search"
        COMPREPLY=($(compgen -W "${snippet_commands}" -- ${cur}))
        return 0
    elif [[ ${prev} == "logs" ]]; then
        COMPREPLY=($(compgen -W "${logs_commands}" -- ${cur}))
        return 0
    elif [[ ${cword} -ge 3 && ${words[1]} == "snippet" ]]; then
        # For commands like "snippet run <name>", complete with snippet names
        # Supports partial matching: typing part of snippet name will suggest matches
        if [[ ${words[2]} == "run" ]] || [[ ${words[2]} == "delete" ]] || [[ ${words[2]} == "get" ]]; then
            # Get snippet names from ~/.devkit/snippets.json
            if [ -f ~/.devkit/snippets.json ]; then
                local snippets=$(python3 -c "import json; print(' '.join(json.load(open('$HOME/.devkit/snippets.json')).keys()))" 2>/dev/null)
                COMPREPLY=($(compgen -W "${snippets}" -- ${cur}))
            fi
            return 0
        fi
    fi
    
    # Main command completion with partial matching
    # Typing "s" will suggest "status", "snippet" (both start with 's')
    # Typing "sn" will suggest "snippet" (more specific)
    # Typing "st" will suggest "status" (more specific)
    # Typing "g" will suggest nothing (no commands start with 'g')
    if [[ ${cword} -eq 1 ]]; then
        COMPREPLY=($(compgen -W "${commands} snippet logs" -- ${cur}))
        return 0
    fi
    
    return 0
}

complete -F _devkit_completion devkit

