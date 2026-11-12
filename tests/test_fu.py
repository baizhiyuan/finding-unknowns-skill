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
        self.assertEqual(self.lint("quote-export", "--strict").returncode, 0)
        self.edit("- the remote-zone rate is synthetic until the carrier card arrives",
                  "\n".join("- open item %d %s" % (n, " ".join(["word"] * 19)) for n in range(40)))
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


class GuardBase(Workspace):
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


class Guard(GuardBase):
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


class GuardForms(GuardBase):
    """S4: forms of the irreversible command the guard must ask about."""

    ASKS = (
        "python publish.py build/quotes.json 2>&1",
        "python publish.py build/quotes.json > out.log 2>&1",
        "python publish.py build/quotes.json 2>&1 | tee log.txt",
        "timeout 60 python publish.py build/quotes.json",
        "timeout -s KILL 5m python3 publish.py build/quotes.json",
        "env A=1 B=2 python publish.py build/quotes.json",
        "env -i PATH=/usr/bin python publish.py build/quotes.json",
        "nohup python publish.py build/quotes.json &",
        "sudo -u deploy python publish.py build/quotes.json",
        "time python publish.py build/quotes.json",
        "command python publish.py build/quotes.json",
        "exec python publish.py build/quotes.json",
        "echo build/quotes.json | xargs python publish.py build/quotes.json",
        'eval "python publish.py build/quotes.json"',
        "uv run python publish.py build/quotes.json",
        "poetry run python3 publish.py build/quotes.json",
        "(cd . && python publish.py build/quotes.json)",
        "echo $(python publish.py build/quotes.json)",
        "echo `python publish.py build/quotes.json`",
        'echo "$(python publish.py build/quotes.json)"',
        'sh -c "python publish.py build/quotes.json"',
        "bash -lc 'cd x && python3 publish.py build/quotes.json'",
        'zsh -c "timeout 9 python publish.py build/quotes.json >/dev/null"',
        "python publish.py build/quotes.json --force",
        "strace -f python publish.py build/quotes.json",
        "if true; then python publish.py build/quotes.json; fi",
        "{ python publish.py build/quotes.json; }",
    )

    def test_every_form_asks(self):
        for cmd in self.ASKS:
            out = self.pre(cmd)
            self.assertIsNotNone(out, cmd)
            self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "ask", cmd)

    def test_wrapped_exact_forms_are_exact(self):
        for cmd in ("timeout 60 python publish.py build/quotes.json 2>&1", 'bash -c "python publish.py build/quotes.json"',
                    "uv run python publish.py build/quotes.json"):
            self.assertIn("irreversible step `", self.pre(cmd)["hookSpecificOutput"]["permissionDecisionReason"], cmd)
        self.assertIn("variant", self.pre("python publish.py build/quotes.json --force")["hookSpecificOutput"]["permissionDecisionReason"])

    AMEND_IRR = "M2 2026-11-12 09:50 · after D2 · confirmed: also drop the stale cache · why: found mid-build\n"

    def _amend_irreversible(self, cmd="rm -rf cache/old"):
        self.edit("## Deltas\n", self.AMEND_IRR + "Irreversible: `%s`\n\n## Deltas\n" % cmd)

    def test_irreversible_line_under_an_amendment_lints_clean_and_the_guard_asks(self):
        self._amend_irreversible()
        r = self.lint()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertNotIn("brief-form", rules(r.stdout, "FAIL"))
        out = self.pre("rm -rf cache/old")
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "ask")
        self.assertIn("irreversible step `rm -rf cache/old`", out["hookSpecificOutput"]["permissionDecisionReason"])

    def test_malformed_irreversible_line_under_an_amendment_fails(self):
        self._amend_irreversible("x")
        self.edit("Irreversible: `x`", "Irreversible: rm -rf cache/old")
        self.assertIn("brief-form", rules(self.lint().stdout, "FAIL"))

    def test_irreversible_line_outside_brief_and_amendments_fails(self):
        self.edit("## Open\n", "## Open\nIrreversible: `rm -rf cache/old`\n")
        self.assertIn("brief-form", rules(self.lint().stdout, "FAIL"))

    def test_decisions_line_form_warns(self):
        self.assertNotIn("decisions-form", self.lint().stdout)
        (self.fu / "decisions.md").write_text("# decisions\n- billing basis: scale weight only (2026-11-12)\n", encoding="utf-8")
        self.assertIn("decisions-form", rules(self.lint().stdout, "WARN"))

    def test_npm_run_script(self):
        self.edit("Irreversible: `%s`" % IRR, "Irreversible: `npm run deploy`")
        self.edit("  - check: `python publish.py --dry-run build/quotes.json` exits 0", "  - check: `npm run build` exits 0")
        for cmd in ("npm run-script deploy", "npm run deploy -- --prod", "CI=1 npm run deploy"):
            self.assertIsNotNone(self.pre(cmd), cmd)
        self.assertIsNone(self.pre("npm run build"))

    def test_lint_irreversible_check_uses_the_same_matcher(self):
        for check in ("`timeout 60 python3 publish.py build/quotes.json 2>&1`", "`bash -c \"python publish.py build/quotes.json\"`",
                      "`env A=1 python publish.py build/quotes.json > out.log`"):
            text = self.card.read_text(encoding="utf-8")
            old = "  - check: `python publish.py --dry-run build/quotes.json` exits 0"
            self.card.write_text(text.replace(old, "  - check: %s exits 0" % check, 1), encoding="utf-8")
            self.assertIn("irreversible-check", rules(self.lint().stdout, "FAIL"), check)
            self.card.write_text(text, encoding="utf-8")

    def test_dry_run_check_on_a_runner_neither_asks_nor_records(self):
        self.edit("Irreversible: `%s`" % IRR, "Irreversible: `python -m pkg.publish`")
        self.edit("  - check: `python publish.py --dry-run build/quotes.json` exits 0",
                  "  - check: `python -m pkg.publish --dry-run` exits 0")
        self.assertNotIn("irreversible-check", self.lint().stdout)
        for cmd in ("python -m pkg.publish --dry-run", "python3 -m pkg.publish --dry-run 2>&1 | tail -5"):
            self.assertIsNone(self.pre(cmd), cmd)
            self.post(cmd)
        self.assertFalse((self.fu / "logs" / "approvals.jsonl").exists())
        self.assertIn("State: waiting on you", self.card.read_text(encoding="utf-8"))
        self.assertIsNotNone(self.pre("python -m pkg.publish --env prod"))  # not the card's check: asks
        self.assertIn("irreversible step `", self.pre("python -m pkg.publish")["hookSpecificOutput"]["permissionDecisionReason"])

    def test_post_tool_use_failure_is_recorded_and_warns_on_retry(self):
        r = run(["guard", "post"], self.tmp, stdin=hook(IRR, self.tmp, "PostToolUseFailure"))
        self.assertEqual((r.returncode, r.stdout, r.stderr), (0, "", ""))
        rec = json.loads((self.fu / "logs" / "approvals.jsonl").read_text(encoding="utf-8").splitlines()[-1])
        self.assertTrue(rec["failed"])
        reason = self.pre(IRR)["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("already ran once at %s and failed" % rec["time"], reason)
        self.post(IRR)
        rec = json.loads((self.fu / "logs" / "approvals.jsonl").read_text(encoding="utf-8").splitlines()[-1])
        self.assertNotIn("failed", rec)

    def test_post_clears_needs_you(self):
        self.post(IRR)
        self.assertIn("Needs you: nothing", self.card.read_text(encoding="utf-8"))

    def test_guard_log_holds_no_command_text(self):
        self.assertIsNone(self.pre("rm -rf /srv/secret-dir-name"))
        prof = self.fu / "profile.md"
        prof.write_text(prof.read_text(encoding="utf-8").replace("guard: ask", "guard: log"), encoding="utf-8")
        self.assertIsNone(self.pre(IRR + " # secret-token"))
        lines = (self.fu / "logs" / "guard.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(set(json.loads(lines[0])), {"time", "pattern", "sha256"})
        self.assertEqual(set(json.loads(lines[1])), {"time", "slug", "sha256", "would"})
        self.assertNotIn("secret", "".join(lines))

    def test_destructive_tokens(self):
        prof = self.fu / "profile.md"
        prof.write_text(prof.read_text(encoding="utf-8").replace("strict: no", "strict: yes"), encoding="utf-8")
        for cmd in ("rm -fr x", "rm -r -f x", "sudo rm --recursive --force x", "git push -f", "git push origin +main",
                    "git -C repo push --force-with-lease", "git reset --hard", 'psql -c "drop table users"',
                    "bash -c 'rm -rf build'"):
            self.assertIsNotNone(self.pre(cmd), cmd)
        for cmd in ("rm -r x", "rm -f x", "git push -u origin main", "git reset --soft HEAD~1"):
            self.assertIsNone(self.pre(cmd), cmd)

    def test_prompt_text_is_cleaned_and_names_the_card(self):
        evil = "python publish.py build/quotes.json\x1b[2J‮" + "x" * 300
        self.edit("Irreversible: `%s`" % IRR, "Irreversible: `%s`" % evil)
        reason = self.pre(evil)["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertNotIn("\x1b", reason)
        self.assertNotIn("‮", reason)
        self.assertLess(len(reason), 300)
        self.assertIn("· .finding-unknowns/tasks/quote-export.md", reason)

    def test_one_bad_card_does_not_unguard_the_others(self):
        tasks = self.fu / "tasks"
        (tasks / "a-broken.md").write_bytes(b"# a-broken\nGoal: \xff\xfe \xc3 \xb7 State: building\nIrreversible: `x`\n")
        os.symlink(str(self.tmp / "missing.md"), str(tasks / "b-dangling.md"))
        (tasks / "c-unreadable.md").mkdir()  # a directory named like a card
        logs = self.fu / "logs"
        logs.mkdir(exist_ok=True)
        (logs / "approvals.jsonl").mkdir()  # the prior-run lookup fails
        out = self.pre(IRR)
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "ask")
        self.assertIsNone(self.pre("ls"))
        self.assertEqual(run(["list", "--all"], self.tmp).returncode, 0)

    def test_device_symlink_card_does_not_disable_the_guard(self):
        import time
        os.symlink("/dev/zero", str(self.fu / "tasks" / "zz.md"))
        start = time.time()
        out = self.pre(IRR)
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "ask")
        self.assertLess(time.time() - start, 5)

    def test_interpreter_options_before_the_script_still_ask(self):
        for cmd in ("python -u publish.py build/quotes.json", "python3 -X utf8 publish.py build/quotes.json",
                    "python -- publish.py build/quotes.json", "python3 -W ignore -u ./publish.py build/quotes.json"):
            out = self.pre(cmd)
            self.assertIsNotNone(out, cmd)
            self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "ask", cmd)
        self.assertIsNone(self.pre("python -u other.py build/quotes.json"))

    def test_redos_inputs_finish_fast(self):
        import time
        for cmd in ("git push " + "a " * 32000, "git" + " push" * 16000 + " -f", "rm " + "-r " * 20000,
                    "a;" * 32000, "$(" * 30000, "`" * 65536, "bash -c " * 8000, "eval " * 13000, "x" * 65536 + IRR):
            start = time.time()
            r = run(["guard", "pre"], self.tmp, stdin=hook(cmd, self.tmp))
            self.assertEqual((r.returncode, r.stderr), (0, ""))
            self.assertLess(time.time() - start, 3, cmd[:20])
        long_lines = ("- You expected " + "x → y, because " * 4000 + "z [conf",
                      "Needs you: " + "a (recommendation: b; settles c" * 3000,
                      "M1 2026-11-12 09:40 · after D2 · confirmed: " + "a · why: b · " * 5000,
                      "- " + "P1 A9 {a | " * 8000)
        for line in long_lines:
            text = self.card.read_text(encoding="utf-8")
            self.card.write_text(text.replace("## Open\n", "## Open\n" + line + "\n", 1), encoding="utf-8")
            start = time.time()
            for args in (["lint", "quote-export", "--strict"], ["render", "quote-export"], ["render", "--list"]):
                run(args, self.tmp)
            self.assertLess(time.time() - start, 6, line[:20])
            self.card.write_text(text, encoding="utf-8")

    def test_hook_command_runs_with_python_only_and_without_python(self):
        cfg = json.loads((REPO / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        command = cfg["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        bindir = self.tmp / "bin"
        bindir.mkdir()
        os.symlink(sys.executable, str(bindir / "python"))
        for path, want_ask in ((str(bindir), True), (str(self.tmp / "nothing"), False)):
            r = subprocess.run(["/bin/sh", "-c", command], input=hook(IRR, self.tmp), capture_output=True, text=True,
                               env={"PATH": path, "CLAUDE_PLUGIN_ROOT": str(REPO)}, timeout=60)
            self.assertEqual((r.returncode, r.stderr), (0, ""), path)
            self.assertEqual(bool(r.stdout.strip()), want_ask, path)



class SafeWrites(Workspace):
    """S1: no write follows a symlink, for every path fu writes (dangling and existing targets)."""

    def setUp(self):
        super().setUp()
        self.out = Path(tempfile.mkdtemp(prefix="fu-victim-"))
        self.victim = self.out / "bashrc"
        self.victim.write_text("orig\n", encoding="utf-8")
        self.open_card()

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(self.out, ignore_errors=True)

    def open_card(self):
        text = self.card.read_text(encoding="utf-8").replace("State: debriefed", "State: waiting on you")
        self.card.write_text(text, encoding="utf-8")

    def link(self, path: Path, dangling: bool):
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() or path.is_symlink():
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
        target = self.out / "missing" if dangling else self.victim
        os.symlink(str(target), str(path))

    def assert_untouched(self, label):
        self.assertEqual(self.victim.read_text(encoding="utf-8"), "orig\n", label)
        self.assertEqual(sorted(p.name for p in self.out.iterdir()), ["bashrc"], label)

    def cli(self, args, label):
        r = run(args, self.tmp)
        self.assertEqual(r.returncode, 2, (label, r.stdout))
        self.assertIn("refusing to write", r.stdout, label)

    def hook_call(self, phase, cmd, label):
        r = run(["guard", phase], self.tmp, stdin=hook(cmd, self.tmp, "PreToolUse" if phase == "pre" else "PostToolUse"))
        self.assertEqual((r.returncode, r.stderr), (0, ""), label)
        return r.stdout

    def test_every_file_write_refuses_a_symlink(self):
        logs, view = self.fu / "logs", self.fu / "view"
        prof = self.fu / "profile.md"
        cases = (
            ("approvals.jsonl", logs / "approvals.jsonl", lambda l: self.hook_call("post", IRR, l)),
            ("guard.jsonl", logs / "guard.jsonl", lambda l: self.hook_call("pre", "rm -rf build", l)),
            ("view card", view / "quote-export.html", lambda l: self.cli(["render", "quote-export"], l)),
            ("view index", view / "index.html", lambda l: self.cli(["render", "--list"], l)),
            ("predictions-log", self.fu / "predictions-log.md", lambda l: self.cli(["log", "quote-export"], l)),
        )
        for dangling in (True, False):
            for label, path, act in cases:
                self.link(path, dangling)
                act("%s dangling=%s" % (label, dangling))
                self.assert_untouched("%s dangling=%s" % (label, dangling))
                path.unlink()
            self.link(prof, dangling)
            self.assertIn('"ask"', self.hook_call("pre", IRR, "profile"))
            self.cli(["init"], "profile dangling=%s" % dangling)
            self.assert_untouched("profile")
            prof.unlink()
            prof.write_text("mode: ship\nstrict: no\ncommits: yes\nguard: ask\n", encoding="utf-8")

    def test_symlinked_directories_are_refused(self):
        for name, act in (("logs", lambda: self.hook_call("post", IRR, "logs")),
                          ("view", lambda: self.cli(["render", "quote-export"], "view"))):
            d = self.fu / name
            if d.exists():
                shutil.rmtree(d)
            os.symlink(str(self.out), str(d))
            act()
            self.assert_untouched(name)
            d.unlink()

    def test_card_deltas_and_claim_writes_refuse_symlinks(self):
        card = self.fu / "tasks" / "search-export.md"
        text = card.read_text(encoding="utf-8")
        self.victim.write_text(text, encoding="utf-8")
        card.unlink()
        os.symlink(str(self.victim), str(card))
        self.cli(["freeze", "search-export", "--stage", "stop"], "card")
        self.assertEqual(self.victim.read_text(encoding="utf-8"), text)
        card.unlink()
        card.write_text(text.replace("## Brief (frozen 2026-11-12 11:00)", "## Brief (draft)"), encoding="utf-8")
        deltas = card.with_name("search-export.deltas.md")
        deltas.unlink()
        os.symlink(str(self.out / "missing"), str(deltas))
        self.cli(["freeze", "search-export", "--stage", "brief"], "deltas")
        self.assertFalse((self.out / "missing").exists())
        claim = self.fu / "predictions" / "latency.md"
        claim.parent.mkdir(exist_ok=True)
        self.victim.write_text("Claim under test  : x\nWritten           : 2026-11-12\n", encoding="utf-8")
        os.symlink(str(self.victim), str(claim))
        self.cli(["freeze", "latency", "--stage", "brief"], "claim")
        self.assertNotIn("Timing", self.victim.read_text(encoding="utf-8"))

    def test_guard_post_does_not_write_a_symlinked_card(self):
        text = self.card.read_text(encoding="utf-8")
        self.victim.write_text(text, encoding="utf-8")
        self.card.unlink()
        os.symlink(str(self.victim), str(self.card))
        self.assertEqual(self.hook_call("post", IRR, "card"), "")
        self.assertEqual(self.victim.read_text(encoding="utf-8"), text)  # still `waiting on you`
        self.assertTrue((self.fu / "logs" / "approvals.jsonl").is_file())  # the record itself is written

    def test_symlinked_project_dir_and_tasks_dir_are_refused(self):
        real = self.out / "real-fu"
        shutil.copytree(self.fu, real)
        shutil.rmtree(self.fu)
        os.symlink(str(real), str(self.fu))
        self.cli(["render", "quote-export"], "fu dir")
        self.assertFalse((real / "view").exists())
        self.fu.unlink()
        shutil.copytree(real, self.fu)
        shutil.rmtree(self.fu / "tasks")
        os.symlink(str(real / "tasks"), str(self.fu / "tasks"))
        before = (real / "tasks" / "search-export.md").read_text(encoding="utf-8")
        self.cli(["freeze", "search-export", "--stage", "stop"], "tasks dir")
        self.assertEqual((real / "tasks" / "search-export.md").read_text(encoding="utf-8"), before)


class IdsAndCaps(Workspace):
    """C2 (the person's words are never an id-reserved FAIL) and C3 (strict caps that a real card meets)."""

    def test_person_quotes_with_id_like_words_pass(self):
        claim = 'P1 (you · medium) "the bulky parcel\'s cheapest quote is Economy at 4.00, and the bulky parcel costs the same as a \\"compact\\" one"'
        new = 'P1 (you · medium) "P99 drops below 200 ms and parcel P3 ships with A2 rates"'
        self.assertEqual(self.card.read_text(encoding="utf-8").count(claim), 2)
        text = self.card.read_text(encoding="utf-8").replace(claim, new)
        self.card.write_text(text, encoding="utf-8")
        r = self.lint()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertNotIn("id-reserved", r.stdout)
        self.assertEqual(run(["log", "quote-export"], self.tmp).returncode, 0)
        self.assertEqual(run(["render", "quote-export"], self.tmp).returncode, 0)

    def test_bottom_line_ignores_long_percentile_names(self):
        self.edit("did not hold: coverage needed an invented service (P2)",
                  "did not hold: coverage needed an invented service (P2); P99 under 200 ms was never in question")
        r = self.lint()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertNotIn("bottom-line", r.stdout)

    def test_frozen_brief_id_fail_does_not_block_log(self):
        self.edit("  - add one remote-zone service because parcel 3 has no service in the table",
                  "  - add one remote-zone service for P3")
        r = self.lint()
        self.assertIn("id-reserved", rules(r.stdout, "FAIL"))
        r = run(["log", "quote-export"], self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_undefined_id_outside_the_brief_warns_inside_fails(self):
        self.edit("  - measured: Economy 4.00 (build/quotes.json)", "  - measured: Economy 4.00 for parcel P3 (build/quotes.json)")
        r = self.lint()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("id-reserved", rules(r.stdout, "WARN"))
        self.assertEqual(run(["log", "quote-export"], self.tmp).returncode, 0)
        self.edit("  - measured: Economy 4.00 for parcel P3 (build/quotes.json)", "  - measured: Economy 4.00 for parcel `P3` (build/quotes.json)")
        self.assertNotIn("id-reserved", self.lint().stdout)
        self.edit("  - bill on scale weight only because", "  - bill on scale weight only for P3 because")
        self.assertIn("id-reserved", rules(self.lint().stdout, "FAIL"))
        self.assertNotIn("P12", self.lint().stdout)

    def test_long_ids_are_not_ids(self):
        self.edit("- the remote-zone rate is synthetic", "- P10 and A12 are part numbers; the remote-zone rate is synthetic")
        self.assertNotIn("id-reserved", self.lint().stdout)

    def regrade(self):
        text = self.card.read_text(encoding="utf-8")
        debrief = text[text.index("## Debrief"):]
        self.card.write_text(text + "\n" + debrief.replace("2026-11-12 10:30", "2026-11-13 09:00"), encoding="utf-8")

    def test_realistic_two_plus_two_card_with_a_regrade_meets_strict(self):
        r = self.lint("quote-export", "--strict")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.regrade()
        r = self.lint("quote-export", "--strict")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(run(["log", "quote-export"], self.tmp).returncode, 0)

    def test_card_at_the_item_caps_meets_the_word_cap(self):
        text = self.card.read_text(encoding="utf-8")
        a3 = ('A3 (agent · low) "the Overnight row is the only change to the rate table"\n'
              "  - falsifier: any other row in rates.py differs from the freeze\n"
              "  - should not change: the Economy and Standard prices for all parcels\n")
        text = text.replace("Stop-points:", a3 + "Stop-points:", 1)
        items = "".join("C%d the quote for parcel %d is the cheapest available service\n"
                        "  - check: `python -m pytest tests/test_quotes.py -k p%d` passes\n"
                        "  - does NOT prove: that the carrier honours the published service levels\n"
                        "  - lane: reversible\n" % (n, n, n) for n in (3, 4, 5))
        text = text.replace("Check files:", items + "Check files:", 1)
        row = ('A3 (agent · low) "the Overnight row is the only change to the rate table"\n'
               "  - measured: one row added (git diff rates.py)\n  - consistent?: consistent\n"
               "  - mechanism: the selector reads only the table it was given [supported]\n")
        text = text.replace("Integrity:", row + "Integrity:", 1)
        text = text.replace("Did NOT prove:\n", "Did NOT prove:\n" + "".join(
            "  - C%d quote → leaves open: whether the carrier honours it · still holds: the quote is cheapest\n" % n
            for n in (3, 4, 5)), 1)
        text = text.replace("one-shot publish (P1, A1)", "one-shot publish (P1, A1, A3)")
        self.assertEqual((text.count("A3 (agent"), text.count("  - lane: reversible"), text.count("C5 quote")), (2, 4, 1))
        self.card.write_text(text, encoding="utf-8")
        r = self.lint("quote-export", "--strict")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.regrade()
        self.assertEqual(self.lint("quote-export", "--strict").returncode, 0)

    def test_whole_card_caps_render_under_the_banner(self):
        prof = self.fu / "profile.md"
        prof.write_text(prof.read_text(encoding="utf-8").replace("strict: no", "strict: yes"), encoding="utf-8")
        self.edit("- the remote-zone rate is synthetic until the carrier card arrives",
                  "\n".join("- open item %d" % n for n in range(45)))
        self.assertIn("live-length", rules(self.lint().stdout, "FAIL"))
        r = run(["render", "quote-export"], self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout)
        html = (self.fu / "view" / "quote-export.html").read_text(encoding="utf-8")
        self.assertIn("live-length", html)

    def test_frozen_brief_lines_do_not_count_toward_live_length(self):
        text = self.card.read_text(encoding="utf-8")
        pad = "".join("  - decision %d because reason %d\n" % (n, n) for n in range(40))
        self.card.write_text(text.replace("Approach:\n", "Approach:\n" + pad, 1), encoding="utf-8")
        self.assertNotIn("live-length", self.lint().stdout)
        text = self.card.read_text(encoding="utf-8").replace("## Brief (frozen 2026-11-12 09:05)", "## Brief (draft)")
        self.card.write_text(text, encoding="utf-8")
        self.assertIn("live-length", rules(self.lint().stdout, "WARN"))


# -------------------------------------------------------------------------- freeze

def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True, timeout=30)


class FreezeBase(unittest.TestCase):
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


class Freeze(FreezeBase):
    def test_brief_commits_only_card_paths(self):
        r = self.freeze()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertRegex(r.stdout, r"(?m)^committed [0-9a-f]+ \(brief search-export\)$")
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

    def test_failing_commit_unstages_and_self_reports(self):
        git(self.tmp, "config", "commit.gpgsign", "true")
        git(self.tmp, "config", "gpg.program", "false")
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


class FreezeAndIntegrity(FreezeBase):
    def test_stop_needs_and_resume_clears(self):
        self.assertEqual(self.freeze().returncode, 0)
        needs = "approve `python publish.py build/quotes.json` (recommendation: yes; settles the one publish)"
        r = run(["freeze", "search-export", "--stage", "stop", "--needs", needs], self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout)
        text = self.card.read_text(encoding="utf-8")
        self.assertIn("Needs you: " + needs, text)
        self.assertIn("State: waiting on you", text)
        self.assertEqual(run(["lint", "search-export"], self.tmp).returncode, 0)
        self.assertEqual(self.freeze("resume").returncode, 0)
        text = self.card.read_text(encoding="utf-8")
        self.assertIn("Needs you: nothing", text)
        self.assertIn("State: building", text)
        before = self.card.read_text(encoding="utf-8")
        for args in (["--stage", "stop", "--needs", "just a question"], ["--stage", "debrief", "--needs", needs]):
            r = run(["freeze", "search-export", *args], self.tmp)
            self.assertEqual(r.returncode, 2, r.stdout)
        self.assertEqual(self.card.read_text(encoding="utf-8"), before)

    def test_brief_freeze_initialises_and_prints_gitignore_lines_once(self):
        r = self.freeze()
        self.assertIn("add to .gitignore:\n  .finding-unknowns/profile.md\n  .finding-unknowns/predictions-log.md\n", r.stdout)
        self.assertNotIn(".finding-unknowns/logs/", r.stdout)  # already in .gitignore
        self.assertTrue((self.tmp / ".finding-unknowns" / "profile.md").is_file())
        self.assertNotIn("gitignore", self.freeze().stdout)

    def test_fsmonitor_never_runs_and_commit_hooks_are_honoured(self):
        hooks = self.tmp / "person-hooks"
        hooks.mkdir()
        hook_flag, fsm_flag = self.tmp / "hook-ran", self.tmp / "fsmonitor-ran"
        (hooks / "pre-commit").write_text("#!/bin/sh\ntouch '%s'\n" % hook_flag, encoding="utf-8")
        (hooks / "pre-commit").chmod(0o755)
        git(self.tmp, "config", "core.hooksPath", str(hooks))
        git(self.tmp, "config", "core.fsmonitor", "touch '%s'; false" % fsm_flag)
        self.assertEqual(self.freeze().returncode, 0)
        self.assertEqual(run(["integrity", "search-export"], self.tmp).returncode, 1)
        self.assertTrue(hook_flag.exists())
        self.assertFalse(fsm_flag.exists())

    def test_failing_commit_hook_self_reports(self):
        hooks = self.tmp / "person-hooks"
        hooks.mkdir()
        (hooks / "pre-commit").write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        (hooks / "pre-commit").chmod(0o755)
        git(self.tmp, "config", "core.hooksPath", str(hooks))
        r = self.freeze()
        self.assertEqual(r.returncode, 3)
        self.assertEqual(git(self.tmp, "diff", "--cached", "--name-only").stdout, "")
        self.assertIn("Timing: self-reported", self.card.read_text(encoding="utf-8"))

    def test_commit_timeout_kills_the_hook_group_and_names_the_lock(self):
        import importlib.util
        hooks = self.tmp / "person-hooks"
        hooks.mkdir()
        (hooks / "pre-commit").write_text("#!/bin/sh\nsleep 31 &\nsleep 31\n", encoding="utf-8")
        (hooks / "pre-commit").chmod(0o755)
        git(self.tmp, "config", "core.hooksPath", str(hooks))
        spec = importlib.util.spec_from_file_location("fu_under_test", str(FU))
        fu = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fu)
        fu.GIT_COMMIT_TIMEOUT = 2
        import contextlib
        import io
        buf, cwd = io.StringIO(), os.getcwd()
        os.chdir(str(self.tmp))
        try:
            with contextlib.redirect_stdout(buf):
                code = fu.main(["freeze", "search-export", "--stage", "brief"])
        finally:
            os.chdir(cwd)
        self.assertEqual(code, 3)
        self.assertIn(".git/index.lock may remain; remove it if no git process is running", buf.getvalue())
        self.assertTrue((self.tmp / ".git" / "index.lock").exists())  # the killed git left it; the note says so
        self.assertEqual(subprocess.run(["pgrep", "-f", "^sleep 31"], capture_output=True).stdout, b"")  # hook group is gone

    def test_unlogged_hunks_need_the_full_relative_path(self):
        self.assertEqual(self.freeze().returncode, 0)
        (self.tmp / "docs").mkdir()
        (self.tmp / "docs" / "README.md").write_text("new\n", encoding="utf-8")
        deltas = self.card.with_name("search-export.deltas.md")
        deltas.write_text(deltas.read_text(encoding="utf-8")
                          + "D1 2026-11-12 11:30 deviation: touched README.md → README.md\n", encoding="utf-8")
        line = run(["integrity", "search-export"], self.tmp).stdout.splitlines()[2]
        self.assertIn("docs/README.md:1-1", line)

    def test_integrity_reports_check_files_created_after_the_freeze(self):
        text = self.card.read_text(encoding="utf-8").replace("Check files: none", "Check files: tests/test_new.py, tests/extra")
        self.card.write_text(text, encoding="utf-8")
        self.assertEqual(self.freeze().returncode, 0)
        (self.tmp / "tests" / "extra").mkdir(parents=True)
        (self.tmp / "tests" / "test_new.py").write_text("def test(): assert True\n", encoding="utf-8")
        (self.tmp / "tests" / "extra" / "t.py").write_text("x\n", encoding="utf-8")
        line = run(["integrity", "search-export"], self.tmp).stdout.splitlines()[1]
        self.assertEqual(line, "Check files: created after the freeze: tests/extra, tests/extra/t.py, tests/test_new.py")
        git(self.tmp, "add", "tests/test_new.py")
        line = run(["integrity", "search-export"], self.tmp).stdout.splitlines()[1]
        self.assertIn("created after the freeze:", line)
        self.assertIn("tests/test_new.py", line)
        self.assertNotIn("changed: tests/test_new.py", line)

    def test_unlogged_hunks_match_path_tokens_exactly(self):
        self.assertEqual(self.freeze().returncode, 0)
        (self.tmp / "a.py").write_text("new\n", encoding="utf-8")
        deltas = self.card.with_name("search-export.deltas.md")
        deltas.write_text(deltas.read_text(encoding="utf-8")
                          + "D1 2026-11-12 11:30 deviation: touched data.py and app.py. → data.py:3\n"
                          + "D2 2026-11-12 11:31 deviation: notes → ./notes.txt\n", encoding="utf-8")
        line = run(["integrity", "search-export"], self.tmp).stdout.splitlines()[2]
        self.assertEqual(line, "Unlogged hunks: a.py:1-1")  # `a.py` is inside `data.py`, but not a token

    def test_untracked_fifo_symlink_and_large_files_are_not_read(self):
        self.assertEqual(self.freeze().returncode, 0)
        os.mkfifo(str(self.tmp / "pipe"))
        os.symlink("/dev/zero", str(self.tmp / "zero-link"))
        with open(str(self.tmp / "big.bin"), "wb") as fh:
            fh.write(b"\n" * (6 * 1024 * 1024))
        r = run(["integrity", "search-export"], self.tmp)
        line = r.stdout.splitlines()[2]
        for name in ("big.bin:1-1", "zero-link:1-1"):
            self.assertIn(name, line)


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
        self.assertIn("lint FAIL in the frozen Brief or a whole-card cap", html)

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
        self.assertIn("You: 1 of 2 held · Agent: 5 of 5 held · the agent held every one: its predictions are likely too safe", r3.stdout)
        self.assertNotIn("?", r3.stdout.splitlines()[-1])

    def test_log_without_debrief_exits_1(self):
        r = run(["log", "search-export"], self.tmp)
        self.assertEqual(r.returncode, 1)
        self.assertIn("no Debrief", r.stdout)

    def test_init_keeps_keys_and_prints_gitignore_lines_once(self):
        r = run(["init", "--guard", "log"], self.tmp)
        self.assertEqual(r.returncode, 0)
        prof = (self.fu / "profile.md").read_text(encoding="utf-8")
        self.assertIn("guard: log", prof)
        self.assertIn("mode: ship", prof)
        self.assertNotIn("gitignore", r.stdout)  # profile.md existed: not the first time
        (self.fu / "profile.md").unlink()
        r = run(["init"], self.tmp)
        self.assertIn("add to .gitignore:", r.stdout)
        self.assertIn(".finding-unknowns/predictions-log.md", r.stdout)
        self.assertIn("guard: ask", (self.fu / "profile.md").read_text(encoding="utf-8"))  # plugin layout
        self.assertNotIn("gitignore", run(["init"], self.tmp).stdout)


class RenderSafety(Workspace):
    def test_index_href_is_quoted_and_pages_carry_a_csp(self):
        tasks = self.fu / "tasks"
        evil = 'javascript:alert(1)"x'
        text = (tasks / "search-export.md").read_text(encoding="utf-8").replace("# search-export", "# " + evil, 1)
        (tasks / (evil + ".md")).write_text(text, encoding="utf-8")
        (self.fu / "view").mkdir(exist_ok=True)
        (self.fu / "view" / (evil + ".html")).write_text("x", encoding="utf-8")
        self.assertEqual(run(["render", "quote-export"], self.tmp).returncode, 0)
        self.assertEqual(run(["render", "--list"], self.tmp).returncode, 0)
        index = (self.fu / "view" / "index.html").read_text(encoding="utf-8")
        hrefs = re.findall(r'href="([^"]*)"', index)
        self.assertTrue(hrefs)
        for h in hrefs:
            self.assertTrue(h.startswith("./"), h)
        self.assertIn('href="./javascript%3Aalert%281%29%22x.html"', index)
        csp = "<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; style-src 'unsafe-inline'; img-src data:\">"
        for page in ("index.html", "quote-export.html"):
            self.assertIn(csp, (self.fu / "view" / page).read_text(encoding="utf-8"))


class Packaging(unittest.TestCase):
    def test_marker_and_hook_config(self):
        self.assertIn("finding-unknowns", FU.read_text(encoding="utf-8").splitlines()[1])
        cfg = json.loads((REPO / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        self.assertEqual(sorted(cfg["hooks"]), ["PostToolUse", "PostToolUseFailure", "PreToolUse"])
        for event, phase in (("PreToolUse", "pre"), ("PostToolUse", "post"), ("PostToolUseFailure", "post")):
            entry = cfg["hooks"][event][0]
            self.assertEqual(entry["matcher"], "Bash")
            script = '"${CLAUDE_PLUGIN_ROOT}/scripts/fu.py" guard %s 2>/dev/null' % phase
            self.assertEqual(entry["hooks"][0]["command"], "python3 %s || python %s || true" % (script, script))

    def test_install_never_removes_or_follows_what_is_not_ours(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            ktr = tmp / "skills" / "keep-the-reasoning"
            ktr.mkdir(parents=True)
            (ktr / "SKILL.md").write_text("---\nname: keep-the-reasoning\ndescription: finding-unknowns fan\n---\n", encoding="utf-8")
            cmds = tmp / "commands"
            cmds.mkdir()
            (cmds / "fu-view.md").write_text("my own fu-view, mentions finding-unknowns\n", encoding="utf-8")
            (cmds / "keep-the-reasoning.md").write_text("---\nSkill tool keep-the-reasoning SKILL.md\n---\n", encoding="utf-8")
            outside = tmp / "outside.md"
            outside.write_text("victim\n", encoding="utf-8")
            (tmp / "agents").mkdir()
            os.symlink(str(outside), str(tmp / "agents" / "mechanism-auditor.md"))
            old_ours = cmds / "fu-debrief.md"
            old_ours.write_text("---\n#finding-unknowns:plugin-file\nold\n---\n", encoding="utf-8")
            r = subprocess.run(["bash", str(REPO / "install.sh")], env=dict(os.environ, CLAUDE_CONFIG_DIR=str(tmp)),
                               capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("name: keep-the-reasoning", (ktr / "SKILL.md").read_text(encoding="utf-8"))
            self.assertTrue((cmds / "keep-the-reasoning.md").is_file())
            self.assertEqual(outside.read_text(encoding="utf-8"), "victim\n")
            self.assertFalse((tmp / "agents" / "mechanism-auditor.md").is_symlink())
            baks = list(cmds.glob("fu-view.md.bak.*"))
            self.assertEqual(len(baks), 1)
            self.assertEqual(baks[0].read_text(encoding="utf-8"), "my own fu-view, mentions finding-unknowns\n")
            self.assertEqual(list(cmds.glob("fu-debrief.md.bak*")), [])  # ours: replaced in place
            self.assertEqual(old_ours.read_text(encoding="utf-8"), (REPO / "commands" / "fu-debrief.md").read_text(encoding="utf-8"))
            proj = tmp / "proj"
            proj.mkdir()
            run_installed = subprocess.run([sys.executable, str(tmp / "scripts" / "fu.py"), "init"], cwd=str(proj),
                                           capture_output=True, text=True, timeout=60)
            self.assertEqual(run_installed.returncode, 0)
            self.assertIn("guard: off", (proj / ".finding-unknowns" / "profile.md").read_text(encoding="utf-8"))
        finally:
            shutil.rmtree(tmp)

    def test_guard_installed_needs_our_hook_in_the_file(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("fu_installed", str(FU))
        fu = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fu)
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / "scripts").mkdir()
            (tmp / "hooks").mkdir()
            fu.__file__ = str(tmp / "scripts" / "fu.py")
            self.assertFalse(fu.guard_installed())
            (tmp / "hooks" / "hooks.json").write_text('{"hooks": {"Stop": []}}', encoding="utf-8")
            self.assertFalse(fu.guard_installed())
            shutil.copy(str(REPO / "hooks" / "hooks.json"), str(tmp / "hooks" / "hooks.json"))
            self.assertTrue(fu.guard_installed())
        finally:
            shutil.rmtree(tmp)

    def test_install_lists_unmarked_legacy_files_and_keeps_them(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / "agents").mkdir()
            legacy = tmp / "agents" / "blindspot-scout.md"
            legacy.write_text("---\nname: blindspot-scout\n---\n", encoding="utf-8")
            r = subprocess.run(["bash", str(REPO / "install.sh")], env=dict(os.environ, CLAUDE_CONFIG_DIR=str(tmp)),
                               capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(legacy.is_file())
            lines = [l for l in r.stdout.splitlines() if "Legacy file left in place" in l]
            self.assertEqual(len(lines), 1, r.stdout)
            self.assertIn(str(legacy), lines[0])
        finally:
            shutil.rmtree(tmp)

    def test_bin_fu_works_through_a_symlink(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            os.symlink(str(REPO / "bin" / "fu"), str(tmp / "fu"))
            r = subprocess.run(["sh", str(tmp / "fu"), "--help"], capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)
        finally:
            shutil.rmtree(tmp)

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
