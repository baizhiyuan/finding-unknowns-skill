# Changelog

All notable changes to this project are documented in this file. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[2.1.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v2.1.0
[2.0.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v2.0.0
[1.0.0]: https://github.com/baizhiyuan/finding-unknowns-skill/releases/tag/v1.0.0
