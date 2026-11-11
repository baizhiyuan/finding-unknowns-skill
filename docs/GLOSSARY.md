# Glossary

The 5.0 vocabulary. [SKILL.md](../skills/finding-unknowns/SKILL.md) and its references
define each term where it is used; this page is where they meet. Chinese labels follow
[`references/results.md`](../skills/finding-unknowns/references/results.md).

## The card

- **Task card** — one Markdown file per task, `.finding-unknowns/tasks/{slug}.md`, read by
  the person and kept current by the agent. Header, frozen Brief, Amendments, Deltas, Model
  changes, Open, Debrief. Committed by default.
- **Brief** — the top of the card, written by `/fu-brief` and frozen on the person's yes:
  approach with one line of why per decision, both sides' predictions, the stop-points with
  a budget multiple, and the contract. Never edited after it freezes.
- **Amendment** — a dated, append-only change to the approach or a premise, tagged
  `decided-for-you` (reversible path remained) or `confirmed` (the person agreed). It
  explains a miss; it never removes a prediction from grading.
- **Delta** — one line logged during the build: `deviation`, `surprise` or
  `decided-for-you`, with an evidence pointer. All deltas go to `{slug}.deltas.md`; the
  card shows the current session's and a three-line rollup of earlier ones.
- **Model change** — "You expected X → it is Y, because Z". At most five live lines, each
  `shown, not confirmed` until the person confirms it.
- **Last seen** — the delta the person last saw, updated only after `/fu-catch-up` or
  `/fu-debrief` has shown the card. `/fu-catch-up` shows only what came after it.
- **Timing** — the header line recording when the Brief froze: `commit {hash}` when the
  card was committed, else `self-reported` (no git, an ignored path, other work staged,
  history mid-operation, a failing hook, or commits declined).
- **Mode** — `ship` or `learn`, asked once per project and stored in `profile.md`. Ship:
  one skippable prediction question, one-line explanations. Learn: up to three questions,
  a short why with one concrete example on misses. Never announced during work.

## Predictions and checks

- **Prediction vs contract check** — a prediction is a claim about something the agent
  does not control: where the bug is, how many callers break, a number, an outcome. What
  the agent makes true ("the tests will pass") is a contract check. A card may honestly
  say "No real prediction here; contract only".
- **Falsifier** — the result that would show a prediction wrong. Every prediction also has
  a "should not change" half: where the effect should be absent.
- **Contract** — `claim | check (can fail) | does NOT prove | lane`. A check must be able to
  fail; the "does NOT prove" column is mandatory; checks named in it are not edited by the
  implementer.
- **Prediction log** — `.finding-unknowns/predictions-log.md`, personal and not committed:
  one line per graded prediction (date, slug, ID, owner, verdict, confidence). The
  person's hit rate is a learning signal; an agent hit rate near 100 % means its
  predictions are too soft.

## Interruptions

- **Stop-point** — one of the four conditions on which the build stops for the person:
  irreversible action, scope change, dead premise (no reversible path left), budget
  overrun past the agreed multiple. Everything else becomes a delta.
- **Lane** — reversibility only: `reversible` (contained, cheap to undo) · `wide`
  (undoable, touches shared surface) · `irreversible` (data rewritten or dropped,
  deletion, production data, money, external publication, commitments to people).
  Classify upward when unsure.
- **Irreversibility floor** — confidence never substitutes for the person on an
  irreversible item; downgrading from `irreversible` needs the person's yes.
- **Build rule** — for an irreversible step, the agent prepares the exact command; the
  person runs it or says yes to that command (a general "go ahead" is not one); the
  contract's post-check runs before the item closes.

## Grading

- **Fresh-context grading** — `mechanism-auditor` (or any fresh subagent) receives the
  frozen card and the artifact paths, never the build transcript, and fills Measured and
  Consistent?. Without subagents the Debrief is labelled `same-context — weaker`.
- **Theory → Measured → Consistent? → Mechanism** (理论预期 → 实测 → 是否一致 → 机理) —
  the four-part card every measured prediction is graded in. Research claims add a
  stopping rule (how many runs before any verdict) and an append-only run table.
- **Consistent? verdicts** — `consistent` 一致 · `partly` 部分一致 · `inconsistent` 不一致 ·
  `can't tell` 无法判断. The interval governs: an interval holding both 0 and the
  predicted size is `can't tell`.
- **Post-hoc fit** (事后拟合) — a prediction written after the result was seen. Not a test;
  its mechanism tier is at most `inferred`, and it never feeds a rule verdict.
- **Mechanism tiers** — `verified` 已验证 (a test that would have come out differently if
  the mechanism were false) · `supported` 有数据支持 (fits, no discriminating test) ·
  `inferred` 推断 (a story with no check) · `untested` 未检验 (named so it can be tested).
- **Rule verdict vs direction verdict** — the rule verdict is mechanical, in the frozen
  rule's own labels (e.g. `PASS · FAIL · UNCERTAIN`) or `descriptive only`. The direction
  verdict, `alive` 仍成立 · `alive-but-constrained` 有条件成立 · `weakened` 已削弱 ·
  `dead` 已否定, is proposed by the agent and owned by the person. A good story never
  turns a FAIL into a PASS.
- **Void** (作废) — a run marked `void: pipeline defect`, only with evidence that the
  defect changes the headline number. The original verdict stays visible.

*Removed in 5.0:* quadrants as announced routing, the ledger, regret, clarity scores, the
six-condition gate, rigor level and packet size announcements. See tag `v4.3.2`.
