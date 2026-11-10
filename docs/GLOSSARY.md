# Glossary

One vocabulary across the three skills (`finding-unknowns`, `keep-the-reasoning`,
`theory-vs-result`), the five agents and the three commands. Each skill still defines what it
uses, because skills are installed standalone; this page is where the terms meet.

- **KK / KU / UK / UU** — the quadrant map of a gap: Known Knowns (stated; write them down),
  Known Unknowns (nameable gaps), Unknown Knowns ("I'll know it when I see it" taste), Unknown
  Unknowns (blind spots). The quadrant picks the discovery technique. *Used in:*
  finding-unknowns Phase 0, Cartographer ledger rows and clarity scores.
- **Regret** — `cost-if-wrong (1–5) × P(wrong)` for one ledger row. It *orders* the work; it
  never decides what must reach the user (reversibility does). *Used in:* Cartographer C0–C2,
  `ledger-keeper`.
- **Route** — how a ledger row gets cleared: `interview` · `territory` · `experiment` ·
  `audit`. Regret picks the row; route picks the instrument. *Used in:* Cartographer C1.
- **Lane** — reserved for **reversibility**: `reversible` · `wide` · `irreversible`. A row's,
  a contract criterion's, or a task's lane decides who may close it; irreversible work is
  prepared by the agent and executed by the user. *Used in:* Cartographer C0, the verification
  contract's `lane` column, Phase E, `fu-execute-verified`.
- **Rigor level** — how much of `theory-vs-result` a measured result gets: `note` (one line) ·
  `report` (cards + table) · `decision` (adds the frozen rule and the rule/direction split).
  A reproducible, deterministic failure takes the lighter **debug path** instead. *Used in:*
  theory-vs-result Step 0, `mechanism-auditor`.
- **Packet size** — how much of the handoff packet `keep-the-reasoning` delivers: `offload`
  (one line) · `compact` (four sections) · `full` (nine sections). Scales with consequence,
  not effort. *Used in:* keep-the-reasoning Step 0, Cartographer merge (always `full`).
- **Mode** — finding-unknowns' operating mode: **lightweight** (techniques 1–8, short report)
  or **Cartographer** (ledger, gate, spec). Cartographer's breadth is its **depth**
  (`--quick` · `--standard` · `--deep`). *Used in:* finding-unknowns Phase 0, `/cartographer`.
- **Prior** — any expectation recorded before the result is seen: the user's or the agent's.
  A theory-vs-result **Theory** (prior + mechanism chain) and its **prediction card** are the
  measured-claim form of a prior. A prior recorded by any of the three skills in a session is
  reused, never asked again. *Used in:* finding-unknowns Phase 0, ledger `prior:` entries,
  keep-the-reasoning Step 1 and Prior vs result, theory-vs-result Step 1.
- **Verification contract / "verified"** — per claim or acceptance criterion, written before
  the work: the check, its artifact, what it proves, what it does NOT prove. A claim is
  "verified" only when its contract checks ran and could have failed. A plan's **Definition of
  verified** (Technique 5) is the same contract at plan scale. *Used in:* keep-the-reasoning
  Step 1, Cartographer spec (C2.5), Phase E.
- **Mechanism tier** — the evidence behind an explanation of a measured result: `verified`
  (a discriminating test ran) · `supported` · `inferred` · `untested`. The tier word
  `verified` grades a *mechanism*; it is not the contract sense above. *Used in:*
  theory-vs-result Step 3, `mechanism-auditor`, Cartographer `experiment` mapping.
- **Fresh-context refutation** — the shared primitive: a context that did not produce a claim
  tries to refute it from the same evidence and returns the strongest alternative explanation
  plus the cheapest discriminating check. Without a separate context, the fallback is labelled
  `same-context — weaker`. Canonical in keep-the-reasoning ("Fresh-context refutation (shared
  primitive)"). *Used in:* the full packet's Strongest counterargument / Did I miss anything?,
  theory-vs-result Fresh_Context_Check and `mechanism-auditor`, Cartographer C1 step 3.5 and
  `fu-verify-panel`.
- **Ledger** — `.finding-unknowns/unknowns-ledger.md`: header + one row per unknown (quadrant,
  prior, regret, route, lane, status). It is the Cartographer resume state; rows are never
  deleted. *Used in:* Cartographer, `ledger-keeper`, `quiz-master`.
- **Spec** — `.finding-unknowns/unknowns-spec-{slug}.md`, written on gate PASS: goal,
  constraints, acceptance criteria, verification contract; pending approval, and the default
  end of Cartographer. *Used in:* Cartographer C2.5, Phase E.
- **Artifact directory** — `.finding-unknowns/` at the project root holds every file the
  skills write (ledger, spec, `implementation-notes.md`, `prototypes/`, `change-report.md`,
  `predictions/`, handoff packets written to disk). It is working state, ignored by default
  (`.gitignore` line `.finding-unknowns/`). To review ledgers and specs in PRs, ignore the
  contents instead and re-include the two files (git cannot re-include a file inside an
  ignored directory):
  ```
  .finding-unknowns/*
  !.finding-unknowns/unknowns-ledger.md
  !.finding-unknowns/unknowns-spec-*.md
  ```
  *Used in:* all three skills, `ledger-keeper`, `prototype-smith`, `quiz-master`.
- **Schema** — the ledger format version, the ledger's first line (`schema: 2` since 4.3.0;
  no line = schema 1, pre-4.3). On resume, `ledger-keeper` upgrades schema 1 by adding the
  missing header fields and reports what it added. *Used in:* Cartographer C0 and Resume,
  `ledger-keeper`.
