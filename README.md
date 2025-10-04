# DevKit 🛠️

> AI-powered terminal assistant for developers

DevKit is your companion for terminal operations - helping you save, find, and run commands faster, while writing better git commits and debugging with time-travel capabilities.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/flurry101/devkit.git
cd devkit

# Install in development mode
pip install -e .

# Or install from PyPI (once published)
pip install devkit-cli
```

### First Steps

```bash
# Save your first snippet
devkit snippet save docker-clean "docker system prune -a"

# List all snippets
devkit snippet list

# Run a snippet
devkit snippet run docker-clean

# Create a proper commit
devkit commit
```

## 📋 Features

- **Snippet Management**
  - Save frequently used commands with tags
  - List all saved snippets with filtering
  - Search snippets by name, command, or tags
  - Run snippets with one command
  - Delete snippets you don't need
  - Export/import snippets to/from files

- **Commit Helper**
  - Interactive conventional commit flow
  - AI-powered commit message generation
  - Structured commit messages
  - Type, scope, and description prompts

- **Time-Travel Debugging**
  - View command history
  - AI analysis of recent commands
  - Find failed commands
  - Rewind and analyze patterns

- **Emergency Rollback**
  - Detect dangerous commands
  - AI-powered rollback suggestions
  - Statistics on risky operations
  - Panic mode for emergencies

- **AI Integration**
  - Natural language command suggestions
  - Command explanation and analysis
  - Smart error handling with helpful messages

## 📖 Complete Usage Guide

### Snippet Commands

#### Save a Snippet
```bash
# Basic snippet
devkit snippet save <name> "<command>"

# With tags
devkit snippet save docker-clean "docker system prune -a" --tags "docker,cleanup"

# Examples
devkit snippet save ports "lsof -i -P -n | grep LISTEN" --tags "network,monitoring"
devkit snippet save git-undo "git reset --soft HEAD~1" --tags "git,undo"
```

#### List Snippets
```bash
# List all snippets
devkit snippet list

# Filter by tag
devkit snippet list --tag docker
devkit snippet list --tag git
```

#### Search Snippets
```bash
# Search by name, command, or tags
devkit snippet search "docker"
devkit snippet search "clean"
devkit snippet search "network"
```

#### Get Snippet Details
```bash
# Show specific snippet with metadata
devkit snippet get docker-clean
```

#### Run Snippets
```bash
# Execute a saved snippet
devkit snippet run docker-clean
devkit snippet run ports
```

#### Export/Import Snippets
```bash
# Export to JSON (default)
devkit snippet export my_snippets.json

# Export to text format
devkit snippet export my_snippets.txt --format txt

# Import snippets
devkit snippet import my_snippets.json

# Import with overwrite
devkit snippet import my_snippets.json --overwrite
```

#### Delete Snippets
```bash
# Delete a snippet
devkit snippet delete docker-clean
```

### AI Commands

#### Ask for Command Suggestions
```bash
# Get AI-powered command suggestions
devkit ask "find files larger than 100MB"
devkit ask "compress all images in folder"
devkit ask "check disk usage by directory"
```

#### Explain Commands
```bash
# Get detailed command explanations
devkit explain "docker run -p 8080:80 nginx"
devkit explain "git rebase -i HEAD~3"
devkit explain "find . -name '*.py' -exec grep -l 'import' {} \;"
```

### Commit Helper

#### Interactive Commit
```bash
# Start interactive commit flow
devkit commit

# Example output:
# Type: feat
# Scope: auth
# Description: add JWT validation
# Result: feat(auth): add JWT validation
```

#### AI-Powered Commit
```bash
# Generate commit message from git diff
git add .
devkit commit --ai

# AI analyzes your changes and generates appropriate commit message
```

### Time-Travel Debugging

#### View Command History
```bash
# Show last 10 commands
devkit rewind

# Show last 20 commands
devkit rewind -n 20

# Show only failed commands
devkit rewind --failures
```

#### AI Analysis
```bash
# Get AI analysis of recent commands
devkit rewind --analyze

# AI will identify issues and suggest fixes
```

### Emergency Rollback

#### Panic Mode
```bash
# Check for dangerous commands
devkit panic

# Get AI-powered rollback suggestions
devkit panic  # Will prompt for AI analysis

# View dangerous command statistics
devkit panic --stats
```

### Configuration

#### Set API Key
```bash
# Set Gemini API key
devkit config --api-key "AIza..."

# Or use environment variable
export GEMINI_API_KEY="AIza..."
```

#### View Configuration
```bash
# Show current configuration
devkit config
```

### Status and Utilities

#### Check Status
```bash
# Show comprehensive status
devkit status

# Displays:
# - Number of snippets
# - Command history count
# - Dangerous commands detected
# - AI features status
```

#### Clear History
```bash
# Clear command history (use with caution!)
devkit clear
```

## 🏗️ Project Structure

```
devkit/
├── devkit/
│   ├── __init__.py
│   ├── main.py          # CLI entry point
│   ├── ai.py            # AI integration (Claude API)
│   ├── storage.py       # Data persistence
│   ├── time_travel.py   # Command history & debugging
│   └── rollback.py      # Emergency rollback features
├── tests/
│   └── test_snippets.py # Unit tests
├── demo/
│   ├── examples.sh      # Example snippets loader
│   └── rollback_examples.md # Emergency scenarios
├── setup.py             # Installation config
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## 🔧 Development

### Setup Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with verbose output
pytest -v
```

### Adding AI Features

To add AI capabilities, you'll need a Gemini API key:

```bash
# Set your API key
export GEMINI_API_KEY="your-key-here"

# Or add to config
devkit config --api-key "your-key-here"

# Verify
devkit config
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=devkit

# Run specific test file
pytest tests/test_snippets.py
```

## 🎯 Examples

### Load Example Snippets
```bash
# Run the examples script to load common snippets
./demo/examples.sh

# This loads 12 useful snippets:
# - ports: Show listening ports
# - size: Show directory sizes
# - find-large: Find large files
# - git-undo: Undo last commit
# - docker-clean: Clean Docker system
# - And more...
```

### Common Workflows

#### Daily Development
```bash
# Check what's running
devkit snippet run ports

# Clean up Docker
devkit snippet run docker-clean

# Check disk usage
devkit snippet run disk-usage

# Create a commit
devkit commit --ai
```

#### Debugging Session
```bash
# Something went wrong? Check recent commands
devkit rewind --analyze

# Look for dangerous operations
devkit panic

# Get rollback suggestions
devkit panic  # AI will suggest fixes
```

#### Snippet Management
```bash
# Search for Docker-related commands
devkit snippet search docker

# Export your snippets for backup
devkit snippet export backup.json

# Import snippets on new machine
devkit snippet import backup.json
```

## 🐛 Troubleshooting

### Common Issues

#### "Command not found: devkit"
```bash
# Fix: Reinstall
pip uninstall devkit-cli
pip install -e .

# Or run directly
python3 -m devkit.main --help
```

#### "API key not configured"
```bash
# Option 1: Environment variable
export GEMINI_API_KEY="AIza..."

# Option 2: Config file
devkit config --api-key "AIza..."

# Verify
devkit config
```

#### "ModuleNotFoundError"
```bash
# Install dependencies
pip install -r requirements.txt

# Or install specific packages
pip install click google-generativeai colorama
```

#### AI features not working
```bash
# Check API key is set
devkit config

# Test with a simple command
devkit ask "list files"

# Check for error messages
```

## Additional Features

### Snippet Tags
```bash
# Save with multiple tags
devkit snippet save deploy "kubectl apply -f k8s/" --tags "k8s,deploy,production"

# Filter by tag
devkit snippet list --tag production

# Search by tag
devkit snippet search "production"
```

### Export Formats
```bash
# JSON format (includes metadata)
devkit snippet export snippets.json

# Text format (human-readable)
devkit snippet export snippets.txt --format txt
```

### Time-Travel Analysis
```bash
# Get AI analysis of what went wrong
devkit rewind --analyze

# Find patterns in failures
devkit rewind --failures
```

## 🚀 Publishing a Release

### Prepare for Release

1. **Update version in setup.py**
2. **Update CHANGELOG.md**
3. **Run tests**
4. **Build package**

```bash
# Update version
vim setup.py  # Change version number

# Run tests
pytest

# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

### Release Checklist

- [ ] All tests pass
- [ ] Version updated
- [ ] CHANGELOG updated
- [ ] Documentation updated
- [ ] Package builds successfully
- [ ] Uploaded to PyPI

## 🤝 Contributing

Contributions are welcome! This is a hackathon project that can grow into something bigger.

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - feel free to use and modify!

---

