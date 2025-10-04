#!/bin/bash
# DevKit Examples Script
# Load common snippets to get started with DevKit

echo "🚀 Loading DevKit example snippets..."

# System monitoring snippets
python3 -m devkit.main snippet save ports "lsof -i -P -n | grep LISTEN"
python3 -m devkit.main snippet save size "du -sh * | sort -h"
python3 -m devkit.main snippet save find-large "find . -type f -size +100M"

# Git snippets
python3 -m devkit.main snippet save git-undo "git reset --soft HEAD~1"
python3 -m devkit.main snippet save git-clean "git clean -fd && git reset --hard HEAD"
python3 -m devkit.main snippet save git-log "git log --oneline -10"

# Docker snippets
python3 -m devkit.main snippet save docker-clean "docker system prune -af"
python3 -m devkit.main snippet save docker-ps "docker ps -a"
python3 -m devkit.main snippet save docker-logs "docker logs -f"

# Development snippets
python3 -m devkit.main snippet save npm-audit "npm audit fix"
python3 -m devkit.main snippet save pip-update "pip list --outdated"
python3 -m devkit.main snippet save disk-usage "df -h"

# Network snippets
python3 -m devkit.main snippet save ping-test "ping -c 4 google.com"
python3 -m devkit.main snippet save port-check "netstat -tulpn | grep"

echo "✅ Loaded 12 example snippets!"
echo ""
echo "📋 Your snippets:"
python3 -m devkit.main snippet list

echo ""
echo "🎯 Try these commands:"
echo "  python3 -m devkit.main snippet run ports     # Show listening ports"
echo "  python3 -m devkit.main snippet run size      # Show directory sizes"
echo "  python3 -m devkit.main snippet run git-undo  # Undo last commit"
echo "  python3 -m devkit.main snippet run docker-clean # Clean Docker system"
echo ""
echo "💡 Pro tip: Use 'python3 -m devkit.main ask <question>' for AI-powered command suggestions!"
