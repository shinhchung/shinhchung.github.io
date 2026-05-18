---
title: "GitHub Release Guide"
date: 2025-07-27
tags: [git, github, code]
folder: "Programming"
---

How to create a GitHub Release — both via the web UI and via CLI.

---

## Prerequisites

- A GitHub repository
- Git installed: https://git-scm.com/
- For CLI: GitHub CLI (`gh`): https://cli.github.com/

Login with:

```bash
gh auth login
```

---

## UI Method (Web)

### Step 1: Commit and push

```bash
git add .
git commit -m "feat: add new feature"
git push origin main
```

### Step 2: Create and push a tag

```bash
git tag v1.2.3
git push origin v1.2.3
```

### Step 3: Create Release on GitHub

1. Go to your repo → find `Releases` in the sidebar
2. Click `Create a new release`
3. Fill in Tag version, Release title, Description
4. Click `Publish release`

---

## CLI Method

### Step 1–2: Same as above (commit, tag, push)

### Step 3: Create release via CLI

```bash
gh release create v1.2.3 \
  --title "v1.2.3" \
  --notes "### Bug Fixes\n- Fix JSON special character handling (#2481)"
```

Or use a Markdown file:

```bash
gh release create v1.2.3 \
  --title "v1.2.3" \
  --notes-file CHANGELOG.md
```

---

## Useful Commands

```bash
# Delete a release
gh release delete v1.2.3

# Delete a remote tag
git tag -d v1.2.3
git push origin :refs/tags/v1.2.3
```
