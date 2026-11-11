<!-- Advisor review by GPT 6 Astra (gpt-6-astra), 2026-11-11, read-only against tag v4.3.2 plus the then-unreleased eval docs. File paths and line numbers refer to that state. Reproduced verbatim except that local absolute links were turned into plain paths. -->

**The proposed loop is a good interface, but an incomplete architecture.** I would organise 5.0 around a persistent record of **what we believe, what we are authorised to do, and what evidence changed either**. Brief → Quiet build → Debrief then becomes the way people interact with that record.

For long tasks, use one task-level Brief and several bounded cycles of work and reconciliation. Waiting until the final Debrief would reproduce the drift you want to prevent. Conversely, requiring a complete understanding before starting would make research unnecessarily difficult: some understanding must emerge through experiments.

The following budgets are design proposals to test, not established optima.

**Continuity should be the central feature.** Cartographer’s “Resume” (`skills/finding-unknowns/references/cartographer.md:472`) currently restores the ledger and gate status. That restores procedure better than it restores the person’s understanding.

Use a task-specific directory under `.finding-unknowns/`, containing:

| Artifact | Purpose |
|---|---|
| `brief.md` | Original objective, constraints, authorisations, explanations, predictions and checks. Preserve revisions rather than overwriting commitments. |
| `now.md` | One screen: current milestone, completed/pending work, consequential deviations, unresolved decisions, and next action. |
| `changes.md` | Append-only consequential changes, each linked to evidence and affected beliefs or decisions. |
| `predictions/` and result artifacts | Detailed research records, loaded only when relevant. |

Keep `now.md` around 250–400 words. Its central sentence should be: “We expected X; observed Y; therefore Z changes.” Include a timestamp, code/data version, pending experiment identifiers, and the last checkpoint shown to the user.

Distinguish **user-stated belief**, **agent inference about that belief**, and **proposed correction**. An explanation delivered is not evidence that the person understood or accepted it. Record “shown, not confirmed” where appropriate.

At session start, reconcile this record with actual files and completed runs, then offer a five-line orientation: objective, progress, surprise, unresolved issue, next step. Avoid restarting the interview. At milestones, refresh the current view from source evidence rather than repeatedly summarising old summaries.

Quiet execution can maintain an accurate record; it cannot maintain the understanding of somebody who never reads it. Make that limitation explicit in the product promise.

**Learning should involve small acts of reasoning.** The current Technique 8 (`skills/finding-unknowns/SKILL.md:286`) prescribes 5–8 questions and a pass condition. I would remove the default examination gate. It risks turning ownership into compliance with the model’s answer key.

Explain only principles that change a decision or predict an observable outcome. A useful unit is:

> “Caching helps repeated requests. Your keys include session IDs, so repetition across sessions may not produce hits. We’ll measure hit rate before predicting the latency gain.”

Then ask one useful question when learning is desired: “Which workload should benefit least?” This tests application rather than vocabulary.

For the Brief, default to one batch of up to three independent questions and roughly 300–500 words. Permit another round only when an unresolved answer changes the approach, acceptance criteria, or authority. Stop when remaining uncertainty can be investigated cheaply.

Adapt along two separate dimensions:

- **Expertise:** novices receive a concrete example and one causal link; experts receive assumptions, boundary conditions and competing explanations.
- **Purpose:** shipping emphasises the decision and its consequences; learning adds a prediction or teach-back and a later transfer question.

Yes, sometimes let the person predict **before** the agent explains, especially when testing a suspected misconception. Make it skippable: “What do you expect, and why? ‘Unsure’ is useful.” Do not require guesses on unfamiliar quantities or repeatedly ask for already-recorded beliefs.

**Interruptions need a broader rule than irreversibility and scope changes.** Also interrupt when a central assumption fails and continuing would materially waste work, exceed an agreed resource budget, or invalidate the authorised approach.

Define the boundary in the Brief through concrete examples and thresholds. Within it, the agent chooses reversible defaults and logs them. Outside it, pause only dependent work, explain the consequence, and continue independent authorised work.

Separate **notifications** from **questions requiring an answer**. A milestone update can say “The speed prediction failed; correctness still holds; I’m investigating the cache keys” without demanding a response. Bundle ordinary deviations into checkpoints. Keep urgent decision-critical information visible; a quiet-build promise must not bury it.

This extends the sound foundation in Technique 6, “Implementation notes” (`skills/finding-unknowns/SKILL.md:260`).

**Research needs nested prediction–result cycles.** A research Brief should distinguish the scientific hypothesis, the proposed mechanism, and the practical decision rule. A promising hypothesis need not satisfy today’s adoption threshold; a threshold-crossing result need not establish its mechanism.

Preserve theory-vs-result Steps 1–3 (`skills/theory-vs-result/SKILL.md:130`), particularly prospective predictions, fair comparisons, explicit uncertainty and post-hoc labels. Give each experiment a stable identifier linking:

- Prediction version and whether it preceded result access.
- Code, data, configuration, baseline and intended analysis.
- Run status, failures, exclusions and consumed evaluation data.
- Results, uncertainty, interpretation and next discriminating test.

Debrief when a planned batch or decision-relevant result arrives, not after every seed. Pending results remain pending across sessions. Report independent replication batches separately and retain failed runs; do not let the latest successful experiment replace the history.

Predefine when results will be inspected and what permits stopping or extending runs. Repeated peeking, dependent backtest windows and adaptive tuning require appropriate analysis; a generic “interval” is insufficient. Seed spread is not automatically a confidence interval, and repeated windows are not independent samples.

Two existing requirements need softening:

1. **“Every mismatch names the broken link” can force storytelling.** Sometimes the evidence cannot distinguish a pipeline problem from a false hypothesis. Report candidate links and the separating experiment.
2. **Magnitude is not always honestly predictable.** Allow “magnitude unknown; decision-relevant effect ≥ X.” A directional prediction can be falsifiable; mandatory numerical guesses create false precision.

Preserve Step 4’s rule-verdict/direction-verdict distinction (`skills/theory-vs-result/SKILL.md:278`). Allow exploration without forcing an immediate confirmatory follow-up when no decision warrants one.

**An honest Debrief requires provenance, not just a self-critical prompt.** Quote the original prediction by identifier, including misses and unresolved predictions. Keep amendments dated and prospective. A mutable timestamp written by the same agent is weak evidence of timing; important research commitments should have independently recorded version history.

Use mechanism-auditor’s investigation protocol (`agents/mechanism-auditor.md:63`) to rederive numbers and challenge explanations. Ideally the reviewer assesses predictions and raw evidence before reading the author’s causal narrative. Fresh context reduces one source of bias; it does not create independent empirical evidence.

Retain unresolved reviewer disagreements. Replace “your model was corrected” with “the evidence challenges X; the proposed replacement is Y.” The agent’s model must be equally open to correction.

**I would make these repository changes.**

| Current location | Recommendation |
|---|---|
| `finding-unknowns/SKILL.md`, Phase 0 and Cartographer summary | Remove mandatory quadrant classification and routing announcements. Keep quadrants as an optional discovery aid. |
| Same file, Techniques 3, 5, 6 and 7 | Merge into the Brief, ongoing record and Debrief. Preserve territory-first investigation and verification limits. |
| Same file, Techniques 1, 2 and 4 | Keep as optional discovery instruments. Interviews alone cannot elicit tacit preferences. |
| `references/cartographer.md`, clarity scoring, C1 round displays and C2 gate | Remove numerical scoring and the universal six-condition gate. Retain concrete unknowns, dependencies, conservative defaults and authorisation boundaries. |
| `references/workflows.md`; `tests/workflows/run.mjs` | Move experimental orchestration into a separately maintained package or archive. Its stub-tested executor is a different product responsibility. |
| `keep-the-reasoning/SKILL.md`, Steps 0–3 | Merge duplicated setup into the shared record. Preserve “what checks did NOT prove”; remove compulsory nine-section packets and ritual “unchecked” filler. |
| `theory-vs-result/SKILL.md` | Keep as an independently usable research capability, progressively loaded by the loop. |
| `agents/ledger-keeper.md`, `agents/prototype-smith.md` | Remove specialised agents from the default package; retain useful techniques inline. |
| `agents/quiz-master.md`, `commands/change-quiz.md` | Make learning checks optional; remove must-pass framing. |
| `agents/mechanism-auditor.md`, `agents/blindspot-scout.md` | Retain optional read-only reviewer and reconnaissance roles. |

Also reconsider keep-the-reasoning’s mandatory evidence-first order (`skills/keep-the-reasoning/SKILL.md:139`). A short, qualified decision statement with adjacent evidence and limitations may be easier to use. Raw output first is an untested presentation hypothesis.

Protect attribution, bilingual parity, inline operation, evidence links and the irreversibility floor. Honour existing explicit authorisation rather than repeatedly requesting it. Update `ARCHITECTURE`, `GLOSSARY`, tutorials and landing pages around the final model, with independent review of the migration.

**Packaging should expose phases without multiplying protocols.** Keep one canonical loop skill, thin `/brief`, `/resume` and `/debrief` dispatchers, and the separately callable research skill. Avoid same-named command/skill collisions. Descriptions should mirror explicit requests, but activation must not depend on descriptions alone: once started, the persisted task phase determines continuation.

Do not ship a general reminder hook. A narrowly scoped hook that locates an already-active task record could be tested later. Plain Markdown and explicit invocation must remain sufficient across hosts.

Spend tokens on causal explanations, alternatives, consequential surprises, evidence limitations and orientation. Cut scoring displays, duplicate packets, blanket multi-agent reviews, repeated source summaries and protocol announcements. Model-only instructions are not inherently waste: a short rule preventing retrospective prediction edits serves the person. Measure reading time and decision quality alongside tokens.

**The smallest credible human evaluation needs people beyond the author.** Simulated users can regression-test elicitation and interruption rules. They cannot establish learning: their hidden requirements and scripted misconceptions make them unusually cooperative and measurable.

Start with 16 participants, spanning relevant expertise, each completing two matched task variants in randomised, counterbalanced order. Include engineering and research task families, with work resumed the following day. Compare the loop against an active control offering a concise plan, progress notes and a test summary, using the same model and comparable attention budget.

Have someone outside the skill’s authorship construct held-out tasks and scoring criteria. Include an initially plausible wrong expectation, a consequential deviation and evidence insufficient for a confident conclusion.

Pre-register:

- Primary outcome: correct decisions on new scenarios, supported by valid reasons.
- Delayed transfer after 48–72 hours without the assistant.
- Ability to resume and decide using the saved artifact.
- Confidence calibration, rework, missed necessary interruptions and active user time.

Grade answers blind where possible; do not score repetition of the agent’s explanation. Report participant-level uncertainty and order effects: crossover learning can contaminate the control.

Define a worthwhile improvement and acceptable attention cost before collecting data. This is a feasibility pilot, not broad proof. A sceptic should demand transfer and better decisions, followed by independent replication. Satisfaction or immediate recall alone is insufficient. Precise evidence of negligible benefit, worse confident errors, or gains outweighed by attention cost would argue against the design; wide intervals mean uncertainty.

Finally, your evidence interpretation is slightly too strong. v3’s Results and Limitations (`docs/evals/2026-11-11-v3-hook/README.md:54`) support **no demonstrated general benefit on these tasks**, not universal ineffectiveness. Reference skills changed scope, names and bodies alongside descriptions, so wording was not isolated. The 4/5 versus 1/12 finding is exploratory and conditions on invocation. Preserve that promising step, but test it directly. The human-facing direction fits the author’s goal; its value remains a hypothesis.

No files were modified.