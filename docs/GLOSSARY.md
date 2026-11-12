# Glossary

The 5.2 vocabulary. [SKILL.md](../skills/finding-unknowns/SKILL.md) and its references
define each term where it is used, and [`references/card.md`](../skills/finding-unknowns/references/card.md)
is normative for the card format; this page is where the terms meet. Chinese labels follow
[`references/results.md`](../skills/finding-unknowns/references/results.md) and the
Chinese README.

## Setup

- **The 56 words** — the always-on text in [`CLAUDE.md`](../CLAUDE.md), measured in Stage 0
  (where the arm is called "w60"). The recommended setup. Pinned verbatim.
- **`CLAUDE.next.md`** — an 82-word candidate that adds "non-trivial", one batch of
  decisions with a recommendation, and the irreversible-step rule. Untested; it replaces
  the 56 words only after the Tier 1 check.
- **Classic line** — branch `v4` (v4.3.2): structured mode, Cartographer and the 4.x
  agents. Bug fixes only.

## The card

- **Task card** — one Markdown file per task, `.finding-unknowns/tasks/{slug}.md`: a
  five-line header, the Brief, Amendments, a Deltas rollup, Model changes, Open, and the
  Debrief at the end. One format everywhere: lines with fixed keys in a fixed order,
  nested lists, no tables.
- **Header** — `Goal · State`, `Needs you`, `Mode · Last seen by you`, `Timing`. `Needs
  you` exists once, here. `fu freeze` owns `State` and `Timing`.
- **State** — `briefing | building | waiting on you | debriefed`. A card is open until it
  is `debriefed`.
- **Brief** — written by `/fu-brief` and frozen on the person's yes: the approach (one
  reason per decision), both sides' predictions, the stop-points with a budget multiple,
  `Irreversible:` lines, the contract and the check files. Never edited after it freezes.
- **Amendment** — `M{n} {time} · after D{n} · {decided-for-you | confirmed}: … · why: …`.
  Dated and append-only. It explains a miss; it never removes a prediction from grading.
- **Delta** — one line in `{slug}.deltas.md`, the only place deltas live:
  `D{n} {time} {deviation | surprise | decided-for-you}: … → {evidence path}`. A
  `decided-for-you` delta adds `cost if wrong`; an optional `[stop: …]` tag marks a stop.
  The card keeps `Latest:` and a rollup of at most three lines.
- **Model change** — `You expected X → it is Y, because Z`, at most five,
  `shown, not confirmed` until the person confirms it.
- **Last seen** — the delta the person last saw. `/fu-catch-up` shows only what came
  after it.
- **Timing** — `Brief frozen {time}, commit {hash}` after `fu freeze`; `self-reported` when
  no commit was possible (no git, an ignored path, other work staged, a failing hook, or
  `commits: no`).
- **`decisions.md`** — answers only the person could give, quoted and dated, the newest 30
  lines. Read before every Brief so an answered question is never asked again.
- **Profile** — `.finding-unknowns/profile.md`, local: `mode: ship | learn`,
  `strict: no | yes`, `view: yes | no`, `commits: yes | no`, `guard: off | log | ask`.

## Predictions and checks

- **Prediction vs contract check** — a prediction is a claim about something the agent
  does not control: where the bug is, a number, an outcome. What the agent makes true
  ("the tests will pass") is a contract check.
- **`P{n}` and `A{n}`** — the person's and the agent's predictions, and nothing else.
  `P` lines quote the person verbatim; with no answer the line is `P: none given`. The
  agent never writes a `P` line on the person's behalf.
- **Confidence** — person: `low | medium | high | no idea | not given` (never inferred);
  agent: `low | medium | high`.
- **Falsifier** — the result that would show a prediction wrong. Every prediction also has
  a **should not change** half: where no effect should appear.
- **Contract** — items `C{n} {claim}` with `check`, `does NOT prove` and `lane`. A check
  must be able to fail; `does NOT prove` is mandatory; check files are locked against the
  builder.
- **Prediction log** — `.finding-unknowns/predictions-log.md`, local, written only by
  `fu log`: one line per graded prediction. From five graded predictions per side, a
  calibration line; an agent that holds every one is predicting too safely.

## Interruptions

- **Stop-point** — one of four conditions on which the build stops for the person:
  irreversible step, scope change, dead premise, budget overrun. Everything else becomes a
  delta.
- **Turn-end rule** — once the build starts, every turn ends with a completion report or a
  stop request; never an optional question, a menu, or a question about committing the
  person's code.
- **Lane** — reversibility only: `reversible` (contained, cheap to undo) · `wide`
  (undoable, touches shared surface) · `irreversible` (data rewritten or dropped,
  deletion, production, money, publication, commitments to people). Classify upward when
  unsure.
- **Irreversible step** — named on a Brief `Irreversible:` line with its exact command;
  its checks are dry runs; it runs once, only after a chat yes to that exact command; a
  `post-check` closes it. The guard hook's permission prompt is a second check, never the
  yes.
- **Dead premise** — a Brief premise or a falsifier fired and no reversible path remains.
  Two failed fixes that share an assumption: log and test it; a third failure is the stop.

## Code

- **`fu` script** — `scripts/fu.py`, Python standard library only: `init`, `lint`,
  `freeze`, `integrity`, `log`, `list`, `render`, and `guard` for the hook. Everything
  deterministic; the model never does by hand what `fu` does.
- **Guard hook** — `hooks/hooks.json`, plugin install only. A second safety net: asks
  (`ask`) before a Bash command that matches an open card's `Irreversible:` line, records
  each run, asks again on a second run. Under `bypassPermissions`, where Claude Code
  ignores a hook's ask, it only records. Advisory: never denies, fails open.
- **Hard enforcement** — a Claude Code `permissions.ask` or `permissions.deny` rule for
  the exact command in user or managed settings, which the agent cannot edit; per Claude
  Code's docs, these apply in bypass-permissions mode too.
- **Strict profile** — `strict: yes`, set with `fu init --strict` or on request. Template
  only; `fu lint` caps must pass before the Brief-approval ask; generic destructive
  commands also ask. Meant for small models; untested.
- **HTML view** — `fu render` output under `.finding-unknowns/view/`, offered inside the
  Brief-approval ask for a complex task. Fixed templates, no script, no network.

## Grading

- **Completion report = Debrief** — when carded work completes, its report is the
  Debrief. `/fu-debrief` is for late results and re-grades.
- **Fresh-context grading** — `mechanism-auditor` receives the frozen card and the artifact
  paths, never the transcript or the builder's claims. Used for an irreversible-lane card,
  a measured result, or on request; otherwise the Debrief is labelled
  `same-context — weaker`.
- **Integrity** — three lines from `fu integrity`: the Brief against its freeze commit,
  the check files, and changed hunks no delta or Amendment names; plus
  `Irreversible runs:` when a card-named command ran more than once.
- **Bottom line** — `holds` (consistent IDs), `did not hold` (partly, inconsistent),
  `stops at` (can't tell, post-hoc fit). Every graded ID appears once.
- **Theory → Measured → Consistent? → Mechanism** (理论预期 → 实测 → 是否一致 → 机理) —
  how every measured prediction is graded. Research claims add a stopping rule and an
  append-only run table.
- **Consistent? verdicts** — `consistent` 一致 · `partly` 部分一致 · `inconsistent` 不一致 ·
  `can't tell` 无法判断 · `post-hoc fit` 事后拟合. An interval holding both 0 and the
  predicted size is `can't tell`.
- **Post-hoc fit** — a prediction written after the result was seen. Not a test; its tier
  is at most `inferred`, and it never feeds a rule verdict.
- **Mechanism tiers** — `verified` 已验证 (a test that would have failed were it false) ·
  `supported` 有数据支持 · `inferred` 推断 · `untested` 未检验. The verb never claims more
  than the tier.
- **Rule verdict vs direction verdict** — the rule verdict is mechanical, in the frozen
  rule's labels or `descriptive only`. The direction verdict, `alive` 仍成立 ·
  `alive-but-constrained` 有条件成立 · `weakened` 已削弱 · `dead` 已否定, is the person's.
- **No rescue** — a good story explains a miss; it never turns it into a hit.

*Removed in 5.2 and kept on branch `v4`:* structured mode, Cartographer, the unknowns
ledger, regret, clarity scores, the six-condition gate, quadrant routing, the numbered
techniques and the full handoff packet.
