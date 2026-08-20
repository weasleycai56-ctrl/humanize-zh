from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_text.py"
FIXTURES = ROOT / "tests" / "fixtures"

spec = importlib.util.spec_from_file_location("audit_text", SCRIPT)
audit_text = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = audit_text
spec.loader.exec_module(audit_text)


def load_cases():
    for path in sorted(FIXTURES.glob("*.json")):
        for case in json.loads(path.read_text(encoding="utf-8")):
            yield path.name, case


class FixtureContractTests(unittest.TestCase):
    def test_all_profiles_and_modes_are_covered(self):
        cases = [case for _, case in load_cases()]
        self.assertEqual(
            {"casual", "professional", "academic", "social", "marketing"},
            {case["style"] for case in cases},
        )
        self.assertEqual({"audit", "light", "strong"}, {case["mode"] for case in cases})
        self.assertGreaterEqual(len(cases), 10)

    def test_fixture_schema_and_preservation_examples(self):
        required = {
            "id",
            "style",
            "mode",
            "input",
            "expected_rules",
            "preserve",
            "avoid_in_rewrite",
            "expected_after",
            "notes",
        }
        seen = set()
        for filename, case in load_cases():
            with self.subTest(case=case.get("id"), fixture=filename):
                self.assertEqual(required, set(case))
                self.assertNotIn(case["id"], seen)
                seen.add(case["id"])
                for token in case["preserve"]:
                    self.assertIn(token, case["input"])
                    self.assertIn(token, case["expected_after"])
                for phrase in case["avoid_in_rewrite"]:
                    self.assertNotIn(phrase, case["expected_after"])

    def test_expected_rules_are_found(self):
        for filename, case in load_cases():
            with self.subTest(case=case["id"], fixture=filename):
                report = audit_text.audit(case["input"])
                found = {issue["rule_id"] for issue in report["issues"]}
                self.assertTrue(set(case["expected_rules"]).issubset(found), (case["id"], found))


class CliTests(unittest.TestCase):
    def test_json_cli_has_authorship_disclaimer(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--text", "这是一段具体、清楚的通知。", "--format", "json"],
            check=True,
            capture_output=True,
            text=True,
        )
        report = json.loads(result.stdout)
        self.assertIn("不是 AI 作者身份检测", report["disclaimer"])
        self.assertEqual("低", report["signal"])

    def test_markdown_cli_is_explainable(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--text", "重磅发布，这份内容不容错过。"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("类型", result.stdout)
        self.assertIn("原因", result.stdout)
        self.assertIn("建议", result.stdout)
        self.assertIn("ZH03", result.stdout)


if __name__ == "__main__":
    unittest.main()
