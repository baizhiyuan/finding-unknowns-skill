"""Build the two isolated CODEX_HOME directories used by the pilot.

Copies only the model/provider keys from ~/.codex/config.toml (no AGENTS.md, no hooks,
no memories, no shell environment, no third-party skills), links auth.json, and adds
this repo's three skills to arm B. Prints key names only, never values.
Usage: python3 make_homes.py <repo-root> [<out-dir>=/tmp/fu-eval/homes]
"""
import os, re, shutil, sys, pathlib

repo = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "/tmp/fu-eval/homes")
src = (pathlib.Path.home() / ".codex/config.toml").read_text(encoding="utf-8").splitlines()
TOP = {"model_provider", "model", "model_reasoning_effort", "disable_response_storage",
       "openai_base_url", "service_tier", "model_context_window"}
top, provider, section = [], [], None
for ln in src:
    m = re.match(r"^\[(.+)\]\s*$", ln)
    if m:
        section = m.group(1)
        continue
    if section is None and ln.split("=", 1)[0].strip() in TOP:
        top.append(ln)
    elif section is not None and section.startswith("model_providers.") and ln.strip():
        provider.append((section, ln))
cfg = top + ["", "[features]", "memories = false", "hooks = false"]
for sec in dict.fromkeys(s for s, _ in provider):
    cfg += ["", f"[{sec}]"] + [ln for s, ln in provider if s == sec]
for arm in ("A", "B"):
    home = out / f"base-{arm}"
    home.mkdir(parents=True, exist_ok=True)
    (home / "config.toml").write_text("\n".join(cfg) + "\n", encoding="utf-8")
    os.chmod(home / "config.toml", 0o600)
    link = home / "auth.json"
    if not link.exists():
        link.symlink_to(pathlib.Path.home() / ".codex/auth.json")
skills = out / "base-B" / "skills"
for name in ("finding-unknowns", "keep-the-reasoning", "theory-vs-result"):
    shutil.rmtree(skills / name, ignore_errors=True)
    shutil.copytree(repo / "skills" / name, skills / name)
print("keys:", [ln.split("=", 1)[0].strip() for ln in cfg if "=" in ln])
