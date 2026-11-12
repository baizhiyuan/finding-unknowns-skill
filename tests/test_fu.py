"""Tier 0 tests for scripts/fu.py (stdlib unittest; also runs under pytest).

    python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FU = REPO / "scripts" / "fu.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
VALID = FIXTURES / "valid" / ".finding-unknowns"
QWEN = FIXTURES / "qwen-card" / ".finding-unknowns"
IRR = "python publish.py build/quotes.json"


def run(args, cwd, stdin=None, env=None):
    full_env = dict(os.environ, **(env or {}))
    return subprocess.run([sys.executable, str(FU), *args], cwd=str(cwd), input=stdin,
                          capture_output=True, text=True, env=full_env, timeout=60)


def rules(output: str, level: str) -> set:
    return set(re.findall(r"^%s \S+:\d+ (\S+):" % level, output, flags=re.M))


class Workspace(unittest.TestCase):
    """Each test gets a temp project holding a copy of the valid fixture."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="fu-test-"))
        shutil.copytree(VALID, self.tmp / ".finding-unknowns")
        self.fu = self.tmp / ".finding-unknowns"
        self.card = self.fu / "tasks" / "quote-export.md"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def edit(self, old: str, new: str, path: Path = None):
        path = path or self.card
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def lint(self, slug="quote-export", *extra):
        return run(["lint", slug, *extra], self.tmp)


# ---------------------------------------------------------------------------- lint

class LintFixtures(unittest.TestCase):
    def test_valid_cards_pass(self):
        r = run(["--root", str(VALID.parent), "lint", "quote-export"], REPO)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("lint: 0 FAIL", r.stdout)
        r = run(["--root", str(VALID.parent), "lint", "search-export"], REPO)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("lint: 0 FAIL, 0 WARN", r.stdout)

    def test_qwen_pilot_card_fails_with_expected_rules(self):
        r = run(["--root", str(QWEN.parent), "lint", "cheapest-service"], REPO)
        self.assertEqual(r.returncode, 1)
        fails = rules(r.stdout, "FAIL")
        for rule in ("header", "needs-you-once", "id-reserved", "prediction-form", "delta-location",
                     "delta-form", "contract-form", "brief-form", "sections", "debrief-form"):
            self.assertIn(rule, fails, r.stdout[-2000:])
        warns = rules(r.stdout, "WARN")
        for rule in ("delta-time", "model-changes-place", "live-length"):
            self.assertIn(rule, warns)

    def test_raw_template_fails_on_placeholders(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            text = (REPO / "commands" / "fu-brief.md").read_text(encoding="utf-8")
            tpl = re.search(r"```markdown\n(.*?)```", text, flags=re.S).group(1).replace("{slug}", "tpl", 1)
            (tmp / ".finding-unknowns" / "tasks").mkdir(parents=True)
            (tmp / ".finding-unknowns" / "tasks" / "tpl.md").write_text(tpl, encoding="utf-8")
            r = run(["lint", "tpl"], tmp)
            self.assertEqual(r.returncode, 1)
            self.assertIn("placeholder", rules(r.stdout, "FAIL"))
            self.assertIn("{exact command}", r.stdout)
        finally:
            shutil.rmtree(tmp)


class NineSchemaProblems(Workspace):
    """The nine problems found in the real pilot card (round-2 design §7)."""

    def test_1_needs_you_twice(self):
        self.edit("Not checked:\n", "Needs you: the rate card\nNot checked:\n")
        r = self.lint()
        self.assertIn("needs-you-once", rules(r.stdout, "FAIL"))

    def test_2_ids_name_premises(self):
        self.edit("  - add one remote-zone service because parcel 3 has no service in the table",
                  "  - add one remote-zone service because premise A3 fired")
        r = self.lint()
        self.assertIn("id-reserved", rules(r.stdout, "FAIL"))
        self.assertIn("A3 is cited but not a Brief prediction", r.stdout)

    def test_2b_p_belongs_to_the_person(self):
        text = self.card.read_text(encoding="utf-8").replace('P2 (you · low) "every', 'P2 (agent · low) "every')
        self.card.write_text(text, encoding="utf-8")
        self.assertIn("id-reserved", rules(self.lint().stdout, "FAIL"))

    def test_3_two_prediction_syntaxes(self):
        self.edit('A2 (agent · medium) "parcel 3\'s cheapest is Overnight at 8.00"\n',
                  "A2 parcel 3's cheapest is Overnight at 8.00 · falsifier: not 8.00\n")
        self.assertIn("prediction-form", rules(self.lint().stdout, "FAIL"))

    def test_4_amendment_without_anchor(self):
        self.edit("M1 2026-11-12 09:40 · after D2 · confirmed:", "M1 2026-11-12 09:40 · confirmed:")
        r = self.lint()
        self.assertIn("amend-anchor", rules(r.stdout, "WARN"))
        self.assertEqual(r.returncode, 0)

    def test_5_deltas_written_in_the_card(self):
        self.edit("Latest: D3\n", "Latest: D3\nD3 2026-11-12 10:05 surprise: no rate card → docs/rates.md\n")
        self.assertIn("delta-location", rules(self.lint().stdout, "FAIL"))

    def test_6_two_model_changes_blocks(self):
        self.edit("## Open\n", "## Open\n- You expected the tie-break to matter → it did not, because no tie exists [confirmed]\n")
        r = self.lint()
        self.assertIn("model-changes-place", rules(r.stdout, "WARN"))

    def test_7_dates_without_times(self):
        deltas = self.fu / "tasks" / "quote-export.deltas.md"
        self.edit("D3 2026-11-12 10:05 surprise", "D3 2026-11-12 surprise", deltas)
        r = self.lint()
        self.assertIn("delta-time", rules(r.stdout, "WARN"))
        self.assertEqual(r.returncode, 0)

    def test_8_open_lists_settled_facts_is_not_lintable(self):
        before = self.lint().stdout
        self.edit("- the remote-zone rate is synthetic until the carrier card arrives",
                  "- the bulky parcel costs 4.00 (settled)")
        r = self.lint()
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, before)  # no rule can tell a settled fact from an open one

    def test_9_confidence_wording(self):
        self.edit('P2 (you · low) "every', 'P2 (you · fairly sure) "every')
        self.assertIn("confidence", rules(self.lint().stdout, "FAIL"))

    def test_9b_agent_confidence_has_no_no_idea(self):
        text = self.card.read_text(encoding="utf-8").replace("A1 (agent · high)", "A1 (agent · no idea)")
        self.card.write_text(text, encoding="utf-8")
        self.assertIn("confidence", rules(self.lint().stdout, "FAIL"))


class LintRules(Workspace):
    def test_contract_check_must_not_rerun_the_irreversible_command(self):
        self.edit("  - check: `python publish.py --dry-run build/quotes.json` exits 0",
                  "  - check: `python3 ./publish.py  build/quotes.json` twice; the second raises")
        r = self.lint()
        self.assertIn("irreversible-check", rules(r.stdout, "FAIL"))

    def test_post_check_must_not_rerun_the_irreversible_command(self):
        self.edit("  - post-check: `sha256sum build/quotes.json` equals the receipt's sha256",
                  "  - post-check: `python publish.py build/quotes.json` raises FileExistsError")
        self.assertIn("irreversible-check", rules(self.lint().stdout, "FAIL"))

    def test_dry_run_check_is_allowed(self):
        self.assertNotIn("irreversible-check", self.lint().stdout)

    def test_irreversible_lane_needs_post_check(self):
        self.edit("  - post-check: `sha256sum build/quotes.json` equals the receipt's sha256\n", "")
        self.assertIn("contract-form", rules(self.lint().stdout, "FAIL"))

    def test_escaped_quote_in_person_claim_parses(self):
        self.assertIn('\\"compact\\"', self.card.read_text(encoding="utf-8"))
        self.assertEqual(self.lint().returncode, 0)

    def test_unescaped_inner_quote_fails(self):
        text = self.card.read_text(encoding="utf-8").replace('\\"compact\\"', '"compact"')
        self.card.write_text(text, encoding="utf-8")
        self.assertIn("prediction-form", rules(self.lint().stdout, "FAIL"))

    def test_p_none_given(self):
        text = self.card.read_text(encoding="utf-8")
        brief_p = re.search(r'^P1 \(you.*?\n(?=A1 )', text, flags=re.S | re.M).group(0)
        text = text.replace(brief_p, "P: none given\n", 1)
        debrief_p = re.search(r'^P1 \(you.*?\n(?=A1 )', text, flags=re.S | re.M).group(0)
        text = text.replace(debrief_p, "P: none given\n", 1)
        text = text.replace("(P1, A1)", "(A1)").replace("(P2)", "none")
        self.card.write_text(text, encoding="utf-8")
        r = self.lint()
        self.assertEqual(r.returncode, 0, r.stdout)
        r = run(["log", "quote-export"], self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertNotIn("· you ·", r.stdout)

    def test_debrief_must_grade_every_prediction(self):
        text = self.card.read_text(encoding="utf-8")
        row = re.search(r'^A2 \(agent.*?\[untested\]\n', text.split("## Debrief")[1], flags=re.S | re.M).group(0)
        text = text.replace(row, "").replace("  - stops at: the Overnight price has no source (A2)", "  - stops at: the Overnight price")
        self.card.write_text(text, encoding="utf-8")
        self.assertIn("debrief-coverage", rules(self.lint().stdout, "FAIL"))

    def test_debrief_id_line_must_match_the_brief(self):
        text = self.card.read_text(encoding="utf-8")
        head, debrief = text.split("## Debrief", 1)
        debrief = debrief.replace('A1 (agent · high) "a second publish raises FileExistsError"',
                                  'A1 (agent · high) "a second publish raises an error"')
        self.card.write_text(head + "## Debrief" + debrief, encoding="utf-8")
        self.assertIn("debrief-coverage", rules(self.lint().stdout, "FAIL"))

    def test_verdict_closed_set_and_tier(self):
        self.edit("  - consistent?: partly", "  - consistent?: mostly")
        self.assertIn("verdict", rules(self.lint().stdout, "FAIL"))

    def test_mechanism_needs_tier(self):
        self.edit("  - mechanism: the receipt is opened in \"x\" mode [verified]", "  - mechanism: the receipt is opened in \"x\" mode")
        self.assertIn("verdict", rules(self.lint().stdout, "FAIL"))

    def test_not_checked_needs_an_item(self):
        self.edit("  - the carrier's actual remote-zone rate card\n", "")
        self.assertIn("not-checked", rules(self.lint().stdout, "FAIL"))

    def test_bottom_line_every_id_once_in_its_place(self):
        self.edit("  - did not hold: coverage needed an invented service (P2)", "  - did not hold: none")
        r = self.lint()
        self.assertIn("bottom-line", rules(r.stdout, "FAIL"))
        self.assertIn("P2 must appear exactly once", r.stdout)

    def test_bottom_line_cant_tell_goes_under_stops_at(self):
        self.edit("  - holds: scale billing and the one-shot publish (P1, A1)", "  - holds: scale billing and the one-shot publish (P1, A1, A2)")
        self.edit("  - stops at: the Overnight price has no source (A2)", "  - stops at: the Overnight price has no source")
        r = self.lint()
        self.assertIn("A2 is can't tell and belongs under `stops at`", r.stdout)

    def test_superlative_and_verb_tier_warn(self):
        self.edit("  - holds: scale billing and the one-shot publish (P1, A1)", "  - holds: everything works (P1, A1)")
        self.edit("  - mechanism: parcel 3 is covered only by a service the agent added [inferred]",
                  "  - mechanism: the added service causes the coverage [inferred]")
        r = self.lint()
        self.assertIn("superlative", rules(r.stdout, "WARN"))
        self.assertIn("verb-tier", rules(r.stdout, "WARN"))

    def test_strict_caps(self):
        r = self.lint("quote-export", "--strict")
        self.assertIn("strict-caps", rules(r.stdout, "FAIL"))
        self.assertIn("live-length", rules(r.stdout, "FAIL"))

    def test_strict_field_cap_exempts_person_words_and_commands(self):
        r = run(["lint", "search-export", "--strict"], self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout)
        long_words = " ".join(["word"] * 30)
        self.edit('P1 (you · high) "前缀搜索会比全文搜索快"', 'P1 (you · high) "%s"' % long_words, self.fu / "tasks" / "search-export.md")
        self.edit("  - check: `python -m json.tool build/search.json` exits 0",
                  "  - check: `python -m json.tool build/search.json %s` exits 0" % long_words, self.fu / "tasks" / "search-export.md")
        r = run(["lint", "search-export", "--strict"], self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.edit("  - falsifier: the prefix query is slower on the 10k fixture",
                  "  - falsifier: %s" % long_words, self.fu / "tasks" / "search-export.md")
        r = run(["lint", "search-export", "--strict"], self.tmp)
        self.assertIn("strict-caps", rules(r.stdout, "FAIL"))

    def test_strict_extra_person_predictions_warn_only(self):
        card = self.fu / "tasks" / "search-export.md"
        extra = "".join('P%d (you · low) "claim %d"\n  - falsifier: f\n  - should not change: s\n' % (n, n) for n in (2, 3, 4))
        self.edit("A1 (agent · medium)", extra + "A1 (agent · medium)", card)
        r = run(["lint", "search-export", "--strict"], self.tmp)
        self.assertIn("strict-caps", rules(r.stdout, "WARN"))
        self.assertNotIn("strict-caps", rules(r.stdout, "FAIL"))

    def test_sections_order_and_rollup(self):
        self.edit("Rollup:\n  - D1–D2: test updated and Overnight added; both logged with cost if wrong\n",
                  "Rollup:\n  - a\n  - b\n  - c\n  - d\n")
        self.assertIn("rollup", rules(self.lint().stdout, "FAIL"))

    def test_lint_before_freeze_does_not_need_deltas_file(self):
        (self.fu / "tasks" / "search-export.deltas.md").unlink()
        self.assertEqual(run(["lint", "search-export"], self.tmp).returncode, 0)

    def test_claim_file_without_card(self):
        claim = self.fu / "predictions" / "latency.md"
        claim.parent.mkdir(exist_ok=True)
        good = ("Claim under test  : the cache cuts p95\nMechanism chain   : hit → skip db\n"
                "Person prediction : \"p95 drops by half\" (medium)\nAgent prediction  : p95 drops 30-50 %\n"
                "Falsifier         : p95 within noise\nWritten           : 2026-11-12; before running\n")
        claim.write_text(good, encoding="utf-8")
        r = run(["lint", "latency"], self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout)
        claim.write_text(good.replace('"p95 drops by half" (medium)', "p95 drops by half"), encoding="utf-8")
        self.assertIn("claim-form", rules(run(["lint", "latency"], self.tmp).stdout, "FAIL"))

    def test_unknown_slug_exits_2(self):
        self.assertEqual(run(["lint", "nope"], self.tmp).returncode, 2)


# --------------------------------------------------------------------------- guard

def hook(command, cwd, event="PreToolUse", tool="Bash"):
    data = {"session_id": "t", "cwd": str(cwd), "permission_mode": "default", "hook_event_name": event,
            "tool_name": tool, "tool_input": {"command": command, "description": "x"}, "tool_use_id": "toolu_1"}
    if event == "PostToolUse":
        data["tool_response"] = {"stdout": "", "stderr": "", "interrupted": False}
    return json.dumps(data)


class Guard(Workspace):
    def setUp(self):
        super().setUp()
        # an open card naming the irreversible command (the fixture's quote-export is debriefed)
        text = self.card.read_text(encoding="utf-8").replace("State: debriefed", "State: waiting on you")
        self.card.write_text(text, encoding="utf-8")

    def pre(self, command, cwd=None):
        r = run(["guard", "pre"], self.tmp, stdin=hook(command, cwd or self.tmp))
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stderr, "")
        return json.loads(r.stdout) if r.stdout.strip() else None

    def post(self, command):
        r = run(["guard", "post"], self.tmp, stdin=hook(command, self.tmp, "PostToolUse"))
        self.assertEqual((r.returncode, r.stdout, r.stderr), (0, "", ""))

    def test_exact_match_asks_with_the_command(self):
        out = self.pre(IRR)
        hso = out["hookSpecificOutput"]
        self.assertEqual(hso["hookEventName"], "PreToolUse")
        self.assertEqual(hso["permissionDecision"], "ask")
        self.assertIn("card quote-export: irreversible step `%s`" % IRR, hso["permissionDecisionReason"])

    def test_variants_ask(self):
        for cmd in ("python3 publish.py build/quotes.json", "python  ./publish.py   build/quotes.json",
                    "cd sub && python3.11 publish.py build/quotes.json", "FOO=1 /usr/bin/python3 publish.py build/quotes.json"):
            out = self.pre(cmd)
            self.assertIsNotNone(out, cmd)
            self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "ask")

    def test_dry_run_and_other_args_do_not_match_a_script_command(self):
        self.assertIsNone(self.pre("python publish.py --dry-run build/quotes.json"))
        self.assertIsNone(self.pre("python publish.py build/other.json"))

    def test_runner_variant_with_trailing_args(self):
        self.edit("Irreversible: `%s`" % IRR, "Irreversible: `python -m pkg.publish --env prod`")
        self.edit("  - check: `python publish.py --dry-run build/quotes.json` exits 0", "  - check: `python -m pkg.publish --dry-run` exits 0")
        out = self.pre("python3 -m pkg.publish --env staging")
        self.assertIn("variant", out["hookSpecificOutput"]["permissionDecisionReason"])
        self.assertIsNone(self.pre("python -m pytest -q"))
        self.assertIsNone(self.pre("python -m pkg.other --env prod"))

    def test_second_run_asks_with_already_ran_reason(self):
        self.post(IRR)
        log = (self.fu / "logs" / "approvals.jsonl").read_text(encoding="utf-8").splitlines()
        rec = json.loads(log[-1])
        self.assertEqual(rec["slug"], "quote-export")
        self.assertEqual(len(rec["sha256"]), 64)
        out = self.pre("python3 publish.py build/quotes.json")
        reason = out["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("already ran once at %s" % rec["time"], reason)
        self.assertIn("a post-check must not re-execute it", reason)

    def test_post_moves_waiting_on_you_to_building(self):
        self.post(IRR)
        self.assertIn("State: building", self.card.read_text(encoding="utf-8"))

    def test_unrelated_command_is_silent(self):
        self.assertIsNone(self.pre("ls -la"))
        self.post("ls -la")
        self.assertFalse((self.fu / "logs" / "approvals.jsonl").exists())

    def test_debriefed_card_is_not_guarded(self):
        text = self.card.read_text(encoding="utf-8").replace("State: waiting on you", "State: debriefed")
        self.card.write_text(text, encoding="utf-8")
        self.assertIsNone(self.pre(IRR))

    def test_malformed_input_no_root_and_bad_args_fail_open(self):
        for args, stdin, cwd in ((["guard", "pre"], "{not json", self.tmp),
                                 (["guard", "pre"], "", self.tmp),
                                 (["guard", "pre"], json.dumps({"tool_name": "Bash", "tool_input": "x"}), self.tmp),
                                 (["guard", "pre"], hook(IRR, "/"), Path("/")),
                                 (["guard"], hook(IRR, self.tmp), self.tmp),
                                 (["guard", "sideways"], hook(IRR, self.tmp), self.tmp),
                                 (["guard", "pre", "--bogus"], hook(IRR, self.tmp), self.tmp)):
            r = run(args, cwd, stdin=stdin)
            self.assertEqual((r.returncode, r.stdout, r.stderr), (0, "", ""), (args, stdin[:40]))

    def test_non_bash_tool_is_silent(self):
        r = run(["guard", "pre"], self.tmp, stdin=hook(IRR, self.tmp, tool="Write"))
        self.assertEqual((r.returncode, r.stdout), (0, ""))

    def test_guard_off_and_log(self):
        prof = self.fu / "profile.md"
        prof.write_text(prof.read_text(encoding="utf-8").replace("guard: ask", "guard: off"), encoding="utf-8")
        self.assertIsNone(self.pre(IRR))
        prof.write_text(prof.read_text(encoding="utf-8").replace("guard: off", "guard: log"), encoding="utf-8")
        self.assertIsNone(self.pre(IRR))
        rec = json.loads((self.fu / "logs" / "guard.jsonl").read_text(encoding="utf-8").splitlines()[-1])
        self.assertEqual(rec["would"], "ask")

    def test_destructive_patterns_log_only_unless_strict(self):
        self.assertIsNone(self.pre("rm -rf build"))
        self.assertIsNone(self.pre("git push --force origin main"))
        lines = (self.fu / "logs" / "guard.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual([json.loads(x)["pattern"] for x in lines], ["rm -rf", "force-push"])
        prof = self.fu / "profile.md"
        prof.write_text(prof.read_text(encoding="utf-8").replace("strict: no", "strict: yes"), encoding="utf-8")
        out = self.pre("git reset --hard HEAD~1")
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "ask")

    def test_never_denies(self):
        src = FU.read_text(encoding="utf-8")
        self.assertNotIn('"deny"', src)


# -------------------------------------------------------------------------- freeze

def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True, timeout=30)


class Freeze(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="fu-freeze-"))
        git(self.tmp, "init", "-q", "-b", "main")
        for k, v in (("user.name", "t"), ("user.email", "t@example.invalid"), ("commit.gpgsign", "false"),
                     ("core.hooksPath", ".git/hooks")):
            git(self.tmp, "config", k, v)
        (self.tmp / "app.py").write_text("x = 1\n", encoding="utf-8")
        (self.tmp / ".gitignore").write_text(".finding-unknowns/logs/\n.finding-unknowns/view/\n", encoding="utf-8")
        git(self.tmp, "add", "-A")
        git(self.tmp, "commit", "-q", "-m", "init")
        tasks = self.tmp / ".finding-unknowns" / "tasks"
        tasks.mkdir(parents=True)
        src = (VALID / "tasks" / "search-export.md").read_text(encoding="utf-8")
        src = src.replace("State: building", "State: briefing").replace("Timing: Brief frozen 2026-11-12 11:00, commit 9f8e7d6", "Timing: draft")
        src = src.replace("## Brief (frozen 2026-11-12 11:00)", "## Brief (draft)").replace("Latest: D1", "Latest: none")
        self.card = tasks / "search-export.md"
        self.card.write_text(src, encoding="utf-8")
        (self.tmp / "app.py").write_text("x = 2\n", encoding="utf-8")  # unrelated, unstaged change
        (self.tmp / "notes.txt").write_text("untracked\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def freeze(self, stage="brief"):
        return run(["freeze", "search-export", "--stage", stage], self.tmp)

    def test_brief_commits_only_card_paths(self):
        r = self.freeze()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertRegex(r.stdout, r"^committed [0-9a-f]+ \(brief search-export\)")
        files = git(self.tmp, "show", "--name-only", "--format=", "HEAD").stdout.split()
        self.assertEqual(sorted(files), [".finding-unknowns/tasks/search-export.deltas.md", ".finding-unknowns/tasks/search-export.md"])
        self.assertEqual(git(self.tmp, "log", "-1", "--format=%s").stdout.strip(), "chore(card): brief search-export")
        status = git(self.tmp, "status", "--porcelain").stdout
        self.assertIn(" M app.py", status)
        self.assertIn("?? notes.txt", status)
        text = self.card.read_text(encoding="utf-8")
        self.assertRegex(text, r"## Brief \(frozen \d{4}-\d{2}-\d{2} \d{2}:\d{2}\)")
        self.assertIn("State: building", text)
        short = git(self.tmp, "rev-parse", "--short", "HEAD").stdout.strip()
        self.assertRegex(text, r"Timing: Brief frozen \d{4}-\d{2}-\d{2} \d{2}:\d{2}, commit %s" % short)
        committed = git(self.tmp, "show", "HEAD:.finding-unknowns/tasks/search-export.md").stdout
        self.assertIn("Timing: draft", committed)  # the Timing line stays uncommitted until the next freeze

    def test_stop_resume_debrief_set_state(self):
        self.assertEqual(self.freeze().returncode, 0)
        for stage, state in (("stop", "waiting on you"), ("resume", "building"), ("debrief", "debriefed")):
            r = self.freeze(stage)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("State: %s" % state, self.card.read_text(encoding="utf-8"))

    def test_skip_commits_no_still_freezes_heading_and_state(self):
        (self.tmp / ".finding-unknowns" / "profile.md").write_text("commits: no\n", encoding="utf-8")
        head = git(self.tmp, "rev-parse", "HEAD").stdout
        r = self.freeze()
        self.assertEqual(r.returncode, 3)
        self.assertIn("self-reported: commits: no", r.stdout)
        text = self.card.read_text(encoding="utf-8")
        self.assertIn("State: building", text)
        self.assertIn("## Brief (frozen ", text)
        self.assertIn("Timing: self-reported", text)
        self.assertEqual(git(self.tmp, "rev-parse", "HEAD").stdout, head)

    def test_skip_other_changes_staged(self):
        git(self.tmp, "add", "app.py")
        r = self.freeze()
        self.assertEqual(r.returncode, 3)
        self.assertIn("other changes already staged", r.stdout)

    def test_skip_not_a_git_repo(self):
        shutil.rmtree(self.tmp / ".git")
        r = self.freeze()
        self.assertEqual(r.returncode, 3)
        self.assertIn("not a git repository", r.stdout)

    def test_skip_detached_head(self):
        git(self.tmp, "checkout", "-q", "--detach")
        self.assertEqual(self.freeze().returncode, 3)

    def test_skip_ignored_path(self):
        (self.tmp / ".gitignore").write_text(".finding-unknowns/\n", encoding="utf-8")
        r = self.freeze()
        self.assertEqual(r.returncode, 3)
        self.assertIn("path ignored", r.stdout)

    def test_failing_commit_hook_unstages_and_self_reports(self):
        hookf = self.tmp / ".git" / "hooks" / "pre-commit"
        hookf.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        hookf.chmod(0o755)
        r = self.freeze()
        self.assertEqual(r.returncode, 3)
        self.assertEqual(git(self.tmp, "diff", "--cached", "--name-only").stdout, "")
        self.assertIn("Timing: self-reported", self.card.read_text(encoding="utf-8"))

    def test_claim_file_without_card(self):
        self.card.unlink()
        claim = self.tmp / ".finding-unknowns" / "predictions" / "latency.md"
        claim.parent.mkdir()
        claim.write_text("Claim under test  : x\nWritten           : 2026-11-12; before running\n", encoding="utf-8")
        r = run(["freeze", "latency", "--stage", "brief"], self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertRegex(claim.read_text(encoding="utf-8"), r"Written .*\nTiming: Brief frozen .*, commit [0-9a-f]+")

    def test_integrity_after_freeze(self):
        self.assertEqual(self.freeze().returncode, 0)
        r = run(["integrity", "search-export"], self.tmp)
        lines = r.stdout.splitlines()
        self.assertEqual(lines[0], "Brief vs freeze: unchanged")
        self.assertEqual(lines[1], "Check files: none named")
        self.assertIn("app.py:1-1", lines[2])     # changed, not named in any delta
        self.assertIn("notes.txt:1-1", lines[2])  # untracked
        self.assertEqual(r.returncode, 1)
        text = self.card.read_text(encoding="utf-8").replace("reuse the existing tokenizer", "write a new tokenizer")
        self.card.write_text(text, encoding="utf-8")
        deltas = self.card.with_name("search-export.deltas.md")
        deltas.write_text(deltas.read_text(encoding="utf-8") + "D1 2026-11-12 11:30 deviation: x → app.py\nD2 2026-11-12 11:31 deviation: y → notes.txt\n", encoding="utf-8")
        lines = run(["integrity", "search-export"], self.tmp).stdout.splitlines()
        self.assertRegex(lines[0], r"^Brief vs freeze: edited: lines \d+")
        self.assertEqual(lines[2], "Unlogged hunks: none")

    def test_integrity_not_run_when_self_reported(self):
        text = self.card.read_text(encoding="utf-8").replace("Timing: draft", "Timing: self-reported")
        self.card.write_text(text, encoding="utf-8")
        r = run(["integrity", "search-export"], self.tmp)
        self.assertEqual(r.returncode, 3)
        self.assertEqual(r.stdout.splitlines(), ["Brief vs freeze: not run (timing: self-reported)",
                                                 "Check files: not run (timing: self-reported)",
                                                 "Unlogged hunks: not run (timing: self-reported)"])


# -------------------------------------------------------------------- render, list, log

class RenderListLog(Workspace):
    def test_render_escapes_injected_html_and_has_no_external_resources(self):
        self.edit("Goal: Write build/quotes.json", "Goal: <script>alert(1)</script> Write build/quotes.json")
        self.edit("  - the carrier's actual remote-zone rate card", "  - <img src=x onerror=alert(2)> `<b>code</b>`")
        r = run(["render", "quote-export"], self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout)
        html = (self.fu / "view" / "quote-export.html").read_text(encoding="utf-8")
        self.assertNotIn("<script", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertNotIn("<img", html)
        self.assertIn("<code>&lt;b&gt;code&lt;/b&gt;</code>", html)
        self.assertIsNone(re.search(r"https?:|//[a-z]|<link|@import|url\(", html, flags=re.I))
        self.assertIn("prefers-color-scheme:dark", html)
        self.assertIn("Noto Sans SC", html)

    def test_render_blocks_on_fail_outside_the_brief(self):
        self.edit("  - consistent?: partly", "  - consistent?: mostly")
        r = run(["render", "quote-export"], self.tmp)
        self.assertEqual(r.returncode, 1)
        self.assertIn("FAIL", r.stdout)
        self.assertFalse((self.fu / "view" / "quote-export.html").exists())

    def test_render_shows_banner_for_fail_inside_frozen_brief(self):
        self.edit('P2 (you · low) "every parcel has a service"', 'P2 (you · fairly sure) "every parcel has a service"')
        text = self.card.read_text(encoding="utf-8")
        head, debrief = text.split("## Debrief", 1)
        self.card.write_text(head + "## Debrief" + debrief.replace("P2 (you · low)", "P2 (you · fairly sure)"), encoding="utf-8")
        r = run(["render", "quote-export"], self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout)
        html = (self.fu / "view" / "quote-export.html").read_text(encoding="utf-8")
        self.assertIn("lint FAIL inside the frozen Brief", html)

    def test_render_marks_the_irreversible_run(self):
        (self.fu / "logs").mkdir(exist_ok=True)
        (self.fu / "logs" / "approvals.jsonl").write_text(
            json.dumps({"sha256": "0" * 64, "time": "2026-11-12 09:50", "slug": "quote-export"}) + "\n", encoding="utf-8")
        run(["render", "quote-export"], self.tmp)
        html = (self.fu / "view" / "quote-export.html").read_text(encoding="utf-8")
        self.assertIn("irreversible step at run", html)
        self.assertLess(html.index('class="node irr"'), html.index(">D3<"))

    def test_render_list(self):
        run(["log", "quote-export"], self.tmp)
        r = run(["render", "--list"], self.tmp)
        self.assertEqual(r.returncode, 0)
        html = (self.fu / "view" / "index.html").read_text(encoding="utf-8")
        self.assertIn("quote-export", html)
        self.assertIn("为图书馆目录添加前缀搜索导出", html)
        self.assertIn("predictions on one card are not independent", html)
        self.assertNotIn("<svg", html)  # fewer than 10 graded: stat line, no curve

    def test_list_shape(self):
        os.utime(self.card, (1_000_000_000, 1_000_000_000))  # newest first: search-export, then quote-export
        r = run(["list", "--all"], self.tmp)
        self.assertEqual(r.returncode, 0)
        lines = r.stdout.splitlines()
        self.assertEqual(lines[0], "search-export · building")
        pattern = [r"^\S+ · (briefing|building|waiting on you|debriefed)$", r"^  - needs you: .+$",
                   r"^  - last seen: (after D\d+|never) · unseen deltas: \d+$",
                   r"^  - graded: (you \d+ of \d+ held · agent \d+ of \d+ held|not yet)$"]
        for start in (0, 4):
            for i, pat in enumerate(pattern):
                self.assertRegex(lines[start + i], pat)
        self.assertEqual(run(["list"], self.tmp).stdout.splitlines()[0], "search-export · building")
        self.assertNotIn("quote-export", run(["list"], self.tmp).stdout)

    def test_log_is_idempotent_and_prints_the_stat_line_at_five(self):
        r1 = run(["log", "quote-export"], self.tmp)
        self.assertEqual(len(r1.stdout.splitlines()), 4)
        r2 = run(["log", "quote-export"], self.tmp)
        self.assertEqual(r2.stdout.strip(), "log: nothing new for quote-export")
        log = self.fu / "predictions-log.md"
        self.assertEqual(len(log.read_text(encoding="utf-8").splitlines()), 4)
        extra = "".join("2026-11-0%d · old-%d · A1 · agent · consistent · high\n" % (n, n) for n in range(1, 5))
        log.write_text(log.read_text(encoding="utf-8") + extra, encoding="utf-8")
        r3 = run(["log", "quote-export"], self.tmp)
        self.assertIn("You: 1 of 2 held · Agent: 5 of 5 held (too soft?)", r3.stdout)

    def test_log_without_debrief_exits_1(self):
        r = run(["log", "search-export"], self.tmp)
        self.assertEqual(r.returncode, 1)
        self.assertIn("no Debrief", r.stdout)

    def test_init_keeps_keys_and_prints_gitignore_lines(self):
        r = run(["init", "--guard", "log"], self.tmp)
        self.assertEqual(r.returncode, 0)
        prof = (self.fu / "profile.md").read_text(encoding="utf-8")
        self.assertIn("guard: log", prof)
        self.assertIn("mode: ship", prof)
        self.assertIn(".finding-unknowns/predictions-log.md", r.stdout)


class Packaging(unittest.TestCase):
    def test_marker_and_hook_config(self):
        self.assertIn("finding-unknowns", FU.read_text(encoding="utf-8").splitlines()[1])
        cfg = json.loads((REPO / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        for event, phase in (("PreToolUse", "pre"), ("PostToolUse", "post")):
            entry = cfg["hooks"][event][0]
            self.assertEqual(entry["matcher"], "Bash")
            self.assertEqual(entry["hooks"][0]["command"], 'python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fu.py" guard %s' % phase)

    def test_install_layout_path_resolves(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            r = subprocess.run(["bash", str(REPO / "install.sh")], env=dict(os.environ, CLAUDE_CONFIG_DIR=str(tmp)),
                               capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)
            base = tmp / "skills" / "finding-unknowns"
            fu = (base / ".." / ".." / "scripts" / "fu.py").resolve()
            self.assertTrue(fu.is_file())
            self.assertEqual(subprocess.run([sys.executable, str(fu), "--help"], capture_output=True).returncode, 0)
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
