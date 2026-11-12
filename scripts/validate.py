#!/usr/bin/env python3
"""Repository consistency checks (run locally or in CI).

Checks that have broken before in this repo: frontmatter that fails to parse, unsafe or
malformed SVGs, broken relative links, unbalanced code fences or <details>, version and
count drift between plugin.json, README badges and the hero diagram, em dashes in the
Chinese README and tutorial, en/zh README structure drift, Chinese diagrams with live (un-outlined)
CJK text, a broken install script, and runtime text over its word budget.

Usage: python3 scripts/validate.py   (exit 1 on any failure)
"""
from __future__ import annotations

import glob
import json
import re
import subprocess
import sys
import xml.dom.minidom
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ["README.md", "README.zh.md", "CLAUDE.md", "CLAUDE.next.md", "AGENTS.md", "EXAMPLES.md",
        "CONTRIBUTING.md", "CHANGELOG.md", "docs/ARCHITECTURE.md", "docs/recordings/itsdangerous-blindspot.md", "docs/GLOSSARY.md",
        "docs/TUTORIAL.md", "docs/TUTORIAL.zh.md", "docs/results-examples.md"]
DOCS += sorted(str(Path(p).relative_to(ROOT)) for p in glob.glob(str(ROOT / "docs/field-notes/*.md"))
               + glob.glob(str(ROOT / "docs/design/*.md"))
               + glob.glob(str(ROOT / "docs/evals/*/README.md")))
# Word budgets for runtime text (wc -w), from the 5.2 design. Commands are counted together,
# without fenced blocks in fu-brief.md (the card template lives there).
BUDGETS = {"CLAUDE.next.md": 82, "skills/finding-unknowns/SKILL.md": 700,
           "skills/finding-unknowns/references/brief.md": 350,
           "skills/finding-unknowns/references/debrief.md": 450,
           "skills/finding-unknowns/references/results.md": 1200,
           "skills/finding-unknowns/references/view.md": 150,
           "agents/mechanism-auditor.md": 500}
COMMANDS_BUDGET = 450
# CLAUDE.md is the always-on text measured in Stage 0 (56 words). It is pinned verbatim;
# changes go through CLAUDE.next.md and the Tier 1 check.
CLAUDE_MD = ("Before building, ask me to predict the outcome, then give yours; write both, with what "
             "would prove each wrong, in `.finding-unknowns/tasks/`. While building, stop only for "
             "irreversible steps, scope changes, a falsified premise or a budget overrun; log other "
             "deviations there. Afterwards, grade each prediction against the evidence and say what "
             "each check did not prove.")
# Phase 3 of 5.2 rewrites these docs. Until CHANGELOG.md has an entry for this version, their
# problems are reported as PENDING and do not fail the run; the entry ends the grace period.
PHASE3_VERSION = "5.2.0"
PHASE3_FILES = ("README.md", "README.zh.md", "CHANGELOG.md", "EXAMPLES.md", "docs/ARCHITECTURE.md",
                "docs/GLOSSARY.md", "docs/TUTORIAL.md", "docs/TUTORIAL.zh.md", "assets/")
CJK = re.compile(r"[一-鿿　-〿＀-￯]")   # ideographs + CJK/full-width punctuation
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def check_frontmatter() -> None:
    files = sorted(glob.glob(str(ROOT / "skills/*/SKILL.md")) + glob.glob(str(ROOT / "agents/*.md"))
                   + glob.glob(str(ROOT / "commands/*.md")))
    for path in files:
        rel = Path(path).relative_to(ROOT)
        try:
            meta = yaml.safe_load(Path(path).read_text(encoding="utf-8").split("---", 2)[1])
        except Exception as exc:  # noqa: BLE001 - report any parse failure
            fail(f"{rel}: frontmatter does not parse ({exc})")
            continue
        if not isinstance(meta, dict) or not meta.get("description"):
            fail(f"{rel}: frontmatter needs a description")


def check_json() -> None:
    for rel in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"):
        try:
            json.loads(read(rel))
        except Exception as exc:  # noqa: BLE001
            fail(f"{rel}: invalid JSON ({exc})")


def check_svgs() -> None:
    for path in sorted(glob.glob(str(ROOT / "assets/**/*.svg"), recursive=True)):
        rel = Path(path).relative_to(ROOT)
        text = Path(path).read_text(encoding="utf-8")
        try:
            xml.dom.minidom.parseString(text.encode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            fail(f"{rel}: not well-formed XML ({exc})")
        if re.search(r"<script|<foreignObject|@import|href=\"https?:", text):
            fail(f"{rel}: contains script, foreignObject, @import or an external reference")
        published_zh = rel.parts[:2] == ("assets", "zh") and len(rel.parts) == 3
        if published_zh:
            live = [m for m in re.findall(r"<(?:text|tspan)[^>]*>([^<]*)", text) if CJK.search(m)]
            if live:
                fail(f"{rel}: live CJK <text> left un-outlined (run scripts/outline_cjk.py)")


def doc_files() -> list[str]:
    extra = sorted(glob.glob(str(ROOT / "skills/**/*.md"), recursive=True) + glob.glob(str(ROOT / "agents/*.md"))
                   + glob.glob(str(ROOT / "commands/*.md")))
    return DOCS + [str(Path(p).relative_to(ROOT)) for p in extra]


def check_docs() -> None:
    for rel in doc_files():
        text = read(rel)
        if text.count("```") % 2:
            fail(f"{rel}: unbalanced code fences")
        if rel in DOCS and text.count("<details>") != text.count("</details>"):
            fail(f"{rel}: unbalanced <details>")
        base = (ROOT / rel).parent
        for a, b in re.findall(r'(?:src|href)="([^"]+)"|\]\(([^)\s]+)(?:\s+"[^"]*")?\)', strip_code(text)):
            target = (a or b).strip("<>").split("#", 1)[0]
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target):
                continue   # in-page anchor or external URL
            if not (base / target).exists():
                fail(f"{rel}: broken relative link {target}")


def strip_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def check_readme_pair() -> None:
    en, zh = read("README.md"), read("README.zh.md")
    levels = lambda t: re.findall(r"^(#{2,3}) ", strip_code(t), re.M)  # noqa: E731
    if levels(en) != levels(zh):
        fail("README.md and README.zh.md heading structure differs")
    for rel in ("README.zh.md", "docs/TUTORIAL.zh.md"):
        if "——" in strip_code(read(rel)):
            fail(f"{rel}: em dash (——) outside code blocks")


def check_versions_and_counts() -> None:
    version = json.loads(read(".claude-plugin/plugin.json"))["version"]
    skills = len(glob.glob(str(ROOT / "skills/*/SKILL.md")))
    agents = len(glob.glob(str(ROOT / "agents/*.md")))
    for rel in ("README.md", "README.zh.md"):
        text = read(rel)
        badge = re.search(r"badge/version-([0-9.]+)-", text)
        if not badge or badge.group(1) != version:
            fail(f"{rel}: version badge {badge.group(1) if badge else 'missing'} != plugin.json {version}")
        for label, count in (("skills", skills), ("agents", agents)):
            m = re.search(rf"badge/{label}-(\d+)-", text)
            if not m or int(m.group(1)) != count:
                fail(f"{rel}: {label} badge {m.group(1) if m else 'missing'} != {count} on disk")
    for rel in ("assets/hero.svg", "assets/zh/src/hero.svg"):
        if f"v{version}" not in read(rel):
            fail(f"{rel}: does not show v{version}")
    changelog = read("CHANGELOG.md")
    if f"## [{version}]" not in changelog:
        fail(f"CHANGELOG.md: no entry for {version}")
    if f"[{version}]: " not in changelog:
        fail(f"CHANGELOG.md: no link reference for [{version}]")
    # An unreleased version (CHANGELOG "## [x] - unreleased") must be announced as the next
    # release, never as the latest one, and the other way round.
    unreleased = re.search(rf"^## \[{re.escape(version)}\] - unreleased", changelog, re.M) is not None
    en_word, zh_word = ("Next release", "下一个版本为") if unreleased else ("Latest release", "最新版本为")
    for rel, pattern in (("README.md", en_word + r": \*\*v([0-9.]+)\*\*"), ("README.md", r"# expect: ([0-9.]+) \(plugin\)"),
                         ("README.zh.md", zh_word + r" \*\*v([0-9.]+)\*\*"), ("README.zh.md", r"# 预期：([0-9.]+)（插件方式）")):
        m = re.search(pattern, read(rel))
        if not m or m.group(1) != version:
            fail(f"{rel}: '{pattern}' shows {m.group(1) if m else 'nothing'}, plugin.json is {version}")


def check_install_script() -> None:
    result = subprocess.run(["bash", "-n", str(ROOT / "install.sh")], capture_output=True, text=True)
    if result.returncode:
        fail(f"install.sh: {result.stderr.strip()}")


def check_budgets() -> None:
    if read("CLAUDE.md").strip() != CLAUDE_MD:
        fail("CLAUDE.md: differs from the measured 56-word text (change CLAUDE.next.md instead)")
    for rel, limit in BUDGETS.items():
        words = len(read(rel).split())
        if words > limit:
            fail(f"{rel}: {words} words, budget {limit}")
    total = 0
    for path in sorted(glob.glob(str(ROOT / "commands/*.md"))):
        text = Path(path).read_text(encoding="utf-8")
        if Path(path).name == "fu-brief.md":
            text = re.sub(r"```.*?```", "", text, flags=re.S)
        total += len(text.split())
    if total > COMMANDS_BUDGET:
        fail(f"commands/*.md: {total} words without the card template, budget {COMMANDS_BUDGET}")


def phase3_pending() -> bool:
    version = json.loads(read(".claude-plugin/plugin.json"))["version"]
    return version == PHASE3_VERSION and f"## [{version}]" not in read("CHANGELOG.md")


def main() -> int:
    global errors
    for check in (check_frontmatter, check_json, check_svgs, check_docs, check_readme_pair,
                  check_versions_and_counts, check_install_script, check_budgets):
        check()
    if phase3_pending():
        pending = [e for e in errors if e.startswith(PHASE3_FILES)]
        errors = [e for e in errors if not e.startswith(PHASE3_FILES)]
        print("\n".join(f"PENDING (phase 3 docs) {e}" for e in pending))
    if errors:
        print("\n".join(f"FAIL {e}" for e in errors))
        print(f"\n{len(errors)} problem(s)")
        return 1
    print("validate: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
