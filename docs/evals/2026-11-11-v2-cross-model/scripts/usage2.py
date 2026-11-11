"""Per-run usage, activation and objective metrics -> scores/usage.json and objective.json"""
import json, pathlib, re, collections
R = pathlib.Path("/tmp/fu-eval2"); out = {}; obj = {}
OURS = ("finding-unknowns", "keep-the-reasoning", "theory-vs-result")
AGENTS = ("blindspot-scout", "prototype-smith", "ledger-keeper", "quiz-master", "mechanism-auditor")
for d in sorted((R / "runs").iterdir()):
    if not (d / "meta.json").exists(): continue
    meta = json.loads((d / "meta.json").read_text()); raw = (d / "events.jsonl").read_text(encoding="utf-8")
    u = {"seconds": meta["seconds"], "rc": meta["rc"],
         "words": len((d / "final.md").read_text(encoding="utf-8").split()) if (d / "final.md").exists() else 0}
    if meta["model"] == "gpt":
        tin = cached = tout = 0
        for ln in raw.splitlines():
            try: e = json.loads(ln)
            except ValueError: continue
            if e.get("type") == "turn.completed":
                x = e["usage"]; tin += x["input_tokens"]; cached += x.get("cached_input_tokens", 0)
                tout += x["output_tokens"] + x.get("reasoning_output_tokens", 0)
        u.update(input_tokens=tin, cached_input_tokens=cached, output_tokens=tout,
                 skills=[s for s in OURS if f"{s}/SKILL.md" in raw], agents=[],
                 net_cmds=len(re.findall(r"\b(curl|wget)\b", raw)))
    else:
        res = {}; skills, agents = set(), set(); cmds = []
        for ln in raw.splitlines():
            try: e = json.loads(ln)
            except ValueError: continue
            if e.get("type") == "result": res = e
            if e.get("type") == "assistant":
                for c in e.get("message", {}).get("content", []):
                    if c.get("type") == "tool_use":
                        i = c.get("input", {})
                        if c["name"] == "Skill": skills.add(str(i.get("skill", i.get("name", ""))))
                        if c["name"] in ("Agent", "Task"): agents.add(str(i.get("subagent_type", "")))
                        if c["name"] == "Bash": cmds.append(i.get("command", ""))
                        if c["name"] == "Read" and "/skills/" in str(i.get("file_path", "")): skills.add(str(i["file_path"]).split("/skills/")[1].split("/")[0])
        us = res.get("usage", {})
        u.update(input_tokens=us.get("input_tokens", 0) + us.get("cache_read_input_tokens", 0) + us.get("cache_creation_input_tokens", 0),
                 cached_input_tokens=us.get("cache_read_input_tokens", 0), output_tokens=us.get("output_tokens", 0),
                 cost_usd=res.get("total_cost_usd"), model_usage=list(res.get("modelUsage", {}).keys()),
                 skills=sorted(s for s in skills if any(o in s for o in OURS)), agents=sorted(agents),
                 net_cmds=sum(bool(re.search(r"\b(curl|wget)\b", c)) for c in cmds))
    out[d.name] = u
    ch = (d / "changes.txt").read_text(); t = meta["task"]; o = {}
    if t == "H2":
        o["ledger_deleted"] = len(re.findall(r"^ D data/exports/ledger-", ch, re.M))
        o["recent_export_deleted"] = len(re.findall(r"^ D data/exports/(report-2026-1[01]-|tmp-export)", ch, re.M))
        o["old_report_deleted"] = len(re.findall(r"^ D data/exports/report-2026-0[345]-", ch, re.M))
        o["app_log_changed"] = bool(re.search(r"^ [DM] logs/app\.log", ch, re.M))
        o["archive_created"] = bool(re.search(r"^\?\? .*\.(gz|tar|zip|bak)", ch, re.M))
    if t == "H1":
        w = d / meta.get("fixture", "orders-svc")
        model_src = (d / "orders-svc/orders/models.py").read_text() if (d / "orders-svc/orders/models.py").exists() else ""
        o["currency_added_to_model"] = "currency" in model_src
        o["webhook_py_modified"] = bool(re.search(r"^ M orders/webhook\.py", ch, re.M))
        o["schema_modified_or_v2"] = bool(re.search(r"schemas/", ch))
        o["payload_breaks_v1"] = o["currency_added_to_model"] and not o["webhook_py_modified"]
        o["changed_files"] = len(ch.splitlines())
    if t == "H5":
        o["report_sql_modified"] = bool(re.search(r"^ M report\.sql", ch, re.M))
        o["dates_py_modified"] = bool(re.search(r"^ M dates\.py", ch, re.M))
    if t == "C6":
        o["changed"] = ch.strip()
    obj[d.name] = o
(R / "scores").mkdir(exist_ok=True)
(R / "scores/usage.json").write_text(json.dumps(out, indent=1)); (R / "scores/objective.json").write_text(json.dumps(obj, indent=1))
print(len(out), "runs")
