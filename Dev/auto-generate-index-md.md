# Auto-Generate index.md for All Folders in GitHub

This guide describes how to automatically create an `index.md` file in every folder of your repository. The `index.md` will list all Markdown files (`.md`) within that folder, providing easy navigation for projects like GitHub Pages.

## How It Works

### 1. Script Functionality
- Recursively scans all folders in the repository
- Generates an `index.md` file in each folder with links to all `.md` files inside, excluding `index.md` itself

**Example Output for `/Dev`**:
```markdown
# Files in /Dev

- [file1.md](file1.md)
- [file2.md](file2.md)
```

### 2. Automation via GitHub Actions
- The script runs automatically whenever files are pushed to the repository
- Commits updated `index.md` files back to the repository

## Setup Guide

### 1. Add Python Script
Save the following script as `generate_index.py` in your repository:

```python
import os

def generate_indexes(root_path="."):
    for subdir, _, files in os.walk(root_path):
        if ".git" in subdir or "node_modules" in subdir:  # Ignore specific folders
            continue
        
        md_files = [f for f in files if f.endswith(".md") and f != "index.md"]
        
        if not md_files:
            continue
        
        output_file = os.path.join(subdir, "index.md")
        
        with open(output_file, "w") as f:
            f.write(f"# Files in {subdir}\n\n")
            for md_file in sorted(md_files):
                f.write(f"- [{md_file}]({md_file})\n")

if __name__ == "__main__":
    generate_indexes()
```

### 2. Add GitHub Workflow
Save the following as `.github/workflows/generate-index.yml`:

```yaml
name: Generate Index Files

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set Up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.x

      - name: Install Dependencies
        run: pip install --upgrade pip

      - name: Run Index Generator
        run: python generate_index.py

      - name: Commit and Push Changes
        run: |
          git config --local user.name "GitHub Action"
          git config --local user.email "action@github.com"
          git add .
          git commit -m "Auto-generate index.md files"
          git push
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 3. Push Changes
Commit and push the script and workflow to your repository. The workflow will automatically run and generate `index.md` files for all folders.

## Customization

### Exclude Folders
Add folders like `.git` or `node_modules` to the script's ignore list:
```python
if ".git" in subdir or "node_modules" in subdir or "some_other_folder" in subdir:
    continue
```

### Manual Triggers
- Run the workflow manually using the "Actions" tab in GitHub
- Useful for on-demand index regeneration

## Benefits
- Easy navigation across folder structures
- Automatically updated whenever files change
- Useful for GitHub Pages and documentation projects

## Tips
- Ensure your repository has the necessary GitHub Actions permissions
- Test the script locally before pushing to verify behavior
- Consider adding this to repositories with complex folder structures

Feel free to adapt this workflow for your project's specific needs! 🚀
