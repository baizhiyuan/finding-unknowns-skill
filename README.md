<p align="center">
  <img src="assets/hero.svg" alt="finding-unknowns v4.1.0 — map the territory before you build; keep the reasoning when agents hand the work back" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-D97757?style=for-the-badge&labelColor=F0EEE6" alt="Claude Code plugin">
  <img src="https://img.shields.io/badge/version-4.1.0-C15F3C?style=for-the-badge&labelColor=F0EEE6" alt="version 4.1.0">
  <img src="https://img.shields.io/badge/skills-3-D4A27F?style=for-the-badge&labelColor=F0EEE6" alt="3 skills">
  <img src="https://img.shields.io/badge/agents-5-C15F3C?style=for-the-badge&labelColor=F0EEE6" alt="5 agents">
  <img src="https://img.shields.io/badge/license-MIT-788C5D?style=for-the-badge&labelColor=F0EEE6" alt="MIT license">
</p>

<p align="center"><strong>Surface your unknowns before they get expensive — and keep your judgment when agents hand the work back.</strong></p>

<p align="center"><em>The map is not the territory. The quality of long-horizon work is bounded by how well you clarify your unknowns.</em></p>

<p align="center">
  <a href="#quick-start">Get started</a> ·
  <a href="#features">How it works</a> ·
  <a href="#commands">Commands</a> ·
  <a href="#documentation">Docs</a> ·
  <a href="README.zh.md">中文</a>
</p>

---

## Quick Start

**Step 1: Install**

Plugin marketplace (recommended). These are Claude Code slash commands — enter them **one at a time**:

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
```

Then:

```
/plugin install finding-unknowns@finding-unknowns-skill
```

Prefer a clone? `install.sh` installs all three skills, `references/`, the five agents, and the slash commands:

```bash
git clone https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill && bash install.sh
```

No install at all? Copy [`CLAUDE.md`](CLAUDE.md) into a project root for lightweight, always-on guidance.

<details>
<summary><b>Manual copy (skills only)</b></summary>

```bash
mkdir -p ~/.claude/skills/finding-unknowns/references ~/.claude/skills/keep-the-reasoning ~/.claude/skills/theory-vs-result
cp skills/finding-unknowns/SKILL.md ~/.claude/skills/finding-unknowns/
cp skills/finding-unknowns/references/*.md ~/.claude/skills/finding-unknowns/references/
cp skills/keep-the-reasoning/SKILL.md ~/.claude/skills/keep-the-reasoning/
cp skills/theory-vs-result/SKILL.md ~/.claude/skills/theory-vs-result/
```

</details>

**Step 2: First use**

```
/finding-unknowns "add a usage dashboard to the admin app"   # locate the unknown, announce the route, run the technique
/blindspot "src/auth"                                        # read-only recon: landmines, hidden context, expert questions
/change-quiz main..HEAD                                      # change report + must-pass comprehension quiz before merge
```

### Not Sure Where to Start?

If the task is vague, or you're new to the domain or codebase:

```
/finding-unknowns "I want to …"
```

Phase 0 places the gap on the quadrant map, captures your prior, and routes to the cheapest technique that clears it — or says plainly that there are no significant unknowns.

- **High stakes** (hard to reverse, wide blast radius, unfamiliar territory + long horizon) → `/cartographer --deep "…"`
- **Work is done, the risk is accepting it** → `/keep-the-reasoning "…"`
- **A result is in (or about to be measured), the risk is misreading it** → `/theory-vs-result "…"`

### Updating

Update the same way you installed. Latest release: **v4.1.0**.

```
/plugin marketplace update finding-unknowns-skill
```

```
/plugin update finding-unknowns@finding-unknowns-skill
```

<details>
<summary><b>Clone-and-install, manual copy, and version check</b></summary>

**Clone** — `install.sh` overwrites in place, so it doubles as the updater:

```bash
cd finding-unknowns-skill && git pull origin main && bash install.sh
```

**Manual copy** — overwrite the same files. `references/` carries the Cartographer protocol and the Workflow templates and must be updated too; v4 added the `keep-the-reasoning` skill and v4.1 adds `theory-vs-result`.

```bash
cd finding-unknowns-skill && git pull origin main
mkdir -p ~/.claude/skills/finding-unknowns/references ~/.claude/skills/keep-the-reasoning ~/.claude/skills/theory-vs-result
cp skills/finding-unknowns/SKILL.md ~/.claude/skills/finding-unknowns/
cp skills/finding-unknowns/references/*.md ~/.claude/skills/finding-unknowns/references/
cp skills/keep-the-reasoning/SKILL.md ~/.claude/skills/keep-the-reasoning/
cp skills/theory-vs-result/SKILL.md ~/.claude/skills/theory-vs-result/
cp agents/*.md   ~/.claude/agents/
cp commands/*.md ~/.claude/commands/
```

**Verify:**

```bash
grep '"version"' ~/.claude/plugins/*/finding-unknowns*/.claude-plugin/plugin.json 2>/dev/null \
  || ls ~/.claude/skills/finding-unknowns/references/cartographer.md ~/.claude/skills/keep-the-reasoning/SKILL.md ~/.claude/skills/theory-vs-result/SKILL.md
# expect: 4.1.0 (plugin) — or all three files listed (theory-vs-result exists only from v4.1.0 on)
```

</details>

---

## Why finding-unknowns?

- **The map is not the territory** — the map is what you give Claude (prompt, context, skills); the territory is the codebase and the real world. Every gap between them forces the model to guess your intent. Capability is no longer the bottleneck on long-horizon work; clarity is.
- **Route by quadrant, not by habit** — blind spots need reconnaissance, tacit taste needs prototypes, nameable gaps need targeted questions, comprehension needs examination. One uniform interview under-serves all four.
- **Coverage-gated Cartographer mode** — for high stakes: a regret-ordered unknowns ledger, clarity scores shown every round, and a seven-condition gate that won't let implementation start while the territory is unmapped.
- **Irreversibility floor** — gate on blast radius, not confidence. An unknown guarding an irreversible step always reaches you, however confident the evidence looks.
- **Keep the reasoning at the handoff** — an evidence-first packet that says what each check did NOT prove and what went unchecked, so accepting agent work never slides into cognitive surrender.
- **Theory before data** — every measured result arrives as Theory → Measured → Consistent? → Mechanism: the prediction written first, the noise floor stated, the mechanism tagged with how well it is evidenced, and the rule verdict kept apart from the verdict on the idea.
- **Independent judgment** — the author never self-approves. Discovery, scoring, and examination run in contexts that did not do the implementing.
- **Zero dependencies** — plain Markdown. Agents and Workflow scripts add depth; every technique also runs fully inline.

> **Attribution.** The techniques and their names come from Thariq Shihipar's essay _"A Field Guide to Fable: Finding Your Unknowns"_ ([@trq212](https://x.com/trq212/status/2073100352921215386)); credit for the underlying ideas belongs to the original author, and this repository packages them as an installable Claude Code plugin. `keep-the-reasoning` is distilled from Addy Osmani's _"Critical thinking when agents do the work"_ ([source](https://x.com/addyosmani/status/2117512471930167377)): across many handoffs the human slides from **offloading** (delegate, keep ownership) → **deferral** (the output becomes the next input) → **cognitive surrender** (the output quietly becomes your own). `theory-vs-result` is distilled from the author's own empirical research practice and generalized for any measured claim: a number is not a finding until you know what was expected, whether the gap beats noise, and why it came out that way.

---

## Features

### The three skills

| Skill | What it is | Use for |
|-------|------------|---------|
| **`finding-unknowns`** | Phase 0 quadrant routing → eight techniques → optional Cartographer mode | Before and during work: surfacing the unknowns that would otherwise become guesses |
| **`keep-the-reasoning`** | Stakes triage, "verified" defined up front, a fixed-order handoff packet | The handoff: accepting agent work without surrendering judgment |
| **`theory-vs-result`** | Prediction card first, then Theory → Measured → Consistent? → Mechanism cards, with two separate verdicts | Measured results: backtests, benchmarks, A/B tests, ablations, training runs — never a number without its prediction and its reason |

`finding-unknowns` hands over to `keep-the-reasoning` at the end of Phase 3 and of the Cartographer execution bridge. Returning `experiment`-route results are reported through `theory-vs-result`, whose summary table also serves as the handoff packet's "prior vs result" section.

### The eight techniques

<p align="center">
  <img src="assets/lifecycle.svg" alt="Lifecycle: three windows to catch unknowns — pre, during, post — with the techniques that run in each and the handoff at the end" width="92%">
</p>

Phase 0 is blocking: classify the gap, capture your prior in one line, announce the route — then run a technique.

<p align="center">
  <img src="assets/quadrants.svg" alt="The four quadrants: known knowns, known unknowns, unknown knowns, unknown unknowns — each mapped to its techniques" width="78%">
</p>

| Technique | Phase | Quadrant | Use for |
|-----------|-------|----------|---------|
| **1 · Blind-spot pass** | Pre | UU | Unknown unknowns in a new domain or codebase |
| **2 · Brainstorm & prototype** | Pre | UK | "I'll know it when I see it" |
| **3 · Interview** | Pre | KU | Nameable gaps — up to 3 independent questions per round; dependent questions wait for the next round |
| **4 · References** | Pre | UK | When you can't describe it — point at code |
| **5 · Implementation plan** | Pre | KU | Expensive-to-change decisions first, plus a definition of "verified" |
| **6 · Implementation notes** | During | — | Deviations and edge cases, logged as they happen |
| **7 · Pitch & explainer** | Post | — | Buy-in and approvals |
| **8 · Quiz** | Post | UU (post-hoc) | Comprehension check before merge |

Known knowns just get written down before they drift. Full procedures: [`SKILL.md`](skills/finding-unknowns/SKILL.md).

### Cartographer mode

The rigorous escalation for high-stakes work. Full protocol: [`references/cartographer.md`](skills/finding-unknowns/references/cartographer.md), read on demand.

<p align="center">
  <img src="assets/cartographer.svg" alt="Cartographer mode: Round 0 topology, seeded unknowns ledger, regret-ordered clearing loop by route, per-round quadrant scores, dual gate with irreversibility floor, approval-gated execution bridge" width="96%">
</p>

| Part | What it is | Use for |
|------|------------|---------|
| **Unknowns ledger** | Rows with quadrant, prior, `regret = cost-if-wrong × P(wrong)`, route (interview · territory · experiment · audit), reversibility (reversible · wide · irreversible) | Ordering the work; it *is* the resume state |
| **Clearing loop** | A router, not an interview: clear the highest-regret open row by its route; adversarially verify cost ≥ 4 resolutions | Never asking the user what the territory can answer |
| **Clarity scores** | `ambiguity = 1 − (KK×0.20 + KU×0.25 + UK×0.25 + UU×0.30)`, re-scored every round, threshold 0.25 by default | Letting you see and steer how clear the map is |
| **Dual gate** | Coverage (every quadrant probed) AND clarity, plus the irreversibility floor; completeness critic before any PASS | Refusing to build on an unmapped territory |
| **Execution bridge** | Approval-gated: independent planner + reviewer consensus, or Workflow execution | Building from a crystallized, pending-approval spec |

**Flow:** threshold announced → Round 0 topology (1–6 components) → **C0** seed from all four quadrants + a domain checklist → **C1** clear by route → **C2** dual gate → **C2.5** close-out report + crystallized spec → **E** execution bridge → **C3** the ledger stays open through the build and feeds the quiz.

**New in v4.0.0**

- **Irreversibility floor** — regret contains P(wrong), a confidence estimate. For `irreversible` rows confidence never substitutes for the user: never silently defaulted under the regret bar, resolved only with recorded user confirmation. The seventh gate condition; no exit waives it.
- **Priors and surprises** — each row records the expectation held before evidence-based scoring; contradictions surface as surprises.
- **Verification contract** — per criterion: a failable check, its artifact, what it proves, what it does NOT prove, and its lane. Locked against the implementer.
- **Phase E execution rules** — the loop lives inside a task, the graph between tasks; edges name what crosses; failures return `UNIT · VERDICT · REASON · EVIDENCE · SCOPE`; an attempt cap turns a task into a plan-suspect row; a learning edge feeds derived constraints forward; tasks close by reversibility lane on results from a separate check-runner. The human sits at both ends — spec, contract, and task graph at the front; irreversible lane and merge at the back.

### Execution & orchestration

When the host exposes Claude Code's **Workflow tool** and you opt in, the fan-out-heavy operations run as deterministic scripts from [`references/workflows.md`](skills/finding-unknowns/references/workflows.md).

<p align="center">
  <img src="assets/workflows.svg" alt="Workflow orchestration: multi-lens sweep with pipelined verification, three-lens refutation panel, UU loop-until-dry, cross-validated execution, and the three-rung fallback ladder" width="96%">
</p>

| Template | What it is | Use for |
|----------|------------|---------|
| **`fu-multi-lens-sweep`** | Parallel lens scouts; each finding adversarially verified as its lens completes (no barrier); schema-validated ledger rows | Seeding UU rows at high stakes |
| **`fu-verify-panel`** | Three refuters: alternative explanation / evidence independence / reproduction | Cost ≥ 4 resolutions |
| **`fu-uu-until-dry`** | UU probe loop that stops after two consecutive dry rounds | Probing the shallowest quadrant — bounded by information, not a count |
| **`fu-execute-verified`** | Approved execution under Phase E rules; every implementer paired with an independent refute-framed verifier | Running the approved task graph |

**Fallback ladder:** Workflow → parallel Agent calls → fully inline. The logic is normative; the mechanism is not. With no subagents at all, implementer and verifier would share a context, so no lane closes automatically — every task comes to you as `awaiting-human`.

**Enforced in code vs by prompt — stated honestly.**

| In `fu-execute-verified` | Enforcement |
|--------------------------|-------------|
| Fail-closed argument validation; no silent edge drops; per-task scheduling; path locks (paths normalized, globs rejected); lane-based closing; check results matched to contract checks by exact string | code |
| Out-of-scope writes stop the run; check-file hashes compared against a pre-run baseline; tampered check files stop the task | code compares — the check-runner's report is prompted |
| Concurrent tasks' edits attributed to the right task; implementer never executes irreversible actions; runner refuses irreversible checks | prompted |
| Verifier independence | structural |

### Keep the reasoning

<p align="center">
  <img src="assets/handoff.svg" alt="keep-the-reasoning: the offloading → deferral → cognitive-surrender spectrum, and the fixed-order handoff packet from evidence to summary" width="96%">
</p>

| Step | What it is | Use for |
|------|------------|---------|
| **Stakes triage** | `offload` (cheap, reversible, lands only on you) vs `keep-the-reasoning` (lands on others, hard to reverse) | Scaling the packet to consequence, not effort |
| **Before the work** | Capture your hypothesis; define "verified" — a check must be able to fail | Making any outcome un-rationalizable after the fact |
| **Handoff packet** | Evidence first → what checks proved / did NOT prove → decisions & assumptions → prior vs result → fresh-context counterargument → never-empty "not checked" → summary last | Accepting work with your judgment intact |
| **After the handoff** | A rejection becomes a rule (test, hook, lint rule); surrender signals named once, without moralizing | Making taste compound |

When `finding-unknowns` already ran, `keep-the-reasoning` reuses its priors, verification contract, and the quiz-master's Decisions & assumptions instead of repeating them.

### Theory vs result

| Step | What it is | Use for |
|------|------------|---------|
| **Result triage** | `note` (one number, nothing rides on it) · `report` (someone will act on it, or it misses) · `decision` (adopt/ship, a pre-agreed rule, money) | Scaling the card to what rides on the number |
| **Prediction card** | Claim, mechanism chain, direction + magnitude + *where* it should show, noise floor, falsifier, decision rule, and when it was written; saved before the data. A card written after the result is a `post-hoc fit`, not a test | Giving a result something to disagree with |
| **Fair measurement** | Matched baseline, one variable changed, same seeds, the metric you are actually paid for, data budget respected | Not crediting a change with what the sample did |
| **Result card** | Theory → Measured → Consistent? → Mechanism (理论预期 → 实测 → 是否一致 → 机理); consistency is `consistent` · `partly` · `inconsistent` · `can't tell`, read from the interval (one that holds both 0 and the prediction is `can't tell`); mechanism tier is `verified` · `supported` · `inferred` · `untested` | Keeping facts, inferences, and untested stories visibly apart |
| **Mismatch walk** | Pipeline → comparison → metric → theory → environment; name the broken link and the smallest check that separates the explanations | Neither dismissing a direction on one run nor rescuing it with a story |
| **Two verdicts** | Rule verdict (in the rule's own labels, e.g. `PASS` · `FAIL` · `UNCERTAIN`, or `descriptive only` / `void`) vs direction verdict (`alive` · `alive-but-constrained` · `weakened` · `dead`) | A mechanism can keep a direction alive; neither a mechanism nor a rerun on spent data turns a `FAIL` into a `PASS`. A defect found afterwards voids the run instead |

A new or tightened threshold is first explained in plain language — what it protects against, why this number, what failing it means — and frozen only after you approve; it applies from then on, never retroactively. For report and decision lanes, the cards go to the read-only `mechanism-auditor` agent, which downgrades tiers the evidence does not earn and proposes an alternative mechanism that fits the same numbers.

### Agents & model routing

**Commands dispatch, skills decide, agents execute, documents persist.** Procedure lives in one place per skill; commands and agents are enhancements, not dependencies.

<p align="center">
  <img src="assets/framework.svg" alt="Framework layers: six slash commands dispatch into three skills, which delegate to five specialist agents that write persistent artifacts" width="96%">
</p>

| Agent | Model | Tools | Backs | Why isolated |
|-------|-------|-------|-------|--------------|
| **`blindspot-scout`** | sonnet | read-only | Blind-spot pass, References | Wide recon in its own context window; structurally cannot implement |
| **`prototype-smith`** | inherit | writes throwaway files only | Prototype, Plan | N genuinely divergent directions in one pass, sandboxed from the real app |
| **`ledger-keeper`** | inherit | ledger file only | Cartographer | Regret, clarity scores, and the gate verdict — without grading its own interview |
| **`quiz-master`** | inherit | read-only + report | Pitch, Quiz | Fresh-eyes examiner that did not author the change; flags unlogged deviations |
| **`mechanism-auditor`** | inherit | read-only | `theory-vs-result` | Referee that did not write the theory or run the measurement; downgrades unearned verdicts and tiers |

**Model routing** — judgment and creative agents use `model: inherit`, so they run at the session's own strength and are never downgraded. `blindspot-scout` is the one deliberate cost tier (`sonnet`) because recon fans out in parallel; set it to `inherit` for single-lens passes. Follows OMC's role tiers and Deep Research's "strongest model at the synthesis centre, cheaper fan-out" — with the top tier inherited rather than pinned.

---

## Commands

These run **inside a Claude Code session**. Each command is a thin dispatcher into a named skill section.

| Form | Kind | Effect | Example |
|------|------|--------|---------|
| `/finding-unknowns` | Slash command → Phase 0 | Locate the unknown, announce the route, run the matching technique | `/finding-unknowns "add a usage dashboard"` |
| `/blindspot` | Slash command → Technique 1 | Read-only blind-spot pass | `/blindspot "src/auth"` |
| `/cartographer` | Slash command → Phase C | Ledger, scored clearing loop, dual gate, execution bridge | `/cartographer --deep "migrate billing"` |
| `/change-quiz` | Slash command → Technique 8 | Change report + must-pass comprehension quiz | `/change-quiz main..HEAD` |
| `/keep-the-reasoning` | Slash command → `keep-the-reasoning` Step 0 (Step 3 if the work is done) | Stakes triage, then the handoff packet | `/keep-the-reasoning "ship the migration?"` |
| `/theory-vs-result` | Slash command → `theory-vs-result` Step 0 (stops after the prediction card if nothing is measured yet; a result already in hand is marked `post-hoc`) | Triage, then the Theory → Measured → Consistent? → Mechanism cards | `/theory-vs-result "did the new loss beat baseline?"` |
| `finding-unknowns` / `keep-the-reasoning` / `theory-vs-result` | Skill tool | The same skills, no plugin commands needed | invoke via the Skill tool |
| plain language | Prompt | Request one technique directly | _"do a blind-spot pass"_, _"interview me"_, _"brainstorm four directions"_ |

**Notes:**

- The slash commands need the plugin or a manual copy of `commands/`; the skills alone load through the Skill tool.
- Depth flags set the Cartographer threshold: `--quick` 0.35 · `--standard` 0.25 (default) · `--deep` 0.15.
- Copy-paste, end-to-end prompts: [`EXAMPLES.md`](EXAMPLES.md).

<details>
<summary><b>Configuration (optional — zero config by default)</b></summary>

Override the clarity threshold per project or per user in `.claude/settings.json` (flag > project > user > default); Cartographer announces the resolved threshold and its source on entry.

```json
{ "findingUnknowns": { "ambiguityThreshold": 0.25 } }
```

Other defaults — prototype directions (4), regret question bar (1.0, never applied to irreversible rows), quiz size and rounds, Cartographer round caps (soft 10 / hard 20), execution attempt cap (3) — live in the **Defaults** table in [`SKILL.md`](skills/finding-unknowns/SKILL.md) and can be overridden in plain language.

</details>

---

## Demo

> _Illustrative transcripts, written to the output templates in the three `SKILL.md` files and `references/cartographer.md` — not recordings of real sessions._

**Phase 0 routing** — announced before any technique runs, so you can veto it.

```
> /finding-unknowns add a usage dashboard to the admin app

Prior: "a few charts over the existing usage table"
Routing: UU + UK → blind-spot pass, then 4-direction prototype — you're new to this
subsystem (UU) and the dashboard layout is know-it-when-you-see-it (UK).
```

<details>
<summary><b>A Cartographer round report — scores + the seven-condition gate, every round</b></summary>

```
Round 3 complete.

Ledger: 4 open | 1 probing | 6 resolved | 2 deferred
Top regret: U2 (2.0) — which auth path to extend [route: interview]

| Quadrant      | Score   | Weight        | Gap                                        |
|---------------|---------|---------------|--------------------------------------------|
| KK            | 0.90    | 0.20          | clear                                      |
| KU            | 0.50    | 0.25          | auth path (U2) undecided                   |
| UK            | 0.70    | 0.25          | session-UX criteria not yet confirmed      |
| UU            | 0.70    | 0.30          | two scout lenses run; not yet dry          |
| **Ambiguity** | **31%** | threshold 25% | KU × auth middleware — U2 sets the design  |

Coverage gate:
[x] KK locked          [ ] KU resolved/deferred
[x] UK extracted       [x] UU probed
[ ] no open row with regret ≥ 1.0
[x] every irreversible row user-confirmed
[ ] ambiguity 31% ≤ threshold 25%

Next target: U2 — highest-regret open row; a wrong guess forces a rewrite of the
middleware layer.
```

</details>

<details>
<summary><b>A keep-the-reasoning handoff packet — evidence first, summary last</b></summary>

```
Handoff lane: keep-the-reasoning — schema migration on a shared production table.
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

The anti-pattern it replaces: _"Done! The migration is ready and all tests pass ✅."_

</details>

<details>
<summary><b>A theory-vs-result card — the prediction, the miss, and the broken link</b></summary>

```
[R1] Does the read-through cache cut API p95?
Theory      : 80% of reads repeat within 60s → hit rate ~0.8 → p95 roughly halves.
              Writes should not change.
Measured    : read p95 −41 ms (412 → 371, −10%), 5 reruns, spread ±15 ms; hit rate 0.31;
              write p95 +2 ms ±8 (a regression ≥20 ms would matter).
Consistent? : partly — direction yes, magnitude no; writes flat as predicted.
Mechanism   : broken link = "a repeat is a cache hit". Reads do repeat, but the cache
              key includes the session ID, so repeats from different sessions miss
              [supported: the key format explains a 0.31 hit rate].
              Next check: replay one hour of logs with a session-free key; the predicted
              hit rate is ≥0.7.
```

The anti-pattern it replaces: _"p95 only dropped 10%, the cache doesn't work."_

</details>

---

## How it Compares

`finding-unknowns` is a lightweight orienting layer, not an execution engine. Use it to locate an unknown, then escalate to the right specialist.

| Property | finding-unknowns | Deep Interview ([OMC](https://github.com/Yeachan-Heo/oh-my-claudecode)) | OMC execution (autopilot / ralph / team) | [Superpowers](https://github.com/obra/superpowers) |
|----------|------------------|-------------------------|-------------------------|-----------------------|
| Altitude | Meta / orienting | One phase: requirements | Execution & delivery | Discipline primitives |
| Lifecycle | Pre · During · Post | Pre only | During · Post | Mostly single-phase |
| Rigor | Flexible | Ambiguity gating | Verification-gated | Checklist-driven |
| State | Stateless (Cartographer: ledger file) | Persisted, resumable | Persisted, multi-agent | Varies |
| Best when | You don't yet know your unknowns | You need a validated spec | The spec is clear | You need one disciplined move |

Deep Interview (as of OMC 5.8.1) is approval-gated; its `--frontier` mode is the closest analogue of batched independent questions plus territory routing. Cartographer *adopts* its transparency machinery — clarity scores with a threshold, Round 0 topology, challenge modes — and keeps the axes a clarity-scoring interview alone does not cover.

**Defer, don't duplicate.** When a sibling is installed, `finding-unknowns` uses it for the mechanism it owns and keeps the unknowns lens — quadrant routing, regret-priced rows, route-typed clearing, the reversibility floor, lifecycle persistence.

| Need | Sibling (when installed) |
|------|--------------------------|
| Accepting agent output without surrendering judgment | `keep-the-reasoning` (this repository) |
| Reporting a measured result against its prediction | `theory-vs-result` (this repository) |
| Ontology tracking, OMC state, ralplan/autopilot handoff | `oh-my-claudecode:deep-interview` |
| Fog test and decision tickets on a tracker | `oh-my-claudecode:ask-navigator` |
| Adversarial review of a diff or design | `oh-my-claudecode:interrogate` |
| Throwaway prototype to settle a design | `oh-my-claudecode:loft` |
| Decision trail for autonomous work | `oh-my-claudecode:show-me-your-work` |
| Prove a change's blast radius | `oh-my-claudecode:blast-radius` |
| Restate the brief before starting | `oh-my-claudecode:in-your-own-words` / `sharpen` |
| Learner-paced explanation | `oh-my-claudecode:teach` |

<details>
<summary><b>Cartographer vs Deep Interview, axis by axis — and the decision tree</b></summary>

| Axis | Deep Interview | Cartographer mode |
|------|----------------|-------------------|
| Gate criterion | Ambiguity ≤ threshold (goal/constraint/criteria) | Dual: coverage (all four quadrants probed, blind-spot pass required) AND per-quadrant weighted ambiguity ≤ threshold, plus the irreversibility floor |
| Blind spots (UU) | Not modelled | First-class; heaviest weight (0.30) |
| Lifecycle | Ends at the specification | One ledger, seeded pre, appended during, closed post |
| Prioritisation | Fixed dimension weights | Regret orders rows; ambiguity scores quadrants |
| Clearing instrument | Socratic Q&A | Route-typed per unknown: interview / territory / experiment / audit |
| Execution | Approval-gated handoff into OMC pipelines | Approval-gated bridge: planner + reviewer consensus, or Workflow execution with per-task refute-framed verification |

```
finding-unknowns  (orient: which quadrant is this unknown in?)
        ├─ a light reframe is sufficient            → the eight techniques
        ├─ high-stakes, want a coverage gate         → Cartographer mode
        ├─ want ambiguity gating + resumable state   → OMC Deep Interview
        ├─ divergent option generation               → superpowers:brainstorming
        ├─ a rigorous written plan                   → superpowers:writing-plans / omc-plan
        ├─ the specification is already concrete     → OMC autopilot / ralph / team
        ├─ the work is done, the risk is the handoff → keep-the-reasoning
        └─ a result is in, the risk is misreading it → theory-vs-result
```

</details>

---

## Design Notes

What field tests and reviews changed:

- **Field test → the route column (v3.3.0).** In a quant × deep-learning research task, the three highest-regret unknowns all had non-interview routes. The loop became a router: territory rows are never asked of the user; pending experiments suspend the loop instead of spawning empty rounds.
- **A strong result is not a resolved one (v3.4.0).** A strong RankIC looked like it settled "is the signal real?" — but leakage produces the same IC. Cost ≥ 4 rows now need an adversarial check and two independent sources.
- **Field test → visible clarity scoring (v3.6.0).** Discovery was strong, but work drifted into a fuzzy zone the user could not steer. Fix: per-quadrant scores every round, scored in one call from ledger evidence only, with "score drift" named as a failure mode.
- **Confidence vs blast radius (v4.0.0).** Regret multiplies by P(wrong) — the input most prone to optimism — so a confident agent could silently default an irreversible step. Hence the irreversibility floor.
- **Three review rounds of `fu-execute-verified` (v4.0.0).**
  - **Round 1** — an independent adversarial review found 1 CRITICAL and 6 HIGH, reproduced against a stubbed runtime, including argument validation that let an unknown or missing lane through. Validation now fails closed.
  - **Round 2** — closed the remaining fail-open edges: paths normalized and globs rejected before locking, mandatory check files for `wide`/`irreversible` tasks, writes outside every declared path stop the run.
  - **Round 3** — fixed the scope check's false halts: paths already dirty before the run are baselined and excluded.
  - Exercised by a 50-scenario harness against a stubbed agent runtime, plus the reviewer's own adversarial scenarios.
- **Deliberately not adopted.** "Approve only the last step" — a human reviewing only a final artifact they never framed is rubber-stamping. "Confidence is the only input the model can influence" — agents can also edit their own checks, hence the locked contract.

### Roadmap

Not done yet:

- **Run `fu-execute-verified` in a live Workflow runtime** — so far exercised only against a stubbed agent runtime.
- **Move the remaining prompted guarantees into code** where the runtime allows.
- **Ontology / entity-convergence tracking** — consciously deferred in v3.6.0 because the Round 0 topology gate covers convergence more cheaply; to revisit if component drift shows up in tests.

---

## Documentation

- **[Architecture](docs/ARCHITECTURE.md)** — layers, artifact contracts, design principles
- **[finding-unknowns SKILL.md](skills/finding-unknowns/SKILL.md)** — routing, the eight techniques, Cartographer summary, defaults
- **[Cartographer protocol](skills/finding-unknowns/references/cartographer.md)** — the normative ledger, gate, close-out, and Phase E rules
- **[Workflow templates](skills/finding-unknowns/references/workflows.md)** — the four scripts, code-vs-prompt table, fallback ladder
- **[keep-the-reasoning SKILL.md](skills/keep-the-reasoning/SKILL.md)** — stakes triage, handoff packet, surrender signals
- **[theory-vs-result SKILL.md](skills/theory-vs-result/SKILL.md)** — prediction card, result cards, mechanism tiers, the two verdicts
- **[Examples](EXAMPLES.md)** — copy-paste, end-to-end prompts
- **[Changelog](CHANGELOG.md)** — release history
- **[AGENTS.md](AGENTS.md)** — repository guide and invariants for coding agents and contributors
- **[Contributing](CONTRIBUTING.md)** — workflow and local validation; contributions welcome

---

## Requirements

- **Claude Code** — the CLI, desktop app, or an IDE extension.
- **No runtime, no dependencies** — skills, agents, and commands are plain Markdown; nothing is compiled.
- **Optional, all degrade gracefully** — the five companion agents and the Workflow tool; every technique also runs inline.
- **`bash`** — only for `install.sh`.

## Project Layout

<details>
<summary><b>Repository tree</b></summary>

```
finding-unknowns-skill/
├── .claude-plugin/          Plugin and marketplace manifests (/plugin install)
├── commands/                Slash-command entry points (thin dispatchers)
│   ├── finding-unknowns.md    /finding-unknowns — Phase 0 routing
│   ├── blindspot.md           /blindspot — blind-spot pass
│   ├── cartographer.md        /cartographer — Cartographer mode
│   ├── change-quiz.md         /change-quiz — report + merge quiz
│   ├── keep-the-reasoning.md  /keep-the-reasoning — the handoff
│   └── theory-vs-result.md    /theory-vs-result — measured results
├── skills/
│   ├── finding-unknowns/
│   │   ├── SKILL.md         Routing, eight techniques, Cartographer summary
│   │   └── references/
│   │       ├── cartographer.md  Full Cartographer protocol (normative), read on demand
│   │       └── workflows.md     Workflow templates + fallback ladder
│   ├── keep-the-reasoning/
│   │   └── SKILL.md         Stakes triage, handoff packet
│   └── theory-vs-result/
│       └── SKILL.md         Prediction card, Theory → Measured → Consistent? → Mechanism cards
├── agents/                  blindspot-scout (sonnet) · prototype-smith · ledger-keeper · quiz-master · mechanism-auditor (inherit)
├── docs/ARCHITECTURE.md     Design reference: layers, contracts, principles
├── assets/                  README diagrams (SVG); assets/zh/ = Chinese versions
├── AGENTS.md                Repository guide for coding agents and contributors
├── EXAMPLES.md              Copy-paste, end-to-end prompts
├── CLAUDE.md                Passive single-file drop-in
├── install.sh               Installer (skills + references + agents + commands)
├── CONTRIBUTING.md · CHANGELOG.md · LICENSE (MIT)
└── README.md (English, canonical) · README.zh.md (简体中文)
```

</details>

## License & Credits

Released under the [MIT License](LICENSE).

- Technique ideas and names: Thariq Shihipar, _"A Field Guide to Fable: Finding Your Unknowns"_ ([@trq212](https://x.com/trq212/status/2073100352921215386)).
- `keep-the-reasoning` and the verification contract: Addy Osmani, _"Critical thinking when agents do the work"_ ([source](https://x.com/addyosmani/status/2117512471930167377)).
- `theory-vs-result`: distilled from the author's own empirical research practice, generalized for any measured claim.
- Phase E execution rules: Anthropic's _"Building effective agents"_ (evaluator-optimizer, orchestrator-workers) and @hanakoxbt's _"Loops and Graphs"_ ([source](https://x.com/hanakoxbt/status/2091515787366306154)).
- Cartographer's ambiguity gating, topology gate, and challenge modes are adapted from the deep-interview skill in [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode); the comparison also references [Superpowers](https://github.com/obra/superpowers).

**Disclaimer.** This is an independent community project. It is not affiliated with, authorised by, or endorsed by Anthropic.
