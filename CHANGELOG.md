# Changelog

All notable changes to this project are documented in this file. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[3.4.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v3.4.0
[3.3.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v3.3.0
[3.2.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v3.2.0
[3.1.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v3.1.0
[3.0.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v3.0.0
[2.2.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v2.2.0
[2.1.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v2.1.0
[2.0.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v2.0.0
[1.0.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v1.0.0
