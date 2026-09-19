"""Dependency-free regression checks for release validation."""

import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from scripts import neanderthai as tool


class ValidationTests(unittest.TestCase):
    def test_reference_links_are_checked_from_their_own_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            skill = Path(temporary) / "neanderthai"
            shutil.copytree(tool.SOURCE, skill)
            reference = skill / "references" / "communication.md"
            reference.write_text("[recovery](recovery.md) [heading](#local)\n", encoding="utf-8")
            self.assertEqual(tool.validate_tree(skill), [])
            reference.write_text("[missing](missing.md)\n", encoding="utf-8")
            self.assertTrue(any("missing.md" in error for error in tool.validate_tree(skill)))
            outside = Path(temporary) / "outside.md"
            outside.write_text("outside bundle", encoding="utf-8")
            reference.write_text("[outside](../../outside.md)\n", encoding="utf-8")
            self.assertTrue(any("out-of-bundle" in error for error in tool.validate_tree(skill)))

    def test_binary_assets_do_not_crash_text_checks(self):
        with tempfile.TemporaryDirectory() as temporary:
            skill = Path(temporary) / "neanderthai"
            shutil.copytree(tool.SOURCE, skill)
            (skill / "asset.png").write_bytes(b"\x89PNG\xff")
            self.assertEqual(tool.validate_tree(skill), [])

    def test_windows_user_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            skill = Path(temporary) / "neanderthai"
            shutil.copytree(tool.SOURCE, skill)
            (skill / "references" / "recovery.md").write_text(
                r"C:\Users\example\private", encoding="utf-8")
            self.assertTrue(any("absolute path" in error for error in tool.validate_tree(skill)))

    def test_eval_schema_and_required_coverage(self):
        cases = json.loads((tool.ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        invalid = [
            {}, [None], cases + [cases[0]],
            [{**case, "input": " "} for case in cases],
            [{**case, "category": []} for case in cases],
            [case for case in cases if case["category"] != "feedback"],
        ]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "evals").mkdir()
            with patch.object(tool, "ROOT", root), contextlib.redirect_stdout(io.StringIO()) as output:
                for data in invalid:
                    with self.subTest(data=type(data).__name__):
                        (root / "evals" / "cases.json").write_text(json.dumps(data), encoding="utf-8")
                        with self.assertRaises(SystemExit):
                            tool.run_evals()
                (root / "evals" / "cases.json").write_text(json.dumps(cases), encoding="utf-8")
                tool.run_evals()
                self.assertIn("no model behavior tested", output.getvalue())


if __name__ == "__main__":
    unittest.main()
