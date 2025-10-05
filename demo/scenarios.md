# DevKit Demo Scenarios

## Scenario 1: Daily Development Workflow (2 min)
```bash
# Save commonly used commands
devkit snippet save build "npm run build && npm test"
devkit snippet save deploy "git push && kubectl rollout restart deployment/app"

# Use them
devkit snippet run build
devkit snippet run deploy

# Review what happened
devkit rewind
```

## Scenario 2: Debugging a Failed Deployment (3 min)

```bash
# Something broke in production
devkit panic

# AI suggests rollback steps
# Review recent commands
devkit rewind --analyze

# Check logs
kubectl logs -f pod-name > error.log
devkit logs analyze error.log
```

## Scenario 3: Git Workflow Enhancement (2 min)

```bash
# Make changes
git add .

# AI generates perfect commit
devkit commit --ai

# Want to edit it?
devkit commit --ai --edit

# Need signoff for compliance?
devkit commit --ai --signoff
```

## Scenario 4: Team Collaboration (2 min)

```bash
# Initialize project workspace
devkit init

# Share snippets with team
devkit snippet export team-snippets.json
# Team members: devkit snippet import team-snippets.json

# Everyone uses same commands
devkit snippet run test
devkit snippet run deploy
```

## Scenario 5: Learning New Tools (1 min)

```bash
# Don't know the command?
devkit ask "find all python files modified today"

# Don't understand a command?
devkit explain "find . -name '*.py' -mtime 0"

# Save it for later
# (AI prompts to save automatically)
```
