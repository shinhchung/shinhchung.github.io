"""Publish English learning notes from a checked-out HH-vault; standard library only."""

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], encoding="utf-8").strip()


def metadata(text):
    if not text.startswith("---\n"):
        return {}
    front = text.split("---", 2)[1]
    result = {}
    for line in front.strip().splitlines():
        key, separator, value = line.partition(": ")
        if separator:
            try:
                result[key] = json.loads(value)
            except json.JSONDecodeError:
                result[key] = value.strip('"\'')
    return result


def is_english(path, body, known=False):
    if "<!-- publish: false -->" in body:
        return False
    if known or "<!-- publish: english -->" in body:
        return True
    headings = "\n".join(re.findall(r"^#{1,6}\s+(.+)$", body, re.MULTILINE))
    return bool(re.search(r"\benglish\b|英文(?:學習|練習)", path.stem + "\n" + headings, re.I))


def sync(vault, site):
    vault, site = Path(vault).resolve(), Path(site).resolve()
    if not (vault / "HH-vault").is_dir():
        raise ValueError("HH-vault is missing; refusing to change published notes")
    notes = site / "content" / "notes"
    known = {}
    for page in notes.glob("english-*.md"):
        meta = metadata(page.read_text(encoding="utf-8"))
        if meta.get("folder") == "English Learning" and meta.get("source_path"):
            if meta["source_path"] in known:
                raise ValueError("Duplicate source path in published notes")
            known[meta["source_path"]] = (page, meta)

    output = {}
    for source in sorted((vault / "HH-vault").rglob("*.md")):
        relative = source.relative_to(vault)
        if source.is_symlink() or any(part.startswith(".") for part in relative.parts):
            continue
        source_path = relative.as_posix()
        body = source.read_text(encoding="utf-8").strip()
        if not is_english(source, body, source_path in known):
            continue
        revision = git(vault, "log", "-1", "--format=%H", "--", source_path)
        if not revision:
            raise ValueError("Source note must be committed before publication")
        if source_path in known:
            page, meta = known[source_path]
        else:
            date_match = re.match(r"\d{4}-\d{2}-\d{2}", source.stem)
            date = date_match[0] if date_match else git(vault, "log", "-1", "--format=%cs", "--", source_path)
            heading = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
            title = re.sub(r"^\d{4}-\d{2}-\d{2}\s*", "", heading[1] if heading else source.stem).strip() or "English Practice"
            slug = "english-" + date + "-" + hashlib.sha256(source_path.encode()).hexdigest()[:10]
            page = notes / (slug + ".md")
            if page.exists():
                raise ValueError("Generated filename is already occupied")
            meta = {"title": title, "date": date, "slug": slug, "folder": "English Learning", "tags": ["english", "learning"]}
        meta.update(source_path=source_path, source_revision=revision)
        front = "---\n" + "\n".join(key + ": " + json.dumps(value, ensure_ascii=False) for key, value in meta.items()) + "\n---\n\n"
        url = "https://github.com/shinhchung/Obsidian/blob/" + revision + "/" + quote(source_path, safe="/")
        output[page] = front + body + "\n\n---\n\n[HH-vault 原始筆記（需要 GitHub 存取權限）](" + url + ")\n"

    # Resolve everything before writing or removing any managed page.
    for page, content in output.items():
        if not page.exists() or page.read_text(encoding="utf-8") != content:
            page.write_text(content, encoding="utf-8", newline="\n")
    for page, _ in known.values():
        if page not in output:
            page.unlink()
    print(f"Synchronized {len(output)} English learning notes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--site", required=True, type=Path)
    args = parser.parse_args()
    sync(args.vault, args.site)
