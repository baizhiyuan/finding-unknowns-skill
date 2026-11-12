#!/usr/bin/env python3
# finding-unknowns: fu, the deterministic half of the finding-unknowns skill (5.2).
# install.sh keeps an installed copy current only because this header names the project.
"""fu: lint, freeze, integrity, log, list, render and the guard hook for task cards.

Contract: docs/design/fu-cli.md. Card schema: skills/finding-unknowns/references/card.md.
One file, Python 3.8+ standard library only, no network.

  fu init [--strict] [--guard off|log|ask]
  fu lint [slug] [--strict]
  fu freeze <slug> --stage brief|stop|resume|debrief
  fu integrity [slug]
  fu log [slug]
  fu list [--all]
  fu render [slug] | --list
  fu guard pre|post            (hook entry: always exits 0, never writes to stderr)

Exit codes: 0 ok, 1 problems found, 2 usage error or card/root not found, 3 skipped by
design. `--root DIR` overrides project-root discovery.
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import html
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

FU_DIR = ".finding-unknowns"
TIME = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}"
STATES = ("briefing", "building", "waiting on you", "debriefed")
STAGE_STATE = {"brief": "building", "stop": "waiting on you", "resume": "building", "debrief": "debriefed"}
CONFIDENCE = ("low", "medium", "high", "no idea", "not given")   # the person's
AGENT_CONFIDENCE = ("low", "medium", "high")
LANES = ("reversible", "wide", "irreversible")
DELTA_KINDS = ("deviation", "surprise", "decided-for-you")
STOP_KINDS = ("irreversible", "scope", "dead-premise", "budget")
VERDICTS = ("consistent", "partly", "inconsistent", "can't tell", "post-hoc fit")
TIERS = ("verified", "supported", "inferred", "untested")
GITIGNORE_LINES = (".finding-unknowns/logs/", ".finding-unknowns/view/",
                   ".finding-unknowns/profile.md", ".finding-unknowns/predictions-log.md")
PROFILE_DEFAULTS = (("mode", "ship"), ("strict", "no"), ("commits", "yes"), ("guard", "ask"))
LIVE_MAX_LINES = 40
STRICT_MAX_WORDS = 600
STRICT_MAX_FIELD_WORDS = 20
STRICT_MAX_AGENT_PREDICTIONS = 3
STRICT_MAX_CONTRACT = 5
MAX_ROLLUP = 3
MAX_MODEL_CHANGES = 5
DECISIONS_MAX_LINES = 30
STAT_MIN_N = 5          # stat line once a side has this many graded predictions
CURVE_MIN_N = 10        # calibration curve only from this many graded with a confidence
GIT_TIMEOUT = 120

HEADER_SLUG = re.compile(r"^# (\S+)$")
HEADER_GOAL = re.compile(r"^Goal: (.+) · State: (.+)$")
HEADER_NEEDS = re.compile(r"^Needs you: (.+)$")
NEEDS_FORM = re.compile(r"^(.+?) \(recommendation: (.+); settles (.+)\)$")
HEADER_MODE = re.compile(r"^Mode: (ship|learn) · Last seen by you: (never|(" + TIME + r"), after D(\d+))$")
TIMING_RE = re.compile(r"^Timing: (draft|self-reported|Brief frozen (" + TIME + r"), commit ([0-9a-f]{4,40}))$")
BRIEF_HEAD = re.compile(r"^## Brief \((draft|frozen (" + TIME + r"))\)$")
DEBRIEF_HEAD = re.compile(r"^## Debrief \((" + TIME + r"); graded by (fresh context|same-context — weaker)\)$")
PRED_RE = re.compile(r"^([PA])(\d+) \((you|agent) · ([^()]*)\) (.+)$")
PRED_LIKE = re.compile(r"^[PA]\d+\b")
CONTRACT_RE = re.compile(r"^C(\d+) (.+)$")
IRREVERSIBLE_RE = re.compile(r"^Irreversible: `([^`]+)`\s*$")
SUB_RE = re.compile(r"^  - ([^:]+?): ?(.*)$")
BULLET_RE = re.compile(r"^  - (.*)$")
DELTA_LINE = re.compile(r"^D(\d+) (\d{4}-\d{2}-\d{2})(?: (\d{2}:\d{2}))? ([A-Za-z-]+): (.*)$")
DELTA_IN_CARD = re.compile(r"^\s*(?:- )?D\d+\s")
STOP_TAG = re.compile(r" \[stop: ([a-z-]+)\]$")
AMEND_RE = re.compile(r"^M(\d+) (" + TIME + r") · (?:after D(\d+) · )?(decided-for-you|confirmed): (.+) · why: (.+)$")
MODEL_CHANGE_RE = re.compile(r"^- You expected (.+) → (.+), because (.+) \[(shown, not confirmed|confirmed)\]$")
MODEL_CHANGE_LIKE = re.compile(r"^\s*(?:- )?You expected .+ → ")
MECH_RE = re.compile(r"^(.*?)\s*\[(verified|supported|inferred|untested)\]\s*$")
ID_RE = re.compile(r"(?<![\w-])([PA])(\d+)(?!\w)")
PLACEHOLDER_RE = re.compile(r"\{([^{}\n]*)\}")
PLACEHOLDER_WORDS = re.compile(r"^[a-z][a-z '’,-]*$")
CODE_PLACEHOLDERS = {"exact command", "command that can fail", "command", "command that would catch it"}
CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힯]")
STRONG_VERBS = re.compile(r"\b(causes?|caused|proves?|proven|confirms?|confirmed|demonstrates?|"
                          r"guarantees?|establishes|due to|results? in|leads? to|drives?)\b", re.I)
SUPERLATIVE = re.compile(r"\b(all|every|works|no regressions)\b", re.I)
DESTRUCTIVE = (("rm -rf", re.compile(r"(?:^|[\s;&|(])rm\s+(?:-[a-zA-Z]*[rR][a-zA-Z]*\s+-?[a-zA-Z]*[fF]|-[a-zA-Z]*[fF][a-zA-Z]*\s+-?[a-zA-Z]*[rR]|-[a-zA-Z]*(?:[rR][a-zA-Z]*[fF]|[fF][a-zA-Z]*[rR]))")),
               ("force-push", re.compile(r"\bgit\b[^;&|]*\bpush\b[^;&|]*(?:\s--force(?:-with-lease)?\b|\s-[a-zA-Z]*f\b|\s\+\S)")),
               ("DROP", re.compile(r"\bDROP\s+(?:TABLE|DATABASE|SCHEMA|INDEX|VIEW)\b", re.I)),
               ("reset --hard", re.compile(r"\bgit\b[^;&|]*\breset\b[^;&|]*--hard\b")))
# Known runners: the variant key is runner + target (at least 3 tokens); trailing args may vary.
RUNNERS = {("python", "-m"), ("npm", "run"), ("pnpm", "run"), ("yarn", "run"), ("bun", "run"),
           ("uv", "run"), ("poetry", "run"), ("pipenv", "run"), ("npm", "exec"), ("pnpm", "exec"),
           ("cargo", "run"), ("go", "run"), ("deno", "run"), ("bundle", "exec")}
INTERPRETERS = {"python", "node", "bash", "sh", "ruby", "perl", "deno", "bun"}
DEBRIEF_RULES = {"debrief-coverage", "debrief-form", "verdict", "not-checked", "bottom-line"}


# ----------------------------------------------------------------------------- utilities

class UsageError(Exception):
    """Exit 2: usage error, card or root not found."""


def now_str() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def strip_code(text: str) -> str:
    """Text with inline `code` spans removed (IDs and placeholders inside code are not prose)."""
    return re.sub(r"`[^`]*`", " ", text)


def count_words(text: str) -> int:
    return len(CJK.sub(" ", text).split()) + len(CJK.findall(text))


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def read_profile(fu: Path) -> dict:
    prof = {}
    path = fu / "profile.md"
    if path.is_file():
        for line in read_text(path).splitlines():
            m = re.match(r"^\s*([a-z]+)\s*:\s*(\S.*?)\s*$", line)
            if m:
                prof[m.group(1)] = m.group(2)
    return prof


def git(root: Path, *args: str, timeout: int = GIT_TIMEOUT) -> subprocess.CompletedProcess:
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    return subprocess.run(["git", *args], cwd=str(root), capture_output=True, text=True,
                          stdin=subprocess.DEVNULL, env=env, timeout=timeout)


def find_fu_root(start: Path):
    for d in [start, *start.parents]:
        if (d / FU_DIR).is_dir():
            return d
    return None


def find_root(explicit) -> Path:
    if explicit:
        p = Path(explicit).expanduser().resolve()
        if not p.is_dir():
            raise UsageError("root not found: %s" % explicit)
        return p
    cwd = Path.cwd()
    found = find_fu_root(cwd)
    if found:
        return found
    try:
        r = git(cwd, "rev-parse", "--show-toplevel", timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return Path(r.stdout.strip())
    except (OSError, subprocess.SubprocessError):
        pass
    return cwd


def card_files(fu: Path) -> list:
    tasks = fu / "tasks"
    if not tasks.is_dir():
        return []
    return sorted((p for p in tasks.glob("*.md") if not p.name.endswith(".deltas.md")),
                  key=lambda p: p.stat().st_mtime, reverse=True)


def quick_header(text: str) -> dict:
    """Lenient header read for guard, list and the index (never raises)."""
    lines = text.splitlines()
    out = {"slug": None, "goal": None, "state": None, "needs": None, "last_seen_d": None,
           "last_seen": None, "mode": None, "timing": None}
    for i, line in enumerate(lines[:8]):
        if i == 0:
            m = HEADER_SLUG.match(line)
            out["slug"] = m.group(1) if m else None
        m = HEADER_GOAL.match(line)
        if m:
            out["goal"], out["state"] = m.group(1), m.group(2).strip()
        m = HEADER_NEEDS.match(line)
        if m and out["needs"] is None:
            out["needs"] = m.group(1)
        m = HEADER_MODE.match(line)
        if m:
            out["mode"] = m.group(1)
            out["last_seen"] = m.group(2)
            out["last_seen_d"] = int(m.group(4)) if m.group(4) else None
        if line.startswith("Timing: "):
            out["timing"] = line[len("Timing: "):]
    return out


def is_open(text: str) -> bool:
    return quick_header(text).get("state") != "debriefed"


def resolve_card(root: Path, arg, allow_default: bool):
    """Return (root, card path or None, claim path or None, slug, note line or None)."""
    if arg:
        p = Path(arg)
        if arg.endswith(".md") and p.is_file():
            p = p.resolve()
            slug = p.name[:-3]
            if p.parent.name == "tasks" and p.parent.parent.name == FU_DIR:
                return p.parent.parent.parent, p, _claim(p.parent.parent, slug), slug, None
            if p.parent.name == "predictions" and p.parent.parent.name == FU_DIR:
                return p.parent.parent.parent, None, p, slug, None
            return root, p, None, slug, None
        slug = arg[:-3] if arg.endswith(".md") else arg
        if not re.match(r"^[\w.-]+$", slug):
            raise UsageError("not a slug: %s" % arg)
        fu = root / FU_DIR
        card = fu / "tasks" / (slug + ".md")
        claim = _claim(fu, slug)
        if not card.is_file() and claim is None:
            raise UsageError("card not found: %s" % card)
        return root, card if card.is_file() else None, claim, slug, None
    if not allow_default:
        raise UsageError("a slug is required")
    fu = root / FU_DIR
    if not fu.is_dir():
        raise UsageError("no %s/ under %s" % (FU_DIR, root))
    open_cards = [p for p in card_files(fu) if is_open(read_text(p))]
    if not open_cards:
        raise UsageError("no open card under %s" % (fu / "tasks"))
    card = open_cards[0]
    slug = card.name[:-3]
    note = "card: %s (most recently modified open card)" % slug if len(open_cards) > 1 else None
    return root, card, _claim(fu, slug), slug, note


def _claim(fu: Path, slug: str):
    p = fu / "predictions" / (slug + ".md")
    return p if p.is_file() else None


# ------------------------------------------------------------ command tokens and matching

def _tokens(segment: str) -> list:
    try:
        lex = shlex.shlex(segment, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        return list(lex)
    except ValueError:
        return segment.split()


def segments(command: str) -> list:
    """Normalised token lists, one per simple command (split on newlines, ;, &&, ||, |, &)."""
    out = []
    for line in command.splitlines():
        cur = []
        for tok in _tokens(line):
            if tok and set(tok) <= set(";&|"):
                if cur:
                    out.append(cur)
                cur = []
            else:
                cur.append(tok)
        if cur:
            out.append(cur)
    return [normalise(seg) for seg in out if normalise(seg)]


def normalise(tokens: list) -> list:
    toks = list(tokens)
    while toks and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", toks[0]):
        toks.pop(0)
    out = []
    for i, t in enumerate(toks):
        while t.startswith("./"):
            t = t[2:]
        if i == 0:
            t = os.path.basename(t) or t
            t = re.sub(r"^python3(?:\.\d+)?$", "python", t)
        out.append(t)
    return out


def variant_key(irr: list):
    """Runner + target for known runners (>= 3 tokens), else None (exact match only)."""
    if len(irr) < 3 or (irr[0], irr[1]) not in RUNNERS:
        return None
    if irr[2] in INTERPRETERS:
        inner = variant_key(irr[2:])
        return irr[:2] + inner if inner else None
    if irr[2].startswith("-"):
        return None
    return irr[:3]


def match_command(command: str, irr_cmds: list) -> list:
    """[(index into irr_cmds, exact)] for every Irreversible command the command runs."""
    hits = []
    segs = segments(command)
    for idx, irr in enumerate(irr_cmds):
        irr_segs = segments(irr)
        if len(irr_segs) != 1:
            # a compound Irreversible line matches only the whole normalised command
            if [s for s in segs] == irr_segs:
                hits.append((idx, True))
            continue
        target = irr_segs[0]
        key = variant_key(target)
        for seg in segs:
            if seg == target:
                hits.append((idx, True))
                break
            if key and seg[:len(key)] == key:
                hits.append((idx, False))
                break
    return hits


def norm_command(command: str) -> str:
    return " ; ".join(" ".join(s) for s in segments(command))


# ---------------------------------------------------------------------------- lint model

class Lint:
    def __init__(self):
        self.items = []

    def add(self, level: str, file: str, line: int, rule: str, msg: str) -> None:
        self.items.append((level, file, max(int(line), 1), rule, msg))

    def fails(self):
        return [i for i in self.items if i[0] == "FAIL"]

    def warns(self):
        return [i for i in self.items if i[0] == "WARN"]

    def lines(self) -> list:
        order = sorted(set(self.items), key=lambda i: (i[1], i[2], i[0] != "FAIL", i[3], i[4]))
        out = ["%s %s:%d %s: %s" % i for i in order]
        out.append("lint: %d FAIL, %d WARN" % (len(set(self.fails())), len(set(self.warns()))))
        return out


def parse_quoted(s: str):
    """A double-quoted claim; an inner quote must be escaped as \\". None if malformed."""
    if len(s) < 2 or not s.startswith('"'):
        return None
    out, i = [], 1
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s) and s[i + 1] == '"':
            out.append('"')
            i += 2
            continue
        if c == '"':
            return "".join(out) if i == len(s) - 1 else None
        out.append(c)
        i += 1
    return None


def blocks(body: list) -> list:
    """Group (lineno, text) into top-level blocks: [(lineno, head, [(lineno, sub), …])]."""
    out = []
    for ln, text in body:
        if not text.strip():
            continue
        if text.startswith(" ") and out:
            out[-1][2].append((ln, text))
        else:
            out.append((ln, text, []))
    return out


def sub_fields(subs: list, lint: Lint, f: str, rule: str, keys: tuple, optional: tuple = ()) -> dict:
    """Check `  - key: value` lines appear with exactly these keys in this order."""
    got, order = {}, []
    for ln, text in subs:
        m = SUB_RE.match(text)
        if not m:
            lint.add("FAIL", f, ln, rule, "expected `  - key: value`, got %r" % text.strip()[:60])
            continue
        key, val = m.group(1), m.group(2).strip()
        if key not in keys + optional:
            lint.add("FAIL", f, ln, rule, "unexpected key %r (expected %s)" % (key, ", ".join(keys + optional)))
            continue
        if key in got:
            lint.add("FAIL", f, ln, rule, "%r given twice" % key)
            continue
        if not val:
            lint.add("FAIL", f, ln, rule, "%r is empty" % key)
        got[key] = (ln, val)
        order.append(key)
    wanted = [k for k in keys + optional if k in got]
    if order != wanted:
        lint.add("FAIL", f, subs[0][0] if subs else 1, rule, "keys out of order; expected %s" % ", ".join(keys + optional))
    return got


def parse_card(text: str, slug: str, f: str, lint: Lint) -> dict:
    lines = text.splitlines()
    m = {"slug": slug, "goal": None, "state": None, "needs": None, "needs_parts": None,
         "mode": None, "last_seen": None, "last_seen_d": None, "timing": None,
         "timing_time": None, "timing_hash": None, "brief": None, "brief_range": (0, 0),
         "brief_frozen": None, "amendments": [], "latest": None, "rollup": [],
         "model_changes": [], "open": [], "debriefs": [], "live_end": len(lines)}
    _parse_header(lines, slug, f, lint, m)
    sections = []
    for i, line in enumerate(lines, 1):
        if line.startswith("## "):
            sections.append([line, i, []])
        elif sections:
            sections[-1][2].append((i, line))
        elif i > 5 and line.strip():
            lint.add("FAIL", f, i, "header", "unexpected line before the first section")
    _check_section_order(sections, f, lint)
    for idx, (head, ln, body) in enumerate(sections):
        end = sections[idx + 1][1] - 1 if idx + 1 < len(sections) else len(lines)
        if head.startswith("## Brief"):
            bm = BRIEF_HEAD.match(head)
            m["brief_frozen"] = bm.group(2) if bm else None
            m["brief_range"] = (ln, end)
            m["brief"] = _parse_brief(body, f, lint)
        elif head == "## Amendments":
            _parse_amendments(body, f, lint, m)
        elif head == "## Deltas":
            _parse_deltas_section(body, f, lint, m)
        elif head == "## Model changes":
            _parse_model_changes(body, f, lint, m)
        elif head == "## Open":
            m["open"] = [(i, t.strip()[2:] if t.strip().startswith("- ") else t.strip()) for i, t in body if t.strip()]
        elif head.startswith("## Debrief"):
            m["live_end"] = min(m["live_end"], ln - 1)
            m["debriefs"].append(_parse_debrief(head, ln, body, f, lint))
    if m["brief"] is None:
        m["brief"] = _empty_brief()
    _scan_card_lines(lines, sections, f, lint)
    return m


def _parse_header(lines: list, slug: str, f: str, lint: Lint, m: dict) -> None:
    get = lambda i: lines[i] if i < len(lines) else ""  # noqa: E731
    hm = HEADER_SLUG.match(get(0))
    if not hm:
        lint.add("FAIL", f, 1, "header", "line 1 must be `# {slug}`")
    elif hm.group(1) != slug:
        lint.add("FAIL", f, 1, "header", "slug %r does not match the file name %r" % (hm.group(1), slug))
    gm = HEADER_GOAL.match(get(1))
    if not gm:
        lint.add("FAIL", f, 2, "header", "line 2 must be `Goal: {one line} · State: {state}`")
    else:
        m["goal"], m["state"] = gm.group(1), gm.group(2).strip()
        if m["state"] not in STATES:
            lint.add("FAIL", f, 2, "header", "State %r is not one of %s" % (m["state"], " | ".join(STATES)))
    nm = HEADER_NEEDS.match(get(2))
    if not nm:
        lint.add("FAIL", f, 3, "header", "line 3 must be `Needs you: {X} (recommendation: {Y}; settles {Z}) | nothing`")
    else:
        m["needs"] = nm.group(1)
        if m["needs"] != "nothing":
            pm = NEEDS_FORM.match(m["needs"])
            if not pm:
                lint.add("FAIL", f, 3, "header", "Needs you must read `{X} (recommendation: {Y}; settles {Z})` or `nothing`")
            else:
                m["needs_parts"] = pm.groups()
    mm = HEADER_MODE.match(get(3))
    if not mm:
        lint.add("FAIL", f, 4, "header", "line 4 must be `Mode: ship|learn · Last seen by you: {time}, after D{n} | never`")
    else:
        m["mode"], m["last_seen"] = mm.group(1), mm.group(2)
        m["last_seen_d"] = int(mm.group(4)) if mm.group(4) else None
    tm = TIMING_RE.match(get(4))
    if not tm:
        lint.add("FAIL", f, 5, "header", "line 5 must be `Timing: draft | Brief frozen {time}, commit {hash} | self-reported`")
    else:
        m["timing"] = tm.group(1)
        m["timing_time"], m["timing_hash"] = tm.group(2), tm.group(3)


def _check_section_order(sections: list, f: str, lint: Lint) -> None:
    order = ["Brief", "Amendments", "Deltas", "Model changes", "Open"]
    seen = []
    for head, ln, _ in sections:
        name = head[3:]
        if head.startswith("## Brief"):
            if not BRIEF_HEAD.match(head):
                lint.add("FAIL", f, ln, "sections", "Brief heading must be `## Brief (draft)` or `## Brief (frozen {time})`")
            key = "Brief"
        elif head.startswith("## Debrief"):
            if not DEBRIEF_HEAD.match(head):
                lint.add("FAIL", f, ln, "debrief-form",
                         "Debrief heading must be `## Debrief ({time}; graded by fresh context | same-context — weaker)`")
            key = "Debrief"
        elif name in order:
            key = name
        else:
            lint.add("FAIL", f, ln, "sections", "unknown section %r" % head)
            continue
        if key != "Debrief" and key in seen:
            lint.add("FAIL", f, ln, "sections", "section %r appears twice" % key)
        if key != "Debrief" and "Debrief" in seen:
            lint.add("FAIL", f, ln, "sections", "section %r after a Debrief" % key)
        seen.append(key)
    fixed = [k for k in seen if k != "Debrief"]
    dedup = list(dict.fromkeys(fixed))
    if dedup != order:
        lint.add("FAIL", f, sections[0][1] if sections else 1, "sections",
                 "sections must be, in order: %s, then Debrief sections at the end" % ", ".join(order))


def _empty_brief() -> dict:
    return {"approach": [], "preds": [], "none_given": False, "stop_points": None,
            "irreversible": [], "contract": [], "check_files": None}


def _parse_brief(body: list, f: str, lint: Lint) -> dict:
    b = _empty_brief()
    ids = set()
    for ln, head, subs in blocks(body):
        pm = PRED_RE.match(head)
        if head == "Approach:" or head.startswith("Approach:"):
            if head != "Approach:":
                lint.add("FAIL", f, ln, "brief-form", "`Approach:` stands alone; decisions go on `  - {decision} because {why}` lines")
            for sl, st in subs:
                bm = BULLET_RE.match(st)
                if not bm or " because " not in bm.group(1):
                    lint.add("FAIL", f, sl, "brief-form", "Approach line must read `  - {decision} because {why}`")
                else:
                    b["approach"].append((sl, bm.group(1)))
        elif pm:
            _parse_prediction(ln, head, pm, subs, f, lint, b, ids)
        elif head.startswith("P:"):
            if head != "P: none given" or subs:
                lint.add("FAIL", f, ln, "prediction-form", "no person prediction is written exactly `P: none given`")
            b["none_given"] = True
        elif PRED_LIKE.match(head):
            lint.add("FAIL", f, ln, "prediction-form",
                     "prediction must read `{ID} (you|agent · {confidence}) \"{claim}\"` with falsifier and should-not-change lines")
        elif head.startswith("Stop-points:"):
            if not re.match(r"^Stop-points: irreversible · scope · dead-premise · budget > \S.*$", head):
                lint.add("FAIL", f, ln, "brief-form", "must read `Stop-points: irreversible · scope · dead-premise · budget > {k}× {estimate}`")
            b["stop_points"] = head
            _no_subs(subs, f, lint, "brief-form")
        elif head.startswith("Irreversible:"):
            im = IRREVERSIBLE_RE.match(head)
            if not im:
                lint.add("FAIL", f, ln, "brief-form", "must read ``Irreversible: `{exact command}` ``, one command per line")
            else:
                b["irreversible"].append((ln, im.group(1)))
            _no_subs(subs, f, lint, "brief-form")
        elif CONTRACT_RE.match(head):
            cm = CONTRACT_RE.match(head)
            got = sub_fields(subs, lint, f, "contract-form", ("check", "does NOT prove", "lane"), ("post-check",))
            item = {"id": "C" + cm.group(1), "claim": cm.group(2), "line": ln,
                    **{k.replace(" ", "_").replace("-", "_"): v for k, v in got.items()}}
            for need in ("check", "does NOT prove", "lane"):
                if need not in got:
                    lint.add("FAIL", f, ln, "contract-form", "%s has no `%s:` line" % (item["id"], need))
            lane = got.get("lane", (0, ""))[1]
            if lane and lane not in LANES:
                lint.add("FAIL", f, got["lane"][0], "contract-form", "lane %r is not one of %s" % (lane, " | ".join(LANES)))
            if lane == "irreversible" and "post-check" not in got:
                lint.add("FAIL", f, ln, "contract-form", "%s is irreversible and has no `post-check:` line" % item["id"])
            if item["id"] in [c["id"] for c in b["contract"]]:
                lint.add("FAIL", f, ln, "contract-form", "%s defined twice" % item["id"])
            b["contract"].append(item)
        elif head.startswith("Check files:"):
            val = head[len("Check files:"):].strip()
            if not val:
                lint.add("FAIL", f, ln, "brief-form", "`Check files:` needs paths or `none`")
            b["check_files"] = [] if val == "none" else [p.strip("`") for p in re.split(r"[,\s]+", val) if p.strip("`")]
            _no_subs(subs, f, lint, "brief-form")
        elif head.startswith("|"):
            lint.add("FAIL", f, ln, "contract-form", "tables are not part of the card; write contract items as `C{n} {claim}` lines")
        else:
            lint.add("FAIL", f, ln, "brief-form", "unexpected line in the Brief: %r" % head[:60])
    _check_brief_presence(b, body, f, lint)
    return b


def _no_subs(subs: list, f: str, lint: Lint, rule: str) -> None:
    for sl, st in subs:
        lint.add("FAIL", f, sl, rule, "unexpected indented line: %r" % st.strip()[:60])


def _parse_prediction(ln, head, pm, subs, f, lint, b, ids) -> None:
    letter, num, side, conf, rest = pm.groups()
    pid = letter + num
    allowed = CONFIDENCE if letter == "P" else AGENT_CONFIDENCE
    if conf not in allowed:
        lint.add("FAIL", f, ln, "confidence", "%s confidence %r is not one of %s" % (pid, conf, " | ".join(allowed)))
    if (letter == "P") != (side == "you"):
        lint.add("FAIL", f, ln, "id-reserved", "%s belongs to %s; P is the person's (`you`), A the agent's" % (pid, side))
    if pid in ids:
        lint.add("FAIL", f, ln, "id-reserved", "%s defined twice" % pid)
    ids.add(pid)
    claim = parse_quoted(rest)
    if letter == "P" and claim is None:
        lint.add("FAIL", f, ln, "prediction-form", "%s is the person's words: one double-quoted claim (inner quotes as \\\")" % pid)
    if letter == "A" and claim is None:
        if rest.startswith('"'):
            lint.add("FAIL", f, ln, "prediction-form", "%s claim has an unbalanced or unescaped quote" % pid)
        claim = rest
    got = sub_fields(subs, lint, f, "prediction-form", ("falsifier", "should not change"))
    for need in ("falsifier", "should not change"):
        if need not in got:
            lint.add("FAIL", f, ln, "prediction-form", "%s has no `%s:` line" % (pid, need))
    b["preds"].append({"id": pid, "letter": letter, "side": side, "conf": conf, "claim": claim or rest,
                       "quoted": letter == "P" or rest.startswith('"'), "line": ln, "text": head,
                       "falsifier": got.get("falsifier", (0, ""))[1],
                       "should_not_change": got.get("should not change", (0, ""))[1]})


def _check_brief_presence(b: dict, body: list, f: str, lint: Lint) -> None:
    at = body[0][0] if body else 1
    if not b["approach"]:
        lint.add("FAIL", f, at, "brief-form", "no `Approach:` with at least one `  - {decision} because {why}` line")
    has_p = any(p["letter"] == "P" for p in b["preds"])
    if has_p and b["none_given"]:
        lint.add("FAIL", f, at, "prediction-form", "`P: none given` and P lines together")
    if not has_p and not b["none_given"]:
        lint.add("FAIL", f, at, "prediction-form", "no person prediction and no `P: none given`")
    if b["stop_points"] is None:
        lint.add("FAIL", f, at, "brief-form", "no `Stop-points:` line")
    if not b["contract"]:
        lint.add("FAIL", f, at, "contract-form", "no contract item (`C{n} {claim}` with check, does NOT prove, lane)")
    if b["check_files"] is None:
        lint.add("FAIL", f, at, "brief-form", "no `Check files:` line")
    has_irr_lane = any(c.get("lane", (0, ""))[1] == "irreversible" for c in b["contract"])
    if has_irr_lane and not b["irreversible"]:
        lint.add("FAIL", f, at, "contract-form", "an irreversible contract item but no `Irreversible:` line")
    if b["irreversible"] and not has_irr_lane:
        lint.add("FAIL", f, b["irreversible"][0][0], "contract-form", "an `Irreversible:` line but no contract item in the irreversible lane")
    irr = [(ln, segments(cmd), cmd) for ln, cmd in b["irreversible"]]
    for c in b["contract"]:
        for key in ("check", "post_check"):
            if key not in c:
                continue
            cl, val = c[key]
            spans = re.findall(r"`([^`]+)`", val) or [val]
            for _, isegs, cmd in irr:
                if not isegs:
                    continue
                for span in spans:
                    ssegs = segments(span)
                    if any(ssegs[i:i + len(isegs)] == isegs for i in range(len(ssegs))):
                        lint.add("FAIL", f, cl, "irreversible-check",
                                 "%s %s re-runs the irreversible command `%s`" % (c["id"], key.replace("_", "-"), cmd))
                        break


def _parse_amendments(body: list, f: str, lint: Lint, m: dict) -> None:
    for ln, text in body:
        if not text.strip():
            continue
        am = AMEND_RE.match(text)
        if not am:
            lint.add("WARN", f, ln, "amend-form", "amendment should read `M{n} {time} · after D{n} · decided-for-you|confirmed: {what} · why: {why}`")
            m["amendments"].append({"id": None, "time": None, "after": None, "kind": None, "what": text.strip(), "why": "", "line": ln})
            continue
        if not am.group(3):
            lint.add("WARN", f, ln, "amend-anchor", "M%s has no `after D{n}`" % am.group(1))
        m["amendments"].append({"id": "M" + am.group(1), "time": am.group(2),
                                "after": int(am.group(3)) if am.group(3) else None,
                                "kind": am.group(4), "what": am.group(5), "why": am.group(6), "line": ln})


def _parse_deltas_section(body: list, f: str, lint: Lint, m: dict) -> None:
    lines = [(ln, t) for ln, t in body if t.strip()]
    i = 0
    if lines and re.match(r"^Latest: (D\d+|none)$", lines[0][1]):
        m["latest"] = lines[0][1][len("Latest: "):]
        i = 1
    else:
        lint.add("FAIL", f, lines[0][0] if lines else 1, "rollup", "the Deltas section starts with `Latest: D{n} | none`")
    if i < len(lines) and lines[i][1] == "Rollup:":
        i += 1
    else:
        lint.add("FAIL", f, lines[i][0] if i < len(lines) else 1, "rollup", "the Deltas section has a `Rollup:` line after Latest")
    rest = lines[i:]
    for ln, t in rest:
        if DELTA_IN_CARD.match(t):
            continue  # reported by delta-location
        m["rollup"].append(t.strip()[2:] if t.strip().startswith("- ") else t.strip())
    if len(m["rollup"]) > MAX_ROLLUP:
        lint.add("FAIL", f, rest[MAX_ROLLUP][0], "rollup", "Rollup holds at most %d lines" % MAX_ROLLUP)


def _parse_model_changes(body: list, f: str, lint: Lint, m: dict) -> None:
    for ln, text in body:
        if not text.strip():
            continue
        mm = MODEL_CHANGE_RE.match(text)
        if not mm:
            lint.add("FAIL", f, ln, "model-changes", "must read `- You expected X → it is Y, because Z [shown, not confirmed | confirmed]`")
            m["model_changes"].append((ln, text.strip(), None))
        else:
            m["model_changes"].append((ln, text[2:].rsplit(" [", 1)[0], mm.group(4)))
    if len(m["model_changes"]) > MAX_MODEL_CHANGES:
        lint.add("FAIL", f, m["model_changes"][MAX_MODEL_CHANGES][0], "model-changes", "at most %d Model changes lines" % MAX_MODEL_CHANGES)


def _parse_debrief(head: str, hl: int, body: list, f: str, lint: Lint) -> dict:
    hm = DEBRIEF_HEAD.match(head)
    d = {"line": hl, "time": hm.group(1) if hm else None, "grader": hm.group(2) if hm else None,
         "evidence": [], "rows": [], "none_given": False, "integrity": [], "not_proved": [],
         "not_checked": [], "bottom": {}, "bottom_lines": {}}
    stage = 0  # 0 evidence, 1 rows, 2 integrity, 3 did not prove, 4 not checked, 5 bottom line
    names = {"Evidence:": 0, "Integrity:": 2, "Did NOT prove:": 3, "Not checked:": 4, "Bottom line:": 5}
    for ln, top, subs in blocks(body):
        if top in names:
            want = names[top]
            if want < stage or (want == 0 and d["evidence"]):
                lint.add("FAIL", f, ln, "debrief-form", "%r out of order (Evidence, predictions, Integrity, Did NOT prove, Not checked, Bottom line)" % top)
            stage = want
            bullets = []
            for sl, st in subs:
                bm = BULLET_RE.match(st)
                if not bm:
                    lint.add("FAIL", f, sl, "debrief-form", "expected `  - …` under %s" % top)
                else:
                    bullets.append((sl, bm.group(1)))
            if want == 0:
                d["evidence"] = bullets or [(ln, "")]
                if not bullets:
                    lint.add("FAIL", f, ln, "debrief-form", "Evidence has no `  - `{command}` → {output}` line")
                    d["evidence"] = []
            elif want == 2:
                d["integrity"] = bullets
                keys = ("Brief vs freeze:", "Check files:", "Unlogged hunks:")
                if len(bullets) != 3 or any(not b[1].startswith(k) for b, k in zip(bullets, keys)):
                    lint.add("FAIL", f, ln, "debrief-form", "Integrity holds the three `fu integrity` lines (Brief vs freeze, Check files, Unlogged hunks)")
            elif want == 3:
                d["not_proved"] = bullets
                for sl, st in bullets:
                    if " → leaves open: " not in st or " · still holds: " not in st:
                        lint.add("FAIL", f, sl, "debrief-form", "Did NOT prove line must read `{check} → leaves open: {…} · still holds: {…}`")
            elif want == 4:
                d["not_checked"] = [b for b in bullets if b[1].strip()]
            else:
                _parse_bottom(ln, subs, f, lint, d)
            continue
        pm = PRED_RE.match(top)
        if pm or top == "P: none given":
            if stage > 1:
                lint.add("FAIL", f, ln, "debrief-form", "prediction rows come after Evidence and before Integrity")
            stage = 1
            if top == "P: none given":
                d["none_given"] = True
                continue
            got = sub_fields(subs, lint, f, "debrief-coverage", ("measured", "consistent?", "mechanism"))
            row = {"id": pm.group(1) + pm.group(2), "letter": pm.group(1), "side": pm.group(3),
                   "conf": pm.group(4), "text": top, "line": ln,
                   "measured": got.get("measured", (ln, ""))[1], "verdict": None, "mechanism": None, "tier": None}
            for need in ("measured", "consistent?", "mechanism"):
                if need not in got:
                    lint.add("FAIL", f, ln, "debrief-coverage", "%s has no `%s:` line" % (row["id"], need))
            if "consistent?" in got:
                vl, v = got["consistent?"]
                v = v.replace("’", "'")
                if v == "post-hoc fit (not a test)":
                    v = "post-hoc fit"
                if v not in VERDICTS:
                    lint.add("FAIL", f, vl, "verdict", "%s consistent? %r is not one of %s" % (row["id"], v, " | ".join(VERDICTS)))
                else:
                    row["verdict"] = v
            if "mechanism" in got:
                ml, mv = got["mechanism"]
                mm = MECH_RE.match(mv)
                if not mm:
                    lint.add("FAIL", f, ml, "verdict", "%s mechanism must end with [verified | supported | inferred | untested]" % row["id"])
                    row["mechanism"] = mv
                else:
                    row["mechanism"], row["tier"] = mm.group(1), mm.group(2)
                    _verb_tier(row, ml, f, lint)
            d["rows"].append(row)
            continue
        lint.add("FAIL", f, ln, "debrief-form", "unexpected line in the Debrief: %r" % top[:60])
    if not d["not_checked"]:
        lint.add("FAIL", f, hl, "not-checked", "`Not checked:` needs at least one item")
    if not d["bottom"]:
        lint.add("FAIL", f, hl, "bottom-line", "no `Bottom line:` with holds, did not hold, stops at")
    return d


def _verb_tier(row: dict, ln: int, f: str, lint: Lint) -> None:
    tier, text = row["tier"], row["mechanism"] or ""
    if tier == "untested" and not text.lower().startswith("untested:"):
        lint.add("WARN", f, ln, "verb-tier", "%s: an untested mechanism opens with \"untested:\"" % row["id"])
    if tier != "verified":
        hit = STRONG_VERBS.search(strip_code(text))
        if hit:
            lint.add("WARN", f, ln, "verb-tier", "%s: %r is stronger than [%s]" % (row["id"], hit.group(0), tier))


def _parse_bottom(ln: int, subs: list, f: str, lint: Lint, d: dict) -> None:
    keys = ("holds", "did not hold", "stops at")
    got = sub_fields(subs, lint, f, "bottom-line", keys)
    for k in keys:
        if k not in got:
            lint.add("FAIL", f, ln, "bottom-line", "Bottom line has no `%s:` line" % k)
    d["bottom"] = {k: v for k, (l, v) in got.items()}
    d["bottom_lines"] = {k: l for k, (l, v) in got.items()}


def _scan_card_lines(lines: list, sections: list, f: str, lint: Lint) -> None:
    section_of = {}
    for head, ln, body in sections:
        for i, _ in body:
            section_of[i] = head
    needs = [i for i, t in enumerate(lines, 1) if re.match(r"^\s*(?:- )?Needs you:", t)]
    if len(needs) != 1 or needs[0] != 3:
        for i in needs:
            if i != 3:
                lint.add("FAIL", f, i, "needs-you-once", "`Needs you:` lives once, in the header (line 3); the Debrief updates it there")
        if not needs:
            lint.add("FAIL", f, 3, "needs-you-once", "no `Needs you:` header line")
    for i, t in enumerate(lines, 1):
        sec = section_of.get(i, "")
        if DELTA_IN_CARD.match(t) and not t.lstrip().startswith(("D" + "elta",)):
            lint.add("FAIL", f, i, "delta-location", "a D{n} delta line in the card; deltas live only in {slug}.deltas.md")
        if sec != "## Model changes" and (MODEL_CHANGE_LIKE.match(t) or re.match(r"^#+ Model changes", t) and sec != ""):
            lint.add("WARN", f, i, "model-changes-place", "Model changes belong in the card's `## Model changes` section only")


def scan_placeholders(lines: list, f: str, lint: Lint) -> None:
    """Template `{…}` placeholders. Prose: `{…}`, `{a | b}` or `{lowercase words}`; inside
    code spans only the template's own command placeholders (code may use braces)."""
    for i, t in enumerate(lines, 1):
        found = [ph.strip() for ph in PLACEHOLDER_RE.findall(strip_code(t))
                 if ph.strip() in ("…", "...") or " | " in ph or PLACEHOLDER_WORDS.match(ph.strip())]
        for span in re.findall(r"`([^`]*)`", t):
            found += [ph.strip() for ph in PLACEHOLDER_RE.findall(span) if ph.strip() in CODE_PLACEHOLDERS]
        for body in dict.fromkeys(found):
            lint.add("FAIL", f, i, "placeholder", "template placeholder left in: {%s}" % body)


def scan_ids(lines: list, defined: dict, f: str, lint: Lint) -> None:
    for i, t in enumerate(lines, 1):
        if i == 1 and t.startswith("# "):
            continue
        seen = set()
        for letter, num in ID_RE.findall(strip_code(t)):
            pid = letter + num
            if pid in seen:
                continue
            seen.add(pid)
            if pid not in defined:
                lint.add("FAIL", f, i, "id-reserved",
                         "%s is cited but not a Brief prediction; P{n}/A{n} name predictions only, name premises in words" % pid)


def lint_deltas(path: Path, f: str, lint: Lint) -> list:
    out = []
    if not path.is_file():
        return out
    lines = read_text(path).splitlines()
    seen = set()
    for i, t in enumerate(lines, 1):
        if not t.strip() or (t.startswith("#") and i == 1):
            continue
        dm = DELTA_LINE.match(t)
        if not dm:
            lint.add("FAIL", f, i, "delta-form", "delta must read `D{n} {time} {kind}: {text} → {evidence path}`")
            continue
        num, date, hm, kind, rest = dm.groups()
        d = {"id": "D" + num, "n": int(num), "date": date, "hm": hm, "kind": kind, "line": i,
             "text": rest, "path": "", "cost": None, "stop": None}
        if hm is None:
            lint.add("WARN", f, i, "delta-time", "D%s has a date but no HH:MM" % num)
        if kind not in DELTA_KINDS:
            lint.add("FAIL", f, i, "delta-form", "D%s kind %r is not one of %s" % (num, kind, " | ".join(DELTA_KINDS)))
        sm = STOP_TAG.search(rest)
        if sm:
            if sm.group(1) not in STOP_KINDS:
                lint.add("FAIL", f, i, "delta-form", "D%s stop tag %r is not one of %s" % (num, sm.group(1), " | ".join(STOP_KINDS)))
            d["stop"] = sm.group(1)
            rest = rest[:sm.start()]
        if " · cost if wrong: " in rest:
            rest, d["cost"] = rest.split(" · cost if wrong: ", 1)
        if " → " not in rest:
            lint.add("FAIL", f, i, "delta-form", "D%s has no `→ {evidence path}`" % num)
            d["text"] = rest
        else:
            d["text"], d["path"] = rest.rsplit(" → ", 1)
        if kind == "decided-for-you" and not d["cost"]:
            lint.add("FAIL", f, i, "delta-form", "D%s is decided-for-you and has no `· cost if wrong: …`" % num)
        if d["id"] in seen:
            lint.add("FAIL", f, i, "delta-form", "D%s appears twice" % num)
        seen.add(d["id"])
        out.append(d)
    scan_placeholders(lines, f, lint)
    return out


def lint_claim(path: Path, f: str, lint: Lint) -> dict:
    """A measured-results claim file (references/results.md) without or beside a card."""
    lines = read_text(path).splitlines()
    fields = {}
    for i, t in enumerate(lines, 1):
        km = re.match(r"^([A-Z][A-Za-z ]*?)\s*: (.*)$", t)
        if km and km.group(1) not in fields:
            fields[km.group(1)] = (i, km.group(2).strip())
    if "Person prediction" not in fields and "Your prediction" in fields:  # pre-5.2 label
        fields["Person prediction"] = fields["Your prediction"]
    for need in ("Claim under test", "Person prediction", "Agent prediction", "Falsifier", "Written"):
        if need not in fields:
            lint.add("FAIL", f, 1, "claim-form", "claim file has no `%s :` line" % need)
    if "Person prediction" in fields:
        ln, val = fields["Person prediction"]
        cm = re.match(r'^(".*")(?: \(([^()]*)\))?$', val)
        if val.strip("`") == "none given":
            pass
        elif not cm or parse_quoted(cm.group(1)) is None:
            lint.add("FAIL", f, ln, "claim-form", "`Person prediction` is the person's words in double quotes (inner quotes as \\\"), or `none given`")
        elif cm.group(2) and cm.group(2) not in CONFIDENCE:
            lint.add("FAIL", f, ln, "confidence", "confidence %r is not one of %s" % (cm.group(2), " | ".join(CONFIDENCE)))
    if "Timing" in fields:
        ln, val = fields["Timing"]
        if not TIMING_RE.match("Timing: " + val):
            lint.add("FAIL", f, ln, "claim-form", "`Timing` must be `draft | Brief frozen {time}, commit {hash} | self-reported`")
    scan_placeholders(lines, f, lint)
    return fields


def strict_caps(text: str, m: dict, f: str, lint: Lint) -> None:
    words = count_words(text)
    if words > STRICT_MAX_WORDS:
        lint.add("FAIL", f, 1, "strict-caps", "card has %d words (strict: at most %d)" % (words, STRICT_MAX_WORDS))
    b = m["brief"]
    agent = [p for p in b["preds"] if p["letter"] == "A"]
    person = [p for p in b["preds"] if p["letter"] == "P"]
    if len(agent) > STRICT_MAX_AGENT_PREDICTIONS:
        lint.add("FAIL", f, agent[STRICT_MAX_AGENT_PREDICTIONS]["line"], "strict-caps",
                 "%d agent predictions (strict: at most %d)" % (len(agent), STRICT_MAX_AGENT_PREDICTIONS))
    if len(person) > STRICT_MAX_AGENT_PREDICTIONS:
        lint.add("WARN", f, person[STRICT_MAX_AGENT_PREDICTIONS]["line"], "strict-caps",
                 "%d person predictions; more than %d is fine, but each is graded" % (len(person), STRICT_MAX_AGENT_PREDICTIONS))
    if len(b["contract"]) > STRICT_MAX_CONTRACT:
        lint.add("FAIL", f, b["contract"][STRICT_MAX_CONTRACT]["line"], "strict-caps",
                 "%d contract items (strict: at most %d)" % (len(b["contract"]), STRICT_MAX_CONTRACT))
    fields = []
    if m["goal"]:
        fields.append((2, "Goal", m["goal"]))
    if m["needs"] and m["needs"] != "nothing":
        fields.append((3, "Needs you", m["needs"]))
    fields += [(ln, "Approach", t) for ln, t in b["approach"]]
    for p in b["preds"]:
        if p["letter"] == "A":
            fields.append((p["line"], p["id"], p["claim"]))
        fields += [(p["line"], p["id"] + " falsifier", p["falsifier"]),
                   (p["line"], p["id"] + " should not change", p["should_not_change"])]
    for c in b["contract"]:
        fields.append((c["line"], c["id"], c["claim"]))
        for key in ("check", "does_NOT_prove", "post_check"):
            if key in c:
                fields.append((c[key][0], c["id"] + " " + key.replace("_", " "), c[key][1]))
    for d in m["debriefs"]:
        for r in d["rows"]:
            fields += [(r["line"], r["id"] + " measured", r["measured"]), (r["line"], r["id"] + " mechanism", r["mechanism"] or "")]
        fields += [(ln, "Not checked", t) for ln, t in d["not_checked"]]
        fields += [(d["bottom_lines"].get(k, d["line"]), k, v) for k, v in d["bottom"].items()]
    for ln, name, val in fields:
        n = count_words(strip_code(val))
        if n > STRICT_MAX_FIELD_WORDS:
            lint.add("FAIL", f, ln, "strict-caps", "%s has %d words (strict: at most %d per field)" % (name, n, STRICT_MAX_FIELD_WORDS))


def check_debrief_rows(m: dict, f: str, lint: Lint) -> None:
    brief_preds = {p["id"]: p for p in m["brief"]["preds"]}
    for d in m["debriefs"]:
        rows = d["rows"]
        ids = [r["id"] for r in rows]
        for pid, p in brief_preds.items():
            if pid not in ids:
                lint.add("FAIL", f, d["line"], "debrief-coverage", "%s is in the Brief and not graded" % pid)
        for r in rows:
            p = brief_preds.get(r["id"])
            if p and r["text"] != p["text"]:
                lint.add("FAIL", f, r["line"], "debrief-coverage", "%s line differs from the Brief; copy it exactly" % r["id"])
            if ids.count(r["id"]) > 1:
                lint.add("FAIL", f, r["line"], "debrief-coverage", "%s graded twice" % r["id"])
        letters = [r["letter"] for r in rows]
        if "A" in letters and "P" in letters[letters.index("A"):]:
            lint.add("FAIL", f, d["line"], "debrief-coverage", "the person's predictions (P) come before the agent's (A)")
        if m["brief"]["none_given"] and any(r["letter"] == "P" for r in rows):
            lint.add("FAIL", f, d["line"], "debrief-coverage", "the Brief says `P: none given`; there is no P row to grade")
        _check_bottom(d, f, lint)


def _check_bottom(d: dict, f: str, lint: Lint) -> None:
    if not d["bottom"]:
        return
    verdict = {r["id"]: r["verdict"] for r in d["rows"]}
    where = {}
    for key in ("holds", "did not hold", "stops at"):
        ln = d["bottom_lines"].get(key, d["line"])
        for letter, num in ID_RE.findall(strip_code(d["bottom"].get(key, ""))):
            where.setdefault(letter + num, []).append((key, ln))
    want = {"consistent": "holds", "partly": "did not hold", "inconsistent": "did not hold",
            "can't tell": "stops at", "post-hoc fit": "stops at"}
    for pid, v in verdict.items():
        places = where.get(pid, [])
        if len(places) != 1:
            lint.add("FAIL", f, places[1][1] if len(places) > 1 else d["line"], "bottom-line",
                     "%s must appear exactly once under holds, did not hold or stops at (found %d)" % (pid, len(places)))
            continue
        if v and places[0][0] != want[v]:
            lint.add("FAIL", f, places[0][1], "bottom-line", "%s is %s and belongs under `%s`, not `%s`" % (pid, v, want[v], places[0][0]))
    for pid, places in where.items():
        if pid not in verdict:
            lint.add("FAIL", f, places[0][1], "bottom-line", "%s is in the Bottom line but not graded" % pid)
    holds = d["bottom"].get("holds", "")
    hit = SUPERLATIVE.search(strip_code(holds))
    if hit and any(v != "consistent" for v in verdict.values()):
        lint.add("WARN", f, d["bottom_lines"].get("holds", d["line"]), "superlative",
                 "%r under holds while a row is not consistent" % hit.group(0))


def lint_paths(root: Path, card, claim, slug: str, strict_flag: bool):
    """Lint the card (if any), its deltas file, decisions.md and the claim file (if any)."""
    fu = root / FU_DIR
    lint = Lint()
    strict = strict_flag or read_profile(fu).get("strict") == "yes"
    model = None
    if card is not None:
        f = "tasks/%s.md" % slug
        text = read_text(card)
        model = parse_card(text, slug, f, lint)
        lines = text.splitlines()
        deltas_path = card.with_name(slug + ".deltas.md")
        model["deltas"] = lint_deltas(deltas_path, "tasks/%s.deltas.md" % slug, lint)
        defined = {p["id"]: p for p in model["brief"]["preds"]}
        scan_ids(lines, defined, f, lint)
        if deltas_path.is_file():
            scan_ids(read_text(deltas_path).splitlines(), defined, "tasks/%s.deltas.md" % slug, lint)
        scan_placeholders(lines, f, lint)
        check_debrief_rows(model, f, lint)
        live = [t for t in lines[:model["live_end"]] if t.strip()]
        if len(live) > LIVE_MAX_LINES:
            lint.add("FAIL" if strict else "WARN", f, 1, "live-length",
                     "header to Open is %d lines (at most %d)" % (len(live), LIVE_MAX_LINES))
        if strict:
            strict_caps(text, model, f, lint)
    if claim is not None:
        lint_claim(claim, "predictions/%s.md" % slug, lint)
    dec = fu / "decisions.md"
    if dec.is_file():
        n = len(read_text(dec).splitlines())
        if n > DECISIONS_MAX_LINES:
            lint.add("WARN", "decisions.md", DECISIONS_MAX_LINES + 1, "decisions-length",
                     "decisions.md has %d lines (at most %d)" % (n, DECISIONS_MAX_LINES))
    return lint, model


# ------------------------------------------------------------------------------ commands

def cmd_init(a) -> int:
    root = find_root(a.root)
    fu = root / FU_DIR
    for sub in ("tasks", "predictions", "logs", "view"):
        (fu / sub).mkdir(parents=True, exist_ok=True)
    prof_path = fu / "profile.md"
    existing = read_text(prof_path).splitlines() if prof_path.is_file() else []
    flags = {}
    if a.strict:
        flags["strict"] = "yes"
    if a.guard:
        flags["guard"] = a.guard
    out, keys = [], set()
    for line in existing:
        km = re.match(r"^\s*([a-z]+)\s*:", line)
        if km and km.group(1) in flags:
            out.append("%s: %s" % (km.group(1), flags[km.group(1)]))
        else:
            out.append(line)
        if km:
            keys.add(km.group(1))
    for k, v in PROFILE_DEFAULTS:
        if k not in keys:
            out.append("%s: %s" % (k, flags.get(k, v)))
    write_text(prof_path, "\n".join(out) + "\n")
    print("initialised %s" % fu)
    gi = root / ".gitignore"
    have = set(read_text(gi).splitlines()) if gi.is_file() else set()
    missing = [ln for ln in GITIGNORE_LINES if ln not in have]
    if missing:
        print("add to .gitignore:")
        for ln in missing:
            print("  %s" % ln)
    return 0


def cmd_lint(a) -> int:
    root, card, claim, slug, note = resolve_card(find_root(a.root), a.slug, True)
    if note:
        print(note)
    lint, _ = lint_paths(root, card, claim, slug, a.strict)
    for line in lint.lines():
        print(line)
    return 1 if lint.fails() else 0


def _set_state(text: str, state: str) -> str:
    return re.sub(r"^(Goal: .+ · State: ).*$", lambda mm: mm.group(1) + state, text, count=1, flags=re.M)


def _set_timing(path: Path, value: str, claim: bool) -> None:
    text = read_text(path)
    pat = r"^Timing\s*:.*$"
    if re.search(pat, text, flags=re.M):
        text = re.sub(pat, lambda _m: "Timing: " + value, text, count=1, flags=re.M)
    elif claim:
        if re.search(r"^Written\s*:.*$", text, flags=re.M):
            text = re.sub(r"^(Written\s*:.*)$", lambda mm: mm.group(1) + "\nTiming: " + value, text, count=1, flags=re.M)
        else:
            text = text.rstrip("\n") + "\nTiming: " + value + "\n"
    write_text(path, text)


def _freeze_skip(root: Path, rels: list, profile: dict):
    if profile.get("commits") == "no":
        return "commits: no"
    try:
        top = git(root, "rev-parse", "--show-toplevel", timeout=20)
    except (OSError, subprocess.SubprocessError) as exc:
        return "git not available (%s)" % exc.__class__.__name__
    if top.returncode != 0:
        return "not a git repository"
    for name in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply"):
        gp = git(root, "rev-parse", "--git-path", name).stdout.strip()
        if gp and (root / gp).exists():
            return "merge, rebase or cherry-pick in progress"
    if git(root, "symbolic-ref", "-q", "HEAD").returncode != 0:
        return "detached HEAD"
    for rel in rels:
        if git(root, "check-ignore", "-q", "--", rel).returncode == 0:
            return "path ignored: %s" % rel
    toplevel = Path(top.stdout.strip())
    ours = set()
    for rel in rels:
        try:
            ours.add((root / rel).resolve().relative_to(toplevel.resolve()).as_posix())
        except ValueError:
            ours.add(rel)
    staged = [p for p in git(root, "diff", "--cached", "--name-only").stdout.splitlines() if p]
    others = [p for p in staged if p not in ours]
    if others:
        return "other changes already staged: %s" % ", ".join(others[:3])
    return None


def _changed_decisions(root: Path, fu: Path) -> list:
    """decisions.md when changed, with decisions-archive.md when that changed too."""
    out = []
    for name in ("decisions.md", "decisions-archive.md"):
        path = fu / name
        if not path.is_file() or (name != "decisions.md" and not out):
            continue
        try:
            st = git(root, "status", "--porcelain", "--", path.relative_to(root).as_posix())
            if st.returncode == 0 and st.stdout.strip():
                out.append(path.relative_to(root).as_posix())
        except (OSError, subprocess.SubprocessError):
            pass
    return out


def cmd_freeze(a) -> int:
    root, card, claim, slug, _ = resolve_card(find_root(a.root), a.slug, False)
    fu = root / FU_DIR
    stage = a.stage
    main = card if card is not None else claim
    # Step 1: the card's own edits, before any skip check (fu freeze owns State).
    if card is not None:
        text = read_text(card)
        if stage == "brief":
            text = re.sub(r"^## Brief \(draft\)$", "## Brief (frozen %s)" % now_str(), text, count=1, flags=re.M)
        text = _set_state(text, STAGE_STATE[stage])
        write_text(card, text)
        deltas = card.with_name(slug + ".deltas.md")
        if stage == "brief" and not deltas.is_file():
            write_text(deltas, "# %s deltas (append-only)\n" % slug)
    rels = [main.relative_to(root).as_posix()]
    if card is not None:
        deltas = card.with_name(slug + ".deltas.md")
        if deltas.is_file():
            rels.append(deltas.relative_to(root).as_posix())
        if claim is not None:
            rels.append(claim.relative_to(root).as_posix())
    rels += _changed_decisions(root, fu)
    reason = _freeze_skip(root, rels, read_profile(fu))
    if reason:
        if stage == "brief":
            _set_timing(main, "self-reported", card is None)
        print("self-reported: %s" % reason)
        return 3
    msg = "chore(card): %s %s" % (stage, slug)
    try:
        add = git(root, "add", "--", *rels)
        com = git(root, "commit", "--only", "-m", msg, "--", *rels) if add.returncode == 0 else add
    except (OSError, subprocess.SubprocessError) as exc:
        com = subprocess.CompletedProcess([], 1, "", str(exc))
    if com.returncode != 0:
        try:
            git(root, "reset", "-q", "--", *rels)
        except (OSError, subprocess.SubprocessError):
            pass
        if stage == "brief":
            _set_timing(main, "self-reported", card is None)
        detail = (com.stderr or com.stdout or "").strip().splitlines()
        print("self-reported: commit failed%s" % (" (%s)" % detail[-1][:120] if detail else ""))
        return 3
    short = git(root, "rev-parse", "--short", "HEAD").stdout.strip()
    if stage == "brief":
        _set_timing(main, "Brief frozen %s, commit %s" % (now_str(), short), card is None)
    print("committed %s (%s %s)" % (short, stage, slug))
    return 0


def _brief_block(text: str):
    lines = text.splitlines()
    start = next((i for i, t in enumerate(lines) if t.startswith("## Brief")), None)
    if start is None:
        return None, []
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start, lines[start:end]


def _ranges(nums: list) -> str:
    out, nums = [], sorted(set(nums))
    i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(str(nums[i]) if i == j else "%d-%d" % (nums[i], nums[j]))
        i = j + 1
    return ", ".join(out)


def cmd_integrity(a) -> int:
    root, card, claim, slug, note = resolve_card(find_root(a.root), a.slug, True)
    if note:
        print(note)
    if card is None:
        raise UsageError("integrity reads a card; %s has only a claim file" % slug)
    text = read_text(card)
    tm = TIMING_RE.match(next((t for t in text.splitlines() if t.startswith("Timing:")), ""))
    if not tm or not tm.group(3):
        why = "timing: %s" % (tm.group(1) if tm else "unparsable")
        for k in ("Brief vs freeze", "Check files", "Unlogged hunks"):
            print("%s: not run (%s)" % (k, why))
        return 3
    commit = tm.group(3)
    try:
        return _integrity(root, card, slug, text, commit)
    except (OSError, subprocess.SubprocessError) as exc:
        for k in ("Brief vs freeze", "Check files", "Unlogged hunks"):
            print("%s: not run (git: %s)" % (k, exc.__class__.__name__))
        return 3


def _integrity(root: Path, card: Path, slug: str, text: str, commit: str) -> int:
    rel = card.relative_to(root).as_posix()
    shown = git(root, "show", "%s:./%s" % (commit, rel))
    if shown.returncode != 0:
        for k in ("Brief vs freeze", "Check files", "Unlogged hunks"):
            print("%s: not run (commit %s not readable)" % (k, commit))
        return 3
    findings = 0
    start, now_block = _brief_block(text)
    _, then_block = _brief_block(shown.stdout)
    edited = []
    sm = difflib.SequenceMatcher(a=then_block, b=now_block, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            edited += list(range(start + 1 + j1, start + 1 + max(j2, j1 + 1)))
    if edited:
        findings += 1
        print("Brief vs freeze: edited: lines %s" % _ranges(edited))
    else:
        print("Brief vs freeze: unchanged")
    lint = Lint()
    model = parse_card(text, slug, "card", lint)
    files = model["brief"]["check_files"]
    if not files:
        print("Check files: none named")
    else:
        changed = git(root, "diff", "--name-only", "--relative", commit, "--", *files).stdout.split()
        if changed:
            findings += 1
            print("Check files: changed: %s" % ", ".join(changed))
        else:
            print("Check files: unchanged")
    logged_text = " ".join([read_text(card.with_name(slug + ".deltas.md")) if card.with_name(slug + ".deltas.md").is_file() else ""]
                           + [x["what"] + " " + x["why"] for x in model["amendments"]]
                           + [t for _, t in model["brief"]["approach"]]
                           + [" ".join([c["claim"]] + [v[1] for k, v in c.items() if isinstance(v, tuple)]) for c in model["brief"]["contract"]])
    unlogged = []
    diff = git(root, "diff", "-U0", "--relative", commit, "--", ".", ":(exclude)%s" % FU_DIR).stdout
    path = None
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = None if line[4:] == "/dev/null" else line[6:] if line.startswith("+++ b/") else line[4:]
        elif line.startswith("--- a/") and path is None:
            path = line[6:]
        elif line.startswith("@@") and path:
            hm = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
            if hm:
                s, n = int(hm.group(1)), int(hm.group(2) or 1)
                unlogged.append((path, s, s + max(n, 1) - 1))
        if line.startswith("diff --git"):
            path = None
    untracked = git(root, "ls-files", "--others", "--exclude-standard", "--", ".", ":(exclude)%s" % FU_DIR).stdout.split("\n")
    for p in untracked:
        if p:
            try:
                n = len((root / p).read_text(encoding="utf-8", errors="replace").splitlines())
            except OSError:
                n = 1
            unlogged.append((p, 1, max(n, 1)))
    hunks = ["%s:%d-%d" % h for h in unlogged
             if h[0] not in logged_text and os.path.basename(h[0]) not in logged_text]
    if hunks:
        findings += 1
        print("Unlogged hunks: %s" % ", ".join(hunks))
    else:
        print("Unlogged hunks: none")
    return 1 if findings else 0


def read_log(fu: Path) -> list:
    path = fu / "predictions-log.md"
    out = []
    if path.is_file():
        for t in read_text(path).splitlines():
            parts = [p.strip() for p in t.split(" · ")]
            if len(parts) == 6 and re.match(r"^\d{4}-\d{2}-\d{2}$", parts[0]):
                out.append(parts)
    return out


def calibration(rows: list) -> dict:
    latest = {}
    for r in rows:
        latest[(r[1], r[2])] = r
    stats = {"you": [0, 0], "agent": [0, 0], "excluded": {"can't tell": 0, "post-hoc fit": 0},
             "cards": set(), "by_conf": {}}
    for (slug, _), r in latest.items():
        side, verdict, conf = r[3], r[4], r[5]
        if side not in ("you", "agent"):
            continue
        if verdict in stats["excluded"]:
            stats["excluded"][verdict] += 1
            continue
        held = 1 if verdict == "consistent" else 0
        stats[side][0] += held
        stats[side][1] += 1
        stats["cards"].add(slug)
        if conf in ("low", "medium", "high"):
            cell = stats["by_conf"].setdefault((side, conf), [0, 0])
            cell[0] += held
            cell[1] += 1
    return stats


def stat_line(stats: dict, force: bool = False):
    (yk, yn), (ak, an) = stats["you"], stats["agent"]
    if not force and yn < STAT_MIN_N and an < STAT_MIN_N:
        return None
    soft = " (too soft?)" if an >= STAT_MIN_N and ak == an else ""
    return "You: %d of %d held · Agent: %d of %d held%s" % (yk, yn, ak, an, soft)


def cmd_log(a) -> int:
    root, card, claim, slug, note = resolve_card(find_root(a.root), a.slug, True)
    if note:
        print(note)
    if card is None:
        raise UsageError("log reads a card's Debrief; %s has only a claim file" % slug)
    lint, model = lint_paths(root, card, None, slug, False)
    bad = [i for i in lint.fails() if i[3] in DEBRIEF_RULES or (i[3] == "id-reserved" and model["debriefs"])]
    if not model["debriefs"] or bad:
        for line in lint.lines():
            print(line)
        if not model["debriefs"]:
            print("log: no Debrief section in tasks/%s.md" % slug)
        return 1
    d = model["debriefs"][-1]
    date = (d["time"] or now_str())[:10]
    fu = root / FU_DIR
    rows = read_log(fu)
    latest = {}
    for r in rows:
        latest[(r[1], r[2])] = " · ".join(r)
    new = []
    for r in d["rows"]:
        if not r["verdict"]:
            continue
        line = " · ".join([date, slug, r["id"], r["side"], r["verdict"], r["conf"]])
        if latest.get((slug, r["id"])) != line:
            new.append(line)
    if new:
        path = fu / "predictions-log.md"
        prev = read_text(path) if path.is_file() else ""
        if prev and not prev.endswith("\n"):
            prev += "\n"
        write_text(path, prev + "\n".join(new) + "\n")
    for line in new:
        print(line)
    if not new:
        print("log: nothing new for %s" % slug)
    sl = stat_line(calibration(read_log(fu)))
    if sl:
        print(sl)
    return 0


def card_summary(path: Path) -> dict:
    text = read_text(path)
    h = quick_header(text)
    slug = path.name[:-3]
    deltas_path = path.with_name(slug + ".deltas.md")
    dnums = []
    if deltas_path.is_file():
        dnums = [int(mm.group(1)) for mm in re.finditer(r"^D(\d+) ", read_text(deltas_path), flags=re.M)]
    seen = h["last_seen_d"]
    unseen = len([n for n in dnums if seen is None or n > seen])
    rows = []
    heads = [mm.start() for mm in re.finditer(r"^## Debrief", text, flags=re.M)]
    if heads:
        cur = None
        for line in text[heads[-1]:].splitlines():
            pm = PRED_RE.match(line)
            if pm:
                cur = [pm.group(1) + pm.group(2), pm.group(3), None]
                rows.append(cur)
            vm = re.match(r"^  - consistent\?: (.+)$", line)
            if vm and cur is not None:
                v = vm.group(1).strip().replace("’", "'")
                cur[2] = "post-hoc fit" if v.startswith("post-hoc fit") else v
    return {"slug": slug, "path": path, "header": h, "unseen": unseen, "dnums": dnums,
            "rows": rows, "mtime": path.stat().st_mtime, "text": text}


def graded_counts(rows: list) -> dict:
    out = {}
    for side in ("you", "agent"):
        vals = [r[2] for r in rows if r[1] == side and r[2] in VERDICTS]
        counted = [v for v in vals if v not in ("can't tell", "post-hoc fit")]
        out[side] = (sum(1 for v in counted if v == "consistent"), len(counted))
    return out


def cmd_list(a) -> int:
    root = find_root(a.root)
    fu = root / FU_DIR
    if not fu.is_dir():
        raise UsageError("no %s/ under %s" % (FU_DIR, root))
    cards = [card_summary(p) for p in card_files(fu)]
    shown = [c for c in cards if a.all or c["header"]["state"] != "debriefed"]
    if not shown:
        print("no open cards" if not a.all else "no cards")
    for c in shown:
        h = c["header"]
        print("%s · %s" % (c["slug"], h["state"] or "unparsable header"))
        print("  - needs you: %s" % (h["needs"] or "nothing"))
        seen = "after D%d" % h["last_seen_d"] if h["last_seen_d"] is not None else "never"
        print("  - last seen: %s · unseen deltas: %d" % (seen, c["unseen"]))
        if c["rows"]:
            g = graded_counts(c["rows"])
            print("  - graded: you %d of %d held · agent %d of %d held" % (g["you"] + g["agent"]))
        else:
            print("  - graded: not yet")
    sl = stat_line(calibration(read_log(fu)))
    if sl:
        print(sl)
    return 0


# ------------------------------------------------------------------------------- render

CSS = """
:root{--paper:#FAF9F5;--panel:#F0EEE6;--card:#FFFFFF;--edge:#E3DFD3;--ink:#141413;--sub:#5E5D59;--mute:#B1ADA1;
--acc:#C15F3C;--org:#D97757;--pink:#F5DDD1;--grn:#5F7348;--grn-bg:#E6EBDD;--sand:#9A6A43;--sand-bg:#F4E7DA;
--red:#B5442E;--red-bg:#F6DAD3;
--serif:Georgia,"Times New Roman","Noto Serif SC","Noto Serif CJK SC","Songti SC","Source Han Serif SC",SimSun,serif;
--sans:-apple-system,"Segoe UI",Helvetica,Arial,"Noto Sans SC","Noto Sans CJK SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,"Noto Sans Mono CJK SC","Sarasa Mono SC",monospace;color-scheme:light dark}
@media (prefers-color-scheme:dark){:root{--paper:#191816;--panel:#23221F;--card:#2A2926;--edge:#3A3833;--ink:#EDEBE4;--sub:#A9A69C;--mute:#6F6C64;
--acc:#E58B66;--org:#E58B66;--pink:#3D2A21;--grn:#A4BA84;--grn-bg:#2B3324;--sand:#DDB48F;--sand-bg:#3A2F25;--red:#E8806A;--red-bg:#3E2420}}
*{box-sizing:border-box}html{background:var(--paper);color:var(--ink)}
body{margin:0;font:15px/1.55 var(--sans);background:var(--paper)}
.wrap{max-width:1040px;margin:0 auto;padding:28px 24px 64px}
code{font-family:var(--mono);font-size:.86em;background:var(--panel);border:1px solid var(--edge);border-radius:5px;padding:0 .3em;word-break:break-word}
a{color:var(--acc)}
.kicker{font:700 13px var(--mono);letter-spacing:1.2px;color:var(--acc);text-transform:uppercase}
h1{font:700 26px/1.25 var(--serif);margin:6px 0 10px}
h2{font:700 13px var(--mono);letter-spacing:1.4px;text-transform:uppercase;color:var(--sub);margin:34px 0 10px}
h3{margin:0 0 8px;font:700 15px var(--serif)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font:600 12px var(--mono);border:1px solid var(--edge);background:var(--card);border-radius:999px;padding:2px 10px;color:var(--sub)}
.chip.state{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.chip.warn{border-color:var(--sand);color:var(--sand);background:var(--sand-bg)}
.banner{margin-top:18px;border-radius:10px;background:var(--red-bg);border-left:4px solid var(--red);padding:10px 14px;font-size:13.5px}
.banner b{font:700 12px var(--mono);letter-spacing:1px;color:var(--red);text-transform:uppercase}
.banner ul{margin:6px 0 0;padding-left:18px}
.needs{margin-top:22px;background:var(--card);border:1.5px solid var(--org);border-radius:14px;padding:20px 24px 18px 28px;position:relative}
.needs::before{content:"";position:absolute;left:0;top:14px;bottom:14px;width:6px;border-radius:3px;background:var(--org)}
.needs.none{border-color:var(--edge)}.needs.none::before{background:var(--edge)}
.needs .label{display:flex;align-items:center;gap:8px;font:700 12px var(--mono);letter-spacing:1.4px;color:var(--acc)}
.needs.none .label{color:var(--sub)}
.needs .ask{font:700 23px/1.3 var(--serif);margin:8px 0 6px}
.needs .why{margin-top:10px;display:grid;grid-template-columns:auto 1fr;gap:4px 12px;font-size:14px;color:var(--sub)}
.needs .why b{color:var(--ink);font-weight:600}
.stops{background:var(--card);border:1px solid var(--edge);border-radius:12px;padding:14px 18px}
.stops dl{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:0}
.stops dt{font:700 11px var(--mono);letter-spacing:.8px;text-transform:uppercase;color:var(--sub);padding-top:3px}
.stops dd{margin:0}
.stops dd.edge{font:700 17px/1.4 var(--serif)}
.gaps{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}
.gapcol{background:var(--card);border:1px solid var(--edge);border-radius:12px;padding:14px 16px}
.gapcol ul,.plain{margin:0;padding-left:18px;font-size:13.5px}.gapcol li,.plain li{margin:5px 0}
.muted{color:var(--sub)}
.strip{display:flex;align-items:flex-start;overflow-x:auto;padding:8px 2px 4px;background:var(--card);border:1px solid var(--edge);border-radius:12px}
.node{flex:0 0 auto;width:96px;text-align:center;position:relative;padding-top:4px}
.node::before{content:"";position:absolute;top:13px;left:0;right:0;height:2px;background:var(--edge);z-index:0}
.node:first-child::before{left:50%}.node:last-child::before{right:50%}
.mark{position:relative;z-index:1;display:block;margin:0 auto;width:18px;height:18px;border:2.5px solid var(--sub);background:var(--card);border-radius:50%}
.mark.decided{border-radius:3px;transform:rotate(45deg) scale(.85)}
.mark.surprise{background:var(--ink);border-color:var(--ink)}
.mark.amend{border-style:dashed}
.mark.frame{border-radius:3px;background:var(--sub)}
.mark.seen{border-color:var(--sub);background:var(--panel);border-radius:2px;width:6px;height:22px;margin-top:-2px}
.node.irr .mark{border-color:var(--org);box-shadow:0 0 0 3px var(--pink)}
.node .nid{display:block;font:700 12px var(--mono);margin-top:6px}
.node .nk{display:block;font:11px var(--mono);color:var(--sub)}
.node .nt{display:block;font:10.5px var(--mono);color:var(--mute)}
.node.irr .nk{color:var(--acc);font-weight:700}
.tally{display:flex;gap:10px;flex-wrap:wrap}
.tbox{background:var(--card);border:1px solid var(--edge);border-radius:10px;padding:8px 14px;min-width:110px}
.tbox .n{font:700 24px var(--serif)}.tbox .l{font:12px var(--mono);color:var(--sub)}
.tbox.consistent .n{color:var(--grn)}.tbox.partly .n{color:var(--sand)}.tbox.inconsistent .n{color:var(--red)}.tbox.grey .n{color:var(--mute)}
.rows{list-style:none;margin:12px 0 0;padding:0;border:1px solid var(--edge);border-radius:12px;background:var(--card);overflow:hidden}
.rows>li{border-top:1px solid var(--edge);padding:12px 16px;break-inside:avoid}
.rows>li.sep{background:var(--panel);padding:6px 16px;font:700 11px var(--mono);letter-spacing:1.2px;color:var(--sub)}
.rows>li:first-child{border-top:0}
.id{font:700 13px var(--mono);display:inline-block;min-width:26px;padding:0 6px;border-radius:5px;margin-right:6px;border:1.5px solid var(--ink)}
.id.you{background:var(--ink);color:var(--paper)}.id.agent{background:transparent;color:var(--ink)}
.conf{font:600 11px var(--mono);color:var(--sub);border:1px solid var(--edge);border-radius:999px;padding:0 7px;margin-left:4px;white-space:nowrap}
.kv{display:grid;grid-template-columns:150px 1fr;gap:3px 12px;margin-top:6px;font-size:13.5px}
.kv .k{font:700 10.5px var(--mono);letter-spacing:.8px;text-transform:uppercase;color:var(--mute);padding-top:3px}
.v{font:700 12px var(--mono);border-radius:999px;padding:1px 10px;white-space:nowrap;display:inline-block}
.v.consistent{background:var(--grn-bg);color:var(--grn)}.v.partly{background:var(--sand-bg);color:var(--sand)}
.v.inconsistent{background:var(--red-bg);color:var(--red)}.v.grey,.v.pending{background:var(--panel);color:var(--sub)}
.tier{font:600 11px var(--mono);color:var(--sub);margin-left:6px}
details{background:var(--card);border:1px solid var(--edge);border-radius:12px;margin:10px 0;break-inside:avoid}
summary{cursor:pointer;padding:12px 16px;font:700 15px var(--serif);display:flex;justify-content:space-between;gap:12px}
summary .s{font:12px var(--mono);color:var(--sub);font-weight:400}
.dbody{padding:0 16px 14px;font-size:14px}
.dbody ul{padding-left:18px}.dbody li{margin:5px 0}
.lane{font:700 11px var(--mono);color:var(--sub)}.lane.irreversible{color:var(--acc)}
.foot{margin-top:40px;font:12px var(--mono);color:var(--sub);border-top:1px solid var(--edge);padding-top:10px}
.summary{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}
.sbox{background:var(--card);border:1px solid var(--edge);border-radius:10px;padding:8px 14px}
.sbox b{font:700 22px var(--serif);display:block}.sbox span{font:12px var(--mono);color:var(--sub)}
.sbox.hot{border-color:var(--org)}.sbox.hot b{color:var(--acc)}
.calib{background:var(--card);border:1px solid var(--edge);border-radius:12px;padding:14px 18px}
.calib .line{font:700 18px/1.4 var(--serif)}
.calib .cap{font-size:12.5px;color:var(--sub);margin-top:6px}
.cards{list-style:none;margin:0;padding:0}
.cards>li{background:var(--card);border:1px solid var(--edge);border-radius:12px;padding:12px 16px 12px 20px;margin:10px 0;position:relative;break-inside:avoid}
.cards>li.needs-you::before{content:"";position:absolute;left:0;top:12px;bottom:12px;width:5px;border-radius:3px;background:var(--org)}
.slug{font:700 14px var(--mono)}.slug a{color:var(--ink)}
.st{font:700 11.5px var(--mono);border-radius:999px;padding:1px 9px;margin-left:8px;border:1px solid var(--edge);color:var(--sub)}
.st.debriefed{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.st.waiting{background:var(--org);color:#fff;border-color:var(--org)}
.goal{font-size:13.5px;color:var(--sub);margin:2px 0 6px}
.sq{display:inline-flex;gap:3px;align-items:center;margin-right:12px;vertical-align:middle}
.sq .who{font:600 10.5px var(--mono);color:var(--sub);margin-right:3px}
.sq i{width:12px;height:12px;border-radius:2px;display:inline-block;border:2px solid var(--mute)}
.sq.you i{background:var(--mute)}.sq.agent i{background:transparent}
.sq i.consistent{border-color:var(--grn)}.sq.you i.consistent{background:var(--grn)}
.sq i.partly{border-color:var(--sand)}.sq.you i.partly{background:var(--sand)}
.sq i.inconsistent{border-color:var(--red)}.sq.you i.inconsistent{background:var(--red)}
.sq i.pending{border-style:dashed;background:transparent}.sq.you i.pending{background:var(--edge)}
.legend{display:flex;gap:14px;flex-wrap:wrap;font:11.5px var(--mono);color:var(--sub);margin-top:12px}
svg text{font:11px var(--mono);fill:var(--sub)}
@media (max-width:760px){.gaps{grid-template-columns:1fr}.kv{grid-template-columns:1fr}}
@media print{:root{--paper:#fff;--panel:#F3F1EA;--card:#fff;--edge:#D9D4C7;--ink:#141413;--sub:#4A4945;--mute:#8A877E;
--acc:#A24E2F;--org:#C15F3C;--pink:#F5DDD1;--grn:#4E6339;--grn-bg:#E6EBDD;--sand:#8A5C38;--sand-bg:#F4E7DA;--red:#9E3A26;--red-bg:#F6DAD3}
body{background:#fff;font-size:12px;-webkit-print-color-adjust:exact;print-color-adjust:exact}.wrap{padding:0}
.strip{overflow:visible;flex-wrap:wrap}details::details-content{content-visibility:visible;display:block}}
"""


def esc(s) -> str:
    return html.escape("" if s is None else str(s), quote=True)


def rich(s) -> str:
    """Escape everything; backtick spans become <code>. No other markup passes through."""
    parts = ("" if s is None else str(s)).split("`")
    if len(parts) % 2 == 0:  # unbalanced backticks: no code spans
        return esc(s)
    return "".join(("<code>%s</code>" % esc(p)) if i % 2 else esc(p) for i, p in enumerate(parts))


def page(title: str, body: list) -> str:
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n<div class=\"wrap\">\n%s\n</div>\n</body>\n</html>\n"
            % (esc(title), CSS, "\n".join(body)))


def verdict_class(v) -> str:
    return {"consistent": "consistent", "partly": "partly", "inconsistent": "inconsistent"}.get(v or "", "grey" if v else "pending")


def plural(n: int, word: str, many: str = None) -> str:
    return "%d %s" % (n, word if n == 1 else (many or word + "s"))


def read_approvals(fu: Path, slug: str) -> list:
    path = fu / "logs" / "approvals.jsonl"
    out = []
    if path.is_file():
        for line in read_text(path).splitlines():
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if isinstance(rec, dict) and rec.get("slug") == slug:
                out.append(rec)
    return out


def render_card(fu: Path, slug: str, m: dict, brief_fails: list, warns: list) -> str:
    b, last = m["brief"], (m["debriefs"][-1] if m["debriefs"] else None)
    out = ['<div class="kicker">// task card · %s</div>' % esc(slug), "<h1>%s</h1>" % rich(m["goal"])]
    chips = ['<span class="chip state">%s</span>' % esc(m["state"]), '<span class="chip">mode: %s</span>' % esc(m["mode"])]
    seen = "never" if m["last_seen_d"] is None else "%s, after D%d" % (m["last_seen"].split(",")[0], m["last_seen_d"])
    chips.append('<span class="chip">last seen by you: %s</span>' % esc(seen))
    timing = m["timing"] or ""
    chips.append('<span class="chip%s">timing: %s</span>' % (" warn" if timing in ("self-reported", "draft") else "", esc(timing)))
    if last:
        weak = last["grader"] != "fresh context"
        chips.append('<span class="chip%s">graded by %s</span>' % (" warn" if weak else "", esc(last["grader"])))
    chips += ['<span class="chip warn" title="%s">%s</span>' % (esc(w[4]), esc("%s · %s:%d" % (w[3], w[1], w[2]))) for w in warns]
    out.append('<div class="chips">%s</div>' % "".join(chips))
    if brief_fails:
        out.append('<div class="banner"><b>lint FAIL inside the frozen Brief · reported, not edited</b><ul>%s</ul></div>'
                   % "".join("<li>%s</li>" % esc("%s:%d %s: %s" % (i[1], i[2], i[3], i[4])) for i in brief_fails))
    out.append(_needs_html(m))
    out += _stops_html(m, last)
    out += _strip_html(fu, slug, m)
    out += _verdicts_html(m, last)
    out += _folded_html(m, last)
    out.append('<div class="foot">rendered by fu from .finding-unknowns/tasks/%s.md · %s · lint: %s</div>'
               % (esc(slug), esc(now_str()), esc(plural(len(warns), "WARN", "WARN"))))
    return page("%s · task card" % slug, out)


def _needs_html(m: dict) -> str:
    if m["needs_parts"] is None:
        return ('<section class="needs none" aria-label="Needs you"><div class="label">NEEDS YOU</div>'
                '<div class="ask">Nothing right now.</div></section>')
    x, y, z = m["needs_parts"]
    return ('<section class="needs" aria-label="Needs you"><div class="label">NEEDS YOU</div>'
            '<div class="ask">%s</div><div class="why"><b>Recommendation</b><span>%s</span>'
            '<b>Settles</b><span>%s</span></div></section>' % (rich(x), rich(y), rich(z)))


def _stops_html(m: dict, last) -> list:
    if not last:
        dnp = [c for c in m["brief"]["contract"] if "does_NOT_prove" in c]
        out = ["<h2>Where the evidence stops · not graded yet</h2>",
               '<div class="stops"><p class="muted" style="margin:0 0 6px">No Debrief yet. What each contract check will not prove:</p><ul class="plain">']
        out += ["<li><b>%s</b> %s: %s</li>" % (esc(c["id"]), rich(c["claim"]), rich(c["does_NOT_prove"][1])) for c in dnp]
        out.append("</ul></div>")
        return out
    bl = last["bottom"]
    out = ["<h2>Where the evidence stops</h2>", '<div class="stops"><dl>',
           '<dt>stops at</dt><dd class="edge">%s</dd>' % rich(bl.get("stops at", "")),
           "<dt>holds</dt><dd>%s</dd>" % rich(bl.get("holds", "")),
           "<dt>did not hold</dt><dd>%s</dd>" % rich(bl.get("did not hold", "")), "</dl></div>",
           '<div class="gaps"><div class="gapcol"><h3>Checks did NOT prove · %d</h3><ul>' % len(last["not_proved"])]
    out += ["<li>%s</li>" % rich(t) for _, t in last["not_proved"]] or ['<li class="muted">none listed</li>']
    out.append('</ul></div><div class="gapcol"><h3>Not checked · %d</h3><ul>' % len(last["not_checked"]))
    out += ["<li>%s</li>" % rich(t) for _, t in last["not_checked"]]
    out.append("</ul></div></div>")
    return out


def _strip_html(fu: Path, slug: str, m: dict) -> list:
    deltas = m.get("deltas") or []
    events = []
    if m["brief_frozen"]:
        events.append(("frame", "Brief", "frozen", m["brief_frozen"], "Brief frozen " + m["brief_frozen"], False))
    amend_after = {}
    for am in m["amendments"]:
        amend_after.setdefault(am["after"], []).append(am)
    for am in amend_after.get(None, []) if not deltas else []:
        events.append(("amend", am["id"] or "M?", am["kind"] or "amendment", am["time"] or "", am["what"], False))
    approvals = sorted(read_approvals(fu, slug), key=lambda r: str(r.get("time", "")))
    placed = set()
    kinds = {"deviation": "dev", "decided-for-you": "decided", "surprise": "surprise"}
    for d in deltas:
        when = "%s %s" % (d["date"], d["hm"]) if d["hm"] else d["date"]
        for i, rec in enumerate(approvals):
            if i not in placed and d["hm"] and str(rec.get("time", "")) < when:
                placed.add(i)
                events.append(("frame", "run", "irreversible", str(rec.get("time", "")), "ran the card's irreversible command", True))
        label = d["kind"] + (" · stop: " + d["stop"] if d["stop"] else "")
        events.append((kinds.get(d["kind"], "dev"), d["id"], label, when, d["text"], d["stop"] == "irreversible"))
        if m["last_seen_d"] == d["n"]:
            events.append(("seen", "seen", "last seen by you", "", "Last seen by you: " + (m["last_seen"] or ""), False))
        for am in amend_after.get(d["n"], []):
            events.append(("amend", am["id"] or "M?", am["kind"] or "amendment", am["time"] or "", am["what"], False))
    for i, rec in enumerate(approvals):
        if i not in placed:
            events.append(("frame", "run", "irreversible", str(rec.get("time", "")), "ran the card's irreversible command", True))
    if m["debriefs"]:
        t = m["debriefs"][-1]["time"] or ""
        events.append(("frame", "Debrief", "graded", t, "Debrief " + t, False))
    n_surprise = sum(1 for d in deltas if d["kind"] == "surprise")
    irr_at = [e[1] for e in events if e[5]]
    head = "What happened, in order · %s" % plural(len(deltas), "delta")
    if n_surprise:
        head += ", %s" % plural(n_surprise, "surprise", "surprises")
    if irr_at:
        head += " · irreversible step at %s" % ", ".join(irr_at)
    out = ["<h2>%s</h2>" % esc(head)]
    if not events:
        return out + ['<p class="muted">No deltas yet.</p>']
    out.append('<div class="strip" role="list">')
    for cls, nid, kind, when, title, irr in events:
        hm = when[11:16] if len(when) >= 16 else when[5:10] if len(when) >= 10 else ""
        out.append('<div class="node%s" role="listitem" title="%s"><span class="mark %s"></span>'
                   '<span class="nid">%s</span><span class="nk">%s</span><span class="nt">%s</span></div>'
                   % (" irr" if irr else "", esc(title), esc(cls), esc(nid), esc(kind), esc(hm)))
    out.append("</div>")
    return out


def _verdicts_html(m: dict, last) -> list:
    preds = m["brief"]["preds"]
    rows = {r["id"]: r for r in last["rows"]} if last else {}
    out = []
    if last:
        counts = {v: sum(1 for r in last["rows"] if r["verdict"] == v) for v in VERDICTS}
        n = len(last["rows"])
        head = "Verdicts · %d of %d consistent" % (counts["consistent"], n)
        extra = ["%d %s" % (counts[v], v) for v in VERDICTS[1:] if counts[v]]
        if extra:
            head += "; " + ", ".join(extra)
        out.append("<h2>%s</h2>" % esc(head))
        out.append('<div class="tally">')
        for v in VERDICTS:
            out.append('<div class="tbox %s"><div class="n">%d</div><div class="l">%s</div></div>'
                       % (verdict_class(v), counts[v], esc(v)))
        out.append("</div>")
    else:
        out.append("<h2>%s</h2>" % esc("Predictions · %d, not graded yet" % len(preds)))
    out.append('<ul class="rows">')
    for side, label in (("you", "YOUR PREDICTIONS"), ("agent", "AGENT PREDICTIONS")):
        group = [p for p in preds if p["side"] == side]
        out.append('<li class="sep">%s</li>' % label)
        if side == "you" and m["brief"]["none_given"]:
            out.append('<li class="muted">P: none given</li>')
        for p in group:
            r = rows.get(p["id"])
            v = r["verdict"] if r else None
            item = ['<li><span class="id %s">%s</span>%s<span class="conf">%s</span> '
                    % (esc(side), esc(p["id"]), rich(('"%s"' % p["claim"]) if p["quoted"] else p["claim"]), esc(p["conf"])),
                    '<span class="v %s">%s</span>' % (verdict_class(v), esc(v or "not graded")),
                    '<div class="kv"><span class="k">falsifier</span><span>%s</span>' % rich(p["falsifier"]),
                    '<span class="k">should not change</span><span>%s</span>' % rich(p["should_not_change"])]
            if r:
                item.append('<span class="k">measured</span><span>%s</span>' % rich(r["measured"]))
                item.append('<span class="k">mechanism</span><span>%s<span class="tier">[%s]</span></span>'
                            % (rich(r["mechanism"]), esc(r["tier"] or "no tier")))
            item.append("</div></li>")
            out.append("".join(item))
    out.append("</ul>")
    return out


def _folded_html(m: dict, last) -> list:
    b = m["brief"]
    irr_n = sum(1 for c in b["contract"] if c.get("lane", (0, ""))[1] == "irreversible")
    out = ["<h2>Everything else · folded</h2>", "<details><summary>Brief%s <span class=\"s\">%s · %s</span></summary><div class=\"dbody\">"
           % (esc(" (frozen %s)" % m["brief_frozen"] if m["brief_frozen"] else " (draft)"),
              esc(plural(len(b["contract"]), "contract item")), esc("%d irreversible" % irr_n))]
    out.append("<p><b>Approach</b></p><ul>%s</ul>" % "".join("<li>%s</li>" % rich(t) for _, t in b["approach"]))
    if b["stop_points"]:
        out.append("<p>%s</p>" % rich(b["stop_points"]))
    for _, cmd in b["irreversible"]:
        out.append('<p><span class="lane irreversible">IRREVERSIBLE</span> <code>%s</code></p>' % esc(cmd))
    out.append("<ul>")
    for c in b["contract"]:
        lane = c.get("lane", (0, ""))[1]
        sub = ["<li><b>%s</b> %s <span class=\"lane %s\">%s</span><ul>" % (esc(c["id"]), rich(c["claim"]), esc(lane), esc(lane))]
        for key, label in (("check", "check"), ("does_NOT_prove", "does NOT prove"), ("post_check", "post-check")):
            if key in c:
                sub.append("<li>%s: %s</li>" % (esc(label), rich(c[key][1])))
        out.append("".join(sub) + "</ul></li>")
    out.append("</ul><p>Check files: %s</p></div></details>" % rich(", ".join(b["check_files"] or []) or "none"))
    deltas = m.get("deltas") or []
    out.append("<details><summary>What changed along the way <span class=\"s\">%s · %s</span></summary><div class=\"dbody\"><ul>"
               % (esc(plural(len(m["amendments"]), "amendment")), esc(plural(len(deltas), "delta"))))
    for am in m["amendments"]:
        out.append("<li><b>%s</b> %s · %s: %s · why: %s</li>" % (esc(am["id"] or "M?"), esc(am["time"] or ""),
                   esc("after D%d" % am["after"] if am["after"] is not None else "no anchor"), rich(am["what"]), rich(am["why"])))
    for d in deltas:
        extra = (" · cost if wrong: %s" % rich(d["cost"]) if d["cost"] else "") + (" · stop: %s" % esc(d["stop"]) if d["stop"] else "")
        out.append("<li><b>%s</b> %s %s · %s: %s → <code>%s</code>%s</li>" % (esc(d["id"]), esc(d["date"]), esc(d["hm"] or ""),
                   esc(d["kind"]), rich(d["text"]), esc(d["path"]), extra))
    if m["rollup"]:
        out.append("<li>Rollup: %s</li>" % " · ".join(rich(r) for r in m["rollup"]))
    out.append("</ul></div></details>")
    if m["model_changes"]:
        out.append("<details><summary>Model changes <span class=\"s\">%d</span></summary><div class=\"dbody\"><ul>%s</ul></div></details>"
                   % (len(m["model_changes"]), "".join("<li>%s <span class=\"tier\">[%s]</span></li>" % (rich(t), esc(s or "?"))
                                                       for _, t, s in m["model_changes"])))
    if m["open"]:
        out.append("<details><summary>Open <span class=\"s\">%d</span></summary><div class=\"dbody\"><ul>%s</ul></div></details>"
                   % (len(m["open"]), "".join("<li>%s</li>" % rich(t) for _, t in m["open"])))
    if last:
        out.append("<details><summary>Evidence and integrity <span class=\"s\">%s</span></summary><div class=\"dbody\"><ul>%s</ul><p><b>Integrity</b></p><ul>%s</ul></div></details>"
                   % (esc(plural(len(last["evidence"]), "line")), "".join("<li>%s</li>" % rich(t) for _, t in last["evidence"]),
                      "".join("<li>%s</li>" % rich(t) for _, t in last["integrity"])))
    return out


def render_index(fu: Path) -> str:
    cards = [card_summary(p) for p in card_files(fu)]
    cards.sort(key=lambda c: (c["header"]["needs"] in (None, "nothing"), -c["mtime"]))
    states = [c["header"]["state"] for c in cards]
    graded = sum(1 for c in cards for r in c["rows"] if r[2])
    needs_n = sum(1 for c in cards if c["header"]["needs"] not in (None, "nothing"))
    out = ['<div class="kicker">// .finding-unknowns/tasks · %s</div>' % esc(plural(len(cards), "card")),
           "<h1>Task cards in this repo</h1>", '<div class="summary">',
           '<div class="sbox hot"><b>%d</b><span>need you</span></div>' % needs_n]
    for s in STATES:
        out.append('<div class="sbox"><b>%d</b><span>%s</span></div>' % (states.count(s), esc(s)))
    out.append('<div class="sbox"><b>%d</b><span>predictions graded</span></div></div>' % graded)
    out += _calibration_html(calibration(read_log(fu)))
    out.append("<h2>Cards · need you first, then newest</h2>")
    out.append('<ul class="cards">')
    for c in cards:
        out.append(_index_item(fu, c))
    out.append("</ul>")
    out.append('<div class="legend"><span>verdict colour: green consistent · sand partly · red inconsistent · grey can\'t tell / post-hoc fit</span>'
               '<span>shape: filled = you · hollow = agent · dashed = not graded</span><span>left bar = needs you</span></div>')
    out.append('<div class="foot">rendered by fu from .finding-unknowns/tasks/ and predictions-log.md · %s</div>' % esc(now_str()))
    return page("finding-unknowns · task cards", out)


def _index_item(fu: Path, c: dict) -> str:
    h = c["header"]
    lint = Lint()
    parse_card(c["text"], c["slug"], "card", lint)
    bad = len(lint.fails())
    needs = h["needs"] not in (None, "nothing")
    state = h["state"] or "unparsable"
    link = (fu / "view" / (c["slug"] + ".html")).is_file()
    slug_html = '<a href="%s.html">%s</a>' % (esc(c["slug"]), esc(c["slug"])) if link else esc(c["slug"])
    parts = ['<li class="%s"><div><span class="slug">%s</span><span class="st %s">%s</span>%s</div>'
             % ("needs-you" if needs else "", slug_html, "waiting" if state == "waiting on you" else esc(state), esc(state),
                ' <span class="chip warn">%s</span>' % esc(plural(bad, "lint FAIL", "lint FAILs")) if bad else ""),
             '<div class="goal">%s</div>' % rich(h["goal"] or "")]
    parts.append('<div class="kv"><span class="k">needs you</span><span>%s</span>' % rich(h["needs"] or "nothing"))
    seen = "after D%d" % h["last_seen_d"] if h["last_seen_d"] is not None else "never"
    parts.append('<span class="k">last seen</span><span>%s · unseen deltas: %d</span>' % (esc(seen), c["unseen"]))
    marks = []
    for side in ("you", "agent"):
        rows = [r for r in c["rows"] if r[1] == side]
        if not rows:
            pending = len(re.findall(r"^%s\d+ \(%s · " % ("P" if side == "you" else "A", side), c["text"], flags=re.M))
            rows = [(None, side, None)] * pending
        marks.append('<span class="sq %s"><span class="who">%s</span>%s</span>'
                     % (side, side, "".join('<i class="%s" title="%s"></i>' % (verdict_class(r[2]), esc(r[2] or "not graded")) for r in rows)))
    g = graded_counts(c["rows"])
    count = ("you %d of %d held · agent %d of %d held" % (g["you"] + g["agent"])) if c["rows"] else "not yet graded"
    parts.append('<span class="k">graded</span><span>%s <span class="muted">%s</span></span></div></li>' % ("".join(marks), esc(count)))
    return "".join(parts)


def _calibration_html(st: dict) -> list:
    (yk, yn), (ak, an) = st["you"], st["agent"]
    out = ["<h2>Calibration · from predictions-log.md</h2>", '<div class="calib">']
    if yn + an == 0:
        out.append('<div class="line">No graded predictions in the log yet.</div></div>')
        return out
    out.append('<div class="line">%s</div>' % esc(stat_line(st, force=True)))
    with_conf = sum(n for (_, _), (_, n) in st["by_conf"].items())
    ex = st["excluded"]
    cap = ("n = graded predictions, latest grade per card and ID, from %s; predictions on one card are not independent. "
           "Held = consistent. Excluded: %d can't tell, %d post-hoc fit." % (plural(len(st["cards"]), "card"), ex["can't tell"], ex["post-hoc fit"]))
    if with_conf >= CURVE_MIN_N:
        out.append(_curve_svg(st))
        cap += " Each dot is one confidence level for one side; the number beside it is held/graded. Filled = you, hollow = agent."
    else:
        cap += " %d graded with a stated confidence; a curve needs at least %d, so this is a count only." % (with_conf, CURVE_MIN_N)
    out.append('<div class="cap">%s</div></div>' % esc(cap))
    return out


def _curve_svg(st: dict) -> str:
    w, h, left, top, plot_h = 520, 200, 60, 16, 150
    xs = {"low": left + 70, "medium": left + 220, "high": left + 370}
    parts = ['<svg role="img" aria-label="share held by stated confidence" viewBox="0 0 %d %d" width="%d" height="%d">' % (w, h, w, h)]
    for frac in (0, 0.5, 1):
        y = top + plot_h * (1 - frac)
        parts.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="currentColor" stroke-opacity=".15"/>' % (left, w - 20, y, y))
        parts.append('<text x="%d" y="%.1f" text-anchor="end">%d%%</text>' % (left - 6, y + 4, int(frac * 100)))
    for conf, x in xs.items():
        parts.append('<text x="%d" y="%d" text-anchor="middle">%s</text>' % (x, top + plot_h + 18, conf))
        for side, dx in (("you", -14), ("agent", 14)):
            k, n = st["by_conf"].get((side, conf), (0, 0))
            if not n:
                continue
            y = top + plot_h * (1 - k / n)
            fill = "var(--ink)" if side == "you" else "none"
            parts.append('<circle cx="%d" cy="%.1f" r="6" fill="%s" stroke="var(--ink)" stroke-width="2"><title>%s %s: %d of %d held</title></circle>'
                         % (x + dx, y, fill, side, conf, k, n))
            parts.append('<text x="%d" y="%.1f" text-anchor="%s">%d/%d</text>' % (x + dx + (10 if dx > 0 else -10), y + 4, "start" if dx > 0 else "end", k, n))
    parts.append("</svg>")
    return "".join(parts)


def cmd_render(a) -> int:
    root = find_root(a.root)
    fu = root / FU_DIR
    if a.list:
        if not fu.is_dir():
            raise UsageError("no %s/ under %s" % (FU_DIR, root))
        (fu / "view").mkdir(parents=True, exist_ok=True)
        out = fu / "view" / "index.html"
        write_text(out, render_index(fu))
        print(out)
        return 0
    root, card, claim, slug, note = resolve_card(root, a.slug, True)
    if note:
        print(note)
    if card is None:
        raise UsageError("render reads a card; %s has only a claim file" % slug)
    fu = root / FU_DIR
    lint, model = lint_paths(root, card, None, slug, False)
    lo, hi = model["brief_range"]
    f = "tasks/%s.md" % slug
    in_brief = [i for i in lint.fails() if model["brief_frozen"] and i[1] == f and lo <= i[2] <= hi]
    blocking = [i for i in lint.fails() if i not in in_brief]
    if blocking:
        for line in lint.lines():
            print(line)
        print("render: lint FAIL outside the frozen Brief; fix the card, nothing written")
        return 1
    (fu / "view").mkdir(parents=True, exist_ok=True)
    out = fu / "view" / (slug + ".html")
    write_text(out, render_card(fu, slug, model, sorted(set(in_brief), key=lambda i: i[2]), sorted(set(lint.warns()), key=lambda i: (i[1], i[2]))))
    print(out)
    return 0


# -------------------------------------------------------------------------------- guard

def _open_irreversible(fu: Path) -> list:
    out = []
    for p in card_files(fu):
        text = read_text(p)
        if not is_open(text):
            continue
        for line in text.splitlines():
            im = IRREVERSIBLE_RE.match(line)
            if im:
                out.append((p.name[:-3], im.group(1)))
    return out


def _append_jsonl(path: Path, rec: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(path), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _guard(phase: str, raw: str):
    """Return the hook JSON to print, or None. Raises on any problem (caller fails open)."""
    data = json.loads(raw)
    if not isinstance(data, dict) or data.get("tool_name") != "Bash":
        return None
    command = (data.get("tool_input") or {}).get("command")
    if not isinstance(command, str) or not command.strip():
        return None
    start = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    root = find_fu_root(Path(start).resolve())
    if root is None:
        return None
    fu = root / FU_DIR
    profile = read_profile(fu)
    mode = profile.get("guard", "ask")
    if mode == "off":
        return None
    named = _open_irreversible(fu)
    hits = match_command(command, [c for _, c in named])
    hits.sort(key=lambda h: not h[1])
    norm = norm_command(command)
    when = now_str()
    if phase == "post":
        for idx, exact in hits:
            slug, irr = named[idx]
            _append_jsonl(fu / "logs" / "approvals.jsonl",
                          {"sha256": sha(norm), "line_sha256": sha(norm_command(irr)), "exact": exact,
                           "time": when, "slug": slug})
            card = fu / "tasks" / (slug + ".md")
            text = read_text(card)
            if quick_header(text).get("state") == "waiting on you":
                write_text(card, _set_state(text, "building"))
        return None
    if hits:
        idx, exact = hits[0]
        slug, irr = named[idx]
        prior = _prior_run(fu, slug, norm, irr)
        what = "irreversible step" if exact else "variant of the irreversible step"
        if prior:
            reason = "card %s: `%s` already ran once at %s; a post-check must not re-execute it" % (slug, irr, prior)
        else:
            reason = "card %s: %s `%s`" % (slug, what, irr)
        if mode != "ask":
            _append_jsonl(fu / "logs" / "guard.jsonl", {"time": when, "slug": slug, "sha256": sha(norm),
                                                       "would": "ask", "reason": reason})
            return None
        return _ask(reason)
    for name, rx in DESTRUCTIVE:
        if rx.search(command):
            _append_jsonl(fu / "logs" / "guard.jsonl", {"time": when, "pattern": name, "sha256": sha(norm),
                                                       "command": command[:200], "would": "ask"})
            if mode == "ask" and profile.get("strict") == "yes":
                return _ask("finding-unknowns (strict): destructive pattern `%s`" % name)
            return None
    return None


def _prior_run(fu: Path, slug: str, norm: str, irr: str):
    path = fu / "logs" / "approvals.jsonl"
    if not path.is_file():
        return None
    line_sha, cmd_sha = sha(norm_command(irr)), sha(norm)
    found = None
    for line in read_text(path).splitlines():
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if not isinstance(rec, dict) or rec.get("slug") != slug:
            continue
        if rec.get("sha256") == cmd_sha or (rec.get("line_sha256") == line_sha and rec.get("exact")):
            found = found or rec.get("time")
    return found


def _ask(reason: str) -> dict:
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask",
                                   "permissionDecisionReason": reason}}


def run_guard(argv: list) -> int:
    """Hook entry. Always exit 0; never write to stderr; print JSON only on an ask."""
    try:
        phase = argv[0] if len(argv) == 1 and argv[0] in ("pre", "post") else None
        if phase is None:
            return 0
        raw = sys.stdin.read()
        result = _guard(phase, raw)
        if result is not None:
            sys.stdout.write(json.dumps(result) + "\n")
    except BaseException:  # noqa: BLE001 - fail open on anything, including SystemExit
        pass
    return 0


# --------------------------------------------------------------------------------- main

def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default=argparse.SUPPRESS, help="project root (default: discovered)")
    p = argparse.ArgumentParser(prog="fu", description="finding-unknowns task-card tool (docs/design/fu-cli.md)")
    p.add_argument("--root", default=None, help="project root (default: discovered)")
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("init", parents=[common], help="create .finding-unknowns/ and profile.md")
    s.add_argument("--strict", action="store_true")
    s.add_argument("--guard", choices=("off", "log", "ask"))
    s = sub.add_parser("lint", parents=[common], help="check a card against card.md")
    s.add_argument("slug", nargs="?")
    s.add_argument("--strict", action="store_true")
    s = sub.add_parser("freeze", parents=[common], help="commit the card at a stage")
    s.add_argument("slug")
    s.add_argument("--stage", required=True, choices=("brief", "stop", "resume", "debrief"))
    s = sub.add_parser("integrity", parents=[common], help="Brief, check files and unlogged hunks vs the freeze")
    s.add_argument("slug", nargs="?")
    s = sub.add_parser("log", parents=[common], help="append graded predictions to predictions-log.md")
    s.add_argument("slug", nargs="?")
    s = sub.add_parser("list", parents=[common], help="open cards (or --all)")
    s.add_argument("--all", action="store_true")
    s = sub.add_parser("render", parents=[common], help="write the HTML view")
    s.add_argument("slug", nargs="?")
    s.add_argument("--list", action="store_true")
    return p


COMMANDS = {"init": cmd_init, "lint": cmd_lint, "freeze": cmd_freeze, "integrity": cmd_integrity,
            "log": cmd_log, "list": cmd_list, "render": cmd_render}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "guard":
        return run_guard(argv[1:])
    parser = build_parser()
    a = parser.parse_args(argv)
    if not a.cmd:
        parser.print_help()
        return 2
    try:
        return COMMANDS[a.cmd](a)
    except UsageError as exc:
        print("fu %s: %s" % (a.cmd, exc))
        return 2


if __name__ == "__main__":
    sys.exit(main())
