from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_required_project_files_exist(self):
        required = {
            "SKILL.md",
            "README.md",
            "LICENSE",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "CODE_OF_CONDUCT.md",
            "CHANGELOG.md",
            "THIRD_PARTY_NOTICES.md",
            "VERSION",
            "agents/openai.yaml",
            ".github/workflows/ci.yml",
        }
        missing = sorted(path for path in required if not (ROOT / path).is_file())
        self.assertEqual([], missing)

    def test_skill_frontmatter_is_complete(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", skill, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = match.group(1)
        self.assertRegex(frontmatter, r"(?m)^name: humanize-zh$")
        description = re.search(r"(?m)^description: (.+)$", frontmatter)
        self.assertIsNotNone(description)
        self.assertNotIn("TODO", frontmatter)

    def test_version_is_consistent(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        self.assertIn(f"## [{version}]", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
        self.assertTrue((ROOT / "docs" / "releases" / f"v{version}.md").is_file())

    def test_no_repository_owner_placeholders_remain(self):
        matches = []
        placeholder = "github.com/" + "OWNER/"
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if placeholder in text:
                matches.append(str(path.relative_to(ROOT)))
        self.assertEqual([], matches)


if __name__ == "__main__":
    unittest.main()
