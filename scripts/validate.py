#!/usr/bin/env python3
"""Repository consistency checks (run locally or in CI).

Checks that have broken before in this repo: frontmatter that fails to parse, unsafe or
malformed SVGs, broken relative links, unbalanced code fences or <details>, version and
count drift between plugin.json, README badges and the hero diagram, em dashes in the
Chinese README and tutorial, en/zh README structure drift, Chinese diagrams with live (un-outlined)
CJK text, and a broken install script.

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
DOCS = ["README.md", "README.zh.md", "CLAUDE.md", "AGENTS.md", "EXAMPLES.md",
        "CONTRIBUTING.md", "CHANGELOG.md", "docs/ARCHITECTURE.md", "docs/recordings/itsdangerous-blindspot.md", "docs/field-notes/2026-11-10-jetson-nx.md", "docs/GLOSSARY.md",
        "docs/TUTORIAL.md", "docs/TUTORIAL.zh.md"]
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
    for rel, pattern in (("README.md", r"Latest release: \*\*v([0-9.]+)\*\*"), ("README.md", r"# expect: ([0-9.]+) \(plugin\)"),
                         ("README.zh.md", r"最新版本为 \*\*v([0-9.]+)\*\*"), ("README.zh.md", r"# 预期：([0-9.]+)（插件方式）")):
        m = re.search(pattern, read(rel))
        if not m or m.group(1) != version:
            fail(f"{rel}: '{pattern}' shows {m.group(1) if m else 'nothing'}, plugin.json is {version}")


def check_install_script() -> None:
    result = subprocess.run(["bash", "-n", str(ROOT / "install.sh")], capture_output=True, text=True)
    if result.returncode:
        fail(f"install.sh: {result.stderr.strip()}")


def main() -> int:
    for check in (check_frontmatter, check_json, check_svgs, check_docs, check_readme_pair,
                  check_versions_and_counts, check_install_script):
        check()
    if errors:
        print("\n".join(f"FAIL {e}" for e in errors))
        print(f"\n{len(errors)} problem(s)")
        return 1
    print("validate: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
