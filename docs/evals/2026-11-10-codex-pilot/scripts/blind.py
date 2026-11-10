"""Build blinded grading packets: grade/T?.md with X/Y outputs; key in blind-key.json."""
import json, random, re, pathlib
R = pathlib.Path("/tmp/fu-eval")
pre = (R / "PREREG.md").read_text(encoding="utf-8")
rng = random.Random(20261110)
key, out = {}, R / "grade"; out.mkdir(exist_ok=True)
for t in ["T1", "T2", "T3", "T4", "T5", "T6"]:
    sec = re.search(rf"(### {t} .*?)(?=\n### |\n## )", pre, re.S).group(1)
    arms = ["A", "B"]; rng.shuffle(arms)
    key[t] = {"X": arms[0], "Y": arms[1]}
    parts = [f"# Grading packet {t}\n", "## Task, prompt and pre-registered traps\n", sec, "\n"]
    for label, arm in zip("XY", arms):
        d = R / "runs" / f"{t}-{arm}"
        final = (d / "final.md").read_text(encoding="utf-8") if (d / "final.md").exists() else "(no output)"
        final = re.sub(r"/tmp/fu-eval/runs/T\d-[AB]/", "<repo>/", final)
        parts += [f"\n## Output {label}\n\n", final, "\n"]
        if t == "T6":
            parts += [f"\n### Files changed by output {label}\n```\n", (d / "changes.txt").read_text(), "```\n",
                      "```diff\n", (d / "diff.txt").read_text(), "```\n"]
    (out / f"{t}.md").write_text("".join(parts), encoding="utf-8")
(R / "blind-key.json").write_text(json.dumps(key, indent=1))
print("packets:", sorted(p.name for p in out.iterdir()))
