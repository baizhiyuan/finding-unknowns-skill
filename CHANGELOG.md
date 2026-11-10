# Changelog

All notable changes to this project are documented in this file. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.2.0]

### Changed — Cartographer gates on ledger facts; clarity is a display
- The Cartographer gate goes from seven conditions to six: KK written down; KU resolved or
  deferred-with-default; UK extracted, or marked "not applicable" with the user's
  confirmation recorded in the ledger header (e.g. a backend migration with no taste
  component); UU probed; no open row with regret ≥ 1.0; every irreversible row
  user-confirmed. The irreversibility floor is unchanged and is now the sixth condition.
- The per-quadrant clarity scores and the weighted ambiguity figure are still computed and
  shown every round, but only as a display: the round report labels the row
  `**Ambiguity** (display)` with `—` in place of a threshold, and the figure never passes
  or fails the gate. `ledger-keeper` names "display gating" as a failure mode.
- **Migration: `--quick` / `--standard` / `--deep` now set exploration depth, not a
  threshold.** `--quick` runs a single-lens blind-spot pass and moves the soft check to
  every 5 rounds; `--standard` (the default) runs one blind-spot pass (full report),
  escalating to a multi-lens sweep when the task spans more than one risk domain (e.g.
  money + data + infra); `--deep` always runs a multi-lens sweep at seeding and a UU
  loop-until-dry (`fu-uu-until-dry`) before the gate. Precedence: flag > the user's
  request > default. The first line on entry is now
  `Depth: {quick | standard | deep} (source: {flag | user request | default})`.
- Round limits: a soft check at round 10 and every 10 rounds after (round 5 and every 5
  after under `--quick`) surfaces the top-3 stuck rows and offers resolve /
  defer-with-default / exit. There is no hard round cap.
- The default end of Cartographer is the close-out report plus the spec with its
  verification contract, then STOP. § E is split in two. **E1 — Next step after the spec
  (default, not experimental)** asks "Spec ready. How to proceed?" with option 1,
  consensus-refine (recommended), and option 3, keep refining. **E2 — Workflow execution**
  (option 2, `fu-execute-verified`, Template 4) is **experimental, optional; not yet run in
  a live Workflow runtime**, and runs only on the user's explicit request. Option numbers
  stay 1/2/3, so existing references hold.
- **Any build from the spec — irreversible work stays with the user** (new normative rule,
  `references/cartographer.md` C2.5, enforced through C3). Whatever the execution path (the
  user's own build, the consensus plan after a separate yes, or Phase E), the implementer
  prepares each irreversible change and the exact command and executes nothing
  irreversible; the user runs it or gives a per-command yes; post-checks run before the row
  closes. Previously the irreversible-lane rule bound only Phase E, while discovery exits
  pointed at it; exits now point at this rule, the contract's `lane` column names it, and
  Phase E's irreversible lane is this rule applied per task. Cartographer's merge always
  uses the full `keep-the-reasoning` packet (Cartographer is high stakes by definition).
- Lightweight defaults: analysis outputs (Phase 0 routing analysis, the Technique 1
  blind-spot pass, Technique 4 reference extraction) end in a short report (3 findings
  with evidence + 1 next action; the full technique output on request or at high stakes).
  Surprises are never capped. Prototypes, interview questions, plans (Technique 5,
  including the Definition of verified), implementation notes, pitches (Technique 7), and
  quizzes are always delivered in full. `blindspot-scout` returns a compact report by
  default (top 3 findings + rewritten request, ≤ ~25 lines plus Surprises); when Technique 1
  runs, that compact report *is* the short report, not compressed again. The full
  five-section report on request or at high stakes, and always for Cartographer seeding.
  `keep-the-reasoning` adds a compact four-section packet for medium stakes, with a Prior
  vs result line when a prior was recorded or the claim is measured, and a link to the
  quiz report under Evidence when a quiz ran; the full nine-section packet stays for high
  stakes, and the lane announcement names the size. Packet sections are now referenced by
  name rather than number across `keep-the-reasoning`, `theory-vs-result` and
  ARCHITECTURE, since the two packet sizes number them differently.
- Text first: reports, plans, and quiz reports default to Markdown, with HTML on request;
  `quiz-master` writes `change-report.md` by default (`change-report.html` on request).
  Prototypes stay single-file HTML.
- Skill descriptions are trigger-first (`finding-unknowns`, `keep-the-reasoning`,
  `theory-vs-result`); `keep-the-reasoning` keeps its front-end trigger (starting work
  whose consequences fall on others) and "keep me honest". The plugin description marks
  Workflow execution as experimental. `finding-unknowns` states its precedence over
  `superpowers:brainstorming`: brainstorming when the goal is clear and only options are
  needed; this skill when the risk is what the user does not know (Technique 2 routes
  there).
- The `finding-unknowns` credit key `ambiguity-gating` is renamed `ambiguity-scoring`;
  Cartographer keeps deep-interview's per-quadrant clarity scoring (display-only) and
  topology gate.
- README, README.zh, ARCHITECTURE and EXAMPLES updated to match: six-condition gate,
  display-only clarity, depth flags, the § E1 / § E2 split, the irreversible build rule,
  lightweight defaults, and the round-report example. The Chinese README calls the soft
  check 软检查, matching the diagrams.
- Diagrams updated (en and zh: cartographer, framework, handoff, hero, lifecycle,
  quadrants, workflows): depth replaces the clarity threshold, the gate shows six conditions with
  clarity as a display, the challenge modes are gone, the soft check is shown with no hard
  cap, and the spec is the default end with Workflow execution marked experimental. The
  handoff diagram shows the three triage outcomes (offload, compact packet, full packet).

### Fixed
- `ledger-keeper`: the Output_Format operation list now includes `SCORE-QUADRANTS`
  (`<SEED | RE-SCORE | TARGET | SCORE-QUADRANTS | GATE | CLOSE-OUT>`), matching its
  Operations section.

### Removed
- The clarity threshold as a gate condition, its 0.35 / 0.25 / 0.15 depth-flag presets,
  and the entry line `Clarity threshold: {X}% (source: …)`.
- The `findingUnknowns.ambiguityThreshold` settings key: it is ignored since 4.2.0 (a
  leftover key has no effect), and the "Threshold configuration" section of
  `references/cartographer.md` is replaced by "Settings".
- The challenge modes (Contrarian, Simplifier, Ontologist).
- The round-20 hard cap.

## [4.1.1]

### Fixed — defects found by an outside review (GPT-6-astra, Fable 5.1), verified and tested
- `fu-verify-panel` (Template 2) let a majority vote override a counterexample: one
  refuter's plausible alternative was outvoted by two that found none, contradicting C1
  step 3.5. A resolution now survives only if every refuter reports and none refutes;
  a missing vote also blocks survival.
- Template 1's finding dedup and Template 4's derived-constraint dedup used `\W+`, which
  erases Chinese text, so every Chinese finding collapsed into one key. Both now normalise
  with Unicode letter/number classes.
- Template 4's scope check exempted files that were already dirty before the run, so a
  further edit to such a file went unnoticed. Those files are now content-hashed at the
  baseline and any change to them is a `scope-violation`. Paths are read with
  `core.quotePath=false`, so non-ASCII file names are hashed rather than silently
  "missing"; a "missing" hash is accepted only for a real deletion. A check file that
  cannot be hashed at the baseline is an infra error; directories are hashed by manifest.
- Template 4 also hashes every task's check files on every check run (one task can no
  longer edit another's checks unnoticed) and runs a final sweep after all tasks, which
  catches edits made after the last per-task check (e.g. by a verifier). Any mismatch
  halts the run.
- Template 2 rejects fewer than three distinct lenses (an empty panel used to "survive"),
  and returns `panel-survived` instead of `resolved`: the caller still applies the
  two-source rule. Template 1 keeps earlier lenses' confirmations when a higher-cost
  duplicate arrives; both dedups apply NFKC and keep combining marks.
- Overstated isolation claims corrected: `blindspot-scout` has no file-editing tools but
  does have Bash, and `prototype-smith` can write files; their limits are instructions, not
  a sandbox, and README / ARCHITECTURE now say so. `quiz-master` no longer equates a pass
  with "merge-ready"; merging stays the user's decision.
- Documentation drift: the Cartographer example in EXAMPLES.md now has the `route` column,
  route-typed clearing and the full gate; CONTRIBUTING no longer says the skill is one file;
  version link references added for 4.x.

### Added — tests and CI
- `tests/workflows/run.mjs`: 69 behavioural scenarios for all four Workflow templates,
  extracted from `workflows.md` at test time (the documented code is the tested code). The
  new scenarios fail on 4.1.0 and pass on 4.1.1. Replaces the harness the README
  previously cited but the repository did not contain.
- `scripts/validate.py`: frontmatter, JSON, SVG safety, relative links, fences/details,
  en/zh README structure, em dashes in README.zh, version and skill/agent-count drift
  across plugin.json, badges, hero diagrams and CHANGELOG, outlined Chinese diagrams,
  `bash -n install.sh`, "latest release" lines and CHANGELOG link references; links are
  checked across all Markdown, anchors stripped.
- `.github/workflows/validate.yml` runs both on every push to `main` and every pull request.

## [4.1.0]

### Added — `theory-vs-result`, a third sibling skill for measured results
- New skill `skills/theory-vs-result/SKILL.md` + `/theory-vs-result` command, distilled
  from the author's own empirical research practice and generalized for any
  measured claim (backtest, benchmark, A/B test, ablation, training run, load test, debugging
  hypothesis). Every result is reported as a fixed four-part card — **Theory → Measured →
  Consistent? → Mechanism** (理论预期 → 实测 → 是否一致 → 机理): prediction written before
  data (else labelled `post-hoc`) with direction, magnitude, location and a noise floor;
  fairness checks; a consistency verdict (consistent · partly · inconsistent · can't tell);
  mechanism evidence tiers (verified · supported · inferred · untested); a mismatch walk
  pipeline → comparison → metric → theory → environment; the *rule verdict* (PASS · FAIL ·
  UNCERTAIN · descriptive only) kept separate from the *direction verdict* (alive ·
  alive-but-constrained · weakened · dead); and any new or tightened threshold explained in
  plain language and approved before it is frozen.
- New agent `mechanism-auditor` (read-only, `model: inherit`): the fresh-context audit of
  the cards. Re-derives headline numbers, checks fairness and noise, downgrades unearned
  verdicts and tiers, proposes an alternative mechanism that fits the same numbers, and
  names the cheapest discriminating check. Never re-runs experiments or reads unused data.

### Changed
- `keep-the-reasoning`: packet section 4 (Prior vs result) uses the theory-vs-result
  summary table for measured claims; Relationship_To_Sibling_Tooling cross-links it.
- `finding-unknowns`: `references/cartographer.md` reports returning `experiment`-route
  results as theory-vs-result cards and writes the row resolution from the card; the
  sibling-tooling table lists the new skill.
- README, README.zh, ARCHITECTURE, AGENTS, CLAUDE.md and EXAMPLES updated for the third
  skill and fifth agent.
- Diagrams: `hero` and `framework` (English and Chinese) updated for v4.1.0, three skills
  and five agents.

### Changed — review hardening before merge
- An independent two-round review closed the skill's rescue and post-hoc loopholes: a
  theory written after the result is a `post-hoc fit (not a test)`, capped at `inferred`
  and kept out of rule verdicts; a defect found afterwards voids the run only with
  evidence that it changes the headline number, and any rerun on spent data is a labelled,
  approved `re-read`; verdicts read the interval (one holding both 0 and the prediction is
  `can't tell`); `verified` excludes accounting identities; prediction cards carry a
  `Written` line and are saved before measuring (`predictions/{slug}.md`); the rule
  verdict is computed on the rule's frozen metric; `dead` needs a fired falsifier.
- Cartographer's `experiment` route now specifies rows as prediction cards (clearing line
  through the threshold gate) and maps returned cards onto ledger status; the
  mechanism-auditor reviews every card, including consistent ones.

## [4.0.0]

### Breaking — progressive-disclosure layout
- `SKILL.md` slimmed from 675 to ~490 lines: it keeps routing, the eight techniques, and a
  Cartographer **summary**; the full normative Cartographer protocol (C0–C3, Phase E,
  resume, threshold config, Cartographer checklist) moves to
  `skills/finding-unknowns/references/cartographer.md`, read on demand before entering the
  mode. Anything that read Phase C from `SKILL.md` directly (custom commands, forks) must
  now read the reference file. `/cartographer` is updated.

### Added — `keep-the-reasoning`, a sibling skill for the handoff
- New skill `skills/keep-the-reasoning/SKILL.md` + `/keep-the-reasoning` command,
  distilled from Addy Osmani's "Critical thinking when agents do the work". Where
  finding-unknowns covers the unknowns *before* work, this covers the human's judgment
  *at acceptance*: stakes triage (offload vs keep-the-reasoning), hypothesis before
  asking, "verified" defined up front, and a fixed-order handoff packet — evidence first,
  what each check proved and did NOT prove, decisions & assumptions, prior vs result,
  fresh-context counterargument, a never-empty "not checked", summary last. Also:
  surrender signals, rejection-becomes-a-rule, orchestration-tax warning, opt-in
  practice mode. No OMC skill covered this human-side posture.

### Added — from the two source articles, critically adapted
- **Irreversibility floor** (ledger `reversibility` column: reversible · wide ·
  irreversible). Regret contains P(wrong), a confidence estimate; for irreversible rows
  confidence never substitutes for the user — never silently defaulted under the 1.0
  bar, resolved only with recorded user confirmation. New seventh gate condition.
- **Priors**: every row records the user's/agent's expectation before evidence-based
  scoring; contradictions surface as surprises (blindspot-scout gains a Surprises
  section when given a prior; Phase 0 captures the prior).
- **Verification contract** in the crystallized spec and in Technique 5: per criterion
  a failable check, its artifact, what it proves, what it does NOT prove, and its lane;
  checks locked against the implementer.
- **Phase E execution rules** — the loop lives inside a task, the graph between tasks;
  edges must name what crosses (unnamed edges dropped); mechanical steps are code nodes;
  failures return per unit with `UNIT · VERDICT · REASON · EVIDENCE · SCOPE`; attempt cap
  (default 3) turns a task into a plan-suspect ledger row; a learning edge feeds derived
  constraints to every task not yet started; lanes close tasks by reversibility (the
  irreversible lane always waits for the user); the human sits at both ends — spec +
  contract at the front, irreversible lane + merge at the back — not in the middle.
- `fu-execute-verified` rewritten accordingly, then hardened after an independent
  adversarial review (1 CRITICAL, 6 HIGH, reproduced against a stubbed runtime): argument
  validation fails closed (unknown/missing lane, empty checks, duplicate ids, unknown
  deps, cycles, touched paths overlapping check files, irreversible tasks without
  post-checks); unnamed edges are dropped only from reversible upstreams and only after
  `confirmDroppedEdges`; per-task scheduling replaces wave barriers; path locks serialize
  tasks with overlapping `touches`; a separate check-runner context reports exit codes
  and check-file hashes, compared in code against a pre-run baseline (tampering stops
  the task); the irreversible lane runs only dry-run checks, waits for the user, and
  closes on post-checks after a resume with `executed`; `closed` lets a run resume
  without re-implementing; retries carry a code-built reason and the verifier sees the
  previous return; null agent results become `infra-error` instead of plan defects;
  derived constraints are deduped, conflicting ones halt the run, and already-closed
  tasks are listed for re-check. The template states which guarantees are enforced in
  code and which only by prompt. A second review round closed the remaining fail-open
  edges: paths normalized and globs rejected before locking; no task may touch any
  task's check files, with one baseline hashed before any implementer runs; check
  results matched to contract checks by exact string; check files mandatory for `wide`
  and `irreversible` tasks and missing baseline hashes treated as infra errors;
  `pending` lets a resume return tasks still awaiting the user without re-implementing
  them; writes outside every declared path stop the run (`scope-violation`); an
  implementer that never returns is an infra error, not a plan defect; a verdict whose
  constraint conflicts with the spec halts its own task. A third round fixed the scope
  check's false halts: paths already dirty before the run (the ledger, spec, notes, WIP)
  are baselined and excluded, `changedPaths` is mandatory, `.`/`..` paths are rejected,
  duplicate check results take the worst exit code, and contradictory resume lists are
  rejected. Exercised by a 50-scenario harness against a stubbed agent runtime (task
  inputs are never mutated), plus the reviewer's own adversarial scenarios.
- Exits (early exit, round-20 cap, "just build it") never waive the irreversibility
  floor; reversibility is classified upward when unsure and downgrades need the user;
  the task graph itself is user-approved before execution; the no-subagent rung never
  auto-closes a lane; the ledger's resolution column is append-only so priors survive.
- quiz-master's report gains **Decisions & assumptions** (defaults, scope cuts,
  reinterpreted requirements); Technique 8 matches.
- Not adopted, deliberately: "approve only the last step" (a human reviewing only a
  final artifact they never framed is rubber-stamping — contradicted by the Osmani
  source) and "confidence is the only input the model can influence" (agents can also
  edit their own checks — hence the locked contract). Unsupported magic numbers (3–6
  lanes) were not imported.

### Changed — re-synced with oh-my-claudecode 5.8.1
- Relationship section rewritten as a sibling table: defer to `interrogate`, `loft`,
  `show-me-your-work`, `blast-radius`, `in-your-own-words`/`sharpen`, `teach`,
  `ask-navigator` when installed instead of duplicating them.
- Corrected the deep-interview comparison: it is approval-gated (not "automatic handoff"),
  and its `--frontier` mode is the closest analogue of batched independent questions +
  territory routing.
- Frontmatter adopts OMC's current shape: one-sentence description, `aliases`, and a
  `metadata.credits` block.
- Fixed stale "one question at a time" wording left over from before 3.7.0 across the
  docs.

## [3.7.0]

### Changed — inheritance-aware model routing + batched interview
- **Model routing rebuilt around `inherit`.** The judgment and creative agents —
  `ledger-keeper` (scoring + gate verdict), `prototype-smith` (divergent brainstorm), and
  `quiz-master` (independent grading) — move from pinned tiers (`opus`/`sonnet`) to
  `model: inherit`, so they run at the session's own strength and are never downgraded
  (Fable stays Fable, Opus stays Opus). `blindspot-scout` stays `sonnet` — the one
  deliberate cost tier, because recon fans out in parallel — and is documented as
  overridable to `inherit`. Grounded in OMC's role tiers (opus=judgment, sonnet=execution,
  haiku=breadth) and Deep Research's "strongest model at the synthesis centre, cheaper
  fan-out" pattern; the adaptation is that the top tier is the inherited session model, not
  a hardcoded one — respecting Claude Code's native model-selection.
- **Interview is no longer one-question-at-a-time.** Cartographer's `interview` route and
  Technique 3 now ask via AskUserQuestion with up to **3 independent** questions per round
  (regret/blast-radius ordered), while still forbidding the bundling of *dependent*
  questions (where one answer changes the next). Per-round quadrant ambiguity is unchanged.
  `ledger-keeper`'s TARGET may return a 1–3 independent batch; the round template, the
  Defaults table, and the Bad example were updated accordingly.
- Docs (README + ARCHITECTURE) gained a Model-routing section; the three translated READMEs
  were regenerated to match.

## [3.6.0]

### Added — quadrant ambiguity scoring, mandatory interactive loop, cross-validated execution bridge
Driven by a second field test: discovery was strong, but the user could not see or steer
the model's certainty — work drifted into a fuzzy zone. The cure is deep-interview's
transparency machinery (from oh-my-claudecode), re-based on the four quadrants:

- **Per-quadrant clarity scores (0.0–1.0)** with justification + named gap, re-scored
  every round; weighted ambiguity `1 − (KK×0.20 + KU×0.25 + UK×0.25 + UU×0.30)` (UU
  heaviest). Threshold default 0.25, configurable via settings or
  `--quick 0.35 / --standard 0.25 / --deep 0.15`; announced with its source as the first
  line on Cartographer entry.
- **Round 0 topology gate**: 1–6 top-level components confirmed with the user before any
  scoring; quadrant scores report the weakest active component so one well-described
  component cannot hide sibling fog.
- **The interactive loop is mandatory in Cartographer mode**: every round ends with the
  four-quadrant score table + weighted ambiguity + weakest-target rationale, so the user
  steers instead of discovering drift at the end. Route discipline is unchanged — only
  interview-route rows become user questions.
- **Challenge modes** (Contrarian R4 / Simplifier R6 / Ontologist R8, once each).
- **Dual gate**: coverage conditions AND ambiguity ≤ threshold; round limits (soft 10,
  hard 20, early exit from R3 with transparent risk display).
- **Crystallized spec** `unknowns-spec-{slug}.md` on gate PASS, marked pending approval.
- **Phase E — cross-validated execution bridge** (approval-gated, never auto-executes):
  consensus-refine (independent planner + reviewer agents, ≤3 iterations, separate
  execution approval) or `fu-execute-verified` — a new Workflow template pairing every
  implementer with a refute-framed independent verifier plus one repair round. Normative
  invariant: the context that authored a spec/plan never self-approves its execution.
- `ledger-keeper` gains SCORE-QUADRANTS (single-call scoring, ledger-evidence-only
  justifications, "score drift" named as a failure mode); GATE becomes six conditions.

### Deferred (consciously)
- deep-interview's ontology/entity-convergence tracking — the topology gate covers the
  convergence need at far lower complexity; revisit if component drift shows up in tests.

## [3.5.0]

### Added — dynamic-workflow orchestration (Workflow tool integration)
- **`references/workflows.md`**: three ready-to-run Workflow scripts for the skill's
  fan-out-heavy operations, adopting Deep Research's orchestration discipline:
  - `fu-multi-lens-sweep` — parallel lens scouts, each finding adversarially verified the
    moment its lens completes (pipeline, no barrier), deduped across ALL seen findings,
    returned as schema-validated ledger rows (cross-lens duplicates recorded as
    confirmation).
  - `fu-verify-panel` — perspective-diverse refutation panel (alternative-explanation /
    evidence-independence / reproduction) for cost >= 4 resolutions; survives only if >=2
    refuters fail; refuters' discriminating checks land in the ledger verbatim.
  - `fu-uu-until-dry` — UU probe loop bounded by information (two consecutive dry
    rounds), not by a fixed round count.
- **Fallback ladder** (normative): Workflow -> parallel Agent calls -> fully inline; the
  invariants (named lenses, adversarial check before resolve, dedup vs seen, empty
  results are results) survive every rung.
- SKILL.md wires the templates at C0 (multi-lens sweep), C1 step 3.5 (verification
  panel), and the completeness critic (UU deep probe); Agent_Delegation documents the
  orchestration option, its opt-in requirement, and cost anchors.
- README architecture table, project structure, Cartographer section, and
  docs/ARCHITECTURE.md updated.

## [3.4.0]

### Changed — evidence discipline adopted from deep-research patterns, validated live
- **Adversarial verification before resolving high-cost rows (cost ≥ 4)**: construct the
  strongest alternative explanation consistent with the same evidence; if plausible, the
  row becomes `resolved-provisional` with a named discriminating check. (Live validation:
  a strong RankIC result resolved "is the DL signal real?" only provisionally — leakage
  produces the same IC; the discriminating check is the producer-pipeline audit.)
- **Cross-reference rule**: single-source resolutions of cost ≥ 4 rows are never fully
  resolved; two independent instruments (e.g. experiment AND audit) are required.
- **Confidence labelling**: every resolution records evidence, source(s), and a
  high/medium/low confidence label, with fact separated from inference.
- **Completeness critic before gate PASS**: an explicit "what's missing?" pass (shallowest
  quadrant, provisional resolutions, the unasked expert question) — a PASS without it is
  invalid.
- **Structured close-out report (C2.5)**: executive summary / findings-by-row with
  evidence + confidence / gaps & provisional items / methodology — acknowledging gaps is a
  deliverable, not an apology.
- New ledger status `resolved-provisional`; `ledger-keeper` RE-SCORE and GATE operations
  updated accordingly.

## [3.3.0]

### Changed — driven by a live field test (quant × deep-learning research task)
- **Cartographer's interview loop generalised into a clearing loop (router).** The ledger
  gains a `route` column (interview / territory-verify / experiment / audit); regret
  decides order, route decides instrument. Field test showed the three highest-regret
  unknowns all had non-interview routes — territory rows are now never asked of the user,
  and pending experiment/audit rows suspend the loop instead of spawning extra rounds.
- **Domain checklist hook at seeding**: the ledger is checked against a user-profile
  domain checklist (quant example: funding costs, liquidation distance, capacity, per-leg
  attribution, fee/slippage realism, regime dependence) and missing rows are added.
- **Multi-lens scout sweeps**: for high-stakes tasks, several `blindspot-scout` instances
  may run in parallel, each constrained to one named lens; the scout gains a Phase 0 lens
  check.
- **AFK / timeout handling** added to escalation rules: unanswered interview questions
  leave the row open and re-askable, with the gate suspended — answers are never invented.
- **Cost anchors** added to agent delegation (~50–100k subagent tokens for a codebase
  blind-spot pass) so "trivial cases stay inline" has a measurable bar.
- `ledger-keeper` updated accordingly: route-aware TARGET output, domain-checklist duty at
  SEED, and a new "route blindness" failure mode.

## [3.2.0]

### Changed
- Rewrote all four companion agents as full behavioural contracts following the
  oh-my-claudecode agent paradigm: Role with explicit responsibility boundaries,
  Why-This-Matters, Success-Criteria, Constraints, an investigation/operations protocol,
  an exact Output-Format, a Final-Response-Contract (the last message is the
  deliverable), named Failure-Modes-To-Avoid, Good/Bad examples with rationale, and a
  Final-Checklist. Agents grew from ~50 to ~130 lines each.
- blindspot-scout gains pre-commitment prediction (predict likely landmine categories
  before exploring); prototype-smith gains a divergence check (theses must conflict on
  at least one axis); ledger-keeper gains named operations (SEED / RE-SCORE / TARGET /
  GATE / CLOSE-OUT) with explicit verdict formatting; quiz-master gains diff-to-ledger
  cross-referencing with mandatory unlogged-deviation flagging.

## [3.1.0]

### Added
- `commands/` layer with four slash-command entry points that dispatch into named skill
  sections: `/finding-unknowns`, `/blindspot`, `/cartographer`, `/change-quiz`.
- `docs/ARCHITECTURE.md` — design reference covering the four layers, artifact contracts,
  and design principles.
- `AGENTS.md` — repository guide for coding agents and contributors, with invariants and
  validation commands.

### Changed
- Agent model tiers: `ledger-keeper` upgraded to opus (verdict-giving roles get the
  strongest model); other agents remain sonnet.
- `install.sh` now installs commands alongside the skill and agents.
- README architecture section rewritten around the layered command → skill → agent →
  artifact model.

## [3.0.0]

### Changed
- Restructured the skill into an executable-protocol format modelled on the
  [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) skill paradigm:
  Purpose / Use-When / Do-Not-Use-When / Why-This-Exists / Execution-Policy / phased
  Steps / Agent-Delegation / Good-and-Bad Examples / Escalation-and-Stop-Conditions /
  Final-Checklist / Advanced.
- Added a blocking Phase 0 (quadrant routing must be announced before any technique runs)
  and standardized per-round Cartographer report and question templates.
- Added explicit resume semantics (the unknowns ledger is the state) and a defaults table
  (prototype direction count, regret question bar, quiz size and rounds, soft round cap).
- Added six worked Good/Bad examples with rationale, and split the final checklist into
  lightweight and Cartographer lanes.

## [2.2.0]

### Changed
- Rewrote every technique in the skill as an operational block — When / Procedure /
  Stop-when / Guardrails — replacing prompt-only descriptions. Interviews now sort by
  blast radius; plans lead with tweakable decisions and admit their unknowns; quizzes
  grade honestly with a two-round stop rule; notes distinguish reversible from
  irreversible deviations.
- Added explicit input/output contracts to the companion-agent delegation table.
- Consolidated guardrails into per-technique guardrails plus a short global list.

## [2.1.0]

### Added
- Four companion agents under `agents/`: `blindspot-scout` (read-only reconnaissance),
  `prototype-smith` (divergent throwaway prototyping), `ledger-keeper` (Cartographer-mode
  regret scoring and coverage-gate verdicts), and `quiz-master` (independent post-change
  examiner).
- A "Companion agents" delegation section in the skill, with rules for when to delegate
  and when to stay inline; all techniques continue to work without the agents installed.
- Framework architecture diagram (`assets/framework.svg`) and an Architecture section in
  the README.

### Changed
- `install.sh` now installs the companion agents alongside the skill.
- Fixed YAML frontmatter quoting in the skill description.

## [2.0.0]

### Added
- Cartographer mode: a gated, regret-weighted interview backed by a lifecycle-persistent
  unknowns ledger, with a quadrant-coverage gate.
- Consolidated guardrails section in the skill.
- Plugin packaging under `.claude-plugin/` for installation via `/plugin install`.
- `EXAMPLES.md` with end-to-end prompts and a passive `CLAUDE.md` drop-in.
- SVG diagrams for the hero, four quadrants, lifecycle, and Cartographer mode.
- `CONTRIBUTING.md` and this changelog.

### Changed
- Rewrote the README in a formal, standardised structure.
- Expanded attribution to the source essay and clarified the non-affiliation disclaimer.

## [1.0.0]

### Added
- Initial release: single skill covering eight techniques for surfacing unknowns before,
  during, and after implementation, with an installer and MIT license.

[4.2.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v4.2.0
[4.1.1]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v4.1.1
[4.1.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v4.1.0
[4.0.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v4.0.0
[3.7.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v3.7.0
[3.6.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v3.6.0
[3.5.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v3.5.0
[3.4.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v3.4.0
[3.3.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v3.3.0
[3.2.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v3.2.0
[3.1.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v3.1.0
[3.0.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v3.0.0
[2.2.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v2.2.0
[2.1.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v2.1.0
[2.0.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v2.0.0
[1.0.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v1.0.0
