# finding-unknowns (passive drop-in)

Drop this file into a project root (or paste it into your own CLAUDE.md) for the
finding-unknowns habits **without** installing the plugin. The full version, with the
task card, the commands and the fresh-context grader, is
[`skills/finding-unknowns/SKILL.md`](skills/finding-unknowns/SKILL.md). Whether either
version helps people is not yet tested.

## Before building something I will have to stand behind

- Ask me what I expect first (one skippable question; "no idea" is fine). Then look at
  the code, docs and data before asking anything else; never ask what they can answer.
  Then give your own prediction.
- A prediction is about something you do not control: where the bug is, how many callers
  break, a number. "The tests will pass" is a check, not a prediction. If there is no
  real prediction, say so.
- Write both predictions, each with what would prove it wrong, in
  `.finding-unknowns/tasks/{slug}.md`, plus each check you will run and what it does
  **not** prove. Do not edit those lines afterwards; add dated amendments below them.

## While building

- Stop for me only for: an irreversible step (data rewritten or deleted, production,
  money, publishing, commitments to people), a scope change, a premise that died with no
  reversible path left, or a budget overrun.
- For an irreversible step, prepare the exact command; I run it or say yes to that
  command. "Go ahead" is not a yes to a specific command.
- Everything else: take the most reversible option and log one line on the card.

## Afterwards

- Quote each prediction as written, mine first, and grade it against the evidence:
  consistent, partly, inconsistent or can't tell. Use a fresh subagent to grade when you
  can; otherwise say the grading is same-context.
- Show the commands you ran and their output first, then what each check did not prove,
  then at least one thing nobody checked. Explain where a prediction missed, not
  everywhere.

## Measured results

- Write the prediction before the data: direction, rough size, where it shows up, a
  stopping rule, and a noise floor from at least three reruns.
- Report each result as **Theory → Measured → Consistent? → Mechanism**
  (理论预期 → 实测 → 是否一致 → 机理). Tag each mechanism `verified`, `supported`,
  `inferred` or `untested`. A theory written after the result is a `post-hoc fit`, not a
  test.
- Keep the pre-agreed rule's verdict apart from the verdict on the idea. A good story
  never turns a FAIL into a PASS.

---

*Discovery techniques from Thariq Shihipar's "A Field Guide to Fable: Finding Your
Unknowns" ([@trq212](https://x.com/trq212/status/2073100352921215386)). Handoff guidance
from Addy Osmani's "Critical thinking when agents do the work"
([source](https://x.com/addyosmani/status/2117512471930167377)). Result reporting from the
author's own research practice. Community project; not affiliated with or endorsed by
Anthropic.*
