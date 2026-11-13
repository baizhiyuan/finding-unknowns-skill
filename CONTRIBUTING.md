# Contributing

Thank you for your interest in improving `finding-unknowns`. Contributions are welcome:
wording fixes, evidence from real use, documentation and diagrams.

## Getting started

1. Fork the repository and create a feature branch from `main`.
2. Make your changes. 6.0 is three pieces: [`CLAUDE.md`](CLAUDE.md) (the always-on text),
   [`skills/finding-unknowns/SKILL.md`](skills/finding-unknowns/SKILL.md) and the two
   commands in `commands/`. See [`AGENTS.md`](AGENTS.md) for what to keep in sync.
3. If you change the always-on text or a template, update both READMEs and the
   [glossary](docs/GLOSSARY.md) in the same change, and say in the CHANGELOG what the change
   does to behaviour and that it is unmeasured.
4. Update [`CHANGELOG.md`](CHANGELOG.md).
5. Open a pull request with a clear description of the change and its motivation.

## Guidelines

- **Scope.** The skill keeps the person's map of known and unknown visible. Do not add
  machinery (agents, installed scripts, hooks, files written by the skill) without evidence
  that the short text alone falls short; 5.x added such machinery and was never released.
  `install.sh` is the only script, and the look-back runs one inline filter.
- **Size.** The always-on text stays at or below 130 words and `SKILL.md` at or below 1,150;
  CI enforces both.
- **Evidence.** Claims in the README about what the text does must point to a report in
  `docs/evals/`. If nothing measured it, say so.
- **4.x fixes** go to branch `v4`.
- **Diagrams.** SVG assets in `assets/` must be well-formed XML and render on GitHub.
  `assets/zh/` holds the Chinese versions used by `README.zh.md`; when you change a diagram,
  update its Chinese counterpart in the same change.
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
  [`docs/GLOSSARY.md`](docs/GLOSSARY.md).
- **Release candidates.** During a release candidate the version fields (`plugin.json`,
  `marketplace.json`, the version-check line) keep the plain `X.Y.Z` that `validate.py`
  checks; the badges, the hero, the README alt texts and status lines, the manifest
  descriptions and the CHANGELOG `[X.Y.Z]` compare link name the candidate. At the final
  release, change all of these: set `VERSION` in `scripts/diagrams/hero.py`, regenerate both
  heroes (the Chinese one through `outline_cjk.py`), and update the badges, the alt texts, the
  status lines, the manifest descriptions and the compare link.
- **Attribution.** Preserve the attribution to the original essay. Do not represent this
  project as affiliated with Anthropic.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`,
`refactor:`, `chore:`, and so on.

## Local validation

```bash
python3 scripts/validate.py              # repository consistency checks (also run in CI)
python3 -m unittest discover -s tests    # install.sh and the look-back filter
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
