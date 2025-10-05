#!/bin/bash
# Complete DevKit Demo - All Features Showcase
# Run this to demonstrate all capabilities

set -e  # Exit on error

echo "=========================================="
echo "DevKit Complete Demo"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

demo_step() {
    echo -e "${CYAN}▶ $1${NC}"
    sleep 1
}

demo_command() {
    echo -e "${YELLOW}  $ $1${NC}"
    eval "$1"
    echo ""
    sleep 2
}

# 1. Basic Setup
demo_step "1. Check DevKit Status"
demo_command "devkit --version"
demo_command "devkit status"

# 2. Snippet Management
demo_step "2. Snippet Management"
demo_command "devkit snippet save ports 'lsof -i -P -n | grep LISTEN' --tags 'network,monitoring'"
demo_command "devkit snippet save docker-ps 'docker ps -a' --tags 'docker'"
demo_command "devkit snippet save git-log 'git log --oneline -10' --tags 'git'"

demo_step "2a. List and Search Snippets"
demo_command "devkit snippet list"
demo_command "devkit snippet list --tag docker"
demo_command "devkit snippet search git"

demo_step "2b. Get Snippet Details"
demo_command "devkit snippet get ports"

demo_step "2c. Export Snippets"
demo_command "devkit snippet export demo_snippets.json"
demo_command "cat demo_snippets.json"

# 3. AI Features (if API key configured)
if [ ! -z "$GEMINI_API_KEY" ]; then
    demo_step "3. AI Command Suggestions"
    demo_command "devkit ask 'find files larger than 100MB' <<< 'n'"
    
    demo_step "3a. AI Command Explanation"
    demo_command "devkit explain 'docker run -p 8080:80 nginx'"
else
    echo -e "${YELLOW}⚠️  Skipping AI demos (GEMINI_API_KEY not set)${NC}"
fi

# 4. Project Workspace
demo_step "4. Project Workspace Initialization"
demo_command "devkit init --force"
demo_command "ls -la .devkit/"

# 5. Running Snippets (generates history)
demo_step "5. Execute Snippets"
demo_command "devkit snippet run git-log"

# 6. Time-Travel Debugging
demo_step "6. Time-Travel: View Command History"
demo_command "devkit rewind"
demo_command "devkit rewind -n 5"

# 7. Configuration
demo_step "7. View Configuration"
demo_command "devkit config"

# 8. Git Commit Demo (in git repo)
if [ -d .git ]; then
    demo_step "8. Git Commit Helper"
    
    # Make a test change
    echo "# Demo change" >> DEMO_FILE.txt
    git add DEMO_FILE.txt 2>/dev/null || true
    
    # Show interactive commit
    echo -e "${CYAN}Demo: Interactive commit (would prompt for type/scope/description)${NC}"
    echo "devkit commit"
    
    # Show AI commit
    if [ ! -z "$GEMINI_API_KEY" ]; then
        echo -e "${CYAN}Demo: AI-generated commit${NC}"
        echo "devkit commit --ai"
    fi
    
    # Show commit with flags
    echo -e "${CYAN}Demo: Commit with signoff${NC}"
    echo "devkit commit --ai --signoff"
    
    # Cleanup
    git reset HEAD DEMO_FILE.txt 2>/dev/null || true
    rm -f DEMO_FILE.txt
else
    echo -e "${YELLOW}⚠️  Not in git repo - skipping commit demos${NC}"
fi

# 9. Log Analysis Demo
demo_step "9. Log Analysis"
cat > demo.log << 'LOGEOF'
INFO: Application starting...
INFO: Loading configuration
ERROR: Connection failed to database
ERROR: java.sql.SQLException: Connection timeout
    at DatabaseConnector.connect(DatabaseConnector.java:42)
    at Application.start(Application.java:15)
WARNING: Retrying connection...
ERROR: Max retries exceeded
LOGEOF

if [ ! -z "$GEMINI_API_KEY" ]; then
    demo_command "devkit logs analyze demo.log"
else
    demo_command "cat demo.log"
    echo -e "${CYAN}(AI analysis would identify: Connection timeout, max retries, suggest fixes)${NC}"
fi
rm demo.log

# 10. Emergency Features
demo_step "10. Emergency Rollback (Panic Mode)"
demo_command "devkit panic --stats"

# 11. Snippet Operations
demo_step "11. Advanced Snippet Operations"
demo_command "devkit snippet export demo_backup.json"
demo_command "devkit snippet delete ports"
demo_command "devkit snippet import demo_backup.json"

# 12. Cleanup Demo
demo_step "12. Cleanup"
demo_command "rm -f demo_snippets.json demo_backup.json"

echo ""
echo -e "${GREEN}=========================================="
echo "Demo Complete!"
echo "==========================================${NC}"
echo ""
echo "Summary of features demonstrated:"
echo "  ✓ Snippet management (save, list, search, run, export, import)"
echo "  ✓ AI command suggestions (ask, explain)"
echo "  ✓ Project workspace initialization"
echo "  ✓ Time-travel debugging (command history)"
echo "  ✓ Log analysis"
echo "  ✓ Git commit helpers"
echo "  ✓ Emergency rollback tools"
echo ""
echo "Try these yourself:"
echo "  devkit ask 'your question'"
echo "  devkit commit --ai"
echo "  devkit rewind --analyze"
echo "  devkit panic"