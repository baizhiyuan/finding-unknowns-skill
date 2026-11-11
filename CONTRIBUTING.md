# Contributing

Thank you for your interest in improving `finding-unknowns`. Contributions of all kinds are
welcome, including new techniques, prompt refinements, documentation, and diagrams.

## Getting started

1. Fork the repository and create a feature branch from `main`.
2. Make your changes. The one skill lives in `skills/finding-unknowns/SKILL.md` (at most
   1,500 words); per-phase detail is in `skills/finding-unknowns/references/`. Changes in
   behaviour start from the [5.0 design](docs/design/5.0.md). See [`AGENTS.md`](AGENTS.md)
   for what to keep in sync.
3. If you change the skill, keep the passive drop-in [`CLAUDE.md`](CLAUDE.md),
   [`EXAMPLES.md`](EXAMPLES.md), the [glossary](docs/GLOSSARY.md), and the tutorials
   ([`docs/TUTORIAL.md`](docs/TUTORIAL.md), [`docs/TUTORIAL.zh.md`](docs/TUTORIAL.zh.md))
   consistent with it.
4. Update [`CHANGELOG.md`](CHANGELOG.md) under an "Unreleased" heading.
5. Open a pull request with a clear description of the change and its motivation.

## Guidelines

- **Scope.** Keep the plugin focused on the task card: helping the person predict, follow
  and judge work an agent does. Execution and delivery concerns belong to other tools.
- **Evidence.** Whether the plugin helps people is untested. Do not add claims beyond the
  design and the evals in `docs/evals/`.
- **Commands.** `commands/` holds only `/brief-me`, `/catch-up` and `/debrief`. Do not add
  a command with the same name as a skill or a Claude Code built-in: Claude Code already
  exposes each skill as a slash command, and a same-named command shadows it.
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
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
