# Contributing

Thank you for your interest in improving `finding-unknowns`. Contributions of all kinds are
welcome, including new techniques, prompt refinements, documentation, and diagrams.

## Getting started

1. Fork the repository and create a feature branch from `main`.
2. Make your changes. The skill content lives in `skills/finding-unknowns/SKILL.md`.
3. If you change the skill, keep the passive drop-in [`CLAUDE.md`](CLAUDE.md) and
   [`EXAMPLES.md`](EXAMPLES.md) consistent with it.
4. Update [`CHANGELOG.md`](CHANGELOG.md) under an "Unreleased" heading.
5. Open a pull request with a clear description of the change and its motivation.

## Guidelines

- **Scope.** Keep the skill focused on discovering unknowns. Execution and delivery concerns
  belong to other tools referenced in the README.
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
# Validate SVG assets
for f in assets/*.svg assets/zh/*.svg; do python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse('$f')"; done

# Validate plugin manifests
python3 -c "import json; json.load(open('.claude-plugin/plugin.json')); json.load(open('.claude-plugin/marketplace.json'))"
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
