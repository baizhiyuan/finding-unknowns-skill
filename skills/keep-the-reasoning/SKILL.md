---
name: keep-the-reasoning
description: "Use when starting or handing back agent work whose consequences fall on others; on ship/no-ship, migration or money decisions; or when the user says 'keep me honest', 'review this with me', 'what did you assume', 'what didn't you check'. Defines 'verified' first; hands back a stakes-triaged, evidence-first packet. Not for cheap, reversible tasks."
aliases: []
metadata:
  credits:
    source: "Addy Osmani — Critical thinking when agents do the work (Nov 2026)"
    url: "https://x.com/addyosmani/status/2117512471930167377"
    cognitive-surrender: "Shaw & Nave, Thinking—Fast, Slow, and Artificial (SSRN 6097646)"
    cognitive-debt: "Margaret-Anne Storey"
    sibling: "finding-unknowns (this repository) — the pre-work half"
---

# Keep the Reasoning

*Distilled from Addy Osmani's "Critical thinking when agents do the work"
(https://x.com/addyosmani/status/2117512471930167377). Community skill; not affiliated
with or endorsed by Anthropic.*

<Purpose>
Agents now produce fast, mostly-correct work, and mostly-correct work does not demand a
second look. Across many handoffs the human slides down a spectrum — **offloading**
(delegate the work, keep ownership) → **deferral** (the output stops being a claim to check
and becomes the next input) → **cognitive surrender** (the output quietly becomes your
own; you feel no need to check it). Nothing in an agentic workflow pushes back on that
slide by default. This skill is the push-back, applied at the one moment it is cheap:
the handoff. The agent cannot think for the user, but it can make thinking cheap and
surrender visible. *Take the handoff where being wrong is cheap; keep the reasoning where
others will have to deal with the consequences.*
</Purpose>

<Use_When>
- Delivering non-trivial agent work for the user to accept: a PR, an analysis, a report,
  a migration plan, a recommendation
- The user asks a high-consequence question — what to build, whether it is safe to ship,
  where money goes, anything whose consequences fall on other people
- A long or autonomous run is ending and the user will review its output cold
- The user says "keep me honest", "am I rubber-stamping this", "review this with me",
  "what did you assume", or "what didn't you check"
- Closing out `finding-unknowns` Phase 3, or a Cartographer build at merge (including
  its experimental Phase E, when run)
</Use_When>

<Do_Not_Use_When>
- Being wrong is cheap and reversible (picking a hotel, renaming a local variable, a
  throwaway script) — hand off fully; one line saying so is enough
- The risk is unknowns in the spec rather than acceptance of the output — use
  `finding-unknowns` (its Phase 3 and Cartographer's merge hand back here)
- The user explicitly says "just ship it" — make the top risk visible once (≤3 lines),
  then respect the exit
</Do_Not_Use_When>

<Execution_Policy>
- Triage stakes first; the packet scales with consequence, not with effort spent
- Evidence before summary, always. A summary read first anchors everything after it
- Never fabricate evidence. A check that was not run is reported as "not run"
- "Nothing unchecked" is never a valid entry — every handoff names at least one thing
  that was not verified
- Name surrender signals once, plainly, without moralizing; then let the user decide
- On high-consequence decisions the agent recommends, labelled as a recommendation; the
  user decides. Never present a judgment call as settled fact
- Fresh context for self-critique: the context that produced the work does not grade it
  (the fresh-context refutation primitive, below)
- Artifacts: a packet written to disk goes to `.finding-unknowns/handoff-{slug}.md` at the
  project root — working state, gitignored by default (`finding-unknowns`
  Execution_Policy has the `.gitignore` lines, including how to re-include files the
  team reviews in PRs)
</Execution_Policy>

<Fresh_Context_Refutation>
## Fresh-context refutation (shared primitive)

One instrument, defined here and reused by name across these skills. A
context that did not produce the claim (a subagent; a different model when available)
tries to refute it from the same evidence, and returns two things: the **strongest
alternative explanation** that fits that evidence, and the **cheapest discriminating
check** that would tell the two apart. It reads the evidence the claim used and changes
nothing. Without a separate context, run it yourself and label the result
`same-context — weaker`; never skip it.

Here it fills the full packet's Strongest counterargument and Did I miss anything?
sections. The same primitive, with its own mechanics on top, is `theory-vs-result`'s
Fresh_Context_Check (`mechanism-auditor`), Cartographer's C1 step 3.5 adversarial check,
and the `fu-verify-panel` workflow (three refuters with distinct lenses).
</Fresh_Context_Refutation>

<Steps>

## Step 0: Stakes triage (blocking)

| Packet size | Signals | Handoff |
|-------------|---------|---------|
| **Offload** | cheap to be wrong, reversible, consequences land only on the user | normal handoff + one line: "Low stakes — delegated fully." |
| **Compact** — keep the reasoning (medium stakes) | consequences land on others, but the change is reversible and contained (a PR to shared code behind tests, an internal analysis) | Steps 1–4 below, compact packet |
| **Full** — keep the reasoning (high stakes) | hard to reverse; production, money, safety, people; "what should we build", "is it safe to ship" | Steps 1–4 below, full nine-section packet |

Announce: `Packet size: {offload | compact | full} — {one-line reason}`.
The user can ask for the full packet at any stakes; when unsure between compact and full,
choose full.

## Step 1: Before the work (front end)

1. **Prior first.** Ask the user, in one skippable question, what they expect the
   answer or outcome to be — or infer it from the request and state it back. "No idea"
   is a valid answer and means the user lacks a map: route to `finding-unknowns`
   (Technique 1, blind-spot pass) before proceeding. Record the prior; Step 3 compares
   against it. A prior already recorded in this session by `finding-unknowns` (Phase 0
   or a ledger row's `prior:`) or `theory-vs-result` (a prediction card) is reused,
   never asked again.
2. **Define "verified" up front.** Before doing the work, write the verification
   contract — per claim the handoff will make: the check, the artifact it produces
   (test, screenshot, log, trace), what it proves, and what it does NOT prove. After the
   fact, any outcome can be rationalized. A check must be able to fail: "looks good",
   "no errors were raised", and "the model is confident" are not checks.
3. **Brief check (intent debt).** If the brief lacks audience, out-of-scope, or a
   definition of done, ask instead of silently filling the gap — an agent that fills
   gaps rather than challenging a fuzzy request accumulates intent debt. After two failed
   rounds of correction, recommend rewriting the brief rather than tweaking it again.

Skip Step 1 when the work is already done and only the handoff remains; say so in the
packet ("verification defined after the fact — weaker evidence").

**When `finding-unknowns` already ran**, do not repeat it: its recorded priors satisfy
Step 1 item 1, its plan's Definition of verified or its spec's verification contract
satisfies item 2, and the packet's Decisions & assumptions section links the quiz-master
report's Decisions & assumptions instead of re-listing them. Cartographer's merge always
gets the full packet: Cartographer is high stakes by definition.

## Step 2: During the work

- Log decisions and assumptions at the moment they are made: defaults chosen, scope cut,
  requirements reinterpreted, alternatives rejected. When `finding-unknowns` is active,
  this is Technique 6; when `oh-my-claudecode:show-me-your-work` is installed, its
  decision trail serves.
- Reason from sources, not from summaries of summaries. If a step relied on another
  agent's summary rather than the original material, mark it — the packet must say so.
- Keep the executed commands and their raw outputs; Step 3 shows them first.

## Step 3: The handoff packet (the core deliverable)

Both sizes hold the order rule: **evidence first, summary last**.

**Compact packet (medium stakes).** Deliver in exactly this order:

```
Packet size: compact — {reason}

1. Evidence            — the commands actually executed and their actual output
                         (trimmed, not paraphrased); artifacts by path. When a
                         quiz ran, link the quiz report here.
2. What the checks did NOT prove
                       — one line per check; flag same-context checks.
3. Not checked         — at least one thing nobody verified. Never empty.
4. Summary             — last, and short.
```

When a prior was recorded or the claim is measured, add a **Prior vs result** line before
the Summary: the prior against what came back (for measured claims, the
`theory-vs-result` summary table). Sections are referred to by name, not number, because
the two packet sizes number them differently.

Switch to the full packet when the user asks for it, or when the work turns out to touch
anything in the high-stakes row of Step 0.

**Full packet (high stakes, or on request).** Deliver in exactly this order. Scale each
section to the stakes; omit none.

```
Packet size: full — {reason}

1. Evidence            — the commands actually executed and their actual output
                         (trimmed, not paraphrased); artifacts by path. Before any summary.
2. What the checks proved / did NOT prove
                       — one line each per contract check. Flag same-context checks:
                         a test written by the context that wrote the code can share
                         its mistake and still pass.
3. Decisions & assumptions
                       — defaults chosen, scope cut, requirements reinterpreted,
                         sources summarized rather than read — each with where to look.
4. Prior vs result     — the user's prior against what came back; every mismatch
                         is where to look hardest. For measured claims, use the
                         `theory-vs-result` summary table here instead of rewriting it.
5. Strongest counterargument
                       — fresh-context refutation (the shared primitive above):
                         "what would have to be true for this to be wrong?", the
                         cheapest check that would tell, and whether it was run.
6. Did I miss anything? — the fresh context's answer to that question, verbatim-short.
7. Not checked         — at least one thing nobody verified. Never empty.
8. Answerability       — "Would you bet on this in front of whoever maintains it?"
                         For code, offer the comprehension quiz (`/change-quiz`,
                         finding-unknowns Technique 8) when the change is large.
9. Summary             — last, and short.
```

Strongest counterargument and Did I miss anything? come from one fresh-context
refutation (the shared primitive): a context that did not produce the work. Without
subagents, write them yourself but label them `same-context — weaker`; never skip them.

For high-consequence decisions (what to build, ship or not, who it affects, what to
sacrifice) the Summary becomes **Options and recommendation**: 2–3 options with trade-offs
and a labelled recommendation. The decision line is left for the user.

## Step 4: After the handoff

- **Rejection becomes a rule.** When the user rejects something, offer to encode the
  reason where it will fire next time — a test, a hook, a lint rule, project config —
  rather than in memory. (`oh-my-claudecode:correct` does this when installed.) That is
  how taste compounds.
- **Orchestration tax.** If agents are producing more than the user can stand behind —
  several large unreviewed changes pending, approvals arriving faster than a read takes —
  say so once and recommend tightening checks or slowing down rather than starting
  another session. Producing more than you can review is no longer reviewing; it is
  hoping.

</Steps>

<Surrender_Signals>
Name the signal once, plainly, then let the user decide:

- Approval of a large change with no question about any listed decision or unchecked
  item, especially in the same turn the packet was delivered
- The agent's own tests offered as the only evidence for the agent's own code
- The user asking the agent to decide a high-consequence question outright
- A chain where the agent is reasoning from another agent's summary of the source
- "Just tell me what to do" on a decision whose consequences fall on other people
</Surrender_Signals>

<Practice_Mode>
Opt-in only — offer it when the user asks about skill atrophy, never unprompted.

- **Inventory**: list what the user has stopped doing by hand in the last month; for
  each, ask whether the drop was intentional. Dropping a skill on purpose is fine;
  losing it by drift is not.
- **Calibration**: suggest one small task to do without an agent this week, chosen from
  the inventory, then compare the result against what the agent would have produced.
- **Prediction habit**: before asking, write down what you expect; afterwards, write
  down one thing the agent did not check.
</Practice_Mode>

<Examples>
<Good>
```
Packet size: full — schema migration on a shared production table.
1. Evidence: `pytest tests/migrations -q` → 14 passed; `alembic upgrade head --sql` →
   plan at artifacts/upgrade.sql (ALTER + backfill, 2 statements)
2. Proved: upgrade SQL applies cleanly to an empty schema. NOT proved: runtime on the
   41M-row table; lock behaviour under write load. Tests written in this session.
3. Decisions: backfill default = 'unknown' (spec silent); downgrade drops the column
   (data loss) — see migrations/0042.py:31
4. Your prior: "a quick additive change". Mismatch: the backfill rewrites every row.
5. Counterargument (fresh subagent): if writes continue during backfill, the table lock
   stalls checkout. Not checked.
6. Missed: the replica lag alert threshold.
7. Not checked: lock duration at production size; replica lag.
8. Would you bet on this in front of the on-call? If not: run it on the staging snapshot.
9. Summary: migration is correct on small data; production behaviour unverified.
```
Why good: evidence first, the checks' limits stated, the decision that changes the risk
picture (backfill semantics) surfaced, and the prior mismatch points straight at it.
</Good>

<Good>
```
Packet size: compact — refactor of a shared date helper, behind tests.
1. Evidence: `npm test -- dates` → 38 passed; diff touches src/utils/dates.ts only
2. Did NOT prove: behaviour in the 3 callers outside src/ (no tests there). Tests
   written in this session.
3. Not checked: timezone handling in reports/export.ts.
4. Summary: helper refactored; callers outside src/ unverified.
```
Why good: medium stakes get four sections, not nine — and still evidence first, the
checks' limits, a non-empty "Not checked", summary last.
</Good>

<Bad>
```
Done! The migration is ready and all tests pass ✅. Let me know if you want any changes.
```
Why bad: summary only, a green check presented as proof of a property it never tested,
no decisions surfaced, nothing named as unchecked — an invitation to surrender.
</Bad>

<Bad>
Lecturing on every handoff: "Remember, you must think critically about AI output…"
Why bad: moralizing trains the user to skip the packet. Name a signal once, with
evidence, and move on.
</Bad>
</Examples>

<Final_Checklist>
- [ ] Packet size announced before anything else (offload | compact | full)
- [ ] Prior captured (or "no idea" routed to a blind-spot pass)
- [ ] Verification contract existed before the work, or its absence was stated
- [ ] Packet order held: evidence first, summary last (both sizes)
- [ ] Every check states what it did NOT prove; same-context checks flagged
- [ ] Full packet: decisions & assumptions listed with where to look
- [ ] Full packet: counterargument and "did I miss anything" came from a fresh-context
      refutation (or were labelled `same-context — weaker`)
- [ ] "Not checked" is non-empty
- [ ] High-consequence decisions left with the user, recommendation labelled as such
</Final_Checklist>

<Relationship_To_Sibling_Tooling>
- `finding-unknowns` (this repository) covers the front of the work — the unknowns in
  the spec. This skill covers the back — the human's judgment at acceptance.
  Cartographer offers the full packet at merge; its experimental Phase E, when run, routes
  the irreversible lane and final merge here.
- `oh-my-claudecode:verify` makes the agent prove a behaviour; this skill makes the proof
  legible and its limits explicit to the human. Use both.
- `oh-my-claudecode:interrogate` is a stronger fresh-context counterargument (the
  packet's Strongest counterargument) for code changes when installed.
- `oh-my-claudecode:show-me-your-work` supplies Decisions & assumptions for long
  autonomous runs.
- `oh-my-claudecode:teach` paces learning; `/change-quiz` gates merge on comprehension.
- `theory-vs-result` (this repository) supplies Prior vs result for measured claims
  (backtests, benchmarks, A/B tests): Theory → Measured → Consistent? → Mechanism.
</Relationship_To_Sibling_Tooling>
