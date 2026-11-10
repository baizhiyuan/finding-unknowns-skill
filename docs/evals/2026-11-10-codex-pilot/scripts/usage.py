"""Per-run usage from runs/*/events.jsonl: tokens (incl. cached), time, words, skills read, tool items."""
import collections, json, pathlib
R = pathlib.Path("/tmp/fu-eval/runs"); out = {}
SKILLS = ("finding-unknowns", "keep-the-reasoning", "theory-vs-result")
for d in sorted(R.iterdir()):
    tin = cached = tout = 0; items = collections.Counter(); raw = (d / "events.jsonl").read_text(encoding="utf-8")
    for ln in raw.splitlines():
        try: e = json.loads(ln)
        except ValueError: continue
        if e.get("type") == "turn.completed":
            u = e["usage"]; tin += u["input_tokens"]; cached += u.get("cached_input_tokens", 0)
            tout += u["output_tokens"] + u.get("reasoning_output_tokens", 0)
        if e.get("type") == "item.completed":
            items[e["item"].get("type")] += 1
    out[d.name] = {"input_tokens": tin, "cached_input_tokens": cached, "output_tokens": tout,
                   "seconds": json.loads((d / "meta.json").read_text())["seconds"],
                   "words": len((d / "final.md").read_text(encoding="utf-8").split()),
                   "skills_read": [s for s in SKILLS if f"{s}/SKILL.md" in raw],
                   "items": dict(items)}
print(json.dumps(out, indent=1))
