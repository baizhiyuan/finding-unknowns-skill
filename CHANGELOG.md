# Changelog

All notable changes to this project are documented in this file. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[3.0.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v3.0.0
[2.2.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v2.2.0
[2.1.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v2.1.0
[2.0.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v2.0.0
[1.0.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v1.0.0
