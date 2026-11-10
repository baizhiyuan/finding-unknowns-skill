# finding-unknowns (passive drop-in)

Drop this file into a project root (or paste into your own CLAUDE.md) if you want the
finding-unknowns habits **without** installing the skill or plugin. It's a lighter, always-on
nudge; the full skill (with copy-paste prompts and Cartographer mode) lives in
[`skills/finding-unknowns/SKILL.md`](skills/finding-unknowns/SKILL.md), and the handoff
sibling in [`skills/keep-the-reasoning/SKILL.md`](skills/keep-the-reasoning/SKILL.md), and the
measured-result sibling in [`skills/theory-vs-result/SKILL.md`](skills/theory-vs-result/SKILL.md).

> The map is not the territory. The bottleneck on long-horizon work is clarifying your
> *unknowns*. Before building something ambiguous or unfamiliar, spend cheap words to find
> them — it's always cheaper than rework.

## When a task is fuzzy or unfamiliar, first locate the unknown

- **Unknown Unknowns** (blind spots) → run a **blind-spot pass**: landmines, hidden context,
  what "good" looks like, and the questions an expert would ask. Do not implement yet.
- **Unknown Knowns** ("I'll know it when I see it") → **brainstorm** several throwaway
  directions or **point at reference code**, so tacit taste becomes explicit.
- **Known Unknowns** (nameable gaps) → **interview** with up to 3 independent questions
  per round (dependent questions one at a time), architecture first; or write a **plan
  that leads with the decisions most likely to change**.
- **Known Knowns** → just write them down before they drift.

## During and after

- Mid-build, keep **implementation notes**: log any deviation and the conservative choice.
- Before merge, **quiz** yourself on what actually changed. Comprehension is the gate.
- When handing work over for acceptance, lead with evidence, say what each check did **not**
  prove, list the decisions you made, and name what went unchecked (`keep-the-reasoning`).

## When reporting a measured result

- Write the **prediction before the data** (direction, rough size, where it should show up,
  and the noise floor); a theory written after the result is labelled `post-hoc`.
- Report each result as one card: **Theory → Measured → Consistent? → Mechanism**
  (理论预期 → 实测 → 是否一致 → 机理). Compare like with like: same data, seeds, metric.
- Consistency is consistent / partly / inconsistent / can't tell (inside the noise).
  Tag every mechanism `verified`, `supported`, `inferred`, or `untested` — an inference is
  never a mechanism.
- On a mismatch, walk pipeline → comparison → metric → theory → environment, name the
  broken link, and give the smallest check that would tell the explanations apart.
- Keep two verdicts apart: the pre-agreed **rule** (PASS / FAIL / UNCERTAIN / descriptive
  only) and the **direction** (alive / constrained / weakened / dead). A good story never
  turns a FAIL into a PASS.
- Explain any new or tighter threshold in plain words and get approval before applying it.

## Guardrails

- Discovery ends at understanding — don't slide into implementation.
- Prioritize architecture-changing unknowns over trivia.
- Gate on blast radius, not confidence: an unknown guarding an irreversible step always
  goes to the user.
- "No significant unknowns here" is a valid, valuable result.

---

*Distilled from Thariq Shihipar's essay "A Field Guide to Fable: Finding Your Unknowns"
([@trq212](https://x.com/trq212/status/2073100352921215386)). Handoff guidance draws on
Addy Osmani's "Critical thinking when agents do the work"
([source](https://x.com/addyosmani/status/2117512471930167377)). Result-reporting guidance is
distilled from a long-running empirical research practice. Community project; not
affiliated with or endorsed by Anthropic.*
