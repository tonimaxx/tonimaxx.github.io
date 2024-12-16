# 🚀 Triggering GitHub Actions Workflow Manually

This guide explains how to **manually trigger** a GitHub Actions workflow that has `workflow_dispatch` enabled.

## 📝 Pre-requisites

### Workflow Configuration
Your workflow file must include `workflow_dispatch` in the `on` section:

```yaml
on:
  workflow_dispatch:
```

### Access Requirements
- You need **maintainer** or **write access** to trigger workflows

## 🛠️ Steps to Trigger a Manual Workflow

### 1. Navigate to Repository
- Go to your repository on **GitHub**

### 2. Access the Actions Tab
- Click on the **"Actions"** tab at the top of the repository

### 3. Select the Workflow
- In the left sidebar, locate the workflow name (e.g., **"Generate Index Files"**)

### 4. Trigger the Workflow
- Find the **"Run workflow"** button near the top-right corner
- If `workflow_dispatch` is configured, the button will be visible

### 5. Provide Input (Optional)
- Some workflows allow optional input parameters
- Fill in any required or optional input fields if prompted

### 6. Run the Workflow
- Click **"Run workflow"** to start the process

## 📊 Monitoring Workflow Execution

### Progress Tracking
- Monitor workflow status in the **Actions** tab
- Status indicators:
  - ✅ Success
  - ❌ Failure
  - ⏳ In Progress

### Detailed Logs
- Click on individual job names to view:
  - Detailed step-by-step logs
  - Execution outputs
  - Error messages (if any)

## 🔧 Troubleshooting

### Workflow Not Triggering
**Potential Issues:**
- Incorrect `workflow_dispatch` configuration
- Insufficient repository permissions
- Workflows disabled in repository settings

### Verification Checklist
- Confirm `workflow_dispatch` in YAML file
- Check repository access levels
- Verify Actions are enabled in repository settings

## 📂 Example Workflow File

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

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.x

      - name: Install Python dependencies
        run: python -m pip install --upgrade pip

      - name: Generate index.md files
        run: python generate_index.py

      - name: Commit and push changes
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add .
          git commit -m "Auto-generate index.md files"
          git push
```

## ✅ Quick Reference

- **Trigger Location**: Repository > Actions Tab
- **Key Configuration**: `workflow_dispatch` in YAML
- **Access Needed**: Write/Maintainer permissions

## 🚨 Best Practices

- Always review workflow steps before running
- Use manual triggers for testing or one-off tasks
- Keep workflows idempotent (safe to run multiple times)

Happy Automating! 🚀✨
