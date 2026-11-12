#!/usr/bin/env python3
"""Recompute subject cost per run from archived meta.json files (erratum of 2026-11-12).

The runners summed each turn's `total_cost_usd` from `claude -p --resume`. That value is
cumulative within a Claude Code session, so the sum counts early turns again on every later
turn. The true cost of a run is the sum, over its sessions, of the last turn's value.
(The per-call cost, `model_usage_since_last_result.costUSD` in the raw event logs, gives the
same total; the raw logs are not committed.)

usage: recompute_costs.py [RUNS_DIR] [--ref ARM] [--raw RAW_RUNS_DIR]
  RUNS_DIR  directory of run folders with meta.json (default: ../runs next to this script)
  --ref     print each arm's corrected mean cost as a multiple of this arm's, per task and overall
            (arms without build-task runs, such as the H4-only `sentence` arm, are skipped)
  --raw     directory of the same runs with turn-NN.jsonl event logs: also recompute tokens from
            model_usage_since_last_result (meta.json keeps only the main thread's `usage` of the
            last result event in a turn, which misses subagent calls)

Build tasks are every task except the controls C6 and H4.
"""
import argparse, json, pathlib, statistics
from collections import defaultdict

CONTROLS = {"C6", "H4"}


def run_costs(meta: dict) -> tuple:
    last, prev, monotonic = {}, {}, True
    for t in meta["turn_detail"]:
        s = t.get("session", 1)
        if t["cost"] < prev.get(s, 0.0) - 1e-9:
            monotonic = False
        prev[s] = last[s] = t["cost"]
    return meta["cost_usd"], sum(t["cost"] for t in meta["turn_detail"]), sum(last.values()), monotonic


def meta_tokens(meta: dict) -> tuple:
    u = [t.get("usage") or {} for t in meta["turn_detail"]]
    tin = sum(x.get("input_tokens", 0) + x.get("cache_creation_input_tokens", 0) + x.get("cache_read_input_tokens", 0) for x in u)
    return tin, sum(x.get("output_tokens", 0) for x in u)


def raw_tokens(run_dir: pathlib.Path, meta: dict) -> tuple:
    tin = tout = 0
    for t in meta["turn_detail"]:
        for line in (run_dir / f"turn-{t['turn']:02d}.jsonl").read_text().splitlines():
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("type") == "result":
                for v in (e.get("model_usage_since_last_result") or {}).values():
                    tin += v.get("inputTokens", 0) + v.get("cacheReadInputTokens", 0) + v.get("cacheCreationInputTokens", 0)
                    tout += v.get("outputTokens", 0)
    return tin, tout


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="?", default=str(pathlib.Path(__file__).resolve().parent.parent / "runs"))
    ap.add_argument("--ref")
    ap.add_argument("--raw")
    a = ap.parse_args()
    rows = []
    for f in sorted(pathlib.Path(a.runs).glob("*/meta.json")):
        meta = json.loads(f.read_text())
        reported, summed, true, mono = run_costs(meta)
        if abs(reported - summed) > 1e-3 or not mono:
            print(f"WARN {f.parent.name}: reported {reported} vs summed {summed:.4f}, monotonic per session: {mono}")
        tok = meta_tokens(meta)
        raw = raw_tokens(pathlib.Path(a.raw) / f.parent.name, meta) if a.raw else None
        rows.append(dict(run=f.parent.name, arm=meta["arm"], task=meta["task"], reported=reported, true=true, tok=tok, raw=raw))
    mean = lambda xs: statistics.mean(xs) if xs else float("nan")  # noqa: E731
    by = defaultdict(list)
    for r in rows:
        by[(r["arm"], r["task"])].append(r)
    arms = sorted({r["arm"] for r in rows})
    tasks = sorted({r["task"] for r in rows}, key=lambda t: (t in CONTROLS, t))
    print(f"{len(rows)} runs\n\nPer arm x task, mean USD per run (reported -> corrected)")
    for arm in arms:
        cells = [f"{t} {mean([r['reported'] for r in by[(arm, t)]]):.3f}->{mean([r['true'] for r in by[(arm, t)]]):.3f}"
                 for t in tasks if by[(arm, t)]]
        print(f"  {arm:9s} " + "  ".join(cells))
    print("\nPer arm, build tasks (controls excluded)")
    build = {arm: [r for r in rows if r["arm"] == arm and r["task"] not in CONTROLS] for arm in arms}
    for arm, rs in build.items():
        if not rs:
            continue
        line = (f"  {arm:9s} n={len(rs):2d}  mean {mean([r['reported'] for r in rs]):.3f} -> {mean([r['true'] for r in rs]):.3f}"
                f"  total {sum(r['reported'] for r in rs):.2f} -> {sum(r['true'] for r in rs):.2f}"
                f"  tokens in/out (meta usage) {mean([r['tok'][0] for r in rs]) / 1e3:.0f}k/{mean([r['tok'][1] for r in rs]) / 1e3:.1f}k")
        if a.raw:
            line += f"  (event logs) {mean([r['raw'][0] for r in rs]) / 1e3:.0f}k/{mean([r['raw'][1] for r in rs]) / 1e3:.1f}k"
        print(line)
    print(f"\nAll runs: total {sum(r['reported'] for r in rows):.2f} -> {sum(r['true'] for r in rows):.2f}")
    print("\nRatios of corrected build-task means (row / column)")
    bm = {arm: mean([r["true"] for r in rs]) for arm, rs in build.items() if rs}
    print("  " + " " * 9 + "".join(f"{c:>9s}" for c in bm))
    for x in bm:
        print(f"  {x:9s}" + "".join(f"{bm[x] / bm[c]:9.2f}" for c in bm))
    if a.ref and a.ref not in bm:
        print(f"\n--ref {a.ref}: no build-task runs for this arm; ratios skipped")
    elif a.ref:
        print(f"\nCorrected mean as a multiple of {a.ref}, per task / all runs / build tasks")
        ref_all = mean([r["true"] for r in rows if r["arm"] == a.ref])
        for arm in arms:
            if arm == a.ref or arm not in bm:
                continue
            cells = [f"{t} {mean([r['true'] for r in by[(arm, t)]]) / mean([r['true'] for r in by[(a.ref, t)]]):.2f}"
                     for t in tasks if by[(arm, t)] and by[(a.ref, t)]]
            overall = mean([r["true"] for r in rows if r["arm"] == arm]) / ref_all
            print(f"  {arm:9s} " + "  ".join(cells) + f"  all {overall:.2f}  build {bm[arm] / bm[a.ref]:.2f}")


if __name__ == "__main__":
    main()
