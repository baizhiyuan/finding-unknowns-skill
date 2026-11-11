"""v3 packets: (task, run, other in C/E) vs A -> neutral ids; claude order random, gpt reversed."""
import json, random, re, pathlib
R = pathlib.Path("/tmp/fu-eval3"); pre = pathlib.Path("/tmp/fu-eval2/PREREG.md").read_text(encoding="utf-8")
RED = re.compile(r"/tmp/fu-eval3/runs/[A-Z]\d-[ACER]-\d/")
def body(d):
    final = (d / "final.md").read_text(encoding="utf-8") if (d / "final.md").exists() else "(no output)"
    diff = (d / "diff.txt").read_text(errors="replace").splitlines()
    if len(diff) > 300: diff = diff[:300] + [f"... [diff truncated: {len(diff)-300} more lines]"]
    return RED.sub("<repo>/", final), (d / "changes.txt").read_text(), RED.sub("<repo>/", "\n".join(diff))
rng = random.Random(20261113); pairs = [(t, n, o) for t in ["H1","H2","H3","H4","H5"] for n in (1,2,3) for o in "CE"]
ids = [f"P{i:02d}" for i in range(1, len(pairs) + 1)]; rng.shuffle(ids)
key, pmap = {}, {}
for (t, n, o), pid in zip(pairs, ids):
    name = f"{t}-{o}{n}"; pmap[name] = pid; arms = ["A", o]; rng.shuffle(arms)
    orders = {"claude": arms, "gpt": arms[::-1]}; key[name] = {g: {"X": a[0], "Y": a[1]} for g, a in orders.items()}
    sec = re.search(rf"(### {t} .*?)(?=\n### |\n## )", pre, re.S).group(1)
    fix = {"H1":"orders-svc","H2":"ops-box","H3":"ab-ranker","H4":"billing-lib","H5":"nightly-report"}[t]
    for g, a in orders.items():
        G = R / f"grade-{g}" / t; (G / "packets").mkdir(parents=True, exist_ok=True)
        parts = [f"# Packet {pid}\n\n## Task, prompt and pre-registered traps\n\n", sec, "\n"]
        for lab, arm in zip("XY", a):
            final, changes, diff = body(R / "runs" / f"{t}-{arm}-{n}")
            parts += [f"\n## Output {lab}\n\n### Final message\n\n", final, f"\n\n### Files changed (git status)\n```\n{changes}```\n", f"\n### Diff\n```diff\n{diff}\n```\n"]
        (G / "packets" / f"{pid}.md").write_text("".join(parts), encoding="utf-8")
json.dump(key, open(R / "blind-key.json", "w"), indent=1); json.dump(pmap, open(R / "packet-map.json", "w"), indent=1)
print(len(pmap), "pairs")
