---
name: finding-unknowns
description: "Use at the start of an ambiguous or unfamiliar task to surface the user's unknowns (unknown unknowns, unknown knowns) before, during, and after implementation — via blind-spot pass, brainstorm/prototype, interview, references, implementation plan, implementation notes, pitch, and quiz. For high-stakes work, escalate to Cartographer mode — a rigorous, quadrant-coverage-gated, regret-weighted interview backed by a lifecycle-persistent unknowns ledger. Invoke manually when scope is unclear or the domain/codebase is new."
---

# Finding Unknowns

> The map is not the territory.

*Distilled from Thariq Shihipar's essay "A Field Guide to Fable: Finding Your Unknowns"*
*(@trq212 — https://x.com/trq212/status/2073100352921215386). Community skill; not affiliated*
*with or endorsed by Anthropic.*

The **map** is what the user gives you — the prompt, the skills, the context. The
**territory** is where the work actually happens — the codebase, the real world, its
constraints. The gap between them is **unknowns**. Every unknown forces you to guess what
the user wants; the more work being done, the more guesses. The bottleneck on long-horizon
work is no longer model capability — it is how well the user's unknowns get clarified.

This skill is a toolbox for discovering unknowns cheaply, **before** they get expensive to
fix. Do not run every technique every time; pick by quadrant and by stakes.

## When to use

- Starting work in a **new domain** or an unfamiliar **part of the codebase**.
- **Design / taste** work where the user will "know it when they see it" but can't spec it.
- **Long-horizon** tasks where a wrong early assumption compounds.
- A task came back wrong and the spec — not the execution — is the suspect.

**Skip** for well-specified, trivial changes (typo, one-liner, obvious bug fix). Adding
discovery process there is pure overhead.

## First move: locate the unknown

Before picking a technique, classify where the gap lives:

| | User is aware of it | User is not aware of it |
|---|---|---|
| **User knows it** | **Known Knowns** — in the prompt. *Write them down; they drift if implicit.* | **Unknown Knowns** — know-it-when-I-see-it criteria. *→ Brainstorm, References* |
| **User doesn't know it** | **Known Unknowns** — nameable gaps. *→ Interview, Plan* | **Unknown Unknowns** — blind spots. *→ Blind-spot pass, Quiz* |

Also ask for (or infer) the user's **starting point**: where they are in their thinking and
their experience with this problem and codebase. The same task needs different probing for
a domain expert than for a first-timer.

---

## Pre-implementation techniques

### 1. Blind-spot pass — for unknown unknowns

**When:** the user is entering territory they don't know well (new module, new domain), or
asks for a "blindspot pass" / their "unknown unknowns". Delegate to `blindspot-scout` when
a real codebase sweep is involved; run inline for small, conversational cases.

**Procedure:**
1. Establish the user's goal and experience level with this specific area — inferred
   conservatively if unstated.
2. Explore the territory yourself first: the module, its tests, its git history, its
   conventions, prior art in the repo; for external domains, what practitioners consider
   table stakes. Never ask the user for facts the territory can tell you.
3. Report in five sections: **Landmines** (typical newcomer mistakes + repo-specific
   potholes, cited), **Hidden context** (constraining decisions and invariants, with
   evidence), **What good looks like** (2–3 real examples to calibrate against),
   **Questions you should be asking** (3–5 expert questions with best-guess answers and
   confidence), and a **Rewritten request** that shows the user the difference between
   their map and the territory.

**Stop when:** the report is delivered. This technique ends at understanding — never roll
into implementation.

**Guardrails:** prioritize architecture-changing findings over trivia. "You have no
significant blindspots here" is a valid, valuable result — say it plainly rather than
manufacturing concerns.

```
I'm adding a new auth provider but I know nothing about the auth modules in this
codebase. Do a blindspot pass to surface my relevant unknown unknowns and help me
prompt you better.
```

### 2. Brainstorm & prototype — for unknown knowns

**When:** criteria are "I'll know it when I see it" — visual design, UX flows, report
layouts, API ergonomics. Also as the default opening of any session to set scope with
intent. Delegate to `prototype-smith` for multi-direction artifacts.

**Procedure:**
1. Gather the raw material (data samples, constraints, references) so options are concrete.
2. Produce N **genuinely different** directions (default 4) — different hierarchies,
   framings, or interaction models. Variations on one idea are a failure mode; explore the
   corners of the space.
3. Present as one self-contained HTML artifact, each direction labelled with a one-sentence
   thesis plus what it optimizes for and sacrifices.
4. Close with a reaction guide: 3–5 questions that help the user articulate what they like.

**Stop when:** the user has reacted and named what resonates. Convert their reactions into
explicit criteria before any real code is written.

**Guardrails:** fake every backend; wiring is waste at this stage. Never modify the real
application while prototyping. Small spec changes cause large implementation changes —
surfacing taste here is 10× cheaper than during the build.

```
Before wiring anything up, make a single HTML file mocking the new editor toolbar with
fake data — 4 wildly different directions. I want to react to layout before you touch
the real app.
```

### 3. Interview — for residual known unknowns

**When:** brainstorming/exploration is done but nameable gaps remain, or the user asks to
be interviewed. (For high-stakes work, use Cartographer mode below instead — it adds
regret-weighted targeting and a coverage gate.)

**Procedure:**
1. Read everything already established — request, spec, prototypes, relevant code. Never
   ask what is already answered or discoverable from the codebase; go look instead.
2. Privately list open ambiguities and sort by blast radius: **architecture-changers**
   first (data model, interfaces, overall approach), then **behavior definers** (edge
   cases, failure modes, defaults), **polish** last — usually propose-and-move-on rather
   than ask.
3. Ask exactly one question per turn, with the context that makes it matter and 2–3
   concrete options plus your recommendation. Accept "you decide" as an answer you then own.
4. Every few questions, checkpoint: restate all decisions so far in one tight list.

**Stop when:** remaining unknowns are cheaper to discover during implementation than to
ask about now — and say so explicitly. End with the final decision list.

**Guardrails:** one question means one — no bundles. If an answer contradicts an earlier
decision, flag the conflict immediately instead of silently taking the newest answer.

```
Interview me one question at a time about anything ambiguous. Prioritize questions
where my answer would change the architecture.
```

### 4. References — when the user can't describe it

**When:** the user lacks the vocabulary, or describing would take longer than pointing.
The richest reference is **source code** — a library, module, or component they like, even
in another language. `blindspot-scout` can do the reading when the reference is large.

**Procedure:**
1. Have the user point at the reference (path, repo, URL) and say what property they want
   from it — semantics, structure, feel.
2. Read the *underlying implementation*, not a surface description or screenshot.
3. Extract the transferable essence: the behavior, invariants, and structure to carry over
   — and state explicitly what will *not* transfer (language idioms, deps, scale
   assumptions).
4. Confirm the extraction with the user before reimplementing.

**Stop when:** the user confirms the extracted semantics match what they meant.

**Guardrails:** a paraphrase of a reference is a weaker spec than the reference. When the
reference conflicts with the host codebase's conventions, surface the conflict — don't
silently pick a side.

```
The Rust crate in vendor/rate-limiter implements the exact backoff behavior I want.
Read it and reimplement the same semantics in our TypeScript API client.
```

### 5. Implementation plan — surface the risky decisions early

**When:** discovery is done and the user thinks they're ready to build. The plan's job is
not to prove thoroughness — it is to put the expensive-to-change decisions in front of the
user while changing them is still free. `prototype-smith` can render it as HTML.

**Procedure:**
1. Open with three lines: what is being built, the chosen approach, the single riskiest
   assumption.
2. **Decisions likely to change** first: data model, new interfaces, API shapes, anything
   user-facing — each with the choice made, one alternative, and the cost of changing later.
3. **Known unknowns and their defaults**: where ambiguity remains, the default that will be
   taken and the signal that would trigger a pivot.
4. **Mechanical work** last, compressed — refactors, wiring, tests. Reviewing it wastes the
   user's attention.
5. End with the 2–4 specific decisions you want a yes/no or a pick on.

**Stop when:** the user has ruled on the flagged decisions.

**Guardrails:** keep it reviewable in minutes — skimmed plans hide bad decisions. Leave
room for improvisation; over-specified plans fail exactly where the territory disagrees
with the map. If a better approach appears mid-planning, present the pivot as its own
decision.

```
Write an implementation plan in HTML. Lead with the decisions I'm most likely to tweak:
data model changes, new type interfaces, anything user-facing. Bury the mechanical
refactoring at the bottom — I trust you on that part.
```

---

## During implementation

### 6. Implementation notes — log deviations, don't bury them

**When:** implementing against any agreed plan or spec, especially long autonomous
sessions. No amount of planning removes every unknown; some appear only once the code is
open.

**Procedure:**
1. At build start, create `implementation-notes.md` with three headings: **Deviations**,
   **Discovered edge cases**, **Questions for review**.
2. When reality forces an unplanned choice: pick the conservative option (conservative =
   most reversible, not simplest), log it under Deviations — what the plan said, what was
   done, why, what revisiting would take — and keep going. Do not block the user on
   reversible decisions.
3. Log edge cases even when handled cleanly — they are exactly what the next plan should
   account for.
4. Anything irreversible or scope-changing goes under Questions for review AND stops work
   at a safe checkpoint. Deviating conservatively is fine; deviating expensively needs a
   human.
5. At the end, append a five-line summary and reference the file in the handoff or PR.

**Stop when:** the build ends and the summary is written.

**Guardrails:** entries stay 2–3 lines; this is working memory, not documentation. An
unlogged deviation is worse than no notes at all — the file claims completeness.

---

## Post-implementation

### 7. Pitch & explainer — for buy-in

**When:** the work needs approval from people who start with the same unknowns the user
had.

**Procedure:** package the prototype, the spec/plan, and the implementation notes into one
document. Lead with the demo; follow with the decisions taken and the failure points an
expert reviewer would probe (pull these from the notes' Deviations section). One document,
droppable into chat.

**Stop when:** the document is delivered. **Guardrail:** reviewers' objections are
predictable from the unknowns you already logged — answer them preemptively rather than
defensively.

### 8. Quiz — comprehension is the merge gate

**When:** after a long session, before merge. A diff shows surface; behavior lives in how
the change interacts with existing code paths. Delegate to `quiz-master` — an examiner
that didn't write the change probes what its author glosses over.

**Procedure:**
1. Report first, four sections: **Context**, **What changed** (grouped by intent, not by
   file), **How it interacts** (existing paths that now behave differently — including in
   files the diff doesn't show), **Intuition** (the 2–3 mental-model updates to keep).
2. Then 5–8 questions weighted toward deviations, edge cases, and interaction effects —
   mixing recall with prediction ("if someone calls X with a stale token, what happens
   now?"). Never trivia about names.
3. Grade honestly. For each miss, give the right answer AND classify it: a gap in the
   user's model, or a sign the change is too clever — say which.

**Stop when:** the user passes, or after two failed rounds — at which point the
recommendation is to simplify or split the change, not to keep quizzing.

**Guardrails:** never mark the user correct out of politeness; a false pass defeats the
technique. An unexplained change found in the diff but absent from notes and ledger is an
**unlogged deviation** — flag it prominently.

---

## Companion agents — delegate when depth pays

Four specialist agents ship with this skill (under `agents/`). Delegate via the Agent tool
when they're installed; otherwise run the technique inline — everything above works
standalone.

| Agent | Backs | Contract: give it → it returns |
|-------|-------|-------------------------------|
| `blindspot-scout` | Blind-spot pass, References | goal + experience level → five-section recon report (read-only; cannot implement) |
| `prototype-smith` | Brainstorm, Plan | problem + data sources + N → one HTML artifact of N divergent directions + reaction guide (writes only throwaway files) |
| `ledger-keeper` | Cartographer mode | task/answers/discoveries → updated ledger, regret scores, next target, gate verdict (touches only the ledger) |
| `quiz-master` | Quiz, Pitch | diff + notes + ledger → HTML report + must-pass quiz (read-only; flags unlogged deviations) |

Delegation rules:
- Real-codebase blind-spot pass → `blindspot-scout`; relay its report, don't re-explore.
- Multi-direction artifacts → `prototype-smith` with data sources and N.
- Cartographer mode → the main conversation interviews; `ledger-keeper` seeds, re-scores,
  picks targets, and rules on the gate. **The gate verdict is the keeper's, not yours.**
- Post-implementation quiz → `quiz-master`. Self-quizzing is graded too kindly.
- Trivial cases stay inline; agent overhead needs a payoff.

## Cartographer mode — the rigorous escalation

For high-stakes work, escalate from ad-hoc techniques to a **gated** process that refuses
to start building until the territory is mapped. Inspired by OMC's deep-interview, but
optimized differently: it gates on **coverage** (were all four quadrants probed — including
a mandatory blind-spot pass for UU?), persists across the **whole lifecycle**, and targets
questions by **regret**, not fixed weights.

> Deep Interview measures *ambiguity reduction*. Cartographer measures *territory coverage,
> weighted by blast radius, across the full lifecycle.*

### The unknowns ledger

One artifact for the whole task — `unknowns-ledger.md` (owned by `ledger-keeper` when
available). Every unknown is a row; rows are never dropped, only resolved or deferred.

| id | quadrant | unknown | cost-if-wrong (1–5) | P(wrong) | **regret** | status | phase | resolution / conservative default |
|----|----------|---------|--------------------|----------|-----------|--------|-------|-----------------------------------|
| U1 | UU | (found by blind-spot pass) | 5 | 0.7 | **3.5** | open | pre | — |
| U2 | KU | which auth path to extend | 4 | 0.5 | **2.0** | probing | pre | — |
| U3 | UK | "done" = p95 < 200ms | 3 | 0.2 | 0.6 | resolved | pre | confirmed with user |

- **`regret = cost-if-wrong × P(wrong)`** — the only prioritization signal.
- `status` ∈ {open, probing, resolved, deferred}; `deferred` requires a logged conservative
  default. `phase` ∈ {pre, during, post} records when the unknown surfaced.

### Regret-weighted targeting

Each round, target the **highest-regret open row** with exactly one question; re-score its
`P(wrong)` after the answer. **Leave-open rule:** any row with `regret < 1.0` gets a
conservative default logged and is not worth a question. Rigor means spending attention
where a wrong guess is expensive — not interrogating everything.

### The quadrant-coverage gate

Building may start only when **all** hold (this replaces "ambiguity ≤ threshold"):

- [ ] **KK locked** — knowns are written down (implicit knowns drift).
- [ ] **KU resolved or deferred** — every named gap answered or defaulted.
- [ ] **UK extracted** — at least one brainstorm / prototype / reference ran.
- [ ] **UU probed** — at least one blind-spot pass ran; its findings are tracked rows.
- [ ] **No open row has `regret ≥ 1.0`.**

If UU was never probed, the gate FAILS — that is its entire point. Never pass the gate out
of politeness; when `ledger-keeper` is available, its verdict is final.

### Lifecycle loop

1. **Pre** — seed the ledger (blind-spot pass → UU; brainstorm/references → UK; write down
   KK/KU), then interview in regret order until the gate passes.
2. **During** — keep the ledger open; every mid-build discovery becomes a row with quadrant
   + regret; conservative option chosen and logged (technique #6 feeds the ledger).
3. **Post** — build the quiz *from the ledger*: one question per resolved high-regret row
   and per named UU. Merge only when no open row has `regret ≥ 1.0`.

### Kick-off prompt

```
Enter Cartographer mode for this task. Maintain unknowns-ledger.md with columns:
id, quadrant (KK/KU/UK/UU), unknown, cost-if-wrong (1-5), P(wrong), regret (=cost×P),
status, phase, resolution.

1. Seed it: run a blind-spot pass to populate Unknown Unknowns, then list the Known
   Unknowns and any tacit criteria.
2. Interview me ONE question at a time, always targeting the highest-regret open row.
   Re-score P(wrong) after each answer. Skip anything with regret < 1.0 — log a
   conservative default instead.
3. Show me the ledger + the four-quadrant coverage checklist each round. Don't let me
   start building until all four quadrants are probed (especially UU) and no open row
   has regret >= 1.0.
Keep the ledger open through implementation and build the final quiz from it.
```

## Global guardrails

- **Discovery ends at understanding.** No discovery technique slides into implementation.
- **Architecture-changing unknowns outrank trivia** — always.
- **"No significant unknowns here" is a valid result.** Don't manufacture questions.
- **One question at a time** in any interview.
- **Deviations get logged, not buried.**
- **Comprehension is the merge gate, not a green diff.**
- **HTML artifacts by default** for anything visual or reviewable (multiple directions,
  plans leading with risk, quiz reports); markdown fallback for pure-terminal flows.

## Related skills — when to hand off

This skill is a compass, not an execution engine. Once the unknown is located, hand off
when depth is warranted:

- **Math-gated, resumable spec with execution handoff** → `oh-my-claudecode:deep-interview`.
  Prefer it over Cartographer when you want ambiguity thresholds, topology/ontology
  tracking, and a `Skill()` bridge into autopilot/ralph/team.
- **Divergent option generation** → `superpowers:brainstorming`.
- **A rigorous written plan** → `superpowers:writing-plans` or `oh-my-claudecode:plan`.
- **Spec already concrete** (file paths, acceptance criteria) → skip discovery; go to
  `oh-my-claudecode:autopilot` / `ralph` / `team`.
- **A light reframe is enough** → stay here.

Use finding-unknowns to discover *that* you're confused and *where*; use the heavier
skills to resolve it rigorously. Don't merge them — compose them.
