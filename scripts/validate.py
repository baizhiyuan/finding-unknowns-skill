#!/usr/bin/env python3
"""Repository consistency checks (run locally or in CI).

Checks: the 6.0 file set and word budgets (always-on text, SKILL.md, commands), frontmatter that
fails to parse, the READMEs quoting CLAUDE.md verbatim, unsafe or malformed SVGs, broken relative
links, unbalanced code fences or <details>, version drift between plugin.json, marketplace.json,
README badges, the hero diagram and the CHANGELOG, em dashes in the Chinese README, en/zh README
structure drift, Chinese diagrams with live (un-outlined) CJK text, and a broken install script.

Usage: python3 scripts/validate.py   (exit 1 on any failure)

Opt-in copy lint (docs/COPY.md), not run by default or in CI:
       python3 scripts/validate.py --copy   (exit 1 on any finding)
It flags internal labels and the author persona in README.md and README.zh.md (作者 is allowed
under a credits or licence heading), the same fraction appearing more than twice in one README (it
counts repeated numbers, not claims), and SVG marks in assets/ that do not pair one label with one
footnote.
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
DOCS = ["README.md", "README.zh.md", "CLAUDE.md", "AGENTS.md", "CONTRIBUTING.md", "CHANGELOG.md",
        "docs/GLOSSARY.md", "docs/COPY.md"]
DOCS += sorted(str(Path(p).relative_to(ROOT)) for p in glob.glob(str(ROOT / "docs/field-notes/*.md"))
               + glob.glob(str(ROOT / "docs/design/*.md"))
               + glob.glob(str(ROOT / "docs/evals/*/README.md"))
               + glob.glob(str(ROOT / "docs/evals/*/PLAN.md")))
# The shipped plugin: nothing else may appear under skills/, commands/ or agents/.
SHIPPED = {"skills/finding-unknowns/SKILL.md", "commands/fu-interview.md", "commands/fu-lookback.md"}
WORD_LIMITS = {"CLAUDE.md": 140, "skills/finding-unknowns/SKILL.md": 1150}
COMMAND_BODY_LIMIT = 40
HEADERS = ("fu:before", "fu:after", "fu:interview", "fu:lookback", "fu-note:")
CJK = re.compile(r"[一-鿿　-〿＀-￯]")   # ideographs + CJK/full-width punctuation
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def check_file_set() -> None:
    present = {str(Path(p).relative_to(ROOT)) for pattern in ("skills/**/*", "commands/**/*", "agents/**/*")
               for p in glob.glob(str(ROOT / pattern), recursive=True) if Path(p).is_file()}
    for rel in sorted(present - SHIPPED):
        fail(f"{rel}: not part of the 6.0 file set (update SHIPPED in scripts/validate.py if intended)")
    for rel in sorted(SHIPPED - present):
        fail(f"{rel}: missing")


def words(text: str) -> int:
    return len(text.split())


def check_budgets() -> None:
    for rel, limit in WORD_LIMITS.items():
        count = words(read(rel))
        if count > limit:
            fail(f"{rel}: {count} words, limit {limit}")
    for path in sorted(glob.glob(str(ROOT / "commands/*.md"))):
        body = Path(path).read_text(encoding="utf-8").split("---", 2)[-1]
        if words(body) > COMMAND_BODY_LIMIT:
            fail(f"{Path(path).relative_to(ROOT)}: body has {words(body)} words, limit {COMMAND_BODY_LIMIT}")


def check_frontmatter() -> None:
    files = sorted(glob.glob(str(ROOT / "skills/*/SKILL.md")) + glob.glob(str(ROOT / "commands/*.md")))
    for path in files:
        rel = Path(path).relative_to(ROOT)
        try:
            meta = yaml.safe_load(Path(path).read_text(encoding="utf-8").split("---", 2)[1])
        except Exception as exc:  # noqa: BLE001 - report any parse failure
            fail(f"{rel}: frontmatter does not parse ({exc})")
            continue
        if not isinstance(meta, dict) or not meta.get("description"):
            fail(f"{rel}: frontmatter needs a description")
        elif rel.name == "SKILL.md" and meta.get("name") != rel.parent.name:
            fail(f"{rel}: frontmatter name {meta.get('name')!r} != directory {rel.parent.name!r}")
        elif rel.parts[0] == "commands" and "finding-unknowns" not in Path(path).read_text(encoding="utf-8"):
            fail(f"{rel}: must name the finding-unknowns skill (install.sh uses it as our marker)")


def check_text_consistency() -> None:
    always_on = read("CLAUDE.md").strip()
    for rel in ("README.md", "README.zh.md"):
        if f"> {always_on}" not in read(rel):
            fail(f"{rel}: does not quote CLAUDE.md verbatim")
    skill = read("skills/finding-unknowns/SKILL.md")
    for token in HEADERS:
        if token not in skill:
            fail(f"skills/finding-unknowns/SKILL.md: header token {token} missing")
    for token in ("fu:before", "fu:after"):
        if token not in always_on:
            fail(f"CLAUDE.md: header token {token} missing")


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
    extra = sorted(glob.glob(str(ROOT / "skills/**/*.md"), recursive=True) + glob.glob(str(ROOT / "commands/*.md")))
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
    for rel in ("README.zh.md",):
        if "——" in strip_code(read(rel)):
            fail(f"{rel}: em dash (——) outside code blocks")


def check_versions() -> None:
    plugin = json.loads(read(".claude-plugin/plugin.json"))
    version = plugin["version"]
    market = json.loads(read(".claude-plugin/marketplace.json"))
    for entry in market["plugins"]:
        if entry.get("version") != version:
            fail(f".claude-plugin/marketplace.json: version {entry.get('version')} != plugin.json {version}")
        if entry.get("name") != plugin["name"]:
            fail(f".claude-plugin/marketplace.json: plugin name {entry.get('name')!r} != plugin.json {plugin['name']!r}")
    install_line = f"/plugin install {plugin['name']}@{market['name']}"
    for rel in ("README.md", "README.zh.md"):
        if install_line not in read(rel):
            fail(f"{rel}: no '{install_line}' line (plugin and marketplace names must match the README)")
    for rel in ("README.md", "README.zh.md"):
        badge = re.search(r"badge/version-([0-9.]+)-", read(rel))
        if not badge or badge.group(1) != version:
            fail(f"{rel}: version badge {badge.group(1) if badge else 'missing'} != plugin.json {version}")
    for rel in ("assets/hero.svg", "assets/zh/src/hero.svg"):
        if f"v{version}" not in read(rel):
            fail(f"{rel}: does not show v{version}")
    changelog = read("CHANGELOG.md")
    if f"## [{version}]" not in changelog:
        fail(f"CHANGELOG.md: no entry for {version}")
    if f"[{version}]: " not in changelog:
        fail(f"CHANGELOG.md: no link reference for [{version}]")
    for rel, pattern in (("README.md", r"# expect: ([0-9.]+) \(plugin\)"),
                         ("README.zh.md", r"# 预期：([0-9.]+)（插件方式）")):
        m = re.search(pattern, read(rel))
        if not m or m.group(1) != version:
            fail(f"{rel}: '{pattern}' shows {m.group(1) if m else 'nothing'}, plugin.json is {version}")


def check_install_script() -> None:
    result = subprocess.run(["bash", "-n", str(ROOT / "install.sh")], capture_output=True, text=True)
    if result.returncode:
        fail(f"install.sh: {result.stderr.strip()}")


# --- Copy lint (opt-in: --copy). Rules in docs/COPY.md. -------------------------------------------
COPY_READMES = ("README.md", "README.zh.md")
COPY_MAX_FRACTION_REPEATS = 2
# Run ids first, so W2-F4d-1 is reported once rather than also as F4d.
COPY_LABEL = re.compile(r"\b[A-Z]\d+-[A-Z]\w*-\d+\b|\bF4[a-d]\b|\bF5\b|\bv6f\w+")
COPY_FRACTIONS = (  # each yields (N, M) for "N of M"
    (re.compile(r"(?<![\w/.])(\d+) of (\d+)(?!\w)"), lambda m: (m.group(1), m.group(2))),
    (re.compile(r"(?<![\w/.:-])(\d+)/(\d+)(?![\w/]|\.\w)"), lambda m: (m.group(1), m.group(2))),
    (re.compile(r"(\d+)\s*[次个张项条][^\d\s，。；、（）()]{0,4}中[，,]?[有的]?\s*(\d+)"),
     lambda m: (m.group(2), m.group(1))),
)
COPY_PERSONA = re.compile(r"(?i)\bthe owner\b|(?<!原)作者")
# 作者 names a third party under these headings, so it is not the author persona there.
COPY_CREDITS_HEADING = re.compile(r"(?i)credit|licen[cs]e|acknowledg|致谢|鸣谢|许可")
COPY_HEADING = re.compile(r"^(#{1,6})\s+(.*)$", re.M)
SVG_LABEL_MARK = re.compile(r"(\*+|[†‡§])$")
SVG_FOOTNOTE_MARK = re.compile(r"^(\*+|[†‡§])\s")


def mask_code(text: str) -> str:
    """Blank fenced code blocks but keep their newlines, so line numbers stay true."""
    return re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def credits_spans(prose: str) -> list[tuple[int, int]]:
    """Character ranges of sections whose heading names credits or a licence, subsections included."""
    headings = [(m.start(), len(m.group(1)), m.group(2)) for m in COPY_HEADING.finditer(prose)]
    spans = []
    for i, (start, level, title) in enumerate(headings):
        if COPY_CREDITS_HEADING.search(title):
            end = next((s for s, lv, _ in headings[i + 1:] if lv <= level), len(prose))
            spans.append((start, end))
    return spans


def copy_readme_findings(rel: str, text: str) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for m in COPY_LABEL.finditer(text):
        found.append(("label", f"{rel}:{line_of(text, m.start())}: internal label {m.group(0)!r}"))
    prose = mask_code(text)
    credits = credits_spans(prose)
    for m in COPY_PERSONA.finditer(prose):
        if m.group(0) == "作者" and any(start <= m.start() < end for start, end in credits):
            continue
        found.append(("persona", f"{rel}:{line_of(prose, m.start())}: author persona {m.group(0)!r}"))
    seen: dict[tuple[str, str], list[int]] = {}
    for pattern, key in COPY_FRACTIONS:
        for m in pattern.finditer(prose):
            seen.setdefault(key(m), []).append(line_of(prose, m.start()))
    for (n, total), lines in sorted(seen.items(), key=lambda kv: (int(kv[0][1]), int(kv[0][0]))):
        if len(lines) > COPY_MAX_FRACTION_REPEATS:
            where = ", ".join(str(ln) for ln in sorted(lines))
            found.append(("fraction", f"{rel}: '{n} of {total}' appears {len(lines)} times "
                                      f"(limit {COPY_MAX_FRACTION_REPEATS}), lines {where}; this counts "
                                      f"repeated numbers, not claims, so check whether they are one claim"))
    return found


def svg_text(text: str) -> list[str]:
    return [t.strip() for t in re.findall(r"<(?:text|tspan)[^>]*>([^<]*)", text) if t.strip()]


def copy_svg_findings(rel: str, text: str) -> list[tuple[str, str]]:
    labels: dict[str, list[str]] = {}
    notes: dict[str, int] = {}
    for t in svg_text(text):
        note = SVG_FOOTNOTE_MARK.match(t)
        if note:
            notes[note.group(1)] = notes.get(note.group(1), 0) + 1
            continue
        mark = SVG_LABEL_MARK.search(t)
        if mark:
            labels.setdefault(mark.group(1), []).append(t)
    found = []
    for mark in sorted(set(labels) | set(notes)):
        marked, count = labels.get(mark, []), notes[mark] if mark in notes else 0
        if count > 1:
            found.append(("svg-mark", f"{rel}: mark {mark!r} has {count} footnotes; one mark, one footnote"))
        if not marked:
            found.append(("svg-mark", f"{rel}: footnote mark {mark!r} is used by no label"))
        elif len(marked) > count:
            found.append(("svg-mark", f"{rel}: {len(marked)} label(s) marked {mark!r} but "
                                      f"{count} footnote(s): {', '.join(map(repr, marked))}"))
    return found


def copy_findings(root: Path = ROOT) -> list[tuple[str, str]]:
    found = []
    for rel in COPY_READMES:
        found += copy_readme_findings(rel, (root / rel).read_text(encoding="utf-8"))
    for path in sorted(glob.glob(str(root / "assets/**/*.svg"), recursive=True)):
        rel = str(Path(path).relative_to(root))
        found += copy_svg_findings(rel, Path(path).read_text(encoding="utf-8"))
    return found


def copy_main() -> int:
    found = copy_findings()
    if not found:
        print("validate --copy: no findings")
        return 0
    print("\n".join(f"COPY [{rule}] {msg}" for rule, msg in found))
    counts: dict[str, int] = {}
    for rule, _ in found:
        counts[rule] = counts.get(rule, 0) + 1
    print(f"\n{len(found)} finding(s): " + ", ".join(f"{r} {c}" for r, c in sorted(counts.items())))
    return 1


def main() -> int:
    for check in (check_file_set, check_budgets, check_frontmatter, check_text_consistency, check_json,
                  check_svgs, check_docs, check_readme_pair, check_versions, check_install_script):
        check()
    if errors:
        print("\n".join(f"FAIL {e}" for e in errors))
        print(f"\n{len(errors)} problem(s)")
        return 1
    print("validate: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(copy_main() if "--copy" in sys.argv[1:] else main())
