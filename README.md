# DevKit 🛠️  
**AI-powered terminal assistant for developers**

DevKit is your smart companion for the command line. It helps you find the right commands without leaving your terminal, manage and reuse helpful snippets, write perfect git commits, and even turn back time when things go wrong. Spend less time searching and more time coding.

---

## ✨ Key Features

**AI Command Suggestions:**  
Ask for any command in plain English.  
`devkit ask "find files larger than 100MB"`

**Snippet Manager:**  
Save, search, and run your favorite commands.  
`devkit snippet save ports "lsof -i -P -n"`

**Smart Commits:**  
Generate conventional commit messages from your changes.  
`devkit commit --ai`

**Time-Travel Debugging:**  
Rewind your command history to see what went wrong.  
`devkit rewind --analyze`

**Emergency Rollback:**  
Get AI-powered help when a deployment breaks.  
`devkit panic`

---

## 🚀 Quick Start

### 1. Installation  
Get started in seconds. All you need is Python 3.8+.

```bash
pip install devkit-cli
````

### 2. Configure Your AI *(Optional, but Recommended)*

To unlock the AI features, you need a free Google AI API key.

* Get your key from **Google AI Studio**.

Set it up with DevKit:

```bash
devkit config --api-key YOUR_API_KEY_HERE
```

### 3. Basic Usage

Here's a quick tour of what you can do:

```bash
# Get a command for finding large files
devkit ask "find all files over 500MB in my home directory"

# Save a useful command as a snippet
devkit snippet save large-files "find ~ -type f -size +500M" --tags "disk,files"

# Run your new snippet anytime
devkit snippet run large-files

# Stage your files and let AI write the commit message
git add .
devkit commit --ai

# Something broke? See what you did last and get an AI analysis.
devkit rewind --analyze
```

---

## 📖 Usage Guide

### Installation

The recommended way to install DevKit is via pip:

```bash
pip install devkit-cli
```

This will make the `devkit` command available in your terminal.

---

### AI Commands

#### `ask` - Get Command Suggestions

Never google a command again. Describe what you want to do, and DevKit will give you the command.

```bash
devkit ask "how to check disk usage by directory"
devkit ask "compress all jpg images in the current folder"
```

#### `explain` - Understand a Command

Unsure what a cryptic command does? Get a clear, part-by-part explanation.

```bash
devkit explain "find . -name '*.py' -exec grep -l 'import' {} \;"
devkit explain "git rebase -i HEAD~3"
```

---

### Snippet Management

#### `snippet save`

Save any command for later use. Adding tags helps you find it easily.

```bash
devkit snippet save git-undo "git reset --soft HEAD~1" --tags "git,undo"
devkit snippet save k8s-pods "kubectl get pods -n production" --tags "k8s,prod"
```

#### `snippet list` & `snippet search`

View all your snippets or find specific ones.

```bash
# List everything
devkit snippet list

# Filter by tag
devkit snippet list --tag git

# Search by name, command, or tag
devkit snippet search "git"
```

#### `snippet run`

Execute a saved snippet directly.

```bash
devkit snippet run git-undo
```

---

### Git Commit Helper

#### `commit`

Create perfectly formatted conventional commit messages.

```bash
# Stage your changes
git add .

# Let AI generate the commit message from your staged changes
devkit commit --ai

# Or use the interactive helper
devkit commit
```

---

### Time-Travel & Rollback

#### `rewind`

View your command history and get AI analysis to debug issues.

```bash
# See the last 10 commands you ran
devkit rewind

# Get an AI analysis of what might have gone wrong recently
devkit rewind --analyze

# Show only commands that failed
devkit rewind --failures
```

#### `panic`

Made a mistake in production? Panic mode scans for recent dangerous commands (like deploy, delete, push --force) and suggests how to roll them back.

```bash
# Something just broke after a command? Run this immediately!
devkit panic
```

---

## 🤝 Contributing

Interested in making DevKit better? We'd love your help! Whether you're fixing a bug, adding a feature, or improving documentation, your contributions are welcome.

Please read our [Contributing Guide](https://github.com/flurry101/devkit/blob/main/CONTRIBUTING.md) to get started with the development setup, code style, and submission process.

---

## 📝 License

DevKit is licensed under the [**MIT License**](LICENSE).

```