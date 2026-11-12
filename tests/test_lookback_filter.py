"""The look-back filter in SKILL.md, run exactly as documented, against a synthetic transcript.

The code is extracted from the Markdown at test time, so the documented filter is the tested
filter. Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = (ROOT / "skills/finding-unknowns/SKILL.md").read_text(encoding="utf-8")


def filter_code() -> str:
    match = re.search(r"<<'EOF'\n(.*?)\nEOF\n", SKILL, re.S)
    if not match:
        raise AssertionError("no look-back filter found in SKILL.md")
    return match.group(1)


def line(kind: str, content, **extra) -> str:
    return json.dumps({"type": kind, "timestamp": "2026-11-12T10:00:00Z",
                       "message": {"role": kind, "content": content}, **extra})


TRANSCRIPT = [
    line("user", "Fix the parser. fu-note: did not know the cache was per-user"),
    line("assistant", [{"type": "text", "text": "fu:before · fix the parser\n- You expect: not stated"}]),
    line("assistant", [{"type": "tool_use", "name": "Bash", "input": {"command": "echo fu:after"}}]),
    line("user", [{"type": "tool_result", "content": "fu:after from a tool"}]),
    line("assistant", [{"type": "text", "text": "fu:after · from a subagent"}], isSidechain=True),
    json.dumps({"type": "progress", "data": "fu:before in progress traffic"}),
    '{"type": "assistant", "broken json fu:before',
    line("assistant", [{"type": "text", "text": "no header here"}]),
    line("assistant", [{"type": "thinking", "thinking": "fu:after"}, {"type": "text", "text": "fu:after · done"}]),
    line("user", [{"type": "text", "text": "fu:before · {task}\n- You expect: \"{their words}\""}], isMeta=True),
]


class LookbackFilterTest(unittest.TestCase):
    def run_filter(self, lines: list[str]) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "session.jsonl"
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            result = subprocess.run([sys.executable, "-", str(path)], input=filter_code(),
                                    capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_keeps_only_user_and_assistant_text_with_a_header(self) -> None:
        out = self.run_filter(TRANSCRIPT)
        self.assertIn("fu-note: did not know the cache was per-user", out)
        self.assertIn("fu:before · fix the parser", out)
        self.assertIn("fu:after · done", out)
        for excluded in ("echo fu:after", "from a tool", "from a subagent", "progress traffic", "broken json",
                         "{their words}"):
            self.assertNotIn(excluded, out)
        self.assertEqual(len(re.findall(r"^2026-11-12T10:00:00Z (user|assistant)$", out, re.M)), 3)

    def test_prints_nothing_without_headers(self) -> None:
        self.assertEqual(self.run_filter([line("user", "hello"), line("assistant", "plain reply")]), "")

    def test_caps_a_long_block(self) -> None:
        out = self.run_filter([line("assistant", "fu:after · " + "x" * 10000)])
        self.assertLess(len(out), 1600)

    def test_finds_a_block_at_the_end_of_a_long_message(self) -> None:
        text = "x" * 10000 + "\n\n```\nfu:after · done\n- Not proved\n  - the test → leaves open load\n```\nafter"
        out = self.run_filter([line("assistant", [{"type": "text", "text": text}])])
        self.assertIn("fu:after · done", out)
        self.assertIn("leaves open load", out)
        self.assertNotIn("x" * 50, out)
        self.assertNotIn("after\n", out.split("leaves open load", 1)[1])

    def test_prints_each_block_not_the_prose_between(self) -> None:
        text = "fu:before · a\n- You expect: not stated\n\nlong prose in between\n\nfu:after · a\n- Now known"
        out = self.run_filter([line("assistant", text)])
        self.assertIn("- You expect: not stated", out)
        self.assertIn("fu:after · a", out)
        self.assertNotIn("long prose", out)

    def test_skips_earlier_lookback_output(self) -> None:
        out = self.run_filter([line("assistant", "fu:lookback · 7d\n- Became known\n  - a fact")])
        self.assertEqual(out, "")

    def test_a_note_inside_a_sentence_is_kept_from_the_prefix(self) -> None:
        out = self.run_filter([line("user", "Fix it. fu-note: noise")])
        self.assertIn("fu-note: noise", out)
        self.assertNotIn("Fix it.", out)


if __name__ == "__main__":
    unittest.main()
