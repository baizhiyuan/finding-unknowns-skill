#!/usr/bin/env python3
"""Aggregate Stage 0 per PREREG (frozen at 4c61f06)."""
from __future__ import annotations

import json, pathlib, re, statistics, subprocess
from collections import defaultdict

S = pathlib.Path("/tmp/fu-stage0")
G = S / "grade"
ITEMS = ["M1", "M2_R1", "M2_R2", "M3", "M4", "M6", "M7"]
TASKS = ["T1", "T2", "T3", "T4", "T5", "T6"]
ARMS = ["plain", "w60", "v5"]


def load(pid, g):
    p = G / "out" / f"{pid}.{g}.txt"
    if not p.exists():
        return None
    t = p.read_text()
    try:
        return json.loads(t[t.index("{"): t.rindex("}") + 1])
    except ValueError:
        return None


def combine(a, b):
    def norm(v):
        if v in (0, 1):
            return v
        if v is None:
            return None
        return "u"
    va, vb = norm(a), norm(b)
    if va is None and vb is None:
        return None, "na"
    if va == "u" and vb == "u":
        return 0, "both_ungradable"
    if va == "u":
        return vb, "one_ungradable"
    if vb == "u":
        return va, "one_ungradable"
    if va is None or vb is None:
        return (va if vb is None else vb), "one_null"
    return (1 if va == vb == 1 else 0 if va == vb == 0 else 0.5), ("agree" if va == vb else "disagree")


def words(t):
    return len(re.findall(r"\S+", t or ""))


def main():
    mp = json.loads((G / "map.json").read_text())
    m5 = json.loads((G / "m5.json").read_text())
    rows, agree, missing = [], defaultdict(int), []
    for pid, info in mp.items():
        a, b = load(pid, "opus"), load(pid, "astra")
        if a is None or b is None:
            missing.append((pid, info, a is None, b is None))
            a, b = a or {}, b or {}
        r = dict(info, pid=pid)
        for it in ITEMS + ["H4_primary"]:
            v, how = combine(a.get(it), b.get(it))
            r[it] = v
            agree[how] += 1 if how in ("agree", "disagree") else 0
            if how in ("agree", "disagree"):
                agree[f"{it}:{how}"] += 1
        ca, cb = a.get("completion"), b.get("completion")
        r["completion"] = (1 if ca and cb else 0 if (ca is False and cb is False) else 0.5)
        r["M5"] = m5.get(pid, {}).get("M5")
        r["M5_reason"] = m5.get(pid, {}).get("reason")
        meta = json.loads((S / "runs" / info["dir"] / "meta.json").read_text())
        tr = json.loads((S / "runs" / info["dir"] / "transcript.json").read_text())
        last = [m for m in tr if m["role"] == "assistant"]
        r["final_words"] = words(last[-1]["text"]) if last else 0
        r["cost"] = meta["cost_usd"]
        r["turns"] = meta["turns"]
        r["skills"] = sorted({s for t in meta["turn_detail"] for s in t.get("skills", [])})
        r["changed"] = meta["changed_files"]
        r["composite"] = sum((r[i] or 0) for i in ITEMS) if info["task"] in TASKS else None
        rows.append(r)
    out = {"missing_grades": [(p, i["dir"], ma, mb) for p, i, ma, mb in missing]}
    # primary
    sets = defaultdict(float)
    for r in rows:
        if r["task"] in TASKS and r["arm"] in ARMS:
            sets[(r["arm"], r["run"])] += r["composite"]
    arm_score = {a: statistics.mean(sets[(a, n)] for n in (1, 2, 3)) for a in ARMS}
    ranges = {a: max(sets[(a, n)] for n in (1, 2, 3)) - min(sets[(a, n)] for n in (1, 2, 3)) for a in ARMS}
    noise = max(1.0, max(ranges.values()) / 2)
    beats = lambda x, y: arm_score[x] - arm_score[y] > noise  # noqa: E731
    if beats("v5", "plain") and beats("v5", "w60"):
        branch = "1: release 5.0"
    elif beats("w60", "plain"):
        branch = "2: do not merge v5; ship the 60 words"
    else:
        branch = "3: nothing new ships; can't tell"
    out["primary"] = {"run_set_totals": {f"{a}-{n}": sets[(a, n)] for a in ARMS for n in (1, 2, 3)},
                      "arm_score": arm_score, "ranges": ranges, "noise": noise,
                      "diffs": {"v5-plain": arm_score["v5"] - arm_score["plain"], "v5-w60": arm_score["v5"] - arm_score["w60"],
                                "w60-plain": arm_score["w60"] - arm_score["plain"]}, "branch": branch}
    # per item rates
    per = {}
    for a in ARMS:
        rs = [r for r in rows if r["arm"] == a and r["task"] in TASKS]
        per[a] = {it: round(statistics.mean(r[it] for r in rs if r[it] is not None), 3) for it in ITEMS}
        m5v = [r["M5"] for r in rs if r["M5"] is not None]
        per[a]["M5"] = round(statistics.mean(m5v), 3) if m5v else None
        per[a]["completion"] = round(statistics.mean(r["completion"] for r in rs), 3)
        per[a]["final_words_mean"] = round(statistics.mean(r["final_words"] for r in rs))
        per[a]["cost_total"] = round(sum(r["cost"] for r in rs), 2)
        per[a]["turns_mean"] = round(statistics.mean(r["turns"] for r in rs), 1)
        per[a]["M5_reasons"] = sorted({r["M5_reason"] for r in rs if r["M5"] == 0})
    out["per_arm"] = per
    out["per_task"] = {a: {t: round(statistics.mean(r["composite"] for r in rows if r["arm"] == a and r["task"] == t), 2) for t in TASKS} for a in ARMS}
    # H4
    h4 = defaultdict(list)
    for r in rows:
        if r["task"] == "H4":
            h4[r["arm"]].append(r["H4_primary"] or 0)
    out["H4"] = {a: {"passes": sum(v), "n": len(v), "scores": v} for a, v in h4.items()}
    s, p, v = out["H4"].get("sentence", {}).get("passes", 0), out["H4"].get("plain", {}).get("passes", 0), out["H4"].get("v5", {}).get("passes", 0)
    out["H4"]["rule"] = "sentence is the evidenced piece" if (s >= v and s - p >= 3) else "descriptive only"
    # C6
    c6 = {}
    plain_words = statistics.mean(r["final_words"] for r in rows if r["task"] == "C6" and r["arm"] == "plain")
    for r in rows:
        if r["task"] == "C6" and r["arm"] == "v5":
            card = any(c.startswith(".finding-unknowns/") for c in r["changed"])
            c6[r["dir"]] = {"card": card, "skills": r["skills"], "M4": r["M4"], "words": r["final_words"],
                            "words_vs_plain": round(r["final_words"] / plain_words - 1, 2) if plain_words else None}
    out["C6"] = {"plain_words_mean": plain_words, "v5": c6}
    # hook: first tool call in session 2
    def first_s2_tool(d):
        meta = json.loads((S / "runs" / d / "meta.json").read_text())
        s2 = [t["turn"] for t in meta["turn_detail"] if t["session"] == 2]
        if not s2:
            return None
        for ln in open(S / "runs" / d / f"turn-{s2[0]:02d}.jsonl"):
            try:
                e = json.loads(ln)
            except ValueError:
                continue
            if e.get("type") == "assistant":
                for c in e["message"].get("content", []):
                    if c.get("type") == "tool_use":
                        return json.dumps(c.get("input"))[:200]
        return "no tool"
    hook = {}
    for arm in ("v5", "v5hook"):
        for t in ("T2", "T4"):
            for n in (1, 2, 3):
                d = f"{t}-{arm}-{n}"
                if (S / "runs" / d).exists():
                    ft = first_s2_tool(d)
                    hook[d] = {"first_tool_s2": ft, "reads_card": bool(ft and ".finding-unknowns" in ft),
                               "break": json.loads((S / "runs" / d / "meta.json").read_text()).get("break")}
    rc = {a: sum(1 for k, v in hook.items() if f"-{a}-" in k and v["reads_card"]) for a in ("v5", "v5hook")}
    out["hook"] = {"runs": hook, "reads_card": rc,
                   "ships": rc["v5hook"] >= 5 and rc["v5"] <= 3}
    # card integrity (v5 T runs): Brief text in first card commit vs final
    integ = {}
    for r in rows:
        if r["arm"] == "v5" and r["task"] in TASKS:
            ws = S / "runs" / r["dir"] / "ws"
            cards = sorted((ws / ".finding-unknowns/tasks").glob("*.md")) if (ws / ".finding-unknowns/tasks").exists() else []
            cards = [c for c in cards if not c.name.endswith(".deltas.md")]
            if not cards:
                integ[r["dir"]] = "no card"
                continue
            c = cards[0]
            rel = str(c.relative_to(ws))
            log = subprocess.run(["git", "log", "--format=%H", "--reverse", "--", rel], cwd=ws, capture_output=True, text=True).stdout.split()
            def brief(t):
                m = re.search(r"^## Brief.*?(?=^## )", t, re.S | re.M)
                return m.group(0).strip() if m else None
            if not log:
                integ[r["dir"]] = "card never committed"
                continue
            first = subprocess.run(["git", "show", f"{log[0]}:{rel}"], cwd=ws, capture_output=True, text=True).stdout
            b0, b1 = brief(first), brief(c.read_text())
            integ[r["dir"]] = "unchanged" if b0 and b0 == b1 else ("no Brief section" if not b0 else "Brief edited")
    out["card_integrity"] = integ
    out["grader_agreement"] = {k: v for k, v in agree.items()}
    (G / "results.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    (G / "rows.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    print(json.dumps({k: out[k] for k in ("primary", "per_arm", "per_task", "H4", "hook", "missing_grades")}, indent=1, ensure_ascii=False)[:6000])


if __name__ == "__main__":
    main()
