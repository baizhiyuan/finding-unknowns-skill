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
  const k = r.unknown.normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{M}\p{N}]+/gu, ' ').trim()
  if (!byKey[k] || r.costIfWrong > byKey[k].costIfWrong)
    byKey[k] = { ...r, confirmedBy: byKey[k]?.confirmedBy ?? [] }   // keep earlier lenses
  byKey[k].confirmedBy.push(r.lens)
}
return { rows: Object.values(byKey) }
```

After the run: hand `rows` to `ledger-keeper` (or seed the ledger inline). Rows confirmed
by ≥2 lenses get a note in the evidence column.

## Template 2 — Adversarial verification panel (backs C1 step 3.5, cost ≥ 4 rows)

Three independent refuters, each with a distinct failure lens. A resolution survives only
if every refuter returns and none produces a plausible refutation; one surviving
counterexample keeps the row `resolved-provisional` (C1 step 3.5: evidence does not lose a
majority vote). A refuter that returns nothing also blocks survival. Diversity of lenses
catches failure modes redundancy cannot.

```javascript
export const meta = {
  name: 'fu-verify-panel',
  description: 'Perspective-diverse refutation panel for a high-cost ledger resolution',
  phases: [{ title: 'Refute' }],
}
// args: { claim, evidence, lenses?: string[] }
const DEFAULT_LENSES = ['alternative-explanation', 'evidence-independence', 'reproduction']
const LENSES = args.lenses ?? DEFAULT_LENSES
if (!Array.isArray(LENSES) || new Set(LENSES).size < 3)
  return { status: 'invalid-args', problems: ['the panel needs at least three distinct lenses'] }
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
// Fail closed: every lens must report, and none may refute.
const survives = v.length === LENSES.length && v.every(x => !x.refuted)
return { survives,
  status: survives ? 'panel-survived' : 'resolved-provisional',   // not 'resolved': see below
  discriminatingChecks: v.filter(x => x.refuted).map(x => x.discriminatingCheck).filter(Boolean),
  votes: v }
```

If `survives === false`, the row stays `resolved-provisional` and the returned
`discriminatingChecks` go into the ledger verbatim. `panel-survived` is not a resolution
by itself: the caller still applies the cross-reference rule from C1 step 3.5 (a second,
independent source) before marking the row `resolved`.

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

Implements the Phase E execution rules in `cartographer.md`. Only run it after the user
has approved **the task graph itself** (tasks, edges with what crosses, lanes, touched
paths, checks) — the template implements, unlike everything else in this skill.

What is enforced in code vs by prompt — stated honestly:

| Guarantee | Enforcement |
|-----------|-------------|
| Invalid args (unknown lane, empty checks, duplicate ids, missing deps, cycles, touches overlapping check files) stop the run before any agent call | code |
| Unnamed edges are never dropped silently: dropped only from `reversible` upstreams and only after `confirmDroppedEdges`; kept (fail closed) otherwise | code |
| Only real dependencies wait (per-task scheduling, no wave barrier) | code |
| Tasks whose touched paths overlap never run concurrently (paths normalized; globs rejected) | code |
| Edits outside every task's declared paths stop the run (`scope-violation`); paths already dirty before the run (ledger, spec, notes, WIP) are excluded from the path check but content-hashed, so a further edit to them is still caught | code compares the runner's report and hashes against the pre-run baseline |
| (Consequence) Check artifacts such as coverage reports must be gitignored, or they count as out-of-scope writes | by design — fails closed |
| Every task's check files are hashed on every check run and again in a final sweep after all tasks; any change halts the run | code compares the runner's hashes against the baseline |
| Do not edit files that were already dirty before the run (the ledger, notes, WIP) while it runs: any change to them halts every task | by design — fails closed |
| Before resuming after a `scope-violation`, revert or commit the stray files; otherwise they count as pre-dirty on the next run | by instruction |
| A concurrent task's edits are attributed to the right task, and a sibling's mid-edit state never disturbs this task's checks | prompted — keep checks narrow to the task's paths |
| Lanes decide closing; `irreversible` never closes in-run | code |
| Check results are matched to contract checks by exact string; missing ones fail | code |
| Check-file hashes come from a separate check-runner context and are compared by code against one baseline taken before any implementer runs; `wide`/`irreversible` tasks must declare check files; no task may touch any task's check files | code compares; the runner's report is prompted |
| Tampered check files stop the task immediately | code (given the runner's hashes) |
| Implementer does not execute irreversible actions; runner refuses irreversible checks | prompted |
| Verifier independence (different context from implementer) | structural |

```javascript
export const meta = {
  name: 'fu-execute-verified',
  description: 'Graph-scheduled implementation with code-checked verify loops, reversibility lanes, and a learning edge',
  phases: [{ title: 'Implement' }, { title: 'Check' }, { title: 'Verify' }],
}
// args: {
//   specPath, maxAttempts?: number (default 3), confirmDroppedEdges?: boolean,
//   closed?:   [{ id, evidence }]   // resume: tasks closed in a previous run (skipped)
//   executed?: [id]                 // resume: irreversible tasks the USER has executed
//   pending?:  [{ id, prepared }]   // resume: irreversible tasks still awaiting the user
//                                   //   (returned as-is with their reviewed command)
//   tasks: [{ id, description, acceptance,
//     lane: 'reversible'|'wide'|'irreversible',  // max lane of the criteria it covers
//     touches: string[],      // files/dirs the task may change (SCOPE ceiling; no globs)
//     checks: string[],       // contract checks, safe to run before any irreversible step
//     checkFiles?: string[],  // files defining the checks (hashed; must not change);
//                             //   required for wide and irreversible lanes
//     postChecks?: string[],  // irreversible lane: run after the user executes
//     dependsOn?: [{ id, crosses }] }] }   // crosses = the artifact that flows A -> B
const LANES = ['reversible', 'wide', 'irreversible']
const MAX = args.maxAttempts ?? 3
const problems = []

// ---- Code node 1: validate, fail closed ----------------------------------------
const normPath = p => p.trim().replace(/^(\.\/)+/, '').replace(/\/{2,}/g, '/').replace(/\/$/, '')
const under = (a, b) => a === b || a.startsWith(b + '/')
const overlaps = (xs, ys) => xs.some(x => ys.some(y => under(x, y) || under(y, x)))
const isList = v => Array.isArray(v) && v.length > 0 && v.every(x => typeof x === 'string' && x.trim())
const isStrList = v => Array.isArray(v) && v.every(x => typeof x === 'string')
// Normalized copies — the caller's task objects are never mutated.
const tasks = (args.tasks ?? []).map(t => ({ ...t,
  touches: isStrList(t?.touches) ? t.touches.map(normPath) : t?.touches,
  checkFiles: t?.checkFiles === undefined ? [] : isStrList(t.checkFiles) ? t.checkFiles.map(normPath) : t.checkFiles }))
const byId = {}
if (!tasks.length) problems.push('no tasks')
for (const t of tasks) {
  if (typeof t.id !== 'string' || !t.id) { problems.push('task without a string id'); continue }
  if (byId[t.id]) problems.push(`duplicate task id: ${t.id}`)
  byId[t.id] = t
  if (!LANES.includes(t.lane)) problems.push(`${t.id}: lane must be one of ${LANES.join(' | ')} (got ${JSON.stringify(t.lane)})`)
  if (!isList(t.checks)) problems.push(`${t.id}: checks must be a non-empty list of failable checks`)
  if (!isList(t.touches)) problems.push(`${t.id}: touches must list the paths the task may change`)
  else if (t.touches.some(x => /[*?[\]]/.test(x))) problems.push(`${t.id}: touches may not contain globs — list files or directories`)
  else if (t.touches.some(x => x === '' || x === '.' || x.split('/').includes('..')))
    problems.push(`${t.id}: touches may not be the repo root or contain '..' — name real paths`)
  if (!isStrList(t.checkFiles)) problems.push(`${t.id}: checkFiles must be a list of paths`)
  else if (t.checkFiles.some(x => x === '' || x === '.' || x.split('/').includes('..')))
    problems.push(`${t.id}: checkFiles may not be the repo root or contain '..'`)
  if (t.lane !== 'reversible' && !isList(t.checkFiles))
    problems.push(`${t.id}: ${t.lane} tasks need checkFiles so tampering can be detected`)
  if (t.lane === 'irreversible' && !isList(t.postChecks ?? []))
    problems.push(`${t.id}: irreversible tasks need postChecks to run after the user executes`)
}
// No task may touch ANY task's check files (not just its own).
const allCheckFiles = tasks.flatMap(t => Array.isArray(t.checkFiles) ? t.checkFiles : [])
for (const t of tasks)
  if (isList(t.touches) && overlaps(t.touches, allCheckFiles))
    problems.push(`${t.id}: touches overlaps a contract check file — implementers may not edit checks`)
const allTouches = tasks.flatMap(t => Array.isArray(t.touches) ? t.touches : [])
const deps = {}, droppedEdges = [], keptUnnamedEdges = []
for (const t of tasks) {
  deps[t.id] = []
  for (const d of t.dependsOn ?? []) {
    if (!byId[d?.id]) { problems.push(`${t.id} depends on unknown task ${d?.id}`); continue }
    const named = typeof d.crosses === 'string' && d.crosses.trim()
    if (named) deps[t.id].push(d.id)
    else if (byId[d.id].lane !== 'reversible') { deps[t.id].push(d.id); keptUnnamedEdges.push(`${d.id} -> ${t.id}`) }
    else droppedEdges.push(`${d.id} -> ${t.id}`)
  }
}
for (const c of args.closed ?? []) if (!byId[c?.id]) problems.push(`closed: unknown task ${c?.id}`)
for (const id of args.executed ?? []) if (byId[id]?.lane !== 'irreversible') problems.push(`executed: ${id} is not an irreversible task`)
for (const p of args.pending ?? []) if (byId[p?.id]?.lane !== 'irreversible') problems.push(`pending: ${p?.id} is not an irreversible task`)
for (const p of args.pending ?? []) if ((args.executed ?? []).includes(p?.id)) problems.push(`${p.id} is both pending and executed — pick one`)
for (const c of args.closed ?? []) if ((args.executed ?? []).includes(c?.id) || (args.pending ?? []).some(p => p?.id === c?.id))
  problems.push(`${c.id} is listed as closed and as executed/pending — pick one`)
const color = {}
const visit = (id, path) => {
  if (color[id] === 2) return
  if (color[id] === 1) { problems.push(`dependency cycle: ${[...path, id].join(' -> ')}`); return }
  color[id] = 1; deps[id].forEach(d => visit(d, [...path, id])); color[id] = 2
}
if (!problems.length) tasks.forEach(t => visit(t.id, []))
if (problems.length) return { status: 'invalid-args', problems }
if (droppedEdges.length && !args.confirmDroppedEdges)
  return { status: 'confirm-dropped-edges', droppedEdges, keptUnnamedEdges,
    note: 'These edges name nothing that crosses. Confirm the tasks are truly independent ' +
          '(rerun with confirmDroppedEdges: true) or add the crossing artifact.' }

// ---- Shared state -----------------------------------------------------------------
const status = {}
const closedIn = new Map((args.closed ?? []).map(c => [c.id, c.evidence ?? 'closed in a previous run']))
const executed = new Set(args.executed ?? [])
const pending = new Map((args.pending ?? []).map(p => [p.id, p.prepared ?? 'prepared in a previous run']))
const derived = [], recheck = [], conflicts = []
let halted = false
const norm = x => x.normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{M}\p{N}]+/gu, ' ').trim()

// Path locks: a task waits for every earlier-registered task whose touches overlap.
const registry = []
const withPaths = async (paths, fn) => {
  const waitOn = registry.filter(r => overlaps(r.paths, paths)).map(r => r.done)
  let release
  const done = new Promise(r => { release = r })
  registry.push({ paths, done })
  await Promise.all(waitOn)
  try { return await fn() } finally { release() }
}

// ---- Agents -------------------------------------------------------------------------
const RUN = { type: 'object', required: ['results', 'hashes', 'changedPaths'], properties: {
  results: { type: 'array', items: { type: 'object', required: ['check', 'exitCode'],
    properties: { check: { type: 'string' }, exitCode: { type: 'integer' }, output: { type: 'string' } } } },
  hashes: { type: 'object', additionalProperties: { type: 'string' } },
  changedPaths: { type: 'array', items: { type: 'string' } },
  deletedPaths: { type: 'array', items: { type: 'string' } } } }
const VERDICT = { type: 'object', required: ['pass', 'reason', 'evidence'], properties: {
  pass: { type: 'boolean' }, reason: { type: 'string' }, evidence: { type: 'string' },
  scope: { type: 'string' }, dependents: { type: 'string' },
  derivedConstraint: { type: 'string' }, constraintConflictsWithSpec: { type: 'boolean' } } }
const IRREV = 'Do NOT execute anything irreversible (migrations that rewrite or drop data, ' +
  'deletions, production data, money movement, publication). '

const runChecks = (t, list, label, files = t.checkFiles) => agent(
  `You are a check runner. Edit nothing. Run each check exactly as written and report its ` +
  `exit code and the last 20 lines of output: ${list.length ? list.join(' ;; ') : '(none)'}. ` +
  IRREV + `If a check would do any of that, do not run it: report exitCode -1 and output ` +
  `"refused: irreversible". Then report the sha256 of each of these paths (sha256sum; for a directory, the sha256 of ` +
  `its sorted manifest: \`find DIR -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum\`; ` +
  `"missing" if absent): ${files.join(', ') || '(none)'}. Finally report changedPaths: the ` +
  `union of \`git -c core.quotePath=false diff --name-only HEAD\` and ` +
  `\`git -c core.quotePath=false ls-files --others --exclude-standard\` (bare paths, one per ` +
  `entry), and deletedPaths: \`git -c core.quotePath=false diff --diff-filter=D --name-only HEAD\`. Report each check under its exact ` +
  `string as given. Raw results only — no interpretation.`, { label, phase: 'Check', schema: RUN })
// Code: match results to checks by exact string (counting is not enough).
const grade = (list, run) => {
  const rank = c => (c === 0 ? 0 : c === -1 ? 2 : 1)   // refused > failed > passed
  const byCheck = new Map()
  for (const r of run.results ?? [])      // duplicates: the worst result wins
    if (!byCheck.has(r.check) || rank(r.exitCode) > rank(byCheck.get(r.check).exitCode)) byCheck.set(r.check, r)
  const missing = list.filter(c => !byCheck.has(c))
  const refused = list.filter(c => byCheck.get(c)?.exitCode === -1)
  const failing = list.filter(c => byCheck.has(c) && byCheck.get(c).exitCode !== 0)
    .map(c => ({ check: c, exitCode: byCheck.get(c).exitCode, output: byCheck.get(c).output }))
  return { missing, refused, failing, green: !missing.length && !failing.length }
}
let preexisting = new Set()          // dirty before the run (ledger, spec, notes, WIP)
let watched = [], dirtyBase = {}     // pre-dirty paths outside every task: hashed, must not change
const outOfScope = run => run.changedPaths.map(normPath).filter(p => !preexisting.has(p) &&
  !allTouches.some(x => under(p, x)) && !allCheckFiles.some(x => under(p, x)))

const implementPrompt = (t, ret) =>
  `Implement task ${t.id} from the spec at ${args.specPath}: ${t.description}. ` +
  `Acceptance: ${t.acceptance}. Honor the spec's constraints, non-goals and deferred defaults. ` +
  `Derived constraints so far: ${derived.map(d => d.text).join(' | ') || 'none'}. ` +
  `You may change ONLY these paths: ${t.touches.join(', ')}. You may NOT modify the contract ` +
  `checks or their files: ${[...t.checks, ...(t.checkFiles ?? [])].join('; ')}. ` +
  (t.lane === 'irreversible'
    ? `IRREVERSIBLE lane: prepare the change and the exact command(s) for the user. ` + IRREV : '') +
  (ret ? `This unit was returned: VERDICT fail · REASON ${ret.reason} · EVIDENCE ${ret.evidence} ` +
    `· SCOPE ${ret.scope}. Fix exactly this, within SCOPE. ` : '') +
  `Return: files changed, the commands you actually executed with their output` +
  (t.lane === 'irreversible' ? ', and the exact command(s) the user must run' : '') + '.'

const verifyPrompt = (t, summary, run, ret) =>
  `You did NOT write this change. Task ${t.id}: ${t.description}. Acceptance: ${t.acceptance}. ` +
  `Review only these paths: ${t.touches.join(', ')}. Evidence, strongest first: (1) check-runner ` +
  `results ${JSON.stringify(run.results)}; (2) the commands the implementer actually executed; ` +
  `(3) your own reading of the changes. The implementer's summary is a claim, not evidence: ` +
  `${summary}. ` + (t.lane === 'irreversible' ? IRREV + 'Judge the prepared change and command. ' : '') +
  (t.lane === 'wide' ? 'WIDE lane: find the dependents of the changed surface and check them; ' +
    'put what you checked, with evidence, in "dependents" ("none found" needs evidence too). ' : '') +
  (ret ? `The previous attempt was returned for: ${ret.reason} (SCOPE ${ret.scope}). Confirm that ` +
    `defect is fixed and the change stayed within SCOPE; raise new objections only for ` +
    `regressions or unmet criteria. ` : '') +
  `Try to FAIL the work: unmet criteria, spec violations, scope creep, broken neighbors. On fail ` +
  `give REASON, EVIDENCE (expected vs got, file:line) and SCOPE (what a fix may touch). If this ` +
  `verdict reveals a constraint the spec did not state, return it as derivedConstraint and set ` +
  `constraintConflictsWithSpec if it contradicts the spec or its contract. Default pass=false if uncertain.`

const verifyWithRetry = async (t, summary, run, ret, attempt) =>
  (await agent(verifyPrompt(t, summary, run, ret), { label: `verify:${t.id}#${attempt}`, phase: 'Verify', schema: VERDICT })) ??
  (await agent(verifyPrompt(t, summary, run, ret), { label: `verify:${t.id}#${attempt}r`, phase: 'Verify', schema: VERDICT }))

const learn = (t, v) => {
  const text = v.derivedConstraint?.trim()
  if (!text) return
  if (v.constraintConflictsWithSpec) { conflicts.push({ from: t.id, text }); halted = true; return 'conflict' }
  if (derived.some(d => norm(d.text) === norm(text))) return
  derived.push({ from: t.id, text })
  const closedSoFar = Object.keys(status).filter(id => status[id] === 'closed')
  if (closedSoFar.length) recheck.push({ constraint: text, closedBefore: closedSoFar })
}

// ---- One task: a loop inside a node ----------------------------------------------
const runTask = async t => {
  if (pending.has(t.id))                  // still with the user: never re-implement
    return { id: t.id, status: 'awaiting-human', prepared: pending.get(t.id), postChecks: t.postChecks }
  if (executed.has(t.id)) {               // user ran the irreversible step; verify after
    const post = await runChecks(t, t.postChecks, `post:${t.id}`)
    if (!post) return { id: t.id, status: 'infra-error', where: 'post-check runner' }
    const g = grade(t.postChecks, post)
    return { id: t.id, status: g.green ? 'closed' : 'post-check-failed', missing: g.missing, failing: g.failing }
  }
  const baseline = baselineHashes
  let ret = null, produced = 0
  for (let attempt = 1; attempt <= MAX; attempt++) {
    if (halted) return { id: t.id, status: 'halted', reason: 'derived constraint conflicts with spec' }
    const summary = await agent(implementPrompt(t, ret), { label: `impl:${t.id}#${attempt}`, phase: 'Implement' })
    if (!summary) {
      ret = { reason: 'previous attempt produced no result', evidence: 'none', scope: t.touches.join(', ') }
      continue
    }
    produced++
    const run = await runChecks(t, t.checks, `check:${t.id}#${attempt}`, sweepFiles)
    if (!run || !Array.isArray(run.changedPaths))
      return { id: t.id, status: 'infra-error', where: 'check runner (no result or no changedPaths)', attempts: attempt }
    const tampered = allCheckFilesU.filter(f => baseline[f] !== run.hashes?.[f])   // any task's checks
    if (tampered.length) { halted = true; return { id: t.id, status: 'tampered', files: tampered, attempts: attempt } }
    const stray = [...outOfScope(run),
      ...watched.filter(f => dirtyBase[f] !== run.hashes?.[f])]   // pre-dirty file changed again
    if (stray.length) {                   // edits outside every declared path: unattributable
      halted = true
      return { id: t.id, status: 'scope-violation', paths: stray, attempts: attempt }
    }
    const g = grade(t.checks, run)
    if (g.refused.length) return { id: t.id, status: 'invalid-check', refused: g.refused, attempts: attempt,
      reason: 'a contract check would perform an irreversible action — move it to postChecks' }
    const v = await verifyWithRetry(t, summary, run, ret, attempt)
    if (!v) return { id: t.id, status: 'infra-error', where: 'verifier', attempts: attempt }
    if (learn(t, v) === 'conflict')
      return { id: t.id, status: 'halted', reason: 'its verdict produced a constraint that conflicts with the spec' }
    const wideOk = t.lane !== 'wide' || !!v.dependents?.trim()
    if (v.pass && g.green && wideOk) {
      if (t.lane === 'irreversible')
        return { id: t.id, status: 'awaiting-human', attempts: attempt, prepared: summary, postChecks: t.postChecks }
      return { id: t.id, status: 'closed', attempts: attempt, evidence: v.evidence, dependents: v.dependents }
    }
    const scope = v.scope || t.touches.join(', ')
    ret = !g.green
      ? { reason: g.missing.length ? `check runner did not report: ${g.missing.join('; ')}`
                                   : `contract checks failed: ${g.failing.map(f => f.check).join('; ')}`,
          evidence: g.failing.map(f => `${f.check} -> exit ${f.exitCode}: ${(f.output ?? '').slice(-300)}`).join(' | ') || 'incomplete run',
          scope }
      : !wideOk
        ? { reason: 'wide lane: dependents were not checked', evidence: v.evidence, scope }
        : { reason: v.reason, evidence: v.evidence, scope }
  }
  if (!produced) return { id: t.id, status: 'infra-error', where: 'implementer (no result on any attempt)' }
  return { id: t.id, status: 'plan-suspect', attempts: MAX, lastReturn: ret }
}

// ---- The graph between nodes: per-task scheduling, real edges only -------------
// One baseline for every check file, before any implementer runs.
const firstTask = tasks[0]
const base = await runChecks(firstTask, [], 'baseline:all', [...new Set(allCheckFiles)])
if (!base || !Array.isArray(base.changedPaths)) return { status: 'infra-error', where: 'baseline' }
const unhashed = allCheckFiles.filter(f => typeof base.hashes?.[f] !== 'string' ||
  base.hashes[f] === 'missing')   // a check file that cannot be hashed cannot be guarded
if (unhashed.length) return { status: 'infra-error', where: 'baseline', missingHashes: unhashed }
const baselineHashes = base.hashes
preexisting = new Set((base.changedPaths ?? []).map(normPath))
watched = [...preexisting].filter(p =>
  !allTouches.some(x => under(p, x)) && !allCheckFiles.some(x => under(p, x)))
if (watched.length) {
  const dirty = await runChecks(firstTask, [], 'baseline:dirty', watched)
  const deleted = new Set((base.deletedPaths ?? []).map(normPath))
  const unhashedDirty = watched.filter(f => typeof dirty?.hashes?.[f] !== 'string' ||
    (dirty.hashes[f] === 'missing' && !deleted.has(f)))   // e.g. a quoted non-ASCII path
  if (!dirty || unhashedDirty.length)
    return { status: 'infra-error', where: 'baseline (pre-dirty files)', missingHashes: unhashedDirty }
  dirtyBase = dirty.hashes
}
const allCheckFilesU = [...new Set(allCheckFiles)]
const sweepFiles = [...allCheckFilesU, ...watched]

const memo = {}
const schedule = id => memo[id] ??= (async () => {
  if (closedIn.has(id)) { status[id] = 'closed'; return { id, status: 'closed', resumed: true, evidence: closedIn.get(id) } }
  await Promise.all(deps[id].map(schedule))
  const notClosed = deps[id].filter(d => status[d] !== 'closed')
  let r
  if (notClosed.length) r = { id, status: 'blocked', reason: `upstream not closed: ${notClosed.join(', ')}` }
  else if (halted) r = { id, status: 'halted', reason: 'derived constraint conflicts with spec' }
  else {
    try { r = await withPaths(byId[id].touches, () => runTask(byId[id])) }
    catch (e) { r = { id, status: 'errored', reason: String(e?.message ?? e) } }
  }
  status[id] = r.status
  return r
})()

const results = (await parallel(tasks.map(t => () => schedule(t.id))))
  .map((r, i) => r ?? { id: tasks[i].id, status: 'errored', reason: 'no result' })

// Code node 3 — final sweep: nothing may have moved after the last per-task check
// (a verifier editing files, a null implementer attempt, another task's late write).
const sweep = await runChecks(firstTask, [], 'sweep:final', sweepFiles)
const finalSweep = !sweep || !Array.isArray(sweep.changedPaths)
  ? { ok: false, reason: 'infra-error: sweep runner returned nothing' }
  : (() => {
      const tamperedEnd = allCheckFilesU.filter(f => baselineHashes[f] !== sweep.hashes?.[f])
      const strayEnd = [...outOfScope(sweep), ...watched.filter(f => dirtyBase[f] !== sweep.hashes?.[f])]
      return { ok: !tamperedEnd.length && !strayEnd.length, tampered: tamperedEnd, stray: strayEnd }
    })()
if (!finalSweep.ok) halted = true
const pick = st => results.filter(r => r.status === st)
return { status: halted ? 'halted' : 'done', results, finalSweep,
  droppedEdges, keptUnnamedEdges, derivedConstraints: derived, recheck, conflicts,
  awaitingHuman: pick('awaiting-human'), planSuspect: pick('plan-suspect'),
  blocked: pick('blocked'), problems: results.filter(r =>
    ['tampered', 'scope-violation', 'invalid-check', 'infra-error', 'errored', 'post-check-failed', 'halted'].includes(r.status)) }
```

After the run:
- `invalid-args` / `confirm-dropped-edges` — nothing ran; fix the task graph or confirm.
- `awaitingHuman` — show the user each prepared command and its `postChecks`. The user
  (or the main agent, on the user's explicit yes for that command) executes it; then
  re-run with `closed` (everything already closed), `executed: [ids]` (what the user ran —
  only their post-checks run) and `pending: [{ id, prepared }]` (what the user has not run
  yet — returned unchanged, never re-implemented), and the run continues downstream.
- `planSuspect` — become ledger rows (`phase: during`): discovered unknowns, not things
  to force through. `tampered` / `invalid-check` / `scope-violation` go to the user with
  the evidence.
- `derivedConstraints` — appended to the spec's Derived constraints; `recheck` lists
  tasks that closed before a constraint appeared (review them against it);
  `conflicts` halted the run — each is a ledger row for the user to rule on.
- `finalSweep` — the last check over every check file, every pre-dirty file and the
  changed paths. If `ok` is false the run is halted; inspect `tampered` / `stray` before
  trusting any `closed` task.
- `droppedEdges` / `keptUnnamedEdges` — reported, so the user sees which sequencing was
  removed and which was kept because its upstream was not reversible.

## Note — quadrant scoring is NOT a fan-out

SCORE-QUADRANTS is a single strongest-tier agent call (ledger-keeper) per round: one
context reading the whole ledger scores more consistently than a panel, and it is cheap.
Reserve fan-out for discovery (Templates 1, 3) and verification (Template 2), where
perspective diversity pays. Per the skill's model routing, this call omits `model` so it
inherits the session's strength (Deep Research's synthesis-centre pattern); only the scout
fan-out runs on the cheaper `blindspot-scout` tier.

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

Execution (Template 4) invariants on every rung: the user approved the task graph; no
irreversible step runs without the user's explicit yes for that command; failures return
per unit with SCOPE; derived constraints are fed forward and conflicts halt. On rung 3
(no subagents) the implementer and verifier would be the same context, so **no lane
closes automatically** — every task is presented to the user with its check results as
an `awaiting-human` item.
