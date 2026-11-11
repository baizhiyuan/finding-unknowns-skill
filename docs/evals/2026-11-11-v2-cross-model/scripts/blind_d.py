"""Arm D packets (D vs A), appended without touching existing packets: P31-P40."""
import json, random, re, pathlib, importlib.util
R = pathlib.Path("/tmp/fu-eval2"); pre = (R / "PREREG.md").read_text(encoding="utf-8")
spec = importlib.util.spec_from_file_location("b2", R / "scripts/blind2.py")
src = (R / "scripts/blind2.py").read_text()
body_src = src[src.index("def body(d):"):src.index("for t in [")]
ns = {"re": re}; exec(body_src, ns); body = ns["body"]
key = json.load(open(R / "blind-key.json")); pmap = json.load(open(R / "packet-map.json"))
rng = random.Random(20261112); ids = [f"P{i}" for i in range(31, 41)]; rng.shuffle(ids); k = 0
for t in ["H1", "H2", "H3", "H4", "H5"]:
    sec = re.search(rf"(### {t} .*?)(?=\n### |\n## )", pre, re.S).group(1)
    for n in (1, 2):
        pid = f"{t}-sonnet-D{n}"; arms = ["A", "D"]; rng.shuffle(arms)
        orders = {"claude": arms, "gpt": arms[::-1]}; key[pid] = {g: {"X": o[0], "Y": o[1]} for g, o in orders.items()}
        new = ids[k]; k += 1; pmap[pid] = new
        for g, o in orders.items():
            parts = [f"# Packet {new}\n\n## Task, prompt and pre-registered traps\n\n", sec, "\n"]
            for lab, arm in zip("XY", o):
                final, changes, diff = body(R / "runs" / f"sonnet-{t}-{arm}-{n}")
                parts += [f"\n## Output {lab}\n\n### Final message\n\n", final, f"\n\n### Files changed (git status)\n```\n{changes}```\n", f"\n### Diff\n```diff\n{diff}\n```\n"]
            (R / f"grade-{g}" / f"{new}.md").write_text("".join(parts), encoding="utf-8")
json.dump(key, open(R / "blind-key.json", "w"), indent=1); json.dump(pmap, open(R / "packet-map.json", "w"), indent=1)
print({p: v for p, v in pmap.items() if "-D" in p})
