"""The opt-in copy lint in scripts/validate.py (`--copy`), on small synthetic texts.

Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("validate", ROOT / "scripts/validate.py")
validate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate)


def rules(found: list[tuple[str, str]]) -> list[str]:
    return [rule for rule, _ in found]


class ReadmeLintTest(unittest.TestCase):
    def test_flags_test_arm_variant_and_run_id_labels(self) -> None:
        text = "Arm F4d passed.\nSee v6f4b.\nRun W2-F4d-1 stopped.\n"
        found = validate.copy_readme_findings("README.md", text)
        self.assertEqual(rules(found), ["label"] * 3)
        self.assertIn("README.md:3:", found[2][1])
        self.assertIn("'W2-F4d-1'", found[2][1])

    def test_ignores_label_like_words(self) -> None:
        text = "F4 key, F4e, xF4d, v6.0.0-rc.1, T1-T8 and run 2-3-4.\n"
        self.assertEqual(validate.copy_readme_findings("README.md", text), [])

    def test_flags_owner_persona_in_both_languages(self) -> None:
        en = validate.copy_readme_findings("README.md", "The owner adopted it.\n")
        zh = validate.copy_readme_findings("README.zh.md", "作者决定采用。\n作者本人使用一周。\n")
        self.assertEqual(rules(en), ["persona"])
        self.assertEqual(rules(zh), ["persona", "persona"])

    def test_neutral_voice_and_original_author_pass(self) -> None:
        text = "It was shipped as the release candidate anyway.\n原作者 Zara Zhang，MIT 许可。\nowners\n"
        self.assertEqual(validate.copy_readme_findings("README.md", text), [])

    def test_bare_author_word_is_flagged_outside_credits(self) -> None:
        found = validate.copy_readme_findings("README.zh.md", "## 评测结果\n\n由作者采用。原作者不算。\n")
        self.assertEqual(rules(found), ["persona"])
        self.assertIn("README.zh.md:3:", found[0][1])

    def test_author_word_is_allowed_in_credits_and_licence_sections(self) -> None:
        for heading in ("## 许可与致谢", "## 致谢", "## License", "## Credits", "## Acknowledgements"):
            text = f"{heading}\n\n该项目的作者是 Zara Zhang。\n\n### 来源\n\n作者保留版权。\n"
            self.assertEqual(validate.copy_readme_findings("README.zh.md", text), [], heading)

    def test_credits_section_ends_at_the_next_heading_of_its_level(self) -> None:
        text = "## 致谢\n\n作者是 Zara Zhang。\n\n## 原则\n\n作者仍决定采用。\n"
        found = validate.copy_readme_findings("README.zh.md", text)
        self.assertEqual(rules(found), ["persona"])
        self.assertIn("README.zh.md:7:", found[0][1])

    def test_owner_persona_is_flagged_even_in_a_credits_section(self) -> None:
        found = validate.copy_readme_findings("README.md", "## Credits\n\nThe owner adopted it.\n")
        self.assertEqual(rules(found), ["persona"])

    def test_persona_inside_code_fence_is_ignored(self) -> None:
        text = "```\nthe owner\n```\n"
        self.assertEqual(validate.copy_readme_findings("README.md", text), [])

    def test_fraction_three_times_across_forms_fails(self) -> None:
        text = "Failed in 3 of 24.\nAgain 3/24.\n24 次运行中有 3 次。\n"
        found = validate.copy_readme_findings("README.md", text)
        self.assertEqual(rules(found), ["fraction"])
        self.assertIn("'3 of 24' appears 3 times", found[0][1])
        self.assertIn("lines 1, 2, 3", found[0][1])
        self.assertIn("counts repeated numbers, not claims", found[0][1])

    def test_chinese_fraction_with_comma_and_other_measure_words(self) -> None:
        text = "在 12 次运行中，12 次都成功。12 次中 12 次。12 张中 12 张。\n"
        found = validate.copy_readme_findings("README.zh.md", text)
        self.assertEqual(rules(found), ["fraction"])
        self.assertIn("'12 of 12' appears 3 times", found[0][1])

    def test_fraction_twice_passes(self) -> None:
        text = "Failed in 3 of 24 (lead).\nEvidence: 3 of 24.\nAlso 12 of 12, 2 of 12, 1 of 6.\n"
        self.assertEqual(validate.copy_readme_findings("README.md", text), [])

    def test_dates_versions_and_paths_are_not_fractions(self) -> None:
        text = "v6.0/1, a/1/2/b, 2026/11/13 three times: 2026/11/13 2026/11/13 docs/2/3 docs/2/3 docs/2/3\n"
        self.assertEqual(validate.copy_readme_findings("README.md", text), [])


class SvgLintTest(unittest.TestCase):
    @staticmethod
    def svg(*lines: str) -> str:
        body = "".join(f"<text x='0' y='{i}'>{t}</text>" for i, t in enumerate(lines))
        return f"<svg xmlns='http://www.w3.org/2000/svg'>{body}</svg>"

    def test_orphan_asterisk_fails(self) -> None:
        text = self.svg("not irreversible steps*", "Decided for you*", "* only after an explicit yes")
        found = validate.copy_svg_findings("assets/x.svg", text)
        self.assertEqual(rules(found), ["svg-mark"])
        self.assertIn("2 label(s) marked '*' but 1 footnote(s)", found[0][1])

    def test_label_without_any_footnote_fails(self) -> None:
        found = validate.copy_svg_findings("assets/x.svg", self.svg("Decided for you*"))
        self.assertEqual(rules(found), ["svg-mark"])

    def test_distinct_marks_with_footnotes_pass(self) -> None:
        text = self.svg("not irreversible steps*", "Decided for you†",
                        "* only after an explicit yes", "† listed so you can undo it")
        self.assertEqual(validate.copy_svg_findings("assets/x.svg", text), [])

    def test_mark_with_two_footnotes_fails(self) -> None:
        text = self.svg("Decided for you*", "* only after an explicit yes", "* listed so you can undo it")
        found = validate.copy_svg_findings("assets/x.svg", text)
        self.assertEqual(rules(found), ["svg-mark"])
        self.assertIn("mark '*' has 2 footnotes", found[0][1])

    def test_footnote_mark_no_label_uses_fails(self) -> None:
        text = self.svg("Decided for you*", "* listed so you can undo it", "† only after an explicit yes")
        found = validate.copy_svg_findings("assets/x.svg", text)
        self.assertEqual(rules(found), ["svg-mark"])
        self.assertIn("footnote mark '†' is used by no label", found[0][1])

    def test_tspan_text_and_unmarked_svg_pass(self) -> None:
        text = "<svg><text><tspan>BEFORE</tspan><tspan>a * b</tspan></text></svg>"
        self.assertEqual(validate.copy_svg_findings("assets/x.svg", text), [])


class CopyModeTest(unittest.TestCase):
    def test_copy_findings_on_clean_tree_is_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "assets").mkdir()
            (root / "README.md").write_text("It was shipped anyway. 3 of 24.\n", encoding="utf-8")
            (root / "README.zh.md").write_text("仍然发布了候选版本。\n", encoding="utf-8")
            (root / "assets/a.svg").write_text(SvgLintTest.svg("label*", "* note"), encoding="utf-8")
            self.assertEqual(validate.copy_findings(root), [])
            (root / "assets/b.svg").write_text(SvgLintTest.svg("orphan*"), encoding="utf-8")
            self.assertEqual(rules(validate.copy_findings(root)), ["svg-mark"])

    def test_cli_exit_codes(self) -> None:
        default = subprocess.run([sys.executable, str(ROOT / "scripts/validate.py")],
                                 capture_output=True, text=True, timeout=60)
        self.assertEqual(default.returncode, 0, default.stdout)
        copy = subprocess.run([sys.executable, str(ROOT / "scripts/validate.py"), "--copy"],
                              capture_output=True, text=True, timeout=60)
        self.assertIn(copy.returncode, (0, 1))
        self.assertEqual(copy.returncode == 1, "COPY [" in copy.stdout)


if __name__ == "__main__":
    unittest.main()
