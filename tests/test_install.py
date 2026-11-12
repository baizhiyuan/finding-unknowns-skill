"""install.sh against temporary config directories (never the real ~/.claude).

Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEGIN = "<!-- finding-unknowns:always-on -->"
END = "<!-- /finding-unknowns:always-on -->"
OURS_AGENT = "---\nname: {0}\ndescription: \"agent for the finding-unknowns skill\"\n---\nbody\n"
LEGACY = {
    "skills/finding-unknowns/SKILL.md": "---\nname: finding-unknowns\ndescription: \"4.x\"\n---\nold\n",
    "skills/finding-unknowns/references/cartographer.md": "Cartographer ledger and Workflow rules\n",
    "skills/finding-unknowns/references/workflows.md": "Workflow templates for the ledger\n",
    "skills/keep-the-reasoning/SKILL.md": "---\nname: keep-the-reasoning\ndescription: \"x\"\n---\nsee finding-unknowns\n",
    "skills/theory-vs-result/SKILL.md": "---\nname: theory-vs-result\ndescription: \"x\"\n---\n",
    "agents/mechanism-auditor.md": "---\nname: mechanism-auditor\ndescription: \"theory-vs-result\"\n---\n",
    "commands/blindspot.md": "---\ndescription: \"blind-spot pass\"\n---\nInvoke the `finding-unknowns` skill\n",
    "commands/cartographer.md": "---\ndescription: \"x\"\n---\nInvoke the `finding-unknowns` skill\n",
    "commands/change-quiz.md": "---\ndescription: \"x\"\n---\nInvoke the `finding-unknowns` skill\n",
    "commands/keep-the-reasoning.md": "---\ndescription: \"x\"\n---\nUse the Skill tool\n",
    **{f"agents/{a}.md": OURS_AGENT.format(a) for a in ("blindspot-scout", "ledger-keeper", "prototype-smith", "quiz-master")},
}


class InstallTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.cfg = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, files: dict[str, str]) -> None:
        for rel, text in files.items():
            (self.cfg / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.cfg / rel).write_text(text, encoding="utf-8")

    def run_install(self, *args: str) -> subprocess.CompletedProcess:
        env = {**os.environ, "CLAUDE_CONFIG_DIR": str(self.cfg)}
        return subprocess.run(["bash", str(ROOT / "install.sh"), *args], env=env,
                              capture_output=True, text=True, timeout=60)

    def install(self, *args: str) -> str:
        result = self.run_install(*args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def files(self) -> set[str]:
        return {str(p.relative_to(self.cfg)) for p in self.cfg.rglob("*") if p.is_file()}

    def backups(self) -> list[Path]:
        return list(self.cfg.glob("finding-unknowns-backup-*"))

    def test_fresh_install(self) -> None:
        self.install()
        self.assertEqual(self.files(), {"CLAUDE.md", "skills/finding-unknowns/SKILL.md",
                                        "commands/fu-interview.md", "commands/fu-lookback.md"})
        claude = (self.cfg / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn((ROOT / "CLAUDE.md").read_text(encoding="utf-8").strip(), claude)
        self.assertTrue(claude.startswith(BEGIN))

    def test_upgrade_from_4x_retires_only_ours_and_keeps_theory_vs_result(self) -> None:
        self.write(LEGACY)
        out = self.install()
        left = self.files()
        for rel in ("skills/keep-the-reasoning/SKILL.md", "agents/blindspot-scout.md", "commands/cartographer.md",
                    "skills/finding-unknowns/references/workflows.md", "commands/keep-the-reasoning.md"):
            self.assertNotIn(rel, left)
        self.assertIn("skills/theory-vs-result/SKILL.md", left)
        self.assertIn("agents/mechanism-auditor.md", left)
        self.assertFalse((self.cfg / "skills/finding-unknowns/references").exists())
        [backup] = self.backups()
        self.assertTrue((backup / "skills/keep-the-reasoning/SKILL.md").is_file())
        self.assertTrue((backup / "agents/quiz-master.md").is_file())
        self.assertEqual((self.cfg / "skills/finding-unknowns/SKILL.md").read_bytes(),
                         (ROOT / "skills/finding-unknowns/SKILL.md").read_bytes())
        self.assertIn("Kept: theory-vs-result", out)

    def test_files_that_are_not_ours_are_left_or_backed_up(self) -> None:
        mine = {"skills/keep-the-reasoning/SKILL.md": "---\nname: keep-the-reasoning\n---\nmy own skill\n",
                "agents/blindspot-scout.md": "---\nname: blindspot-scout\n---\nmy own agent\n",
                "commands/fu-interview.md": "my own command\n"}
        self.write(mine)
        out = self.install()
        for rel in ("skills/keep-the-reasoning/SKILL.md", "agents/blindspot-scout.md"):
            self.assertEqual((self.cfg / rel).read_text(encoding="utf-8"), mine[rel])
        self.assertIn("Left alone", out)
        [bak] = list((self.cfg / "commands").glob("fu-interview.md.*.bak"))
        self.assertEqual(bak.read_text(encoding="utf-8"), "my own command\n")
        self.assertEqual(self.backups(), [])

    def test_second_run_changes_nothing(self) -> None:
        self.write({"CLAUDE.md": "# mine\n"})
        self.install()
        before = {p: (self.cfg / p).read_bytes() for p in self.files()}
        out = self.install()
        self.assertEqual({p: (self.cfg / p).read_bytes() for p in self.files()}, before)
        self.assertNotIn("Backed up", out)

    def test_claude_md_block_replaced_in_place(self) -> None:
        self.write({"CLAUDE.md": f"# top\n\n{BEGIN}\nold text\n<!-- /finding-unknowns:always-on -->\n\n# bottom\n"})
        self.install()
        text = (self.cfg / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# top\n"))
        self.assertTrue(text.endswith("# bottom\n"))
        self.assertNotIn("old text", text)
        self.assertEqual(text.count(BEGIN), 1)
        self.assertEqual(len(list(self.cfg.glob("CLAUDE.md.*.bak"))), 1)

    def test_older_text_is_reported_not_edited(self) -> None:
        old = "Before non-trivial work, ask me once to predict the outcome.\n"
        self.write({"CLAUDE.md": old})
        out = self.install()
        self.assertTrue((self.cfg / "CLAUDE.md").read_text(encoding="utf-8").startswith(old))
        self.assertIn("older finding-unknowns text", out)

    def test_older_texts_of_every_version_are_reported(self) -> None:
        for old in ("Before building, ask me to predict the outcome, then give yours.\n",
                    "# finding-unknowns (passive drop-in)\n\nNotes go under `.finding-unknowns/` at the root.\n",
                    "Before non-trivial work, show `fu:before`: what you rely on, sourced.\n",
                    "For non-trivial work, show me the unknowns. Before starting, one short list.\n"):
            with self.subTest(old=old[:30]):
                self.write({"CLAUDE.md": old})
                self.assertIn("older finding-unknowns text", self.install())
                (self.cfg / "CLAUDE.md").unlink()

    def test_orphan_begin_marker_is_refused(self) -> None:
        original = f"# a\n{BEGIN}\nstray\n# MY RULES\nkeep this\n"
        self.write({"CLAUDE.md": original})
        result = self.run_install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("stray or duplicate", result.stderr)
        self.assertEqual((self.cfg / "CLAUDE.md").read_text(encoding="utf-8"), original)

    def test_duplicate_blocks_are_refused(self) -> None:
        original = f"{BEGIN}\nx\n{END}\n# mine\n{BEGIN}\ny\n{END}\n"
        self.write({"CLAUDE.md": original})
        result = self.run_install()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.cfg / "CLAUDE.md").read_text(encoding="utf-8"), original)

    def test_backups_are_never_overwritten(self) -> None:
        self.write({"CLAUDE.md": f"# top\n{BEGIN}\nfirst\n{END}\n"})
        self.install()
        (self.cfg / "CLAUDE.md").write_text(f"# top\n{BEGIN}\nsecond\n{END}\n", encoding="utf-8")
        self.install()   # usually within the same second as the first run
        saved = sorted(p.read_text(encoding="utf-8") for p in self.cfg.glob("CLAUDE.md.*.bak"))
        self.assertEqual(len(saved), 2)
        self.assertTrue(any("first" in s for s in saved) and any("second" in s for s in saved))

    def test_crlf_file_keeps_its_bytes_outside_the_block(self) -> None:
        (self.cfg / "CLAUDE.md").write_bytes(b"# top\r\nline two\r\n")
        self.install()
        data = (self.cfg / "CLAUDE.md").read_bytes()
        self.assertTrue(data.startswith(b"# top\r\nline two\r\n"))
        self.assertNotIn(b"\n", data.replace(b"\r\n", b""))
        before = data
        self.install()
        self.assertEqual((self.cfg / "CLAUDE.md").read_bytes(), before)

    def test_user_owned_skill_is_backed_up(self) -> None:
        self.write({"skills/finding-unknowns/SKILL.md": "---\nname: my-own\n---\nmine\n"})
        self.install()
        [bak] = list((self.cfg / "skills/finding-unknowns").glob("SKILL.md.*.bak"))
        self.assertEqual(bak.read_text(encoding="utf-8"), "---\nname: my-own\n---\nmine\n")

    def test_no_claude_md_flag(self) -> None:
        self.install("--no-claude-md")
        self.assertNotIn("CLAUDE.md", self.files())


if __name__ == "__main__":
    unittest.main()
