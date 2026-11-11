import json, pathlib, re
R = pathlib.Path("/tmp/fu-eval3"); out = {}
OURS = ("finding-unknowns", "keep-the-reasoning", "theory-vs-result")
REF = ("add-model-field", "disk-cleanup", "ab-test-writeup", "pr-merge-review", "bug-fix-date")
for d in sorted((R / "runs").iterdir()):
    if not (d / "meta.json").exists(): continue
    meta = json.loads((d / "meta.json").read_text()); res = {}; skills = []; agents = []
    for ln in (d / "events.jsonl").read_text(encoding="utf-8").splitlines():
        try: e = json.loads(ln)
        except ValueError: continue
        if e.get("type") == "result": res = e
        if e.get("type") == "assistant":
            for c in e["message"].get("content", []):
                if c.get("type") == "tool_use" and c["name"] == "Skill": skills.append(str(c["input"].get("skill", "")))
                if c.get("type") == "tool_use" and c["name"] in ("Agent", "Task"): agents.append(str(c["input"].get("subagent_type", "")))
    us = res.get("usage", {})
    out[d.name] = dict(task=meta["task"], arm=meta["arm"], run=meta["run"], rc=meta["rc"], seconds=meta["seconds"],
        input_tokens=us.get("input_tokens", 0) + us.get("cache_read_input_tokens", 0) + us.get("cache_creation_input_tokens", 0),
        output_tokens=us.get("output_tokens", 0), cost_usd=res.get("total_cost_usd") or 0,
        words=len((d / "final.md").read_text(encoding="utf-8").split()),
        ours=[s for s in skills if any(o in s for o in OURS)], ref=[s for s in skills if any(r in s for r in REF)], agents=agents,
        changes=(d / "changes.txt").read_text().strip())
(R / "scores" / "usage.json").write_text(json.dumps(out, indent=1)); print(len(out), "runs")
