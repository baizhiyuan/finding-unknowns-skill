---
name: finding-unknowns
description: "Use at the start of an ambiguous or unfamiliar task to surface the user's unknowns (unknown unknowns, unknown knowns) before, during, and after implementation — via blind-spot pass, brainstorm/prototype, interview, references, implementation plan, implementation notes, pitch, and quiz. For high-stakes work, escalate to Cartographer mode — a rigorous, quadrant-coverage-gated, regret-weighted interview backed by a lifecycle-persistent unknowns ledger. Invoke manually when scope is unclear or the domain/codebase is new."
---

# Finding Unknowns

> The map is not the territory.

*Distilled from Thariq Shihipar's essay "A Field Guide to Fable: Finding Your Unknowns"*
*(@trq212 — https://x.com/trq212/status/2073100352921215386). Community skill; not affiliated*
*with or endorsed by Anthropic.*

The **map** is what you give Claude — the prompt, the skills, the context. The
**territory** is where the work actually happens — the codebase, the real world, its
constraints. The gap between them is **unknowns**. Every unknown forces Claude to guess
what you want; the more work being done, the more guesses. On capable models the
bottleneck is no longer the model's ability — it's your ability to clarify your unknowns.

This skill is a toolbox for discovering unknowns cheaply, **before** they get expensive
to fix. You won't use every technique every time; pick what fits.

## When to use

- Starting work in a **new domain** or an unfamiliar **part of the codebase**.
- **Design / taste** work where you'll "know it when you see it" but can't spec it upfront.
- **Long-horizon** tasks where a wrong early assumption compounds.
- Any moment a task comes back wrong and you suspect the spec, not the execution.

**Skip** for well-specified, trivial changes (typo, one-liner, obvious bug fix). Adding
process there is overkill.

## The four quadrants

Before acting, locate where your unknowns live:

| | You're aware of it | You're not aware of it |
|---|---|---|
| **You know it** | **Known Knowns** — what's in your prompt | **Unknown Knowns** — obvious once seen; know-it-when-you-see-it criteria |
| **You don't know it** | **Known Unknowns** — gaps you can name | **Unknown Unknowns** — blind spots you haven't considered |

The best agentic coders have *few* unknowns and *plan for the rest*. Reducing and planning
for unknowns is the core skill — and it improves by practicing it *with* Claude.

**Give Claude your starting point.** Tell it where you are in your thinking, your
experience with the problem and codebase, and let it work as a thought partner. That
context is what lets it target the right unknowns.

---

## Pre-implementation

### 1. Blind-spot pass — for unknown unknowns

When you don't even know what questions to ask, ask Claude to teach you your gaps. Use the
literal words "blindspot pass" and "unknown unknowns," and say who you are / what you know.

```
I'm adding a new auth provider but I know nothing about the auth modules in this
codebase. Do a blindspot pass to surface my relevant unknown unknowns and help me
prompt you better.
```
```
I don't know what color grading is but I need to grade this video. Teach me my unknown
unknowns about color grading so I can prompt better.
```

### 2. Brainstorm & prototype — for unknown knowns

When criteria are "I'll know it when I see it," get reactable options *before* wiring
anything up. Small spec changes cause large implementation changes, so surface these early.
Start most sessions with an explore/brainstorm phase to set scope with intent — it catches
high-value approaches you'd miss and prevents too-narrow or too-wide scope.

```
I want a dashboard for this data but I have no visual taste and don't know what's
possible. Make an HTML page with 4 wildly different design directions so I can react.
```
```
Before wiring anything up, make a single HTML file mocking the new editor toolbar with
fake data. I want to react to the layout before you touch the real app.
```
```
Rough problem: users churn after onboarding. Search the codebase and brainstorm 10
places we could intervene, cheapest to most ambitious. I'll tell you which resonate.
```

### 3. Interview me — after brainstorming, for residual ambiguity

Ask Claude to interview you, one question at a time, guided by context about the problem.

```
Interview me one question at a time about anything ambiguous. Prioritize questions
where my answer would change the architecture.
```

### 4. References — when you can't describe it, point at it

The best reference is **source code**. Point Claude at a library, module, or component
you like — even in another language — and tell it what to look for. (This is how Claude
Design works: point it at a module on a site you like and it reads the underlying markup
and structure, not just a screenshot.)

```
The Rust crate in vendor/rate-limiter implements the exact backoff behavior I want.
Read it and reimplement the same semantics in our TypeScript API client.
```

### 5. Implementation plan — lead with what's most likely to change

When you think you're ready, get a plan you can review — front-loaded with the decisions
you're most likely to tweak, so Claude surfaces what you actually need to alter.

```
Write an implementation plan in HTML, but lead with the decisions I'm most likely to
tweak: data model changes, new type interfaces, and anything user-facing. Bury the
mechanical refactoring at the bottom — I trust you on that part.
```

---

## During implementation

### 6. Implementation notes — capture deviations as they happen

No amount of planning eliminates unknown unknowns; the agent will hit edge cases mid-work.
Have it keep a running notes file so you learn from the attempt.

```
Keep an implementation-notes.md file. If you hit an edge case that forces you to deviate
from the plan, pick the conservative option, log it under 'Deviations', and keep going.
```

---

## Post-implementation

### 7. Pitch & explainer — for buy-in and approvals

Package the artifacts into one doc that accelerates understanding (reviewers start with
the same unknowns you did) and approvals (experts want to see you accounted for the
failure points they'd anticipate).

```
Package the prototype, the spec, and the implementation notes into a single doc I can
drop in Slack to get buy-in. Lead with the demo GIF.
```

### 8. Quiz — understand the change before you merge

After a long session Claude may have done more than you realize, and diffs only give a
light understanding because behavior depends on existing code paths. Make it quiz you —
only merge after you pass.

```
I want to fully understand this change. Give me an HTML report on the changes — context,
intuition, what was done, and why — with a quiz at the bottom I must pass.
```

---

## Guardrails

These keep each technique honest — most importantly, discovery must not silently slide into
implementation.

- **Discovery ends at understanding.** Blind-spot pass, interview, brainstorm, and references
  do *not* start building. Stop at the rewritten, better-informed request.
- **Prioritize architecture-changing unknowns** over trivia — surface what would change the
  approach, not every gap.
- **"No significant unknowns here" is a valid result.** If the area is simpler than feared,
  say so plainly instead of manufacturing questions.
- **One question at a time** in interviews — batching produces shallow answers.
- **Point at real code for references,** even in another language; a screenshot or paraphrase
  is a weaker spec than the source.
- **Deviations get logged, not buried.** Mid-build, record the deviation and the conservative
  choice; don't quietly change direction.
- **Don't merge until you pass the quiz.** Comprehension is the gate, not a green diff.

## Cartographer mode — the rigorous escalation

The eight techniques above are cheap, flexible probes. **Cartographer mode** is what you
escalate to when the work is high-stakes and you want *rigor* — a gated interview that
refuses to let you build until the territory is mapped. It is inspired by OMC's
`deep-interview`, but optimized along three axes that a clarity-scoring interview
structurally misses:

1. **It gates on coverage, not ambiguity.** A clarity score only reduces uncertainty on the
   dimensions the model already knows to ask about — it is blind to **Unknown Unknowns**.
   Cartographer gates on *"have we probed all four quadrants?"*, with blind-spot hunting as a
   first-class part of the gate, not an afterthought.
2. **It persists across the whole lifecycle.** A requirements interview ends at the spec.
   Cartographer maintains one **unknowns ledger** that the pre-interview seeds, the build
   phase appends to, and the final quiz closes out.
3. **It targets by regret, not by fixed weights.** Instead of weighting dimensions with
   constants, Cartographer scores each unknown by *cost-if-wrong* and spends questions only
   where a wrong guess is expensive. Cheap unknowns are logged with a conservative default
   and left open.

> Deep Interview measures *ambiguity reduction*. Cartographer measures *territory coverage,
> weighted by blast radius, across the full lifecycle.*

### The unknowns ledger

Maintain one artifact for the whole task — `unknowns-ledger.md` (or an HTML table). Every
unknown is a row; it is never silently dropped, only resolved or consciously deferred.

| id | quadrant | unknown | cost-if-wrong (1–5) | P(wrong) | **regret** | status | phase | resolution / conservative default |
|----|----------|---------|--------------------|----------|-----------|--------|-------|-----------------------------------|
| U1 | UU | (blind spot found by pass) | 5 | 0.7 | **3.5** | open | pre | — |
| U2 | KU | which auth path to extend | 4 | 0.5 | **2.0** | probing | pre | — |
| U3 | UK | "done" means p95 < 200ms | 3 | 0.2 | 0.6 | resolved | pre | confirmed with user |

- `quadrant` ∈ {KK, KU, UK, UU} — see the four-quadrant table above.
- **`regret = cost-if-wrong × P(wrong)`.** This is the *only* prioritization signal.
- `status` ∈ {open, probing, resolved, deferred}. `deferred` requires a conservative default.

### Regret-weighted targeting

Each round, target the **highest-regret open unknown** — not the weakest "dimension." Ask
one question aimed at it, then re-score its `P(wrong)`. A question that can't lower regret
for any open item is wasted; don't ask it.

**Leave-open rule:** if an unknown's `regret < 1.0`, do not spend a question on it. Log a
conservative default in the ledger and proceed. Rigor means spending attention where a wrong
guess is *expensive*, not interrogating everything.

### The quadrant-coverage gate

You are ready to build when **all four conditions hold** — this replaces "ambiguity ≤ threshold":

- [ ] **KK locked** — the knowns are written down (they drift if left implicit).
- [ ] **KU resolved or deferred** — every named gap is either answered or has a logged default.
- [ ] **UK extracted** — at least one brainstorm/prototype/reference ran to surface tacit,
      "know-it-when-I-see-it" criteria.
- [ ] **UU probed** — at least one explicit **blind-spot pass** ran, and anything it found is
      now a tracked ledger row (a UU you've named is no longer unknown-unknown).
- [ ] **No open unknown has `regret ≥ 1.0`.**

If UU was never probed, you are *not* ready — that is the coverage gate's whole point.

### Lifecycle loop

1. **Pre — seed & interview.** Populate KK. Run a blind-spot pass to seed UU. Brainstorm /
   reference to surface UK. Then interview in regret order, one question at a time, updating
   the ledger after each answer. Stop when the coverage gate passes.
2. **During — append.** Keep the ledger open. When the build surfaces a new unknown (an edge
   case, a wrong assumption), add a row with its quadrant + regret, pick the conservative
   option, keep going. (This is technique #6 feeding the ledger.)
3. **Post — close out.** Generate the quiz (technique #8) *from the ledger* — one question per
   resolved high-regret item and per named UU. Mark rows resolved. Merge only when no open
   row has `regret ≥ 1.0`.

### Kick-off prompt

```
Enter Cartographer mode for this task. Maintain an unknowns-ledger.md with columns:
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

## Why HTML artifacts

For nearly all of these, an **HTML artifact** is the best way to visualize and react to
the unknown: multiple design directions side by side, a plan that leads with the risky
decisions, a quiz you must pass. Default to HTML for anything visual or reviewable.
Fallback to markdown for a pure terminal/CLI flow where rendering HTML is friction.

## Worked example — launching Fable

The Fable launch video was edited entirely by Claude Code in a domain the author wasn't
expert in. It shows the techniques chained:

1. **Start from what you know.** Known: Claude can edit and transcribe video via code.
   Unknown: accuracy. → Asked Claude to **explain** how Whisper-style transcription works
   and whether ums/pauses could be cut accurately with ffmpeg (blind-spot pass).
2. **Prototype the risky idea.** Wanted a UI timed to spoken words but wasn't sure it was
   possible → had Claude build a **Remotion prototype** from a transcription to prove it.
3. **Surface a hidden unknown-known.** The video looked muted (color grading) but the
   author didn't know what "good" looked like → instead of picking blindly, asked Claude
   to **teach** color grading first (blind-spot pass), then decided.

Every explainer, brainstorm, interview, prototype, and reference is a cheap way to find
out what you didn't know — before it gets expensive to fix. Start your next project by
asking Claude to help you find your unknowns.

## Related skills — when to hand off

This skill is a lightweight **compass**, not an execution engine. It shines at the moment
you realize you're confused but don't yet know where. Once your unknown is located, hand off
to the specialist when depth is warranted:

- **Bulletproof, gated spec needed** → `oh-my-claudecode:deep-interview` (Socratic Q&A with
  mathematical ambiguity gating; refuses to proceed until clarity ≥ threshold, then hands off
  to execution). Prefer it over the lightweight "interview me" technique when stakes are high.
- **Divergent option generation** → `superpowers:brainstorming`.
- **A rigorous written plan** → `superpowers:writing-plans` or `oh-my-claudecode:plan`.
- **Spec is already concrete (file paths, acceptance criteria)** → skip discovery; go to
  `oh-my-claudecode:autopilot` / `ralph` / `team`.
- **A light reframe is enough** → stay here.

Rule of thumb: use finding-unknowns to discover *that* you're confused and *where*; use the
heavier skills to resolve it rigorously. Don't merge them — compose them.
