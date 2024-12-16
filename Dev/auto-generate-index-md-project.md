# 🚀 Auto-Generate index.md for All Folders in GitHub

This project automates the creation of `index.md` files in all subdirectories while skipping the root folder and specified excluded directories. This is achieved using a Python script integrated with a GitHub Actions workflow.

## 📂 Workflow File: generate-index.yml

This GitHub Actions workflow runs the Python script to generate `index.md` files and pushes the changes back to the repository.

**File Location**: `.github/workflows/generate-index.yml`

```yaml
name: Generate Index Files

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  generate-index:
    runs-on: ubuntu-latest
    permissions:
      contents: write   # Allow pushing commits to the repository

    steps:
      # Step 1: Check out the code
      - name: Checkout repository
        uses: actions/checkout@v3

      # Step 2: Set up Python
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.x

      # Step 3: Install dependencies
      - name: Install Python dependencies
        run: python -m pip install --upgrade pip

      # Step 4: Generate index.md files
      - name: Generate index.md files
        run: |
          python generate_index.py

      # Step 5: Commit and push changes
      - name: Commit and push changes
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add .
          git commit -m "Auto-generate index.md files" || echo "No changes to commit"
          git push
```

## 🐍 Python Script: generate_index.py

This script generates an `index.md` file for all subdirectories excluding the root folder and directories defined in `EXCLUDE_DIRS`. Each `index.md` contains a list of files in its directory.

**File Location**: `generate_index.py`

```python
import os

# Directories to exclude from processing
EXCLUDE_DIRS = ['.github/workflows']

def generate_index_for_directory(root_dir):
    # Skip generating index.md in the root directory
    if root_dir == '.':
        return

    index_file = os.path.join(root_dir, 'index.md')

    with open(index_file, 'w') as f:
        f.write("# Index of files\n\n")
        for filename in sorted(os.listdir(root_dir)):
            if filename in ['index.md', '.DS_Store'] or os.path.isdir(os.path.join(root_dir, filename)):
                continue
            f.write(f"- [{filename}]({filename})\n")

def walk_directories_and_generate_index():
    for root, dirs, files in os.walk('.'):
        # Skip excluded directories
        if any(excl in root for excl in EXCLUDE_DIRS):
            continue
        
        generate_index_for_directory(root)

if __name__ == "__main__":
    walk_directories_and_generate_index()
    print("Index.md files have been generated successfully!")
```

## 🎯 Key Features

- **Automatic Indexing**
  - Generates an `index.md` file in every subfolder
  - Lists all files in the directory (excluding directories)

- **Root Folder Skipping**
  - No `index.md` is created in the root directory

- **Excluded Directories**
  - Add directories like `.github/workflows` to `EXCLUDE_DIRS` in the script to skip them

- **Seamless Automation**
  - Configured with GitHub Actions for continuous automation

## 🚀 How It Works

1. **Trigger**
   - Workflow runs automatically on a push to the main branch
   - Can also be triggered manually using `workflow_dispatch`

2. **Python Script Execution**
   - The script processes all subdirectories and generates `index.md` files
   - Skips directories defined in `EXCLUDE_DIRS` and the root folder

3. **Commit and Push**
   - The workflow commits the changes back to the repository
   - If no changes are detected, it avoids unnecessary commits

## 🛠️ Workflow Steps Summary

| Step | Description |
|------|-------------|
| Checkout repository | Fetches the latest code to the runner |
| Set up Python | Configures Python environment |
| Install dependencies | Ensures pip is up to date |
| Generate index.md files | Runs the Python script to create index.md |
| Commit and push changes | Pushes the generated files back to GitHub |

## ✅ Example Output

For a directory structure like this:
```
/  
|-- Dev/  
|   |-- file1.txt  
|   |-- file2.txt  
|-- Notes/  
|   |-- note1.md  
|   |-- note2.md  
|-- .github/workflows/  
```

The generated `index.md` files will look like:

**Dev/index.md**:
```markdown
# Index of files  

- [file1.txt](file1.txt)  
- [file2.txt](file2.txt)  
```

**Notes/index.md**:
```markdown
# Index of files  

- [note1.md](note1.md)  
- [note2.md](note2.md)  
```

No `index.md` is created in the root folder or `.github/workflows`.

## 🔧 Customization

1. **Exclude Additional Folders**
   Update the `EXCLUDE_DIRS` list in `generate_index.py`:
   ```python
   EXCLUDE_DIRS = ['.github/workflows', 'logs']
   ```

2. **Commit Message**
   Customize the commit message in the workflow:
   ```bash
   git commit -m "Auto-update index.md files 🎉"
   ```

3. **Trigger Manually**
   Use GitHub's Actions tab to trigger the workflow on demand

## 🎉 Final Notes

- **Automation Made Easy**: Generate consistent `index.md` files across your project
- **Skip Root Folder**: Avoid cluttering the root directory
- **Fully Configurable**: Exclude folders and tweak settings as needed

Happy Automating! 🚀✨
