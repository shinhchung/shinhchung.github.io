---
title: "Git & Jekyll Workflow Notes"
date: 2025-07-19
tags: [git, code, workflow]
folder: "Programming"
---

## Git Workflow

### Stage all changes at once

```bash
git add .
```

`.` means add all modified or new files.

---

### Correct commit message format (to avoid commitlint errors)

```bash
git commit -m "feat: update about page and fix broken icons"
```

| Type | Purpose |
|------|---------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation changes |
| style | Formatting (no logic change) |
| refactor | Code refactor (not a bug fix) |
| chore | Misc tasks (no functional impact) |

> Commit message must follow the format `type: message`, otherwise `commitlint` or `husky` will block the commit.

---

### Push to GitHub

```bash
git push origin main
```

---

## Errors I Encountered

### YAML syntax error

```
could not find expected ':' while scanning a simple key
```

Fix: Open the `.yml` file in VS Code, check indentation, colons, and quotes — especially in locale files like `en.yml`.

---

## Local Jekyll Testing

```bash
bundle exec jekyll serve
```

Preview at `http://localhost:4000`. YAML errors will prevent startup — fix and restart.

---

## Quick Tips

- Use `git status` before committing to see what changed
- If stuck on commit format, `--no-verify` ignores checks (not recommended long-term)
