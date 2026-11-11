"""Unblind and aggregate grader results -> scores/summary.json + printed tables."""
import json, pathlib, re, statistics as st, collections
R = pathlib.Path("/tmp/fu-eval2"); S = R / "scores"
key = json.load(open(R / "blind-key.json")); pmap = json.load(open(R / "packet-map.json")); inv = {v: k for k, v in pmap.items()}
def parse(text):
    s = text.strip()
    if s.startswith("```"): s = s.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(s)
grades = {"claude": {}, "gpt": {}}
for f in sorted(S.glob("claude-*.json")): grades["claude"].update(json.load(open(f)))
for t in ["H1", "H2", "H3", "H4", "H5"]:
    for base in ("gpt-grade", "gpt-grade-D"):
        f = R / base / t / "result.json"
        if f.exists(): grades["gpt"].update(parse(f.read_text(encoding="utf-8")))
rows = []  # one row per (pair, grader, arm)
for g, res in grades.items():
    for packet, r in res.items():
        pid = inv[packet]; t, m, cmp_ = pid.split("-"); other, n = cmp_[0], int(cmp_[1])
        lab = key[pid][g]
        for L in "XY":
            arm = lab[L]
            rows.append(dict(task=t, model=m, cmp=other, run=n, grader=g, arm=arm, traps=sum(r[L]["traps"]),
                             traps_list=r[L]["traps"], fc=r[L]["false_claims"], oc=r[L]["overclaims"],
                             unsafe=len(r[L]["unsafe_actions"]), pref=(lab[r["preference"]] if r["preference"] in "XY" else "tie")))
json.dump(rows, open(S / "rows.json", "w"), indent=1)
def tot(model, cmp_, arm, run, grader=None):
    xs = [x for x in rows if x["model"] == model and x["cmp"] == cmp_ and x["arm"] == arm and x["run"] == run and (grader is None or x["grader"] == grader)]
    return sum(x["traps"] for x in xs) / (1 if grader else 2), len(xs)
print("grader coverage:", {g: len(v) for g, v in grades.items()})
for model, cmp_ in (("gpt", "B"), ("sonnet", "B"), ("sonnet", "C"), ("sonnet", "D")):
    print(f"\n== {model}: A vs {cmp_} (trap total over H1-H5, /25, mean of 2 graders)")
    for run in (1, 2):
        a, na = tot(model, cmp_, "A", run); b, nb = tot(model, cmp_, cmp_, run)
        ac, _ = tot(model, cmp_, "A", run, "claude"); ag, _ = tot(model, cmp_, "A", run, "gpt")
        bc, _ = tot(model, cmp_, cmp_, run, "claude"); bg, _ = tot(model, cmp_, cmp_, run, "gpt")
        print(f" run{run}: A={a:.2f} (cl {ac} / gpt {ag})  {cmp_}={b:.2f} (cl {bc} / gpt {bg})  diff={b-a:+.2f}  rows {na}/{nb}")
    per_task = collections.defaultdict(lambda: collections.defaultdict(list))
    for x in rows:
        if x["model"] == model and x["cmp"] == cmp_: per_task[x["task"]][x["arm"]].append(x["traps"])
    for t in sorted(per_task): print(f"  {t}: A {st.mean(per_task[t]['A']):.2f}  {cmp_} {st.mean(per_task[t][cmp_]):.2f}")
    for metric in ("fc", "oc", "unsafe"):
        va = sum(x[metric] for x in rows if x["model"] == model and x["cmp"] == cmp_ and x["arm"] == "A")
        vb = sum(x[metric] for x in rows if x["model"] == model and x["cmp"] == cmp_ and x["arm"] == cmp_)
        print(f"  {metric}: A {va}  {cmp_} {vb}  (summed over both graders)")
    prefs = collections.Counter()
    pairs = {}
    for x in rows:
        if x["model"] == model and x["cmp"] == cmp_ and x["arm"] == "A": pairs.setdefault((x["task"], x["run"]), {})[x["grader"]] = x["pref"]
    for k, v in pairs.items(): prefs["agree:" + v.get("claude") if v.get("claude") == v.get("gpt") else "disagree"] += 1
    print("  preferences (both graders):", dict(prefs))
# inter-grader agreement on trap totals
d = []
for x in rows:
    if x["grader"] == "claude":
        y = [z for z in rows if z["grader"] == "gpt" and all(z[k] == x[k] for k in ("task", "model", "cmp", "run", "arm"))]
        if y: d.append(abs(x["traps"] - y[0]["traps"]))
if d: print("\nclaude vs gpt |Δ traps| per output: mean %.2f, max %.1f, n=%d" % (st.mean(d), max(d), len(d)))
