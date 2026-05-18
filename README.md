# shinhchung.github.io

Personal site at [blog.hnghd.com](https://blog.hnghd.com).

## Stack

- **Hugo** — static site generator (v0.160.0 extended)
- **Theme** — custom `hnghd` (based on PaperMod)
- **Deploy** — GitHub Actions → GitHub Pages

## Content sections

| Section | Path | Description |
|---------|------|-------------|
| Blog | `content/blog/` | Writing on life, tech, and the world |
| Notes | `content/notes/` | Short-form notes |
| Recipes | `content/recipes/` | Food recipes |
| News | `content/news/` | 股神晨報 morning briefs |

## Local development

```bash
hugo server -D
```

## Deploy

Push to `main` → GitHub Actions builds and deploys automatically.
