# finding-unknowns (passive drop-in)

Drop this file into a project root (or paste into your own CLAUDE.md) if you want the
finding-unknowns habits **without** installing the skill or plugin. It's a lighter, always-on
nudge; the full skill (with copy-paste prompts and Cartographer mode) lives in
[`skills/finding-unknowns/SKILL.md`](skills/finding-unknowns/SKILL.md).

> The map is not the territory. The bottleneck on long-horizon work is clarifying your
> *unknowns*. Before building something ambiguous or unfamiliar, spend cheap words to find
> them — it's always cheaper than rework.

## When a task is fuzzy or unfamiliar, first locate the unknown

- **Unknown Unknowns** (blind spots) → run a **blind-spot pass**: landmines, hidden context,
  what "good" looks like, and the questions an expert would ask. Do not implement yet.
- **Unknown Knowns** ("I'll know it when I see it") → **brainstorm** several throwaway
  directions or **point at reference code**, so tacit taste becomes explicit.
- **Known Unknowns** (nameable gaps) → **interview** one question at a time, architecture
  first; or write a **plan that leads with the decisions most likely to change**.
- **Known Knowns** → just write them down before they drift.

## During and after

- Mid-build, keep **implementation notes**: log any deviation and the conservative choice.
- Before merge, **quiz** yourself on what actually changed. Comprehension is the gate.

## Guardrails

- Discovery ends at understanding — don't slide into implementation.
- Prioritize architecture-changing unknowns over trivia.
- "No significant unknowns here" is a valid, valuable result.

---

*Distilled from Thariq Shihipar's "A Field Guide to Fable: Finding Your Unknowns"
([@trq212](https://x.com/trq212/status/2073100352921215386)). Community project, not
official Anthropic. Prior art: [Neeeophytee/finding-unknowns-skills](https://github.com/Neeeophytee/finding-unknowns-skills).*
