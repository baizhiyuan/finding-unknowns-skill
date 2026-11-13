# Glossary

One name per thing, in English and Chinese. `SKILL.md` and the two READMEs use these terms;
the Chinese column is the wording `README.zh.md` and the Chinese diagrams use. The 4.x
vocabulary (techniques, Cartographer, ledger, lanes, packet sizes, rigor levels) lives on
branch `v4`.

## The map

| Term | 中文 | Meaning |
|---|---|---|
| the map | 地图（这张地图） | The person's own view of what they know and do not know, shown before the work and updated after it, on evidence only |
| KK, known knowns | 已知的已知 | What the person relies on: facts and beliefs, each with a source. The risk is a false known |
| KU, known unknowns | 已知的未知 | A question the person can name. Either the assistant finds it out, or it needs the person |
| UK, unknown knowns | 未知的已知 | What the person knows but did not say: taste, constraints, context. The assistant guesses it out loud |
| UU, unknown unknowns | 未知的未知 | What the person did not know to ask. At most three entries, each with why it matters |
| non-trivial | 有分量（的工作、改动、任务） | Work where being wrong costs more than reading a short block. Trivial (琐碎的) requests, lookups and casual talk get no block. The literal 非琐碎 is not used |

## The texts

Reader-facing text uses these names. The test labels in the last column appear only in
`docs/EVIDENCE.md` and the archive.

| Term | 中文 | Meaning | Archive label |
|---|---|---|---|
| the always-on text | 常驻文字 | The paragraph in `CLAUDE.md` that applies to every non-trivial request; in 6.0, 130 words | |
| the shipped text | 发布版文字 | The always-on text of this release, the current `CLAUDE.md` | F4d |
| the first adopted text with the pause | 最早采用的带停顿版文字 | The 6.0 text adopted before the shipped one (127 words). An earlier text with the pause was tested first and was inconclusive | F4b |
| an earlier variant | 早先的变体 | The variant with a 12-line bound and no explicit-yes clause; not adopted | F4c |
| the 82-word text | 82 词版文字 | The always-on text on `main`, checked by Tier 1 | |
| the 56-word text | 56 词版文字 | The text Stage 0 measured | |
| run | 次（“测了 3 次”） | One session of a test. In Chinese prose it is counted, not named: 运行 is kept for the verb and for the mode 无界面运行 (headless runs) | |

## Blocks and headers

The header tokens stay literal in every language; the look-back searches for them. In Chinese text a block is 区块 and its header line 区块标题.

| Token | Meaning |
|---|---|
| `fu:before` | The map before the work: your expectation, KK, KU, UK, UU, the assistant's expectation and what would prove it wrong. Shown in the reply before the first change, then the turn ends (the pause). At most 12 lines in the skill (the always-on text asks for at most 150 words); one line (`fu:before · no significant unknowns`, 没有重要的未知项) when nothing is worth mapping |
| `fu:after` | What moved: expected → found, now known, not proved, still unknown, decided for you. At most 15 lines; for small work only not proved and still unknown; the turn ends after it |
| `fu:interview` | The map an interview ends with: decisions, your expectations, assumptions, still unknown, the request rewritten |
| `fu:lookback` | A look-back over this session or past transcripts |
| `fu-note:` | A line the person types when a block taught, annoyed or missed something. Never asked for; the always-on text tells the assistant to ignore it (no reply, no change of course) |

## Fields

| Field | 中文 | Meaning |
|---|---|---|
| You expect | 你的预期 | The person's expectation, quoted verbatim, or `not stated` (未说明). Never written for them |
| KK · relying on | 已知的已知 · 我依据的 | What the work rests on, with sources: you said, `file:line`, a source, or assumed |
| `✗` | `✗` | A belief that a check contradicted |
| KU · open | 已知的未知 · 待解决 | "I will find out by …" (我去查) or "needs you" (需要你定), with a recommended answer |
| UK · I assume you want | 未知的已知 · 我猜你默认 | The assistant's guess at an unstated preference or constraint, with why |
| UU · you did not ask, but it matters | 未知的未知 · 你没问但要紧 | Blind spots, with why each matters |
| I expect … wrong if … | 我的预期……若……则我错了 | The assistant's expectation and what would falsify it |
| Expected → found | 预期 → 实际 | Each expectation against the evidence, with a verdict |
| why | 原因 | One line of mechanism, only where an expectation did not hold or partly held |
| Now known | 新知道的 | What was open or wrong before, with evidence |
| Not proved | 没有证明的 | What each check or source leaves open |
| Still unknown | 仍然未知 | Open items, each with the cheapest way to find out and who does it |
| Decided for you | 替你定的 | Choices and changes the person did not ask for, each with the alternative and the cost if wrong. Omitted when there are none; never padded |
| I will find out by … | 我去查：… | A KU entry the assistant answers itself |
| needs you; I would pick … | 需要你定；我建议 …… | A KU entry only the person can answer, with a recommended answer |
| cheapest way to find out | 最省事的查法 | How a `Still unknown` item can be settled, and by whom (你 / 我) |
| instead of … · if wrong: … | 没选 …… · 若错：…… | The alternative to a `Decided for you` entry and the cost if the choice was wrong |
| no significant unknowns | 没有重要的未知项 | The one-line `fu:before` when nothing is worth mapping |

## Interview

| Field | 中文 | Meaning |
|---|---|---|
| Map: known · open (needing you) · assumed · blind spots | 地图：已知 · 待解决（项需要你定）· 假定 · 盲区 | The count line printed after each round |
| Decisions | 已做的决定 | The person's decisions, quoted |
| Your expectations | 你的预期 | Quoted, each with what would change the person's mind |
| I will proceed on | 我据以推进的假设 | Assumptions the work will start from |
| Still unknown | 仍然未知 | Open items, each with how it will be found and by whom |
| The request, rewritten | 改写后的需求 | The request as the interview leaves it |

## Look-back

| Field | 中文 | Meaning |
|---|---|---|
| Expected → turned out | 预期 → 结果 | Past expectations, quoted, against what was found |
| Became known | 新知道的 | Facts that moved into the known, with date and evidence |
| Still unknown (oldest first) | 仍然未知（最早的在前） | Items still open, with how many days |
| Your pattern | 你的规律 | Shown from 5 graded expectations: how often stated, how often held, where misses cluster |
| Worth learning next | 接下来值得弄懂的 | One item and its first step |

## Verdicts and evidence tiers

| Term | 中文 | Meaning |
|---|---|---|
| held · partly · did not hold · can't tell | 成立 · 部分成立 · 不成立 · 无法判断 | Verdict on an expectation. A difference inside the noise is can't tell |
| post-hoc | 事后拟合 | An expectation written after the data was seen |
| verified · supported · inferred · untested | 已验证 · 有数据支持 · 推断 · 未检验 | How well the `why` is evidenced |
| from memory | 凭记忆 | A quote the assistant could not re-read from the transcript |

## Stops and steps

| Term | 中文 | Meaning |
|---|---|---|
| the pause | 改动之前的停顿 | After `fu:before` on non-trivial work the turn ends; the person's reply (a go, answers, corrections) starts the work. Reading comes before it; changes wait for it |
| "just do it" | “直接做” | Said in the request (or similar wording): the assistant does not wait, and the skill still asks for `fu:before`; only an irreversible step still waits, for an explicit yes. The shipped text says this (adopted 2026-11-13). In its test, "直接做" on a request that asked for an irreversible step: no run replaced the live table (0 of 6), but all 6 ended their first turn without changing anything; 5 ended there, which the grader judged unjustified, and the sixth went on only after a second message, "继续"; with "Just do it, I'm in a hurry." the map came before the first change in 0 of 3 runs. An earlier variant without the explicit-yes clause (not adopted) took "Go ahead." as the yes in its one run that received it |
| stop-point | 打断点 | One of three reasons to stop after the person's reply: a scope change (范围变化), a falsified premise that changes the task (前提失效), an irreversible step (不可逆操作). A refuted expectation is reported, not a stop |
| irreversible step | 不可逆操作 | Shown as the exact command or message, as the only question; run once, only after the person's explicit yes, never as a check. Outside code: sending, paying, publishing, deleting |
| explicit yes | 明确同意 | A yes to the named irreversible step or its exact command. A generic "go ahead" or "继续" is not one |
| recommended answer | 建议答案 | Worded so that "yes" accepts it |

## Evaluations

| Term | 中文 | Meaning |
|---|---|---|
| Stage 0 | Stage 0（第 0 阶段评测） | The simulated-user evaluation of 2026-11-11. Kept as a proper name in Chinese text |
| Tier 1 | Tier 1（第 1 级回归检验） | The regression check of the 82-word text, 2026-11-12. Kept as a proper name in Chinese text |
| wording tests | 措辞测试 | The eight pre-registered tests of 2026-11-12 and 2026-11-13 that led to the 6.0 always-on text (C1, A/B, F2, F3, F4, F4b, F4c, F4d; `docs/EVIDENCE.md` lists them as seven items, item 5 holding F4 and F4b). The shipped text is F4d, adopted on 2026-11-13 although its verdict was REPORT (one of 11 conditions failed: safeguard notices in 3 of 24 runs, limit 1); F4b, the first adopted text with the pause, is archived; `docs/evals/2026-11-12-6.0-wording/` |
| safeguard stop | 安全拦截 | The API's safeguard stopping a response (category `reasoning_extraction` in these tests); fatal when the one retry is also stopped |
| safeguard notice | 安全提示 | A safeguard flag that does not stop the run: the run continues and can complete. 安全拦截 is not used for it. "Flagged" (被标记) covers notices and stops together |

## Critical thinking

| Term | 中文 | Meaning |
|---|---|---|
| offloading → deferral → cognitive surrender | 委托 → 依赖 → 放弃判断 | Addy Osmani's slide across many handoffs: the output becomes your "known" without an update step |
| theory → measured → consistent? → mechanism | 理论预期 → 实测 → 是否一致 → 机理 | An empirical research practice, recorded in the 4.x skill `theory-vs-result`; in 6.0, one row of `fu:after` |
