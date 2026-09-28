# Automatic English note publication

The Obsidian repository runs `.github/workflows/publish-english-notes.yml` after
pushes touching `HH-vault/**` or the workflow itself. It can also run manually.
It checks out the latest `main` from both repositories, runs
`scripts/sync_english_notes.py`, validates with Hugo, and pushes changed notes.
The website repository's existing Pages workflow then deploys the update.

A dedicated writable deploy key on `shinhchung/shinhchung.github.io` is stored as
`WEBSITE_DEPLOY_KEY` in the private Obsidian repository's Actions secrets. It is
not a personal access token. SSH pushes trigger the website deployment workflow.

## Selection and preservation

- Previously published English notes stay synchronized, retaining their URLs.
- New Markdown notes with `English` or `英文學習` / `英文練習` in their filename
  or headings are included. Alternatively add `<!-- publish: english -->`.
- Add `<!-- publish: false -->` to exclude a note and remove its published copy.
- Complete note bodies, including personal context, are public as approved by
  the owner. Unrelated vault files and hidden configuration directories are excluded.
- Deleting a source note removes its managed page on the next sync. Renaming a
  source note is treated as deletion plus addition, and may change its URL.
- Each source link points to that file's latest commit. Unchanged notes produce
  no new commit. New content must first be pushed to Obsidian's `main` branch.

## Local validation

```sh
python -m unittest discover -s scripts -p test_sync_english_notes.py
python scripts/sync_english_notes.py --vault /path/to/Obsidian --site .
hugo --minify
```

Use a clean checkout matching the committed vault revision. Check `/notes/`
and changed articles after deployment. To revoke automation access, remove the
website deploy key and the matching Obsidian Actions secret.
