# Workflow Orchestration Templates

When the host environment exposes the **Workflow tool** (Claude Code's dynamic-workflow
scripting: `agent()` / `pipeline()` / `parallel()` with deterministic control flow), the
high-fan-out parts of this skill should run as Workflow scripts instead of ad-hoc Agent
calls from the main context. The gains are the same ones Deep Research gets from it:

- **Determinism** — the fan-out/verify/merge structure is encoded in a script, not left
  to in-context improvisation, so no lens or verification step is silently dropped.
- **No barrier waste** — `pipeline()` lets each finding be verified the moment its scout
  finishes, instead of waiting for the slowest lens.
- **Structured output** — each agent returns schema-validated JSON (ledger rows,
  verdicts), so the ledger is seeded mechanically rather than by prose-parsing.

**Availability gate**: only orchestrate via Workflow when the user has opted into
multi-agent orchestration (the Workflow tool's own opt-in rules apply). Otherwise fall
back to the plain Agent tool (parallel scouts in one message) or fully inline execution —
every template below degrades gracefully; the *logic* is normative, the *mechanism* is not.

**Cost anchor**: a 3-lens sweep with per-finding verification typically costs 150–400k
subagent tokens. Worth it when a wrong assumption forces a redesign (Cartographer-grade
stakes); not worth it for a one-file question.

---

## Template 1 — Multi-lens blind-spot sweep (backs Technique 1 / C0 seeding)

Parallel scouts with distinct lenses → dedup across lenses → adversarial verify each
fresh finding → return structured ledger rows. Verification of lens A's findings starts
while lens B is still scouting (pipeline, no barrier).

```javascript
export const meta = {
  name: 'fu-multi-lens-sweep',
  description: 'Multi-lens blindspot sweep with per-finding adversarial verification',
  phases: [{ title: 'Scout' }, { title: 'Verify' }],
}
// args: { task, experienceLevel, lenses?: string[] }
const LENSES = args.lenses ?? ['domain-risk', 'engineering', 'statistics']
const FINDINGS = { type: 'object', required: ['findings'], properties: { findings: {
  type: 'array', items: { type: 'object',
    required: ['unknown', 'quadrant', 'costIfWrong', 'pWrong', 'route', 'evidence'],
    properties: {
      unknown: { type: 'string' }, quadrant: { enum: ['KK','KU','UK','UU'] },
      costIfWrong: { type: 'integer', minimum: 1, maximum: 5 },
      pWrong: { type: 'number' }, route: { enum: ['interview','territory','experiment','audit'] },
      evidence: { type: 'string' } } } } } }
const VERDICT = { type: 'object', required: ['real', 'reason'],
  properties: { real: { type: 'boolean' }, reason: { type: 'string' } } }

const results = await pipeline(
  LENSES,
  lens => agent(
    `You are a blindspot scout with ONE lens: ${lens}. Task: ${args.task}. ` +
    `User experience level: ${args.experienceLevel}. Explore the territory (code, docs, ` +
    `domain norms) READ-ONLY and return candidate unknowns as ledger rows. Cite evidence ` +
    `for every non-obvious claim. Architecture-changing findings first.`,
    { label: `scout:${lens}`, phase: 'Scout', schema: FINDINGS,
      agentType: 'blindspot-scout' }),
  (r, lens) => parallel((r?.findings ?? []).map(f => () =>
    agent(
      `Adversarially verify this candidate unknown: "${f.unknown}" (evidence: ` +
      `${f.evidence}). Try to REFUTE it: is it already answered by the territory, ` +
      `trivially discoverable, or a generic concern with no repo-specific teeth? ` +
      `Default real=false if uncertain.`,
      { label: `verify:${f.unknown.slice(0, 40)}`, phase: 'Verify', schema: VERDICT })
      .then(v => ({ ...f, lens, verdict: v }))))
)
const rows = results.filter(Boolean).flat().filter(Boolean).filter(f => f.verdict?.real)
// dedup by normalized unknown text; duplicates across lenses = confirmation, keep max cost
const byKey = {}
for (const r of rows) {
  const k = r.unknown.toLowerCase().replace(/\W+/g, ' ').trim()
  if (!byKey[k] || r.costIfWrong > byKey[k].costIfWrong) byKey[k] = { ...r, confirmedBy: [] }
  byKey[k].confirmedBy.push(r.lens)
}
return { rows: Object.values(byKey) }
```

After the run: hand `rows` to `ledger-keeper` (or seed the ledger inline). Rows confirmed
by ≥2 lenses get a note in the evidence column.

## Template 2 — Adversarial verification panel (backs C1 step 3.5, cost ≥ 4 rows)

Three independent refuters, each with a distinct failure lens; a resolution survives only
if ≥2 fail to refute. Diversity of lenses catches failure modes redundancy cannot.

```javascript
export const meta = {
  name: 'fu-verify-panel',
  description: 'Perspective-diverse refutation panel for a high-cost ledger resolution',
  phases: [{ title: 'Refute' }],
}
// args: { claim, evidence, lenses?: string[] }
const LENSES = args.lenses ?? ['alternative-explanation', 'evidence-independence', 'reproduction']
const VERDICT = { type: 'object', required: ['refuted', 'reason'],
  properties: { refuted: { type: 'boolean' }, reason: { type: 'string' },
    discriminatingCheck: { type: 'string' } } }
const votes = await parallel(LENSES.map(lens => () =>
  agent(
    `Lens: ${lens}. Try to REFUTE this resolution: "${args.claim}". ` +
    `Evidence offered: ${args.evidence}. Construct the strongest alternative explanation ` +
    `consistent with the SAME evidence. If one exists, refuted=true and name the single ` +
    `discriminating check that would separate the explanations. Default refuted=true if uncertain.`,
    { label: `refute:${lens}`, phase: 'Refute', schema: VERDICT })))
const v = votes.filter(Boolean)
const survives = v.filter(x => !x.refuted).length >= 2
return { survives,
  status: survives ? 'resolved' : 'resolved-provisional',
  discriminatingChecks: v.filter(x => x.refuted).map(x => x.discriminatingCheck).filter(Boolean),
  votes: v }
```

If `survives === false`, the row stays `resolved-provisional` and the returned
`discriminatingChecks` go into the ledger verbatim.

## Template 3 — UU loop-until-dry (deep probe for the shallowest quadrant)

For the completeness-critic finding "UU was probed most shallowly": keep spawning
differently-angled scouts until 2 consecutive rounds surface nothing new. Simple
one-shot sweeps miss the tail; this bounds the search by information, not by count.

```javascript
export const meta = {
  name: 'fu-uu-until-dry',
  description: 'Loop UU discovery until two consecutive dry rounds',
  phases: [{ title: 'Probe' }],
}
// args: { task, knownUnknowns: string[], angles?: string[][] }
const ROUNDS = args.angles ?? [
  ['failure-modes', 'operational'], ['adversarial-user', 'scale'], ['maintenance', 'compliance']]
const FINDINGS = { type: 'object', required: ['findings'], properties: {
  findings: { type: 'array', items: { type: 'string' } } } }
const seen = new Set(args.knownUnknowns.map(s => s.toLowerCase()))
const fresh = []
let dry = 0
for (let i = 0; i < ROUNDS.length && dry < 2; i++) {
  const found = (await parallel(ROUNDS[i].map(angle => () =>
    agent(`Angle: ${angle}. Task: ${args.task}. Already-tracked unknowns: ` +
      `${[...seen].join('; ')}. Find unknowns NOT in that list. Return [] if none — ` +
      `an empty result is a valid result.`,
      { label: `probe:${angle}`, phase: 'Probe', schema: FINDINGS }))))
    .filter(Boolean).flatMap(r => r.findings)
  const news = found.filter(f => !seen.has(f.toLowerCase()))
  if (!news.length) { dry++; continue }
  dry = 0
  news.forEach(f => { seen.add(f.toLowerCase()); fresh.push(f) })
  log(`round ${i + 1}: ${news.length} new unknowns`)
}
return { fresh, dryStop: dry >= 2 }
```

## Template 4 — Cross-validated execution (backs Phase E option 2)

Approved tasks pipeline through an implementer and an INDEPENDENT refute-framed verifier;
a task closes only on its verifier's pass. Failed tasks return with the verifier's
objections for exactly one repair round. Only run this after the user has explicitly
approved execution — the template implements, unlike everything else in this skill.

```javascript
export const meta = {
  name: 'fu-execute-verified',
  description: 'Implement approved tasks with independent per-task verification',
  phases: [{ title: 'Implement' }, { title: 'Verify' }, { title: 'Repair' }],
}
// args: { specPath, tasks: [{ id, description, acceptance }] }
const VERDICT = { type: 'object', required: ['pass', 'objections'],
  properties: { pass: { type: 'boolean' }, objections: { type: 'array', items: { type: 'string' } } } }
const implementPrompt = t =>
  `Implement task ${t.id} from the spec at ${args.specPath}: ${t.description}. ` +
  `Acceptance criteria: ${t.acceptance}. Honor the spec's constraints, non-goals, and the ` +
  `ledger's deferred defaults. Return a summary of files changed and how each criterion is met.`
const verifyPrompt = (t, summary) =>
  `You did NOT write this change. Task ${t.id}: ${t.description}. Acceptance: ${t.acceptance}. ` +
  `Implementer's summary: ${summary}. Read the actual changes and try to FAIL them: unmet ` +
  `criteria, spec violations, silent scope creep, broken neighbors. Default pass=false if uncertain.`
const results = await pipeline(
  args.tasks,
  t => agent(implementPrompt(t), { label: `impl:${t.id}`, phase: 'Implement' }),
  async (summary, t) => {
    let v = await agent(verifyPrompt(t, summary), { label: `verify:${t.id}`, phase: 'Verify', schema: VERDICT })
    if (v && !v.pass) {
      const fix = await agent(implementPrompt(t) +
        ` A verifier rejected the first attempt with: ${v.objections.join('; ')}. Fix exactly these.`,
        { label: `repair:${t.id}`, phase: 'Repair' })
      v = await agent(verifyPrompt(t, fix), { label: `reverify:${t.id}`, phase: 'Verify', schema: VERDICT })
    }
    return { id: t.id, pass: !!v?.pass, objections: v?.objections ?? ['verifier unavailable'] }
  })
return { results: results.filter(Boolean),
  open: results.filter(Boolean).filter(r => !r.pass) }
```

Tasks still failing after the repair round go back to the user with the objections — they
are open ledger rows, not things to force through. The author-never-self-approves
invariant is structural here: implementer and verifier are always distinct agent contexts.

## Note — quadrant scoring is NOT a fan-out

SCORE-QUADRANTS is a single strongest-tier agent call (ledger-keeper) per round: one
context reading the whole ledger scores more consistently than a panel, and it is cheap.
Reserve fan-out for discovery (Templates 1, 3) and verification (Template 2), where
perspective diversity pays.

---

## Fallback ladder

1. **Workflow tool available + user opted in** → use the templates above.
2. **No Workflow, Agent tool available** → run the same structure manually: launch the
   lens scouts as parallel Agent calls in a single message; verify findings with a second
   parallel batch; you (the orchestrator) do the dedup and merge.
3. **No subagents at all** → run each lens sequentially inline, keeping the same
   report/verify discipline. Slower, same logic.

The invariants that must survive any fallback: every lens named explicitly, every cost ≥ 4
finding adversarially checked before it becomes a resolved row, dedup against *all seen*
(not just accepted) findings, and empty results reported as results.
