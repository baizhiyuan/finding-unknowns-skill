<!-- Advisor review by Fable 5.2 (claude-fable-5-2), 2026-11-11, read-only against tag v4.3.2 plus the then-unreleased eval docs. File paths and line numbers refer to that state. Reproduced verbatim except that local absolute links were turned into plain paths. -->

# Advisor critique: the 5.0 direction for finding-unknowns

**Bottom line:** the direction is right, but I would organise around a persistent per-task card rather than a three-phase loop. I would also put the teaching weight in the Debrief, not the Brief, and treat every "kept" piece as unevidenced until a human eval says otherwise. The largest risk is that a polished debrief makes people feel informed without being informed, so the eval must measure calibration.

## 1. Organising idea: the card, not the loop

Brief → Quiet build → Debrief is the right spine for a one-session task. It breaks in the two areas you care most about:

- **Multi-session work:** phases do not survive a session boundary; files do.
- **Research:** there is one Brief and many Debriefs, spread over days.

I would make the unit a **task card**: one file, frozen Brief on top, append-only deltas below. The commands are then operations on it: `/brief` creates, `/status` reads, `/debrief` closes predictions.

Two changes to the draft loop:

- **Add a re-brief beat.** When a Brief premise dies, the card is amended (dated, old line kept). Otherwise the Debrief compares against a dead document.
- **Separate predictions from contract checks.** "Tests will pass" is something the agent makes true. Only claims about things it does not control test understanding: where the bug is, how many callers break, a benchmark number, an experiment outcome. Many engineering tasks have zero or one of these. Requiring "direction, rough size, where" on every task (§4.1) manufactures ceremony. Say "no real prediction here; contract only".

`theory-vs-result` is the centre of 5.0, not a sibling. The author's goal statement is almost a paraphrase of its card, and it is the most original part of the repo.

## 2. Long and multi-session tasks

**Artifact:** `.finding-unknowns/tasks/{slug}.md`, with a hard cap of about 40 lines on the live part.

1. **Header (3 lines):** goal, state, the next decision that needs you.
2. **Brief (frozen, dated):** approach and one-line why; predictions (yours and mine, separately); stop-points; contract with a "does NOT prove" column.
3. **Deltas (append-only, one line each):** deviations, surprises, decisions made on your behalf, each pointing to evidence.
4. **Model changes (five live lines at most):** "you expected X → it is Y, because Z".
5. **Open:** unchecked items and pending decisions.

**Keeping it short:**

- One-line entries with pointers; detail goes to a log file.
- Each session's deltas roll up to three lines at session end.
- A **last-seen marker**: resume shows only what changed since the person last acknowledged the card. Orientation cost then scales with the delta, not the history.

**Interruptions:** push only on conditions checkable against the card, not on judged stakes.

- An action in an irreversible class (already defined at `references/cartographer.md:108-127`).
- A scope change.
- A Brief premise or a prediction's falsifier has fired and no reversible path remains. The draft lacks this one. v2's H5 ("the bug is in report.sql", and it isn't) and the Jetson field note (the prior was contradicted five times) are both this case.
- A budget overrun past an agreed multiple.

Everything else is written to the card and pulled by the person. Pending questions are batched at a stop.

**Commit the card.** `skills/finding-unknowns/SKILL.md:102-113` gitignores `.finding-unknowns/` by default, and `skills/theory-vs-result/SKILL.md:161-163` already notes this breaks the `Written` line. For `tasks/` and `predictions/`, flip the default. A commit hash gives tamper-evident prediction timing and survives machines and worktrees.

## 3. Learning

- **Move the teaching to the point of error.** Front-loaded principles arrive before the person needs them and get skimmed. In the Brief, give one sentence of "why" per decision, with more on request. The real explanation goes in the Debrief, on the rows where a prediction failed, especially the person's own.
- **Have the person predict first: one question, skippable, with a confidence.** It costs about 15 seconds and buys three things:
  - a prior the agent did not write, so corrections are attributable;
  - the strongest known learning effect here (confident errors that get corrected are remembered);
  - a behavioural expertise signal.

  Ask the person before showing the agent's prediction, so they are not anchored. Use one in shipping mode and up to three in learning mode. "No idea" stays valid (`skills/keep-the-reasoning/SKILL.md:103-109`).
- **Adapt depth from predictions, not self-report.** Ask `ship | learn` once per project. After that, a correct and confident prediction means skip the explanation; a wrong one means explain. For experts, explanation is pure cost.
- **Demote the quiz from gate to tool.** "Must-pass" and "comprehension is the merge gate" (`SKILL.md:286-304`, `agents/quiz-master.md`) are paternalistic on one's own project and will be skipped. Replace with:
  - two or three questions, generated from the deltas and the wrong predictions;
  - asked at the *next* session's start, before showing the card. That is retrieval practice, and it also detects a stale Brief.
  - a two-sentence teach-back as an alternative to multiple questions.
- **Promote the "Prediction habit"** in Practice mode (`keep-the-reasoning/SKILL.md:228-238`). It is the seed of all this and is currently buried.

## 4. Research work

The unit is the **claim**, which outlives many runs.

- **Brief = the prediction card** (`theory-vs-result/SKILL.md:138-154`) plus three additions:
  - the person's prediction and the agent's as separate lines; the disagreement is the most informative row;
  - a **stopping rule** (how many seeds or runs before any verdict);
  - a noise floor *measured* before the rule is frozen.

  The skill says "noise floor first" but sets no minimum. Your own v2 is the cautionary case: its pre-registered rule, built on two runs, called +2.5 "signal" (`docs/evals/2026-11-11-v2-cross-model/README.md:102-111`), and v3 reversed it.
- **Results over days:** an append-only run table per claim (date, config, what changed, result, cumulative trials, data spent), with a one-line Note card per run (`theory-vs-result/SKILL.md:99`). The full debrief runs only at the declared stopping point. Interim status reads "3 of 5 seeds done, no verdict yet". Peeking at noisy interim results is research's version of the interruption.
- **When the person's hypothesis is under test,** the agent's pull is to rescue it. The two-verdict rule (`:298-314`) is the protection: the rule verdict is mechanical, the direction verdict is the person's. Debrief against the person's own quoted words.
- **Protect:** the trials and data-budget lines (`:149-151`), `post-hoc fit`, `void`, the mismatch walk (`:254-271`), and `mechanism-auditor`'s `untraceable` for paper numbers.

## 5. Debrief honesty when one agent wrote both

Make it structural:

- **Freeze the predictions** (committed file). The Debrief quotes them verbatim and never restates them.
- **A fresh context grades.** It gets the frozen card and artifact paths, not the build transcript, and fills the Consistent? column. The builder writes only Mechanism, with its tier. This is the one agent that clearly earns its place: `mechanism-auditor`, generalised.
- **Every prediction needs a falsifier and a "should not change" half.**
- **Track the hit rate across tasks.** Near 100 % consistent means the predictions are too soft.
- **The person's prediction is the ungameable one.**
- **Budget the Debrief to be no longer than a plain answer.** Skill arms wrote 22–54 % more words and made more false claims (`docs/evals/2026-11-11-v3-hook/README.md:101-108`). For a human reader that cost is worse than for a grader.

## 6. Delete, merge, protect

| Action | What |
|---|---|
| **Delete** | `references/workflows.md`, `tests/workflows/run.mjs`, the workflows diagrams, and cartographer §E2 (`cartographer.md:373-456`). It is execution orchestration, off-mission, and by its own text "not yet run in a live Workflow runtime". |
| **Delete** | Cartographer as a mode: clarity scores and the ambiguity figure (`:47-62`, `:201-233`), regret arithmetic on invented probabilities, the six-condition gate, depth flags, schema migration (`:479-493`), `ledger-keeper`, `/cartographer`. |
| **Delete** | In `finding-unknowns/SKILL.md`: Model routing (`:389-409`), the sibling-tooling table and all `oh-my-claudecode:*` references (`:569-590`), the Defaults table, legacy text, and Technique 7. |
| **Delete** | Announcements made to the person: "Routing:", "Rigor level:", "Packet size:", "Depth:". These are protocol narration. Quadrants become internal vocabulary. |
| **Delete** | `prototype-smith`; the full nine-section packet and stakes triage (`keep-the-reasoning/SKILL.md:89-99`, `:165-193`). |
| **Merge** | Techniques 1–5 become Brief instruments. Technique 6 becomes the delta log. The compact packet (`keep-the-reasoning/SKILL.md:143-155`) becomes the Debrief's evidence block. One core skill of at most 1,500 words, with references loaded per phase. |
| **Shrink** | README from 6,900 words to about 1,500; seven diagrams per language to one; the glossary shrinks with the vocabulary. Do this before translating. |
| **Protect** | Almost all of `theory-vs-result`'s rules (move its tables and examples to a reference). The irreversibility floor and build rule (`cartographer.md:118-127`, `:345-351`). The "does NOT prove" column (`:318-343`). "Never ask what the territory can answer". `blindspot-scout`. All of `docs/evals/` and the field note, which are the project's most credible assets. |

## 7. Triggering and tokens

- **Commands are the primary entry:** `/brief`, `/status`, `/debrief`. The person opting in is part of the pedagogy.
- **Phase transitions follow file state, not model judgement:** an open card exists, so resume from it.
- **A state-printing SessionStart hook is worth testing.** It prints the card header only when an open card exists. This differs from v3's rejected reminder hook, but it is untested.
- **I disagree with §4.6's generic descriptions** ("plan / start / review"). v3's 15/15 came from task-specific descriptions on three-line skills, so it is not evidence for generic verbs. Generic verbs will fire on trivial tasks. v3 itself says raising invocation would not raise scores (`v3-hook/README.md:151-152`). Use phrases people actually say: "brief me", "catch me up", "did it match what we expected".
- **Token rule:** the scarce resource is the reader's attention.
  - *Value:* the card, delta lines, raw evidence, and explanation at the point of error.
  - *Waste:* skill text loaded on trivial tasks, per-round score tables, rules stated three times (policy, steps, checklist), sibling tables, and any human-facing sentence that changes neither a decision nor the person's model.
  - Keep the C6 property (no overhead on a typo fix) as a pre-registered guard.

## 8. Smallest credible evaluation

**Stage 0: simulated user, mechanism only (about a day).**

- **Design:** six tasks written by someone other than the author, three runs each, three arms: plain, a 60-word description of the loop in `CLAUDE.md`, and full 5.0.
- **The scripted user holds:** two unstated requirements, one confidently stated wrong belief, limited patience, one premise that dies mid-build, one irreversible step, and one prediction that the territory will falsify.
- **Mechanical measures:**
  - misconception named before any edit;
  - requirements elicited;
  - questions the repo could have answered;
  - interruptions outside the legitimate ones;
  - failed prediction marked inconsistent, with the frozen card unedited (hash check);
  - debrief length and false claims.
- **Kill rule:** if full 5.0 does not beat the 60-word arm, the plugin text is not the active ingredient. Ship the 60 words.
- **Limit:** this says nothing about comprehension.

**Stage 1: humans, the actual claim.**

- **Who:** 8–12 classmates, not the author.
- **Design:** within-subject crossover, counterbalanced, plain Claude Code against the loop. Two matched tasks of about 45 minutes on an unfamiliar repo: one engineering (a planted wrong premise, and tests that prove nothing at handoff) and one small noisy experiment where the intuitive hypothesis is wrong.
- **Pre-registered primaries:**
  - the accept/reject decision with its reason, graded blind;
  - a six-item test 48–72 hours later, written by a third party beforehand, without materials.
- **Secondaries:**
  - calibration (predicted minus actual score);
  - whether the planted belief persists;
  - person-time and annoyance;
  - voluntary `/brief` use in a free week afterwards.
- **Verdict rule:** show every pair. With eight people, only 7–8 pairs agreeing is distinguishable from chance. Pre-commit that anything less is "can't tell, run eight more".

**What would show the idea is wrong:**

- no delayed gain;
- a gain, but nobody uses it voluntarily;
- confidence rises without accuracy. This is the worst case: cognitive surrender with better paperwork.

The author's own diary on real tasks is worth keeping in alternating weeks, with a write-from-memory check before reading the card. Label it descriptive only.

## 9. Where I think the brief is mistaken

- **§4.4's "evidenced pieces":** only one has any evidence, and it is weak. The 4/5 against 1/12 result is a post-hoc pooled subgroup, which by your own rule is a `post-hoc fit`. The floor and the cards were never exercised: no arm did anything unsafe, and H3 sat at ceiling. Keep them on design grounds and say so. Test whether the one sentence "say what each check did not prove" reproduces the H4 effect on fresh fixtures; if it does, the evidenced piece is a sentence.
- **"The value must be on the human side":** this is a hope, not a finding. The measured costs transfer to the human side directly.
- **The goals conflict:** "keep telling them the principles" fights "don't interrupt" and "short". Front-loading resolves it in the pedagogically weakest place.
- **A simulated-user eval written by the skill's author** repeats the author-bias limitation already listed in v2 and v3.
- **The author as the pilot subject** convinces no sceptic.

I read the repo and changed nothing.