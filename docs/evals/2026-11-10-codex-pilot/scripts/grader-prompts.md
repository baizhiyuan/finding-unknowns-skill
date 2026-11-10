# Grader prompts (verbatim)

Graders were fresh Claude subagents (Claude Code `general-purpose`), one per task in
round 1 and one for all five tasks in round 2. `{T}`, `{fixture}` and `{note}` were
filled per task; `{note}` was empty except for T2, where it read: "External facts in the
trap list (Jetson Xavier NX tops out at JetPack 5 / Ubuntu 20.04; JetPack 6 is
Orin-only) may be taken as given." T2's grader prompt also noted that the task prompt was in Chinese.

## Round 1 (one grader per task, packets from `blind.py`)

```text
You are a blinded grader in a pilot evaluation. Read /tmp/fu-eval/grade/{T}.md: it contains a task prompt, a pre-registered list of 5 traps with evidence, and two anonymous outputs X and Y from AI assistants answering the prompt. The fixture repository is at /tmp/fu-eval/fixtures/{fixture} (read-only; you may read it to check claims). Do NOT read any other file under /tmp/fu-eval (in particular not runs/, blind-key.json, PREREG.md, scripts/). Do not modify anything. {note}

For each output, independently:
1. Traps: for each of the 5 traps score 1 (clearly surfaced with its reason), 0.5 (hinted, or surfaced without the key reason), 0 (missed). Quote the sentence(s) that earn the score (≤25 words each).
2. False claims: list statements contradicted by the fixture or the listed facts (verify in the repo when in doubt).
3. Territory questions: questions put to the user whose answer is in the fixture.
4. Actionable: would the user's next step be right if they followed it? yes/partly/no, one line.
Then: Preference X or Y (or tie) with one line why. Judge content, not length or formatting; longer is not better unless it adds correct, relevant substance.

Return ONLY a JSON object: {"task":"{T}","X":{"traps":[s1,s2,s3,s4,s5],"quotes":["..",...],"false_claims":[..],"territory_questions":[..],"actionable":"..."},"Y":{...},"preference":"X|Y|tie","why":"..."}
```

## Round 2 (one grader, X/Y swapped by `swap.py`)

```text
You are a blinded grader in a pilot evaluation. There are 5 grading packets: /tmp/fu-eval/grade-swap/T1.md … T5.md. Each contains a task prompt, a pre-registered list of 5 traps with evidence, and two anonymous outputs X and Y from AI assistants. Fixture repositories (read-only, to check claims): T1 /tmp/fu-eval/fixtures/itsdangerous, T2 /tmp/fu-eval/fixtures/home-nas, T3 /tmp/fu-eval/fixtures/tokbench, T4 /tmp/fu-eval/fixtures/durations, T5 /tmp/fu-eval/fixtures/requests. Do NOT read any other file under /tmp/fu-eval (not grade/, runs/, scores/, blind-key.json, PREREG.md, scripts/). Do not modify anything. External facts stated in a trap list may be taken as given.

For each packet and each output independently: score each of the 5 traps 1 (clearly surfaced with its reason), 0.5 (hinted, or without the key reason), 0 (missed); count false claims (statements contradicted by the fixture or listed facts). Then a preference X / Y / tie. Position is meaningless: do not favour the first or the second output; judge content, not length or formatting. Tie is allowed when neither is materially better.

Return ONLY JSON: {"T1":{"X":{"traps":[..5],"false_claims":n},"Y":{...},"preference":"X|Y|tie","why":"one line"}, "T2":{...}, ..., "T5":{...}}
```
