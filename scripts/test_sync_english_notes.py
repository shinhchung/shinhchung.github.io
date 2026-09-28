import subprocess
import tempfile
import unittest
from pathlib import Path

from sync_english_notes import sync, metadata


class SyncTests(unittest.TestCase):
    def test_create_update_delete_and_scope(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            vault, site = root / "vault", root / "site"
            (vault / "HH-vault").mkdir(parents=True)
            notes = site / "content/notes"
            notes.mkdir(parents=True)
            self.git(vault, "init")
            self.git(vault, "config", "user.name", "Test")
            self.git(vault, "config", "user.email", "test@example.com")
            source = vault / "HH-vault/2026-09-28.md"
            source.write_text("# English practice\n\nOriginal sentence.\n", encoding="utf-8")
            (vault / "HH-vault/ccna.md").write_text("# CCNA\nEnglish materials only.", encoding="utf-8")
            (vault / "HH-vault/private.md").write_text("# English practice\n<!-- publish: false -->", encoding="utf-8")
            (notes / "existing.md").write_text("Existing unrelated note.", encoding="utf-8")
            self.commit(vault)
            sync(vault, site)
            pages = list(notes.glob("english-*.md"))
            self.assertEqual(len(pages), 1)
            page = pages[0]
            first = page.read_text(encoding="utf-8")
            slug = metadata(first)["slug"]
            sync(vault, site)
            self.assertEqual(first, page.read_text(encoding="utf-8"))
            source.write_text("# Changed title\n\nUpdated sentence.\n", encoding="utf-8")
            self.commit(vault)
            sync(vault, site)
            self.assertEqual(metadata(page.read_text(encoding="utf-8"))["slug"], slug)
            self.assertIn("Updated sentence.", page.read_text(encoding="utf-8"))
            source.unlink()
            self.commit(vault)
            sync(vault, site)
            self.assertFalse(page.exists())
            self.assertTrue((notes / "existing.md").exists())

    @staticmethod
    def git(repo, *args):
        subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)

    def commit(self, repo):
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-m", "fixture")


if __name__ == "__main__":
    unittest.main()
