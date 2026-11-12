# Contributing

Thank you for your interest in improving `finding-unknowns`. Contributions of all kinds are
welcome, including new techniques, prompt refinements, documentation, and diagrams.

## Getting started

1. Fork the repository and create a feature branch from `main`.
2. Make your changes. Each skill lives in `skills/<name>/SKILL.md` (finding-unknowns,
   keep-the-reasoning, theory-vs-result); Cartographer's full protocol is in
   `skills/finding-unknowns/references/`. See [`AGENTS.md`](AGENTS.md) for what to keep in sync.
3. If you change the skill, keep [`EXAMPLES.md`](EXAMPLES.md), the
   [glossary](docs/GLOSSARY.md), and the tutorials ([`docs/TUTORIAL.md`](docs/TUTORIAL.md),
   [`docs/TUTORIAL.zh.md`](docs/TUTORIAL.zh.md)) consistent with it. The passive drop-in
   [`CLAUDE.md`](CLAUDE.md) is the 82-word text promoted after the
   [Tier 1 check](docs/evals/2026-11-12-tier1/README.md); it is frozen, so do not edit or
   expand it without a new pre-registered check.
4. Update [`CHANGELOG.md`](CHANGELOG.md) under an "Unreleased" heading.
5. Open a pull request with a clear description of the change and its motivation.

## Guidelines

- **Scope.** Keep the skill focused on discovering unknowns. Execution and delivery concerns
  belong to other tools referenced in the README.
- **Commands.** `commands/` holds only `/blindspot`, `/cartographer` and `/change-quiz`. Do
  not add a command with the same name as a skill: Claude Code already exposes each skill
  as a slash command, and a same-named command shadows it.
- **Prose quality.** Techniques should be actionable and concise. Prefer concrete, copy-paste
  prompts over abstract description.
- **Diagrams.** SVG assets in `assets/` must be well-formed XML and should render on GitHub.
  `assets/zh/` holds the Simplified Chinese versions used by `README.zh.md`; when you change
  a diagram, update its Chinese counterpart in the same change.
- **Chinese diagrams are generated.** Edit the source in `assets/zh/src/NAME.svg` (Chinese text
  uses `font-family="Noto Sans SC, …"`, one line per `<text>`, no letter-spacing), then
  regenerate the published file, which outlines the Chinese glyphs so every viewer sees the
  same typeface:

  ```bash
  # Noto Sans SC Regular / Medium / Bold (SIL OFL) from
  # https://github.com/notofonts/noto-cjk/tree/main/Sans/SubsetOTF/SC
  python3 scripts/outline_cjk.py --fonts /path/to/noto-sans-sc --out assets/zh assets/zh/src/*.svg
  ```

  Never hand-edit `assets/zh/*.svg`; it is overwritten on every build. Chinese wording follows
  the terminology already used in `README.zh.md`.
  Validate with any standard XML parser before committing.
- **Attribution.** Preserve the attribution to the original essay. Do not represent this
  project as affiliated with Anthropic.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`,
`refactor:`, `chore:`, and so on.

## Local validation

```bash
python3 scripts/validate.py      # repository consistency checks (also run in CI)
node tests/workflows/run.mjs     # behavioural tests for the Workflow templates
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
