# DevKit 🛠️  
**AI-powered terminal assistant for developers**

![Demo](demo/enigma.gif)

Meet DevKit, the assistant you didn’t know you needed in your terminal. It's not just another CLI tool; it's your go-to for getting commands on-the-fly, saving your favorite snippets, generating git commit messages that make sense, and even rewinding your mistakes like some sort of coding time-travel wizard. Spend less time googling and more time creating!

> Fun fact: I’ve been using DevKit for everything during development of this, like for debugging, building, even the commit messages. So, you could say I’m DevKit’s very first (and probably most demanding) customer. Pretty meta, huh?

---

## ✨ Key Features

**AI Command Suggestions:**  
No more fumbling or Googling. Ask for any command in plain English. Seriously, just ask!
`devkit ask "find files larger than 100MB"`

**Snippet Manager:**  
Save, search, and run your favorite commands without the usual terminal déjà vu.  
`devkit snippet save ports "lsof -i -P -n"`

**Smart Commits:**  
Generate conventional commit messages from your changes.  
`devkit commit --ai`

**Time-Travel Debugging:**  
When things break (and they will), travel back to see exactly what went wrong.
`devkit rewind --analyze`

**Emergency Rollback:**  
Deployments gone rogue? DevKit has your back with AI-powered panic mode.
`devkit panic`

---

## 💡 Why You Might Care

The terminal is a powerful tool, but it can also be intimidating and frustrating—especially for new developers. And having to repeat the same commands over and over? Yeah, that gets old fast. Here’s a fun (well, not really) fact: over 70% of Node.js snippets on npm have bugs that need manual fixing before they actually work. Repetitive and error-prone command-line work slows development and leads to avoidable mistakes. Many developers get stuck typing complex commands repeatedly or struggle to keep workflows consistent across teams. Beginners often don’t know why commands work or how to troubleshoot effectively, which wastes time and patience. 

### 📢 Is this even a real problem?

Absolutely. The numbers don’t lie:
- 73.7% of Node.js code snippets on npm had errors, but with automation, errors drop to 25.1%.
- Developers spend 20-30% of their time on repetitive terminal tasks.

Repetitive commands, lack of command-line fluency, and inconsistent workflows are common developer headaches. Beginners often struggle with the complexity and uncertainty of commands, while experienced developers grow weary of retyping the same sequences repeatedly. Plus, keeping everyone on the same page with workflows and code style across teams and 🥁... you’ve got a recipe for frustration.. That’s why tools like DevKit are here to save the day (and your sanity). By automating command suggestions, snippet reuse, and AI-crafted commit messages, DevKit helps you avoid dumb mistakes, save precious time, and keep things humming smoothly, so you can get back to what you really enjoy: building awesome software.

---

## 🚀 Quick Start

### 1. Installation  
Get started in seconds. All you need is Python 3.8+.

```bash
pip install devkit-cli
````

Sources:
- https://pypi.org/project/devkit-cli/0.1.0/
- https://test.pypi.org/project/devkit-cli/0.1.0/


### 2. Configure Your AI *(Optional, but Recommended)*

For full AI awesomeness, you’ll need a free Google AI API key. Grab one from Google AI Studio.

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

No more googling random commands, switching between a million tabs, copy-pasting from random forums and losing the overall flow.
Describe what you want, and DevKit will figure it out for you.

```bash
devkit ask "how to check disk usage by directory"
devkit ask "compress all jpg images in the current folder"
```

#### `explain` - Understand a Command

Commands looking like hieroglyphics? DevKit will break it down, one part at a time.

```bash
devkit explain "find . -name '*.py' -exec grep -l 'import' {} \;"
devkit explain "git rebase -i HEAD~3"
```

---

### Snippet Management

#### `snippet save`

Save your most used commands for easy reuse. Tag them for easy searching!

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

Run a saved snippet in a flash.

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

Ever wonder what you did last? DevKit has a rewind feature to show you your history, and help debug!

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


## 🚀 Future Enhancements

Here’s a sneak peek at some of the features coming soon:

* [ ] **AI-Powered Features**: Auto-comlplete commit messages, debug errors, and suggest commands using AI.
* [ ] **Real-Time Collaborative Coding**: Pair program directly in the terminal with shared snippets, commands, and real-time suggestions. 
* [ ] **Self-Healing Terminal**: DevKit automatically detects and fixes errors in commands, missing dependencies, or broken environments. 
* [ ] **Universal Snippet Cloud**: Share snippets globally and pull in top-rated snippets from the community or company as per best practices of the org.
* [ ] **Cross-Project Context Switching**: Automatically switch between projects, loading context-specific snippets and environments.
* [ ] **Automated Security Audits**: Run real-time security audits to detect vulnerabilities in your commands, libraries, and scripts.

P.S. This list will grow as I learn and build, expect frequent updates 🤞

---

## 🤝 Contributing

Interested in making DevKit better? We'd love your help! Whether you're fixing a bug, adding a feature, or improving documentation, your contributions are welcome.

Please read our [Contributing Guide](https://github.com/flurry101/devkit/blob/main/CONTRIBUTING.md) to get started with the development setup, code style, and submission process.

---

## 📝 License

DevKit is licensed under the [**MIT License**](LICENSE).

---