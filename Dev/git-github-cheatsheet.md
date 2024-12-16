# 📘 Complete Git & GitHub Cheatsheet for Daily Use

## 🚀 Getting Started

### Installation & Configuration
```bash
# Install Git
sudo apt-get install git    # Ubuntu/Debian
brew install git           # macOS with Homebrew

# Configure user information
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Configure default branch name
git config --global init.defaultBranch main

# View configurations
git config --list
```

### Repository Setup
```bash
# Initialize a new repository
git init

# Clone an existing repository
git clone <repository-url>
git clone <repository-url> <directory-name>    # Clone to specific directory

# Clone specific branch
git clone -b <branch-name> <repository-url>
```

## 📝 Daily Workflow Commands

### Basic File Operations
```bash
# Check status
git status
git status -s    # Short status

# Stage files
git add <file-name>
git add .                  # Stage all changes
git add *.js              # Stage all JavaScript files
git add -p                # Interactively stage parts of files

# Unstage files
git restore --staged <file-name>
git reset HEAD <file-name>

# Discard changes
git restore <file-name>
git checkout -- <file-name>    # Old syntax
```

### Committing Changes
```bash
# Create a commit
git commit -m "Your message"
git commit -am "Your message"    # Stage tracked files and commit

# Modify last commit
git commit --amend -m "New message"
git commit --amend --no-edit     # Add changes to last commit without editing message

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

### Branching and Merging
```bash
# Branch operations
git branch                          # List branches
git branch -a                       # List all branches (including remote)
git branch <branch-name>            # Create branch
git branch -d <branch-name>         # Delete branch
git branch -D <branch-name>         # Force delete branch
git branch -m <new-name>            # Rename current branch
git branch -m <old> <new>           # Rename specific branch

# Switch branches
git checkout <branch-name>          # Old syntax
git switch <branch-name>            # New syntax
git checkout -b <branch-name>       # Create and switch
git switch -c <branch-name>         # Create and switch (new syntax)

# Merge operations
git merge <branch-name>             # Merge branch into current branch
git merge --abort                   # Abort merge in case of conflicts
git merge --squash <branch-name>    # Squash merge
```

### Stashing Changes
```bash
# Basic stash operations
git stash                    # Stash changes
git stash save "message"     # Stash with description
git stash list              # List stashes
git stash show              # Show stash contents
git stash pop               # Apply and remove last stash
git stash apply             # Apply without removing
git stash drop              # Remove last stash
git stash clear             # Remove all stashes

# Partial stash
git stash -p               # Interactively stash changes
git stash push -m "message" <file-path>    # Stash specific files
```

## 🌐 Remote Operations

### Managing Remotes
```bash
# Remote operations
git remote -v                                # List remotes
git remote add <name> <url>                  # Add remote
git remote remove <name>                     # Remove remote
git remote rename <old-name> <new-name>      # Rename remote
git remote set-url <name> <new-url>         # Change remote URL
```

### Syncing with Remote
```bash
# Fetch changes
git fetch                   # Fetch all branches
git fetch <remote>          # Fetch specific remote
git fetch --all            # Fetch all remotes

# Pull changes
git pull                    # Fetch and merge
git pull --rebase          # Fetch and rebase
git pull <remote> <branch>  # Pull specific branch

# Push changes
git push                    # Push to upstream branch
git push -u origin <branch> # Push and set upstream
git push --force           # Force push (use carefully!)
git push --force-with-lease # Safer force push
```

## 🔍 Inspection and Comparison

### Viewing History
```bash
# Log operations
git log                     # View commit history
git log --oneline          # Compact log view
git log --graph            # Show branch graph
git log -p                 # Show patches
git log --stat             # Show stats
git log --author="name"    # Filter by author
git log --since="2 weeks"  # Filter by date

# Blame
git blame <file>           # Show who changed what
git blame -L 10,20 <file>  # Blame specific lines
```

### Comparing Changes
```bash
# Diff operations
git diff                   # Show unstaged changes
git diff --staged         # Show staged changes
git diff <commit> <commit> # Compare commits
git diff <branch>..<branch> # Compare branches
git diff --name-only      # Show only changed files
```

## 🛠️ Advanced Operations

### Rebase Operations
```bash
# Basic rebase
git rebase <branch>
git rebase -i HEAD~3      # Interactive rebase last 3 commits
git rebase --abort        # Abort rebase
git rebase --continue     # Continue after resolving conflicts

# Squash commits
git rebase -i HEAD~N      # N is number of commits to squash
```

### Cherry-pick
```bash
# Apply specific commits
git cherry-pick <commit-hash>
git cherry-pick <hash1> <hash2>    # Multiple commits
git cherry-pick --abort            # Abort cherry-pick
git cherry-pick --continue         # Continue after resolving conflicts
```

### Tags
```bash
# Tag operations
git tag                           # List tags
git tag -a v1.0.0 -m "message"    # Create annotated tag
git tag v1.0.0                    # Create lightweight tag
git tag -d v1.0.0                # Delete tag
git push origin --tags           # Push all tags
git push origin v1.0.0           # Push specific tag
```

## 🧹 Maintenance and Cleanup

### Cleaning Operations
```bash
# Clean working directory
git clean -n               # Show what will be cleaned
git clean -f              # Force clean untracked files
git clean -fd             # Clean untracked files and directories
git clean -fX             # Clean ignored files

# Garbage collection
git gc                    # Run garbage collection
git prune                # Remove unreachable objects
```

### Repository Maintenance
```bash
# Verify repository
git fsck                  # Check repository integrity
git reflog                # View reference logs
git maintenance start     # Enable background maintenance
```

## 🚫 Common Issues and Fixes

### Fixing Mistakes
```bash
# Remove file from all commits
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch <file>" HEAD

# Reset to remote state
git fetch origin
git reset --hard origin/<branch>

# Fix wrong commit message
git commit --amend -m "New message"

# Recover deleted branch
git reflog                # Find the hash
git checkout -b <branch> <hash>
```

### Resolving Conflicts
```bash
# Tools for conflict resolution
git mergetool            # Launch configured merge tool
git checkout --ours <file>    # Keep our version
git checkout --theirs <file>  # Keep their version

# After resolving
git add <resolved-files>
git commit               # Complete the merge
```

## 🔑 GitHub-Specific Operations

### Pull Requests
```bash
# Create PR from command line (needs GitHub CLI)
gh pr create --title "Title" --body "Description"

# Review PR
gh pr checkout <number>
gh pr review <number> --approve
gh pr review <number> --comment "feedback"
```

### GitHub Actions
```bash
# View workflow runs
gh run list

# Watch running workflow
gh run watch

# Download artifacts
gh run download <run-id>
```

### Repository Management
```bash
# Create repository
gh repo create <name> --public/--private

# Fork repository
gh repo fork <repository>

# Clone repository
gh repo clone <repository>
```

## 📝 Best Practices

1. **Commit Messages**
   - Write clear, concise commit messages
   - Use present tense ("Add feature" not "Added feature")
   - First line should be 50 characters or less
   - Include a more detailed description after the first line if needed

2. **Branching**
   - Use feature branches for new work
   - Keep `main`/`master` branch stable
   - Delete merged branches
   - Use meaningful branch names (e.g., `feature/user-auth`, `bugfix/login-error`)

3. **Before Pushing**
   - Run tests
   - Review your changes (`git diff`)
   - Ensure commits are logical and atomic
   - Check for sensitive information

4. **Collaboration**
   - Pull before pushing
   - Resolve conflicts locally
   - Communicate with team about major changes
   - Use Pull Requests for code review

Remember to regularly update your Git knowledge as new features and best practices emerge. This cheatsheet covers the most common daily operations, but Git has many more capabilities for specific situations.