<p align="center">
  <img src="assets/hero.svg" alt="finding-unknowns v4.3.2 — map the territory before you build; keep the reasoning when agents hand the work back" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-D97757?style=for-the-badge&labelColor=F0EEE6" alt="Claude Code plugin">
  <img src="https://img.shields.io/badge/version-4.3.2-C15F3C?style=for-the-badge&labelColor=F0EEE6" alt="version 4.3.2">
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

**New to the plugin?** The [5-minute tutorial](docs/TUTORIAL.md) walks through three copy-paste exercises: a blind-spot pass on a real open-source repo, a handoff packet, and a theory-vs-result card. Every term the skills share (prior, lane, rigor level, packet size, mode, fresh-context refutation) is defined once in the [Glossary](docs/GLOSSARY.md).

### Not Sure Where to Start?

If the task is vague, or you're new to the domain or codebase:

```
/finding-unknowns "I want to …"
```

Phase 0 places the gap on the quadrant map, captures your prior, and routes to the cheapest technique that clears it — or says plainly that there are no significant unknowns.

- **High stakes** (hard to reverse, wide blast radius, unfamiliar territory + long horizon) → `/cartographer --deep "…"`
- **Work is done, the risk is accepting it** → `/keep-the-reasoning "…"`
- **A result is in (or about to be measured), the risk is misreading it** → `/theory-vs-result "…"` (a failing test or crash that reproduces every time takes its lighter Debug path)

### Updating

Update the same way you installed. Latest release: **v4.3.2**.

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
rm -f ~/.claude/commands/finding-unknowns.md ~/.claude/commands/keep-the-reasoning.md ~/.claude/commands/theory-vs-result.md  # removed in 4.3.0; the skills answer these slashes
```

**Verify:**

```bash
grep '"version"' ~/.claude/plugins/*/finding-unknowns*/.claude-plugin/plugin.json 2>/dev/null \
  || ls ~/.claude/skills/finding-unknowns/references/cartographer.md ~/.claude/skills/keep-the-reasoning/SKILL.md ~/.claude/skills/theory-vs-result/SKILL.md
# expect: 4.3.2 (plugin) — or all three files listed (theory-vs-result exists only from v4.1.0 on)
```

</details>

---

## Why finding-unknowns?

- **The map is not the territory** — the map is what you give Claude (prompt, context, skills); the territory is the codebase and the real world. Every gap between them forces the model to guess your intent. Capability is no longer the bottleneck on long-horizon work; clarity is.
- **Route by quadrant, not by habit** — blind spots need reconnaissance, tacit taste needs prototypes, nameable gaps need targeted questions, comprehension needs examination. One uniform interview under-serves all four.
- **Coverage-gated Cartographer mode** — for high stakes: a regret-ordered unknowns ledger, clarity scores shown every round as a display, and a six-condition gate on checkable ledger facts that won't let implementation start while the territory is unmapped. By default it ends at a spec with a verification contract.
- **Irreversibility floor** — gate on blast radius, not confidence. An unknown guarding an irreversible step always reaches you, however confident the evidence looks.
- **Keep the reasoning at the handoff** — an evidence-first packet that says what each check did NOT prove and what went unchecked, so accepting agent work never slides into cognitive surrender.
- **Theory before data** — every measured result arrives as Theory → Measured → Consistent? → Mechanism: the prediction written first, the noise floor stated, the mechanism tagged with how well it is evidenced, and the rule verdict kept apart from the verdict on the idea.
- **Independent judgment** — the author never self-approves. Discovery, scoring, and examination run in contexts that did not do the implementing, and all three skills share one check: a **fresh-context refutation**, where a context that did not produce a claim names the strongest alternative explanation and the cheapest check that would tell them apart.
- **Zero dependencies** — plain Markdown. Agents and Workflow scripts add depth; every technique also runs fully inline.

> **Attribution.** The techniques and their names come from Thariq Shihipar's essay _"A Field Guide to Fable: Finding Your Unknowns"_ ([@trq212](https://x.com/trq212/status/2073100352921215386)); credit for the underlying ideas belongs to the original author, and this repository packages them as an installable Claude Code plugin. `keep-the-reasoning` is distilled from Addy Osmani's _"Critical thinking when agents do the work"_ ([source](https://x.com/addyosmani/status/2117512471930167377)): across many handoffs the human slides from **offloading** (delegate, keep ownership) → **deferral** (the output becomes the next input) → **cognitive surrender** (the output quietly becomes your own). `theory-vs-result` is distilled from the author's own empirical research practice and generalized for any measured claim: a number is not a finding until you know what was expected, whether the gap beats noise, and why it came out that way.

---

## Features

### The three skills

| Skill | What it is | Use for |
|-------|------------|---------|
| **`finding-unknowns`** | Phase 0 quadrant routing → eight techniques → optional Cartographer mode | Before and during work: surfacing the unknowns that would otherwise become guesses |
| **`keep-the-reasoning`** | Stakes triage, "verified" defined up front, a fixed-order handoff packet | The handoff: accepting agent work without surrendering judgment |
| **`theory-vs-result`** | Prediction card first, then Theory → Measured → Consistent? → Mechanism cards, with two separate verdicts | Measured results: backtests, benchmarks, A/B tests, ablations, training runs — never a number without its prediction and its reason. Reproducible failures take a lighter Debug path |

`finding-unknowns` hands over to `keep-the-reasoning` at the end of Phase 3 and at Cartographer's merge (and at the end of the experimental execution bridge, when it runs). Returning `experiment`-route results are reported through `theory-vs-result`, whose summary table also serves as the handoff packet's "prior vs result" section.

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

**Lightweight mode by default.** Analysis outputs (the routing analysis, the blind-spot pass, reference extraction) end in a short report: the 3 most consequential findings, each with its evidence, and 1 recommended next action. Surprises against your prior are never capped. The blind-spot pass's compact report (top 3 findings + rewritten request) *is* that short report, not compressed again; ask for the "full report" (given by default at high stakes) to get the complete technique output. Prototypes, interview questions, plans (with their definition of "verified"), implementation notes, pitches, and quizzes are always delivered in full. Text comes first: reports, plans, and quiz reports are Markdown, with HTML on request; prototypes stay HTML because they are visual.

### Cartographer mode

The rigorous escalation for high-stakes work. Full protocol: [`references/cartographer.md`](skills/finding-unknowns/references/cartographer.md), read on demand.

<p align="center">
  <img src="assets/cartographer.svg" alt="Cartographer mode: Round 0 topology, seeded unknowns ledger, regret-ordered clearing loop by route, per-round quadrant clarity display, six-condition gate with irreversibility floor, spec as the default end, experimental execution bridge" width="96%">
</p>

| Part | What it is | Use for |
|------|------------|---------|
| **Unknowns ledger** | `.finding-unknowns/unknowns-ledger.md`, first line `schema: 2`. Rows with quadrant, prior, `regret = cost-if-wrong × P(wrong)`, route (interview · territory · experiment · audit), reversibility (reversible · wide · irreversible) | Ordering the work; it *is* the resume state |
| **Clearing loop** | A router, not an interview: clear the highest-regret open row by its route; adversarially verify cost ≥ 4 resolutions (a fresh-context refutation) | Never asking the user what the territory can answer |
| **Clarity display** | `ambiguity = 1 − (KK×0.20 + KU×0.25 + UK×0.25 + UU×0.30)`, re-scored every round; shown to steer, never a gate condition | Letting you see and steer how clear the map is |
| **Six-condition gate** | KK written down; KU resolved or deferred-with-default; UK extracted, or marked not applicable with your confirmation; UU probed; no open row with regret ≥ 1.0; every irreversible row user-confirmed (the irreversibility floor). Completeness critic before any PASS; soft check at round 10 and every 10 rounds after (round 5 and every 5 after under `--quick`), no hard round cap | Refusing to build on an unmapped territory |
| **Spec + verification contract** | `.finding-unknowns/unknowns-spec-{slug}.md`, the default end: close-out report and a pending-approval spec, then stop. Any build from the spec leaves irreversible steps to you: prepared, never executed, until you run each one or say yes to that command | Building from a crystallized, pending-approval spec |
| **Next-step offer (E1)** | The default after the spec: a planner + reviewer consensus plan (recommended; execution is a separate yes), or keep refining. The full `keep-the-reasoning` packet at merge | Choosing how to proceed without anything running on its own |
| **Workflow execution (E2)** | Experimental, optional; not yet run in a live Workflow runtime. Only on your explicit request | Running an approved task graph under Phase E rules |

**Flow:** depth announced → Round 0 topology (1–6 components) → **C0** seed from all four quadrants + a domain checklist → **C1** clear by route → **C2** six-condition gate → **C2.5** close-out report + spec (default stop) → **E** next-step offer (consensus plan; Workflow execution experimental, on explicit request) → **C3** the ledger stays open through the build and feeds the quiz.

**New in v4.0.0**

- **Irreversibility floor** — regret contains P(wrong), a confidence estimate. For `irreversible` rows confidence never substitutes for the user: never silently defaulted under the regret bar, resolved only with recorded user confirmation. A gate condition since 4.0.0 (the sixth since 4.2.0); no exit waives it.
- **Priors and surprises** — each row records the expectation held before evidence-based scoring; contradictions surface as surprises.
- **Verification contract** — per criterion: a failable check, its artifact, what it proves, what it does NOT prove, and its lane. Locked against the implementer.
- **Phase E execution rules** (experimental since v4.2.0; run only on request) — the loop lives inside a task, the graph between tasks; edges name what crosses; failures return `UNIT · VERDICT · REASON · EVIDENCE · SCOPE`; an attempt cap turns a task into a plan-suspect row; a learning edge feeds derived constraints forward; tasks close by reversibility lane on results from a separate check-runner. The human sits at both ends — spec, contract, and task graph at the front; irreversible lane and merge at the back.

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
| **`fu-execute-verified`** | Experimental, optional; not yet run in a live Workflow runtime. Approved execution under Phase E rules; every implementer paired with an independent refute-framed verifier | Running the approved task graph, only on your explicit request |

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
| **Stakes triage → packet size** | `offload` (cheap, reversible, lands only on you; one line) · `compact` (medium stakes: lands on others, but reversible and contained) · `full` (high stakes: hard to reverse) | Scaling the packet to consequence, not effort |
| **Before the work** | Capture your prior (reused if another skill already recorded it this session); define "verified" — a check must be able to fail | Making any outcome un-rationalizable after the fact |
| **Handoff packet** | Compact (four sections): evidence → what the checks did NOT prove → never-empty "not checked" → summary. Full (nine sections): evidence first → what checks proved / did NOT prove → decisions & assumptions → prior vs result → strongest counterargument and "did I miss anything?" from a fresh-context refutation (labelled `same-context — weaker` when no separate context exists) → never-empty "not checked" → summary last | Accepting work with your judgment intact |
| **After the handoff** | A rejection becomes a rule (test, hook, lint rule); surrender signals named once, without moralizing | Making taste compound |

When `finding-unknowns` already ran, `keep-the-reasoning` reuses its priors, verification contract, and the quiz-master's Decisions & assumptions instead of repeating them. A packet written to disk goes to `.finding-unknowns/handoff-{slug}.md`.

### Theory vs result

| Step | What it is | Use for |
|------|------------|---------|
| **Triage → rigor level** | `note` (one number, nothing rides on it) · `report` (someone will act on it, or it misses) · `decision` (adopt/ship, a pre-agreed rule, money) | Scaling the card to what rides on the number |
| **Debug path** | For a reproducible, deterministic failure (a failing test, a crash, the same wrong output every run): repro + observed output → prior → at least two competing explanations → one discriminating check each, cheapest first → fix → the same repro re-run plus one neighbouring case that should not change. No noise floor, no frozen rule; escalates to a rigor level when the failure is flaky or a ship/no-ship rides on the fix | Explaining a bug without dressing it up as an experiment |
| **Prediction card** | Claim, mechanism chain, direction + magnitude + *where* it should show, noise floor, falsifier, decision rule, and when it was written; saved before the data (`.finding-unknowns/predictions/{slug}.md`). A card written after the result is a `post-hoc fit`, not a test | Giving a result something to disagree with |
| **Fair measurement** | Matched baseline, one variable changed, same seeds, the metric you are actually paid for, data budget respected | Not crediting a change with what the sample did |
| **Result card** | Theory → Measured → Consistent? → Mechanism (理论预期 → 实测 → 是否一致 → 机理); consistency is `consistent` · `partly` · `inconsistent` · `can't tell`, read from the interval (one that holds both 0 and the prediction is `can't tell`); mechanism tier is `verified` · `supported` · `inferred` · `untested` | Keeping facts, inferences, and untested stories visibly apart |
| **Mismatch walk** | Pipeline → comparison → metric → theory → environment; name the broken link and the smallest check that separates the explanations | Neither dismissing a direction on one run nor rescuing it with a story |
| **Two verdicts** | Rule verdict (in the rule's own labels, e.g. `PASS` · `FAIL` · `UNCERTAIN`, or `descriptive only` / `void`) vs direction verdict (`alive` · `alive-but-constrained` · `weakened` · `dead`) | A mechanism can keep a direction alive; neither a mechanism nor a rerun on spent data turns a `FAIL` into a `PASS`. A defect found afterwards voids the run instead |

A new or tightened threshold is first explained in plain language — what it protects against, why this number, what failing it means — and frozen only after you approve; it applies from then on, never retroactively. At the report and decision rigor levels, the cards go to the read-only `mechanism-auditor` agent, the fresh-context refutation applied to result cards: it downgrades tiers the evidence does not earn and proposes an alternative mechanism that fits the same numbers.

### Agents & model routing

**Commands dispatch, skills decide, agents execute, documents persist.** Procedure lives in one place per skill; commands and agents are enhancements, not dependencies.

<p align="center">
  <img src="assets/framework.svg" alt="Framework layers: six slash entry points (three skills invoked directly, three commands) lead into three skills, which delegate to five specialist agents that write persistent artifacts" width="96%">
</p>

| Agent | Model | Tools | Backs | Why isolated |
|-------|-------|-------|-------|--------------|
| **`blindspot-scout`** | sonnet | no Write/Edit; Bash for inspection | Blind-spot pass, References | Wide recon in its own context window; it has no file-editing tools, and Bash is limited to inspection by instruction |
| **`prototype-smith`** | inherit | Write + Bash; throwaway files only | Prototype, Plan | N genuinely divergent directions in one pass; instructed to write only under `.finding-unknowns/prototypes/` and never touch the real app |
| **`ledger-keeper`** | inherit | ledger file only | Cartographer | Regret, clarity scores, and the gate verdict — without grading its own interview |
| **`quiz-master`** | inherit | no Write/Edit; Bash for inspection and its report | Pitch, Quiz | Fresh-eyes examiner that did not author the change; flags unlogged deviations |
| **`mechanism-auditor`** | inherit | no Write/Edit; Bash for inspection | `theory-vs-result` | Referee that did not write the theory or run the measurement; downgrades unearned verdicts and tiers |

Tool lists remove file-editing tools where noted, which the runtime enforces. The remaining limits (what Bash may do, which files may be written) are instructions to the agent, not a sandbox.

**Model routing** — judgment and creative agents use `model: inherit`, so they run at the session's own strength and are never downgraded. `blindspot-scout` is the one deliberate cost tier (`sonnet`) because recon fans out in parallel; set it to `inherit` for single-lens passes. Follows OMC's role tiers and Deep Research's "strongest model at the synthesis centre, cheaper fan-out" — with the top tier inherited rather than pinned.

---

## Commands

These run **inside a Claude Code session**. The three skills are invoked directly as `/finding-unknowns`, `/keep-the-reasoning` and `/theory-vs-result`, because Claude Code exposes skills as slash commands. The three plugin commands (`/blindspot`, `/cartographer`, `/change-quiz`) are thin dispatchers: each invokes the `finding-unknowns` skill through the Skill tool and jumps to a named section.

| Form | Kind | Effect | Example |
|------|------|--------|---------|
| `/finding-unknowns` | Skill → Phase 0 | Locate the unknown, announce the route, run the matching technique | `/finding-unknowns "add a usage dashboard"` |
| `/blindspot` | Slash command → Technique 1 | Read-only blind-spot pass | `/blindspot "src/auth"` |
| `/cartographer` | Slash command → Phase C | Ledger, regret-ordered clearing loop, six-condition gate, spec + verification contract (default stop) | `/cartographer --deep "migrate billing"` |
| `/change-quiz` | Slash command → Technique 8 | Change report (Markdown; HTML on request) + must-pass comprehension quiz | `/change-quiz main..HEAD` |
| `/keep-the-reasoning` | Skill → Step 0 (Step 3 if the work is done) | Stakes triage (packet size), then the handoff packet | `/keep-the-reasoning "ship the migration?"` |
| `/theory-vs-result` | Skill → Step 0 (stops after the prediction card if nothing is measured yet; a result already in hand is marked `post-hoc`) | Triage (Debug path or rigor level), then the Theory → Measured → Consistent? → Mechanism cards, or the six Debug path items | `/theory-vs-result "did the new loss beat baseline?"` |
| `finding-unknowns` / `keep-the-reasoning` / `theory-vs-result` | Skill tool | The same skills, invoked by the model instead of by you | invoke via the Skill tool |
| plain language | Prompt | Request one technique directly | _"do a blind-spot pass"_, _"interview me"_, _"brainstorm four directions"_ |

**Notes:**

- `/blindspot`, `/cartographer` and `/change-quiz` need the plugin or a manual copy of `commands/`; the three skill slashes need only the skills installed. Up to 4.2 the plugin also shipped `/finding-unknowns`, `/keep-the-reasoning` and `/theory-vs-result` as command files with the same names as the skills; 4.3.0 removed them (the same invocations now reach the skills), and `install.sh` deletes old copies it recognizes.
- Depth flags set Cartographer's exploration depth: `--quick` single-lens blind-spot pass, soft check every 5 rounds · `--standard` (default) one blind-spot pass, escalating to a multi-lens sweep when the task spans more than one risk domain (e.g. money + data + infra) · `--deep` always a multi-lens sweep at seeding plus a UU loop-until-dry before the gate. Precedence: flag > your request > default.
- Copy-paste, end-to-end prompts: [`EXAMPLES.md`](EXAMPLES.md).

**Artifacts.** Everything the skills write lives under `.finding-unknowns/` at the project root: `unknowns-ledger.md`, `unknowns-spec-{slug}.md`, `implementation-notes.md`, `prototypes/`, `change-report.md`, `predictions/`, and `handoff-{slug}.md`. It is working state, so by default add `.finding-unknowns/` to your `.gitignore`. If your team reviews ledgers and specs in pull requests, use these lines instead (git cannot re-include a file inside an ignored directory, so the one-line form would hide them too):

```
.finding-unknowns/*
!.finding-unknowns/unknowns-ledger.md
!.finding-unknowns/unknowns-spec-*.md
```

Upgrading from 4.2 or earlier: a root-level `unknowns-ledger.md` is still read, and the skill offers in one line to move it (nothing moves silently); a ledger without a `schema: 2` first line is upgraded on resume, with every added header field reported.

<details>
<summary><b>Configuration (optional — zero config by default)</b></summary>

Nothing to configure. Cartographer depth comes from the flag or your request (flag > your request > default `--standard`), and the first line on entry announces it with its source: `Depth: {quick | standard | deep} (source: {flag | user request | default})`. The `findingUnknowns.ambiguityThreshold` settings key is ignored since 4.2.0: the ambiguity figure is display-only, so a leftover key has no effect.

Other defaults — report size (short for analysis outputs: 3 findings + 1 next action, surprises uncapped), report format (Markdown; HTML on request), prototype directions (4), regret question bar (1.0, never applied to irreversible rows), quiz size and rounds, Cartographer soft check (round 10 and every 10 after, or every 5 under `--quick`; no hard cap), execution attempt cap (3, experimental Phase E) — live in the **Defaults** table in [`SKILL.md`](skills/finding-unknowns/SKILL.md) and can be overridden in plain language.

</details>

---

## Demo

> _Illustrative transcripts, written to the output templates in the three `SKILL.md` files and `references/cartographer.md` — not recordings of real sessions. One real, recorded run now exists: a blind-spot pass on the public `pallets/itsdangerous` repo, with the brief as sent to `blindspot-scout` and the verbatim output, in [EXAMPLES.md](EXAMPLES.md#a-real-blind-spot-pass-recorded)._

**Phase 0 routing** — announced before any technique runs, so you can veto it.

```
> /finding-unknowns add a usage dashboard to the admin app

Prior: "a few charts over the existing usage table"
Routing: UU + UK → blind-spot pass, then 4-direction prototype — you're new to this
subsystem (UU) and the dashboard layout is know-it-when-you-see-it (UK).
```

<details>
<summary><b>A Cartographer round report — clarity display + the six-condition gate, every round</b></summary>

```
Round 3 complete.

Ledger: 4 open | 1 probing | 6 resolved | 2 deferred
Top regret: U2 (2.0) — which auth path to extend [route: interview]

| Quadrant                | Score   | Weight | Gap                                        |
|-------------------------|---------|--------|--------------------------------------------|
| KK                      | 0.90    | 0.20   | clear                                      |
| KU                      | 0.50    | 0.25   | auth path (U2) undecided                   |
| UK                      | 0.70    | 0.25   | session-UX criteria not yet confirmed      |
| UU                      | 0.70    | 0.30   | two scout lenses run; not yet dry          |
| **Ambiguity** (display) | **31%** | —      | KU × auth middleware — U2 sets the design  |

Gate:
[x] KK written down    [ ] KU resolved/deferred-with-default
[x] UK extracted or n/a (user-confirmed)
[x] UU probed
[ ] no open row with regret ≥ 1.0
[x] every irreversible row user-confirmed

Next target: U2 — highest-regret open row; a wrong guess forces a rewrite of the
middleware layer.
```

</details>

<details>
<summary><b>A keep-the-reasoning handoff packet — evidence first, summary last</b></summary>

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
| State | Stateless (Cartographer: ledger file in `.finding-unknowns/`) | Persisted, resumable | Persisted, multi-agent | Varies |
| Best when | You don't yet know your unknowns | You need a validated spec | The spec is clear | You need one disciplined move |

Deep Interview (as of OMC 5.8.1) is approval-gated; its `--frontier` mode is the closest analogue of batched independent questions plus territory routing. Cartographer keeps two pieces of its transparency machinery: the Round 0 topology gate and per-quadrant clarity scores, shown every round as a display. Since v4.2.0 it does not adopt a clarity threshold or challenge modes; its gate rules only on ledger facts a reviewer can check, and it keeps the axes a clarity-scoring interview alone does not cover.

**Defer, don't duplicate.** When a sibling is installed, `finding-unknowns` uses it for the mechanism it owns and keeps the unknowns lens — quadrant routing, regret-priced rows, route-typed clearing, the reversibility floor, lifecycle persistence.

| Need | Sibling (when installed) |
|------|--------------------------|
| Accepting agent output without surrendering judgment | `keep-the-reasoning` (this repository) |
| Divergent options when the goal is already clear | `superpowers:brainstorming` (`finding-unknowns` takes precedence when the risk is what you don't know) |
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
| Gate criterion | Ambiguity ≤ threshold (goal/constraint/criteria) | Six ledger-checkable conditions (all four quadrants probed, blind-spot pass required; UK may be marked not applicable with your confirmation; no open row with regret ≥ 1.0) plus the irreversibility floor; per-quadrant clarity is display-only |
| Blind spots (UU) | Not modelled | First-class; heaviest weight (0.30) |
| Lifecycle | Ends at the specification | One ledger, seeded pre, appended during, closed post |
| Prioritisation | Fixed dimension weights | Regret orders rows; the clarity display scores quadrants |
| Clearing instrument | Socratic Q&A | Route-typed per unknown: interview / territory / experiment / audit |
| Execution | Approval-gated handoff into OMC pipelines | Ends at the spec by default; planner + reviewer consensus plan offered. Workflow execution with per-task refute-framed verification is experimental, only on request |

```
finding-unknowns  (orient: which quadrant is this unknown in?)
        ├─ a light reframe is sufficient            → the eight techniques
        ├─ high-stakes, want a coverage gate         → Cartographer mode
        ├─ want ambiguity gating + resumable state   → OMC Deep Interview
        ├─ goal clear, only options needed           → superpowers:brainstorming
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
- **Gate on ledger facts, not a self-scored figure (v4.2.0).** A gate condition on weighted ambiguity let a self-assigned number decide when building could start. The figure stays as a per-round display; the gate keeps six conditions a reviewer can check against the ledger.
- **Confidence vs blast radius (v4.0.0).** Regret multiplies by P(wrong) — the input most prone to optimism — so a confident agent could silently default an irreversible step. Hence the irreversibility floor.
- **Three review rounds of `fu-execute-verified` (v4.0.0).**
  - **Round 1** — an independent adversarial review found 1 CRITICAL and 6 HIGH, reproduced against a stubbed runtime, including argument validation that let an unknown or missing lane through. Validation now fails closed.
  - **Round 2** — closed the remaining fail-open edges: paths normalized and globs rejected before locking, mandatory check files for `wide`/`irreversible` tasks, writes outside every declared path stop the run.
  - **Round 3** — fixed the scope check's false halts: paths already dirty before the run are baselined and excluded.
  - Exercised by [`tests/workflows/run.mjs`](tests/workflows/run.mjs), 69 scenarios against a stubbed agent runtime that read the templates straight from `workflows.md`, run in CI on every push to `main` and every pull request.
- **One word, one meaning (v4.3.0).** "Lane" meant reversibility in Cartographer, a rigor level in `theory-vs-result`, and a packet size in `keep-the-reasoning`. It now means reversibility only; the other two are *rigor level* and *packet size*, finding-unknowns' lightweight/Cartographer split is a *mode*, and the [Glossary](docs/GLOSSARY.md) holds the shared terms.
- **A first comparative eval (v4.3.2).** gpt-6.1-sol in Codex, with and without these skills, on six pre-registered tasks with blinded grading: both arms caught nearly every trap (22 vs 22.75 of 25, inside the noise), and the skills cost 47 % more input tokens. Two misses the skill arm shared with the baseline (no access check for a remote device; no noise estimate from reruns in hand) became the two 4.3.2 fixes. Details, raw outputs and grader replies: [docs/evals/2026-11-10-codex-pilot](docs/evals/2026-11-10-codex-pilot/README.md).
- **Deliberately not adopted.** "Approve only the last step" — a human reviewing only a final artifact they never framed is rubber-stamping. "Confidence is the only input the model can influence" — agents can also edit their own checks, hence the locked contract.

### Roadmap

Not done yet:

- **Run `fu-execute-verified` in a live Workflow runtime** — so far exercised only against a stubbed agent runtime.
- **Move the remaining prompted guarantees into code** where the runtime allows.
- **Ontology / entity-convergence tracking** — consciously deferred in v3.6.0 because the Round 0 topology gate covers convergence more cheaply; to revisit if component drift shows up in tests.

---

## Documentation

- **[5-minute tutorial](docs/TUTORIAL.md)** — install, then three copy-paste exercises
- **[Glossary](docs/GLOSSARY.md)** — one vocabulary across the three skills: lane, rigor level, packet size, mode, prior, fresh-context refutation, artifacts
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
├── commands/                Slash-command entry points (thin dispatchers; the skills answer to their own names)
│   ├── blindspot.md           /blindspot — blind-spot pass
│   ├── cartographer.md        /cartographer — Cartographer mode
│   └── change-quiz.md         /change-quiz — report + merge quiz
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
├── docs/
│   ├── ARCHITECTURE.md      Design reference: layers, contracts, principles
│   ├── GLOSSARY.md          Shared vocabulary across the three skills
│   └── TUTORIAL.md          5-minute tutorial (TUTORIAL.zh.md: Chinese)
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
- Cartographer's per-quadrant clarity scoring and the topology gate are adapted from the deep-interview skill in [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode); the comparison also references [Superpowers](https://github.com/obra/superpowers).

**Disclaimer.** This is an independent community project. It is not affiliated with, authorised by, or endorsed by Anthropic.
