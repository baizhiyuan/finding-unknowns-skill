"""Build grading packets. Each (task, model, run) A/B pair -> one Claude packet (random X/Y)
and one GPT packet (reverse order). Key in blind-key.json."""
import json, random, re, pathlib
R = pathlib.Path("/tmp/fu-eval2"); pre = (R / "PREREG.md").read_text(encoding="utf-8")
rng = random.Random(20261111); key = {}
for g in ("claude", "gpt"): (R / f"grade-{g}").mkdir(exist_ok=True)
def body(d):
    final = (d / "final.md").read_text(encoding="utf-8") if (d / "final.md").exists() else "(no output)"
    final = re.sub(r"/tmp/fu-eval2/runs/[a-z]+-[A-Z]\d-[A-D]-\d/", "<repo>/", final)
    changes = (d / "changes.txt").read_text()
    diff = (d / "diff.txt").read_text(errors="replace").splitlines()
    if len(diff) > 300: diff = diff[:300] + [f"... [diff truncated: {len(diff)-300} more lines]"]
    diff = re.sub(r"/tmp/fu-eval2/runs/[a-z]+-[A-Z]\d-[A-D]-\d/", "<repo>/", "\n".join(diff))
    return final, changes, diff
for t in ["H1", "H2", "H3", "H4", "H5"]:
    sec = re.search(rf"(### {t} .*?)(?=\n### |\n## )", pre, re.S).group(1)
    for m, other in (("gpt", "B"), ("sonnet", "B"), ("sonnet", "C")):
        for n in (1, 2):
            pid = f"{t}-{m}-{other}{n}"
            arms = ["A", other]; rng.shuffle(arms)
            orders = {"claude": arms, "gpt": arms[::-1]}
            key[pid] = {g: {"X": o[0], "Y": o[1]} for g, o in orders.items()}
            for g, o in orders.items():
                parts = [f"# Packet {pid}\n\n## Task, prompt and pre-registered traps\n\n", sec, "\n"]
                for lab, arm in zip("XY", o):
                    final, changes, diff = body(R / "runs" / f"{m}-{t}-{arm}-{n}")
                    parts += [f"\n## Output {lab}\n\n### Final message\n\n", final,
                              f"\n\n### Files changed (git status)\n```\n{changes}```\n",
                              f"\n### Diff\n```diff\n{diff}\n```\n"]
                (R / f"grade-{g}" / f"{pid}.md").write_text("".join(parts), encoding="utf-8")
(R / "blind-key.json").write_text(json.dumps(key, indent=1))
print(len(key), "pairs")
