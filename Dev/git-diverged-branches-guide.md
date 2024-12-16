# Fix Diverged Branches: Local and Remote

## Scenario
Your local branch (`main`) and the remote (`origin/main`) have diverged:
- **Local**: 2 unique commits
- **Remote**: 14 unique commits

## Solution: Rebase and Push

### 1. Pull Remote Changes
Apply remote commits first, then your local commits:
```bash
git pull --rebase origin main
```

### 2. Resolve Conflicts (if any)
- Identify and edit conflicting files
- Mark conflicts as resolved:
  ```bash
  # Edit conflicting files manually
  git add <conflicted-file>
  
  # Continue the rebase process
  git rebase --continue
  ```

### 3. Push Updated Branch
```bash
git push origin main
```

## Optional: Overwrite Remote 

### Force Push (Use with Caution)
Completely replace the remote branch with your local version:
```bash
git push --force origin main
```
⚠️ **Warning**: Only use this method if you are absolutely certain that remote changes are unnecessary.

## Best Practices
- Always communicate with team before force pushing
- Backup important changes before complex git operations
- Verify the state of both local and remote branches

## Potential Risks
- Losing remote commits
- Breaking collaborative workflows
- Creating inconsistent repository state

## Alternative Approaches
1. Merge instead of rebase
2. Use `git pull --rebase=interactive`
3. Carefully review changes before pushing

## Troubleshooting
- If rebase becomes too complex, consider:
  ```bash
  # Abort the rebase
  git rebase --abort
  
  # Or merge instead
  git pull --no-rebase
  ```
