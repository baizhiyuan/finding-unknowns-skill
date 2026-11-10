#!/usr/bin/env node
// Behavioural tests for the Workflow templates in
// skills/finding-unknowns/references/workflows.md. The templates are extracted from the
// Markdown at test time, so the documented code is exactly the tested code. Agents are
// stubbed; no model or Workflow runtime is needed.  Run: node tests/workflows/run.mjs
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const root = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const md = readFileSync(join(root, 'skills/finding-unknowns/references/workflows.md'), 'utf8')
const blocks = [...md.matchAll(/```javascript\n([\s\S]*?)```/g)].map(m => m[1].replace('export const meta', 'const meta'))
if (blocks.length !== 4) throw new Error(`expected 4 templates, found ${blocks.length}`)
const [T1, T2, T3, T4] = blocks
const AsyncFn = Object.getPrototypeOf(async function () {}).constructor
const parallel = async fns => Promise.all(fns.map(f => f().catch(() => null)))
// pipeline(items, s1, s2, ...): each item flows through the stages; stage k>0 gets (prev, item)
const pipeline = async (items, ...stages) => Promise.all(items.map(async item => {
  let r = item
  for (const [i, stage] of stages.entries()) {
    try { r = i === 0 ? await stage(item) : await stage(r, item) } catch { return null }
  }
  return r
}))
const exec = (body, args, agent) => new AsyncFn('args', 'agent', 'parallel', 'pipeline', 'log', body)(args, agent, parallel, pipeline, () => {})

let fails = 0, total = 0
const report = (name, ok, got) => { total++; if (!ok) fails++; console.log(ok ? 'PASS' : 'FAIL', name.padEnd(30), got ?? '') }

// ---- Template 4 helpers -------------------------------------------------------------
const filesIn = p => { const m = p.match(/"missing" if absent\): (.*?)\. Finally/s); return !m || m[1] === '(none)' ? [] : m[1].split(', ') }
const hashAll = (p, overrides = {}) => Object.fromEntries(filesIn(p).map(f => [f, overrides[f] ?? 'h']))
const T = (id, o = {}) => ({ id, description: 'd', acceptance: 'a', lane: 'reversible', touches: [`src/${id}`], checks: ['pytest'], checkFiles: [`tests/${id}.py`], ...o })
const mk = (over = {}) => { const calls = []; const fn = async (p, o) => { calls.push(o.label); const k = o.label.split(':')[0]; const id = o.label.split(':')[1].split('#')[0]
  if (over[k]) { const r = await over[k](p, o, id); if (r !== undefined) return r }
  if (k === 'impl') return 'summary'
  if (['baseline', 'check', 'post', 'sweep'].includes(k)) { const list = k === 'baseline' ? [] : (k === 'post' ? ['post'] : ['pytest']); return { results: list.map(c => ({ check: c, exitCode: 0 })), hashes: hashAll(p), changedPaths: [] } }
  if (k === 'verify') return { pass: true, reason: 'ok', evidence: 'e', dependents: 'callers checked: none (grep evidence)' }
}; fn.calls = calls; return fn }
async function run(name, args, agent, expect) {
  const r = await exec(T4, args, agent)
  const got = r.results ? r.results.map(x => `${x.id}:${x.status}`).sort().join(',') : r.status
  let ok
  try { ok = typeof expect === 'function' ? expect(r, agent.calls) : got === expect }
  catch (e) { ok = false }   // a throwing assertion is a failure, not an aborted run
  report('T4 ' + name, ok, got)
  return r
}

// ---- Templates 1-3 ------------------------------------------------------------------
async function templates123() {
  // T1: Unicode-aware dedup — distinct Chinese findings stay distinct; identical ones merge
  const t1agent = async (p, o) => o.label.startsWith('scout:')
    ? { findings: [
        { unknown: '迁移会锁住订单表', quadrant: 'UU', costIfWrong: 5, pWrong: 0.5, route: 'territory', evidence: 'e' },
        { unknown: '回填会覆盖历史数据', quadrant: 'UU', costIfWrong: 4, pWrong: 0.5, route: 'interview', evidence: 'e' }] }
    : { real: true, reason: 'ok' }
  const r1 = await exec(T1, { task: 't', experienceLevel: 'new', lenses: ['a', 'b'] }, t1agent)
  report('T1 chinese-dedup', r1.rows.length === 2 && r1.rows.every(r => r.confirmedBy.length === 2), `rows=${r1.rows.length}`)
  // T2: evidence does not lose a majority vote; missing votes fail closed
  const panel = votes => async (p, o) => votes[o.label]
  const L = ['alternative-explanation', 'evidence-independence', 'reproduction']
  const all = v => Object.fromEntries(L.map((l, i) => [`refute:${l}`, v[i]]))
  const no = { refuted: false, reason: 'none' }, yes = { refuted: true, reason: 'leak', discriminatingCheck: 'audit pipeline' }
  let r = await exec(T2, { claim: 'c', evidence: 'e' }, panel(all([no, no, no])))
  report('T2 unanimous-survives', r.survives === true && r.status === 'panel-survived', r.status)
  r = await exec(T2, { claim: 'c', evidence: 'e' }, panel(all([yes, no, no])))
  report('T2 one-refutation-blocks', r.survives === false && r.status === 'resolved-provisional' && r.discriminatingChecks[0] === 'audit pipeline', r.status)
  r = await exec(T2, { claim: 'c', evidence: 'e' }, panel(all([no, no, null])))
  report('T2 missing-vote-blocks', r.survives === false, r.status)
  r = await exec(T2, { claim: 'c', evidence: 'e', lenses: [] }, panel({}))
  report('T2 empty-lenses-invalid', r.status === 'invalid-args', r.status)
  r = await exec(T2, { claim: 'c', evidence: 'e', lenses: ['x', 'x', 'x'] }, panel({}))
  report('T2 duplicate-lenses-invalid', r.status === 'invalid-args', r.status)
  // T1: a higher-cost duplicate keeps earlier confirmations; NFKC merges full-width forms
  const t1b = async (p, o) => o.label === 'scout:a' ? { findings: [{ unknown: 'Ｃａｃｈｅ 锁', quadrant: 'UU', costIfWrong: 2, pWrong: 0.5, route: 'territory', evidence: 'e' }] }
    : o.label === 'scout:b' ? { findings: [{ unknown: 'cache 锁', quadrant: 'UU', costIfWrong: 5, pWrong: 0.5, route: 'territory', evidence: 'e' }] }
    : { real: true, reason: 'ok' }
  const r1b = await exec(T1, { task: 't', experienceLevel: 'new', lenses: ['a', 'b'] }, t1b)
  report('T1 unequal-cost-keeps-lenses', r1b.rows.length === 1 && r1b.rows[0].costIfWrong === 5 && r1b.rows[0].confirmedBy.length === 2, JSON.stringify(r1b.rows.map(x => x.confirmedBy)))
  // T3: stops after two consecutive dry rounds; fresh findings are kept once
  let round = 0
  const t3agent = async (p, o) => ({ findings: o.label === 'probe:failure-modes' && round++ === 0 ? ['新的盲区', 'known'] : [] })
  r = await exec(T3, { task: 't', knownUnknowns: ['known'] }, t3agent)
  report('T3 loop-until-dry', r.dryStop === true && r.fresh.length === 1 && r.fresh[0] === '新的盲区', JSON.stringify(r.fresh))
}

// ---- Template 4 additions (review round: pre-dirty files, Unicode constraints) -------
async function template4Extra() {
  const dirtyBaseline = async p => ({ results: [], hashes: hashAll(p), changedPaths: ['notes/wip.md'] })
  await run('pre-dirty-unchanged-ok', { tasks: [T('A')] },
    mk({ baseline: dirtyBaseline, check: async p => ({ results: [{ check: 'pytest', exitCode: 0 }], hashes: hashAll(p), changedPaths: ['notes/wip.md', 'src/A/x.py'] }) }), 'A:closed')
  await run('pre-dirty-edited-caught', { tasks: [T('A')] },
    mk({ baseline: dirtyBaseline, check: async p => ({ results: [{ check: 'pytest', exitCode: 0 }], hashes: hashAll(p, { 'notes/wip.md': 'CHANGED' }), changedPaths: ['notes/wip.md', 'src/A/x.py'] }) }),
    r => r.results[0].status === 'scope-violation' && r.results[0].paths.includes('notes/wip.md'))
  await run('pre-dirty-unhashed-infra', { tasks: [T('A')] },
    mk({ baseline: async (p, o) => o.label === 'baseline:dirty' ? { results: [], hashes: {}, changedPaths: [] } : dirtyBaseline(p) }), 'infra-error')
  await run('pre-dirty-own-path-edited-ok', { tasks: [T('A')] },
    mk({ baseline: async p => ({ results: [], hashes: hashAll(p), changedPaths: ['src/A/wip.py'] }),
         check: async p => ({ results: [{ check: 'pytest', exitCode: 0 }], hashes: hashAll(p), changedPaths: ['src/A/wip.py'] }) }), 'A:closed')
  await run('quoted-path-missing-infra', { tasks: [T('A')] },
    mk({ baseline: async (p, o) => o.label === 'baseline:dirty'
      ? { results: [], hashes: { '"\\347\\254\\224.md"': 'missing' }, changedPaths: [] }
      : { results: [], hashes: hashAll(p), changedPaths: ['"\\347\\254\\224.md"'] } }), 'infra-error')
  await run('deleted-pre-dirty-ok', { tasks: [T('A')] },
    mk({ baseline: async (p, o) => o.label === 'baseline:dirty'
      ? { results: [], hashes: { 'old.md': 'missing' }, changedPaths: [] }
      : { results: [], hashes: hashAll(p), changedPaths: ['old.md'], deletedPaths: ['old.md'] },
      check: async p => ({ results: [{ check: 'pytest', exitCode: 0 }], hashes: hashAll(p, { 'old.md': 'missing' }), changedPaths: ['old.md'] }),
      sweep: async p => ({ results: [], hashes: hashAll(p, { 'old.md': 'missing' }), changedPaths: ['old.md'] }) }), 'A:closed')
  let late = false
  await run('other-task-check-file-tampered', { tasks: [T('A'), T('B', { dependsOn: [{ id: 'A', crosses: 'x' }] })] },
    mk({ impl: async (p, o, id) => { if (id === 'B') late = true; return 'summary' },
         check: async p => ({ results: [{ check: 'pytest', exitCode: 0 }], hashes: hashAll(p, late ? { 'tests/A.py': 'CHANGED' } : {}), changedPaths: [] }),
         sweep: async p => ({ results: [], hashes: hashAll(p, { 'tests/A.py': 'CHANGED' }), changedPaths: [] }) }),
    r => r.results.find(x => x.id === 'B').status === 'tampered' && r.status === 'halted')
  await run('final-sweep-catches-late-edit', { tasks: [T('A')] },
    mk({ sweep: async p => ({ results: [], hashes: hashAll(p, { 'tests/A.py': 'EDITED-BY-VERIFIER' }), changedPaths: [] }) }),
    r => r.status === 'halted' && r.finalSweep.ok === false && r.finalSweep.tampered.includes('tests/A.py'))
  await run('missing-check-file-infra', { tasks: [T('A', { checkFiles: ['tests/A'] })] },
    mk({ baseline: async p => ({ results: [], hashes: hashAll(p, { 'tests/A': 'missing' }), changedPaths: [] }) }), 'infra-error')
  await run('final-sweep-clean', { tasks: [T('A')] }, mk(), r => r.status === 'done' && r.finalSweep.ok === true)
  let n = 0
  await run('chinese-constraints-distinct', { tasks: [T('A'), T('B', { dependsOn: [{ id: 'A', crosses: 'x' }] })] },
    mk({ verify: async () => ({ pass: true, reason: 'ok', evidence: 'e', derivedConstraint: ++n === 1 ? '保持关键字参数不变' : '日志字段名不得修改' }) }),
    r => r.derivedConstraints.length === 2)
}

;(async () => {
  await templates123()
  await run('lane-typo', { tasks: [T('mig', { lane: 'Irreversible' })] }, mk(), 'invalid-args')
  await run('lane-missing', { tasks: [T('mig', { lane: undefined })] }, mk(), 'invalid-args')
  await run('checks-missing', { tasks: [T('A', { checks: undefined })] }, mk(), 'invalid-args')
  await run('checks-empty-wide', { tasks: [T('A', { checks: [], lane: 'wide' })] }, mk(), 'invalid-args')
  await run('dup-ids', { tasks: [T('A'), T('A')] }, mk(), 'invalid-args')
  await run('unknown-dep', { tasks: [T('B', { dependsOn: [{ id: 'A', crosses: 'x' }] })] }, mk(), 'invalid-args')
  await run('cycle', { tasks: [T('X', { dependsOn: [{ id: 'Y', crosses: 'a' }] }), T('Y', { dependsOn: [{ id: 'X', crosses: 'b' }] })] }, mk(), 'invalid-args')
  await run('touches-checkfiles', { tasks: [T('A', { touches: ['tests'] })] }, mk(), 'invalid-args')
  await run('irrev-no-post', { tasks: [T('A', { lane: 'irreversible' })] }, mk(), 'invalid-args')
  await run('happy', { tasks: [T('A'), T('B', { lane: 'wide', dependsOn: [{ id: 'A', crosses: 'api' }] })] }, mk(), 'A:closed,B:closed')
  // unnamed edge from irreversible upstream is KEPT -> B blocked while A awaits human
  await run('unnamed-irrev-kept', { tasks: [T('A', { lane: 'irreversible', postChecks: ['post'] }), T('B', { dependsOn: [{ id: 'A' }] })] }, mk(),
    r => r.results.find(x => x.id === 'B').status === 'blocked' && r.keptUnnamedEdges.length === 1)
  await run('unnamed-rev-confirm', { tasks: [T('A'), T('B', { dependsOn: [{ id: 'A' }] })] }, mk(), 'confirm-dropped-edges')
  await run('unnamed-rev-confirmed', { confirmDroppedEdges: true, tasks: [T('A'), T('B', { dependsOn: [{ id: 'A' }] })] }, mk(), 'A:closed,B:closed')
  // irreversible: awaiting-human; then resume with closed+executed -> post-checks only, downstream runs
  const irr = [T('A', { lane: 'irreversible', postChecks: ['post'] }), T('B', { dependsOn: [{ id: 'A', crosses: 'schema' }] }), T('C')]
  await run('irrev-wait', { tasks: irr }, mk(), 'A:awaiting-human,B:blocked,C:closed')
  const ag = mk()
  await run('irrev-resume', { tasks: irr, closed: [{ id: 'C', evidence: 'run1' }], executed: ['A'] }, ag,
    (r, calls) => r.results.map(x => x.id + ':' + x.status).sort().join() === 'A:closed,B:closed,C:closed' && !calls.some(c => c.startsWith('impl:A') || c.startsWith('impl:C')))
  await run('post-check-fail', { tasks: [irr[0]], executed: ['A'] }, mk({ post: async () => ({ results: [{ check: 'post', exitCode: 1 }], hashes: {}, changedPaths: [] }) }), 'A:post-check-failed')
  // tampering: hashes change after impl -> immediate stop, single attempt
  await run('tampered', { tasks: [T('A')] }, mk({ check: async () => ({ results: [{ check: 'pytest', exitCode: 0 }], hashes: { 'tests/A.py': 'CHANGED' }, changedPaths: [] }) }),
    (r, calls) => r.results[0].status === 'tampered' && calls.filter(c => c.startsWith('impl')).length === 1)
  // verifier claims pass but checks red -> retried with code-built reason; after cap plan-suspect
  let prompts = []
  await run('red-checks', { tasks: [T('A')] }, mk({ impl: async p => { prompts.push(p); return 'summary' }, check: async () => ({ results: [{ check: 'pytest', exitCode: 1, output: 'assert 302 == 200' }], hashes: { 'tests/A.py': 'h' }, changedPaths: [] }) }),
    r => r.results[0].status === 'plan-suspect' && /contract checks failed: pytest/.test(prompts[1]) && /302 == 200/.test(prompts[1]))
  // scoped retry passes on attempt 2 and verifier sees the previous return
  let vprompts = [], n = 0
  await run('scoped-retry', { tasks: [T('A')] }, mk({ verify: async p => { vprompts.push(p); return ++n === 1 ? { pass: false, reason: 'redirect wrong', evidence: 'expected 302 got 200 auth.py:88', scope: 'src/A/auth.py' } : { pass: true, reason: 'ok', evidence: 'e' } } }),
    r => r.results[0].status === 'closed' && r.results[0].attempts === 2 && /redirect wrong/.test(vprompts[1]))
  await run('wide-no-dependents', { tasks: [T('A', { lane: 'wide' })] }, mk({ verify: async () => ({ pass: true, reason: 'ok', evidence: 'e' }) }), 'A:plan-suspect')
  await run('verifier-null', { tasks: [T('A')] }, mk({ verify: async () => null }), (r, calls) => r.results[0].status === 'infra-error' && calls.filter(c => c.startsWith('impl')).length === 1)
  await run('impl-null-once', { tasks: [T('A')] }, (() => { let k = 0; return mk({ impl: async () => (++k === 1 ? null : 'summary') }) })(), r => r.results[0].status === 'closed' && r.results[0].attempts === 2)
  await run('refused-check', { tasks: [T('A', { lane: 'irreversible', postChecks: ['p'] })] }, mk({ check: async () => ({ results: [{ check: 'pytest', exitCode: -1, output: 'refused: irreversible' }], hashes: { 'tests/A.py': 'h' }, changedPaths: [] }) }), 'A:invalid-check')
  // learning edge: constraint from A reaches later task's prompt; dedupe; recheck lists closed tasks
  let bPrompt = ''
  const r = await run('learning-edge', { tasks: [T('A'), T('B', { dependsOn: [{ id: 'A', crosses: 'x' }] }), T('C', { dependsOn: [{ id: 'B', crosses: 'y' }] })] },
    mk({ impl: async (p, o, id) => { if (id === 'C') bPrompt = p; return 'summary' }, verify: async (p, o, id) => ({ pass: true, reason: 'ok', evidence: 'e', derivedConstraint: id === 'A' ? undefined : 'Keep kwargs!' }) }),
    r => (r.derivedConstraints.length === 1 && /Keep kwargs/.test(bPrompt) && r.recheck.length === 1 && r.recheck[0].closedBefore.join() === 'A'))
  await run('conflict-halts', { tasks: [T('A'), T('B', { dependsOn: [{ id: 'A', crosses: 'x' }] })] },
    mk({ verify: async (p, o, id) => ({ pass: true, reason: 'ok', evidence: 'e', derivedConstraint: 'drop auth', constraintConflictsWithSpec: id === 'A' }) }),
    r => r.status === 'halted' && r.results.find(x => x.id === 'A').status === 'halted' && r.results.find(x => x.id === 'B').status === 'blocked' && r.conflicts.length === 1)
  // no barrier: C depends on A only, must start before slow unrelated B ends
  const t0 = Date.now(); const when = {}
  await run('no-barrier', { tasks: [T('A'), T('B'), T('C', { dependsOn: [{ id: 'A', crosses: 'x' }] })] },
    mk({ impl: async (p, o, id) => { if (id === 'B') await new Promise(r => setTimeout(r, 300)); when[id] = Date.now() - t0; return 'summary' } }), () => when.C < 200)
  // path locks: overlapping touches never concurrent
  let active = 0, maxActive = 0
  await run('path-lock', { tasks: [T('A', { touches: ['src/shared'] }), T('B', { touches: ['src/shared/x.py'] })] },
    mk({ impl: async () => { active++; maxActive = Math.max(maxActive, active); await new Promise(r => setTimeout(r, 50)); active--; return 'summary' } }), () => maxActive === 1)
  let a2 = 0, m2 = 0
  await run('no-lock-disjoint', { tasks: [T('A'), T('B')] },
    mk({ impl: async () => { a2++; m2 = Math.max(m2, a2); await new Promise(r => setTimeout(r, 50)); a2--; return 'summary' } }), () => m2 === 2)

  // ---- review round 2 (N1–N8) ----
  let c1 = 0, m1 = 0
  await run('N1-dot-slash-lock', { tasks: [T('A', { touches: ['./src/x.py'] }), T('B', { touches: ['src//x.py'] })] },
    mk({ impl: async () => { c1++; m1 = Math.max(m1, c1); await new Promise(r => setTimeout(r, 40)); c1--; return 'summary' } }), () => m1 === 1)
  await run('N1-glob-rejected', { tasks: [T('A', { touches: ['src/**'] })] }, mk(), 'invalid-args')
  await run('N2-cross-checkfile', { tasks: [T('A'), T('B', { touches: ['tests/A.py'] })] }, mk(), 'invalid-args')
  await run('N2-single-baseline', { tasks: [T('A'), T('B')] }, mk(), (r, calls) => calls.filter(c => c.startsWith('baseline')).length === 1 && calls.indexOf('baseline:all') < calls.findIndex(c => c.startsWith('impl')))
  await run('N3-dup-results', { tasks: [T('A', { checks: ['pytest a', 'pytest b'] })] },
    mk({ check: async () => ({ results: [{ check: 'pytest a', exitCode: 0 }, { check: 'pytest a', exitCode: 0 }], hashes: { 'tests/A.py': 'h' }, changedPaths: [] }) }), 'A:plan-suspect')
  await run('N3-wrong-check', { tasks: [T('A')] },
    mk({ check: async () => ({ results: [{ check: 'echo ok', exitCode: 0 }], hashes: { 'tests/A.py': 'h' }, changedPaths: [] }) }), 'A:plan-suspect')
  await run('N4-wide-needs-files', { tasks: [T('A', { lane: 'wide', checkFiles: [] })] }, mk(), 'invalid-args')
  await run('N4-baseline-missing-hash', { tasks: [T('A')] },
    mk({ baseline: async () => ({ results: [], hashes: {}, changedPaths: [] }) }), r => r.status === 'infra-error' && r.missingHashes?.length === 1)
  await run('N5-pending-not-reimpl', { tasks: [T('A', { lane: 'irreversible', postChecks: ['post'] }), T('B', { lane: 'irreversible', postChecks: ['post'] })], executed: ['A'], pending: [{ id: 'B', prepared: 'psql -f b.sql' }] },
    mk(), (r, calls) => r.results.map(x => x.id + ':' + x.status).sort().join() === 'A:closed,B:awaiting-human' && !calls.some(c => c.startsWith('impl:B')) && r.results.find(x => x.id === 'B').prepared === 'psql -f b.sql')
  await run('N6-scope-violation', { tasks: [T('A'), T('B', { dependsOn: [{ id: 'A', crosses: 'x' }] })] },
    mk({ check: async () => ({ results: [{ check: 'pytest', exitCode: 0 }], hashes: { 'tests/A.py': 'h', 'tests/B.py': 'h' }, changedPaths: ['src/A/a.py', 'etc/passwd'] }) }),
    r => r.results.find(x => x.id === 'A').status === 'scope-violation' && r.results.find(x => x.id === 'B').status === 'blocked')
  await run('N6-inscope-sibling-ok', { tasks: [T('A'), T('B')] },
    mk({ check: async (p, o, id) => ({ results: [{ check: 'pytest', exitCode: 0 }], hashes: { 'tests/A.py': 'h', 'tests/B.py': 'h' }, changedPaths: ['src/A/x.py', 'src/B/y.py'] }) }), 'A:closed,B:closed')
  await run('N7-impl-always-null', { tasks: [T('A')] }, mk({ impl: async () => null }), 'A:infra-error')
  await run('N8-conflict-task-halts', { tasks: [T('A')] },
    mk({ verify: async () => ({ pass: true, reason: 'ok', evidence: 'e', derivedConstraint: 'drop auth', constraintConflictsWithSpec: true }) }), 'A:halted')
  await run('no-mutation', (() => { const a = { tasks: [T('A', { touches: ['./src/A'] })] }; globalThis.__a = a; return a })(), mk(), () => globalThis.__a.tasks[0].touches[0] === './src/A')

  // ---- review round 3 (NEW-1..4) ----
  await run('NEW1-dirty-tree-ok', { tasks: [T('A'), T('B')] },
    mk({ baseline: async p => ({ results: [], hashes: hashAll(p), changedPaths: ['unknowns-ledger.md', 'notes/wip.md'] }),
         check: async p => ({ results: [{ check: 'pytest', exitCode: 0 }], hashes: hashAll(p), changedPaths: ['unknowns-ledger.md', 'notes/wip.md', 'src/A/x.py'] }) }), 'A:closed,B:closed')
  await run('NEW1-new-stray-still-caught', { tasks: [T('A')] },
    mk({ baseline: async p => ({ results: [], hashes: hashAll(p), changedPaths: ['unknowns-ledger.md'] }),
         check: async p => ({ results: [{ check: 'pytest', exitCode: 0 }], hashes: hashAll(p), changedPaths: ['unknowns-ledger.md', 'coverage.xml'] }) }), 'A:scope-violation')
  await run('NEW2-changedPaths-omitted', { tasks: [T('A')] },
    mk({ check: async () => ({ results: [{ check: 'pytest', exitCode: 0 }], hashes: { 'tests/A.py': 'h' } }) }), 'A:infra-error')
  await run('NEW2-baseline-no-changed', { tasks: [T('A')] }, mk({ baseline: async () => ({ results: [], hashes: { 'tests/A.py': 'h' } }) }), 'infra-error')
  await run('NEW3-dot-root', { tasks: [T('A', { touches: ['.'] })] }, mk(), 'invalid-args')
  await run('NEW3-dotdot', { tasks: [T('A', { touches: ['src/../tests/A.py'] })] }, mk(), 'invalid-args')
  await run('NEW3-dot-slash-root', { tasks: [T('A', { touches: ['./'] })] }, mk(), 'invalid-args')
  await run('NEW4-dup-worst-wins', { tasks: [T('A')] },
    mk({ check: async () => ({ results: [{ check: 'pytest', exitCode: 1 }, { check: 'pytest', exitCode: 0 }], hashes: { 'tests/A.py': 'h' }, changedPaths: [] }) }), 'A:plan-suspect')
  await template4Extra()
  console.log(fails ? `\n${fails} of ${total} FAILED` : `\nALL ${total} PASS`)
  process.exit(fails ? 1 : 0)
})()
