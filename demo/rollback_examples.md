# DevKit Rollback Examples

This folder contains common rollback scenarios and examples for the `devkit panic` command.

## Common Dangerous Commands

### Git Operations
```bash
# Dangerous: Force push to main
git push --force origin main

# Rollback: Revert the commit
git revert HEAD
git push origin main

# Or reset to previous commit (if safe)
git reset --hard HEAD~1
git push --force origin main  # Only if you're sure!
```

### Docker Operations
```bash
# Dangerous: Remove all containers and images
docker system prune -af

# Rollback: Restore from backup or rebuild
docker pull <image-name>
docker run <image-name>
```

### Database Operations
```bash
# Dangerous: Drop database
mysql -e "DROP DATABASE production;"

# Rollback: Restore from backup
mysql -e "CREATE DATABASE production;"
mysql production < backup.sql
```

### Kubernetes Operations
```bash
# Dangerous: Delete deployment
kubectl delete deployment my-app

# Rollback: Recreate deployment
kubectl apply -f deployment.yaml
kubectl rollout status deployment/my-app
```

### NPM/Package Operations
```bash
# Dangerous: Publish to npm
npm publish

# Rollback: Unpublish (within 72 hours)
npm unpublish <package>@<version>
```

## Using DevKit Panic Mode

1. **Check for dangerous commands:**
   ```bash
   devkit panic
   ```

2. **Get AI-powered rollback suggestions:**
   ```bash
   devkit panic  # Will prompt for AI analysis
   ```

3. **View dangerous command statistics:**
   ```bash
   devkit panic --stats
   ```

4. **Time-travel debugging:**
   ```bash
   devkit rewind --analyze
   ```

## Prevention Tips

- Always test commands in staging first
- Use `devkit rewind` to review recent commands
- Set up proper backups before dangerous operations
- Use `devkit panic --stats` regularly to monitor risky behavior

## Emergency Contacts

- **Database**: Contact DBA team
- **Kubernetes**: Contact DevOps team  
- **Git**: Contact repository admin
- **Docker**: Check container registry backups
