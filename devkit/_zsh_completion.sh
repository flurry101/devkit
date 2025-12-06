# Zsh completion for DevKit
# Auto-installed by devkit-cli package
# Supports partial matching: typing "g" suggests "get"

#compdef devkit

_devkit() {
    local -a commands snippet_commands logs_commands
    
    commands=(
        'ask:Ask AI for a command suggestion'
        'explain:Explain what a command does'
        'commit:Create a conventional commit message'
        'rewind:Time-travel debugging - view command history'
        'panic:Emergency rollback assistant'
        'status:Show DevKit status and statistics'
        'config:Configure DevKit settings'
        'about:Show DevKit about information'
        'init:Initialize DevKit project workspace'
        'clear:Clear command history'
        'snippet:Manage code snippets'
        'logs:AI-powered log analysis'
    )
    
    snippet_commands=(
        'save:Save a new snippet'
        'list:List all saved snippets'
        'search:Search snippets'
        'run:Run a saved snippet'
        'delete:Delete a saved snippet'
        'get:Show a specific snippet'
        'export:Export snippets to a file'
        'import:Import snippets from a file'
    )
    
    logs_commands=(
        'analyze:Analyze log file for errors'
    )
    
    _arguments \
        '1: :->command' \
        '2: :->subcommand' \
        '*:: :->args'
    
    case $state in
        command)
            _describe 'commands' commands
            ;;
        subcommand)
            case $words[2] in
                snippet)
                    _describe 'snippet commands' snippet_commands
                    ;;
                logs)
                    _describe 'logs commands' logs_commands
                    ;;
            esac
            ;;
        args)
            case $words[2] in
                snippet)
                    case $words[3] in
                        run|delete|get)
                            # Complete with snippet names
                            if [ -f ~/.devkit/snippets.json ]; then
                                local snippets=$(python3 -c "import json; print(' '.join(json.load(open('$HOME/.devkit/snippets.json')).keys()))" 2>/dev/null)
                                _values 'snippets' ${=snippets}
                            fi
                            ;;
                    esac
                    ;;
            esac
            ;;
    esac
}

_devkit "$@"

