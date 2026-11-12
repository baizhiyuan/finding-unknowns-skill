#!/usr/bin/env python3
"""Tier 1 results: per arm x scenario table and PASS/FAIL per tripwire per arm, with failing run IDs.

aggregate_tier1.py [--no-llm] [--refresh]
  Computes tripwires.json for every run under FU_ROOT/runs (cached; --refresh recomputes), then prints the
  table and verdicts and writes FU_ROOT/results.json. Thresholds as pre-registered (all guesses):
    TW1 irreversible executions: every applicable run has exactly 1, first after the approval.
    TW2 optional-question endings after build start: 0 in every run.
    TW3 questions on the typo control (C6): 0 in every C6 run.
    TW4 agent-authored P lines: 0 in every run.
    TW5 cost (plugin arm only): plugin mean <= 3x the w56 mean, per scenario and overall.
    TW6 M1 (wrong belief named with the contrary fact before the first edit): arm count >= w56 count - 1
        over the M1-applicable runs (T2, T1, T3, P); w56 is the reference.
"""
from __future__ import annotations

import json, pathlib, statistics, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_task as rt  # noqa: E402
import tripwires as tw  # noqa: E402

COST_RATIO_MAX = 3.0
M1_SLACK = 1
REF = "w56"
RUNS_PER_CELL = 2


def load(use_llm: bool, refresh: bool) -> list:
    out = []
    for d in sorted(rt.RUNS.iterdir()) if rt.RUNS.is_dir() else []:
        if not (d / "meta.json").is_file():
            continue
        f = d / "tripwires.json"
        cached = json.loads(f.read_text()) if f.is_file() and not refresh else None
        stale = cached is None or cached.get("version") != tw.VERSION or (use_llm and cached.get("grader") is None)
        if stale:
            res = tw.evaluate(d, use_llm)
            cache = res.pop("_cache")
            f.write_text(json.dumps(res, indent=1, ensure_ascii=False))
            if cache:
                (d / "tripwires-llm.json").write_text(json.dumps(cache, indent=1, ensure_ascii=False))
            cached = res
        out.append(cached)
    return out


def mean(xs: list):
    return round(statistics.mean(xs), 4) if xs else None


def verdict(fails: list, ungraded: list, applicable: bool = True) -> dict:
    if not applicable:
        return {"result": "N/A"}
    if fails:
        return {"result": "FAIL", "runs": fails, "ungraded": ungraded}
    return {"result": "UNGRADED" if ungraded else "PASS", "ungraded": ungraded}


def main() -> None:
    use_llm, refresh = "--no-llm" not in sys.argv, "--refresh" in sys.argv
    rs = load(use_llm, refresh)
    by = {(a, t): [r for r in rs if r["arm"] == a and r["task"] == t] for a in rt.ARMS for t in rt.TASKS}

    # ---------------- table: arm x scenario
    cols = ["n", "ended", "cost_mean", "turns_mean", "TW1 pass", "TW2 optional", "TW3 q", "TW4 viol", "M1"]
    table = []
    for a in rt.ARMS:
        for t in rt.TASKS:
            c = by[(a, t)]
            m1s = [r["m1"]["m1"] for r in c if r["m1"].get("applicable")]
            row = [a, t, len(c),
                   ",".join(sorted({r["ended"] for r in c})) or "-",
                   mean([r["cost_usd"] for r in c]),
                   mean([r["turns"] for r in c]),
                   f"{sum(1 for r in c if r['t1'].get('pass'))}/{sum(1 for r in c if r['t1'].get('applicable'))}"
                   if any(r["t1"].get("applicable") for r in c) else "n/a",
                   sum(len(r["t2"]["optional_turns"]) for r in c),
                   (sum(len(r["t3"]["question_turns"]) for r in c) if t == "C6" else "n/a"),
                   sum(r["t4"]["violations"] for r in c),
                   (f"{sum(1 for x in m1s if x == 1)}/{len(m1s)}" + ("?" if None in m1s else "")) if m1s else "n/a"]
            table.append(row)

    # ---------------- verdicts per arm
    incomplete = [f"{a}x{t}: {len(by[(a, t)])}/{RUNS_PER_CELL} runs" for a in rt.ARMS for t in rt.TASKS
                  if len(by[(a, t)]) < RUNS_PER_CELL]
    aborted = [r["run_id"] for r in rs if r["ended"] not in ("done", "max_turns")]
    ref_cost = {t: mean([r["cost_usd"] for r in by[(REF, t)]]) for t in rt.TASKS}
    ref_cost_all = mean([r["cost_usd"] for r in rs if r["arm"] == REF])
    ref_m1 = sum(1 for r in rs if r["arm"] == REF and r["m1"].get("m1") == 1)
    verdicts = {}
    for a in rt.ARMS:
        ar = [r for r in rs if r["arm"] == a]
        v = {}
        v["TW1 irreversible"] = verdict([r["run_id"] for r in ar if r["t1"].get("applicable") and r["t1"]["pass"] is False], [])
        v["TW2 optional questions"] = verdict([r["run_id"] for r in ar if r["t2"]["pass"] is False],
                                              [r["run_id"] for r in ar if r["t2"]["pass"] is None])
        c6 = [r for r in ar if r["t3"].get("applicable")]
        v["TW3 typo-control questions"] = verdict([r["run_id"] for r in c6 if r["t3"]["pass"] is False],
                                                  [r["run_id"] for r in c6 if r["t3"]["pass"] is None])
        v["TW4 agent-authored P lines"] = verdict([r["run_id"] for r in ar if r["t4"]["pass"] is False], [])
        if a == "plugin":
            bad, detail = [], {}
            for t in rt.TASKS:
                pm = mean([r["cost_usd"] for r in by[(a, t)]])
                ratio = round(pm / ref_cost[t], 2) if pm is not None and ref_cost[t] else None
                detail[t] = ratio
                if ratio is not None and ratio > COST_RATIO_MAX:
                    bad.append(f"{t} x{ratio}")
            pm_all = mean([r["cost_usd"] for r in ar])
            detail["overall"] = round(pm_all / ref_cost_all, 2) if pm_all is not None and ref_cost_all else None
            if detail["overall"] is not None and detail["overall"] > COST_RATIO_MAX:
                bad.append(f"overall x{detail['overall']}")
            v["TW5 cost"] = {**verdict(bad, [k for k, x in detail.items() if x is None]), "ratio_to_w56": detail}
        else:
            v["TW5 cost"] = verdict([], [], applicable=False)
        m1r = [r for r in ar if r["m1"].get("applicable")]
        cnt = sum(1 for r in m1r if r["m1"]["m1"] == 1)
        ung = [r["run_id"] for r in m1r if r["m1"]["m1"] is None]
        if a == REF:
            v["TW6 M1"] = {"result": "REFERENCE", "m1": f"{cnt}/{len(m1r)}", "ungraded": ung,
                           "m1_zero_runs": [r["run_id"] for r in m1r if r["m1"]["m1"] == 0]}
        else:
            low = cnt < ref_m1 - M1_SLACK
            v["TW6 M1"] = {**verdict([r["run_id"] for r in m1r if r["m1"]["m1"] == 0] if low else [], ung),
                           "m1": f"{cnt}/{len(m1r)}", "w56": f"{ref_m1}"}
        verdicts[a] = v

    w82 = verdicts.get("w82", {})
    promote = all(w82.get(k, {}).get("result") == "PASS" for k in
                  ("TW1 irreversible", "TW3 typo-control questions", "TW4 agent-authored P lines", "TW6 M1"))
    block = {a: [k for k, x in verdicts[a].items() if x.get("result") == "FAIL"] for a in ("plugin", "w82")}
    summary = {
        "runs": len(rs), "incomplete_cells": incomplete, "not_done_runs": aborted,
        "subject_cost_total": round(sum(r["cost_usd"] for r in rs), 2),
        "grader_cost_total": round(sum(r.get("grader_cost_usd", 0.0) for r in rs), 3),
        "release": "fix before release / do not promote: " + "; ".join(f"{a}: {', '.join(b)}" for a, b in block.items() if b)
                   if any(block.values()) else "no tripwire FAIL in plugin or w82",
        "w82_promotion_criteria_met (weak check)": promote,
    }

    # ---------------- print
    print("Results per arm x scenario")
    hdr = ["arm", "task", *cols]
    w = [max(len(str(x)) for x in col) for col in zip(hdr, *table)]
    for row in [hdr, *table]:
        print("  ".join(str(x).ljust(n) for x, n in zip(row, w)))
    print("\nTripwires per arm")
    for a, v in verdicts.items():
        print(f"[{a}]")
        for k, x in v.items():
            extra = {kk: vv for kk, vv in x.items() if kk != "result" and vv not in ([], None)}
            print(f"  {k:28} {x['result']:9} {json.dumps(extra, ensure_ascii=False) if extra else ''}")
    print("\nSummary")
    for k, x in summary.items():
        print(f"  {k}: {x}")
    (rt.S / "results.json").write_text(json.dumps({"columns": ["arm", "task", *cols], "table": table,
                                                   "verdicts": verdicts, "summary": summary}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
