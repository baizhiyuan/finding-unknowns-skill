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
  Validate with any standard XML parser before committing.
- **Attribution.** Preserve the attribution to the original essay. Do not represent this
  project as affiliated with Anthropic.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`,
`refactor:`, `chore:`, and so on.

## Local validation

```bash
# Validate SVG assets
for f in assets/*.svg; do python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse('$f')"; done

# Validate plugin manifests
python3 -c "import json; json.load(open('.claude-plugin/plugin.json')); json.load(open('.claude-plugin/marketplace.json'))"
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
