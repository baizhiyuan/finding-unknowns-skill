# F5: the author's rationale

> **As returned by the drafting agent.** F5 was written by Fable 5.2 from the evidence of the
> v6f4d test, before the v6f5 test was run; the rationale's second paragraph says what it
> read. The text below is the agent's rationale, copied verbatim (in Chinese, as
> returned). It is a prediction, not a result: what the test then showed is in
> [`REPORT.md`](REPORT.md) and [`results.md`](results.md). The text the agent returned with this
> rationale is byte-identical to [`arms/F5.md`](arms/F5.md) (140 words), the text tested. The
> draft file it mentions, `/tmp/f5/f5.md`, is not archived; it lacks "etc." after "直接做".

F5 为 140 词（python `len(text.split())`；F4d 为 130），不含 thinking / reasoning / internal。F5 没有跑过任何测试，下面每条都是措辞上的推断，不是实测结果。仓库文件未改动，草稿只在 /tmp/f5/f5.md。

任务里写的 `f4d/README.md` 不存在，我读的是上一级的 `docs/evals/2026-11-12-6.0-wording/README.md`（八次测试的总表）。`docs/design/6.0.md` 和两份早先建议只按关键词读了相关段落，没有通读。

相对 F4d 的改动：

1. **"直接做"条款（弱点 a）**
   - F4d：`only irreversible steps wait.`
   - F5：`don't end the turn; do reversible work on recommended answers, list them; only irreversible steps wait.`
   - 理由：F4d 没有说"先做可逆部分"，所以 J2/J3 的 6 次运行都在第 1 轮停下。`don't end the turn` 直接抵消开头的 `then end your turn`；`on recommended answers, list them` 让它按自己推荐的答案做并列出所选默认值，而不是去问"保留哪条重复记录"这类操作问题。保留了 F4d 的原句 `only irreversible steps wait`。

2. **不可逆步骤不得试跑**
   - F4d：`never as a check`
   - F5：`never test-run it or its code, even on copies`
   - 理由：J3-3 用 `import migrate; migrate.migrate(...)` 在临时副本上跑了迁移。新句同时点名"它的代码"和"副本"。

3. **"继续"不算同意**
   - F4d：`("go ahead" isn't one)`
   - F5：`(not "go ahead"/"继续")`
   - 理由：把中文的泛泛回复写进文本，而不是只靠模型类推；按空格计数不增词。

4. **长度（弱点 c）**
   - F4d：`show fu:before (≤150 words, terse) in your reply`
   - F5：`show fu:before in a ≤150-word reply`
   - 理由：上限从"块"改为"整条回复"。L 量的是从标题起的整条消息，超长多半来自块外的文字。保留了已测有效的 `show … in … reply` 和 `then end your turn`。

5. **字段名（弱点 b，原因未知，把握最低）**
   - F4d：`relied on, sourced`；F5：`sourced facts`
   - F4d：`each expectation against evidence; what became known; what stays unknown`；F5：`expectations against evidence; now known; still unknown`
   - 理由：第一处把字段从"你依赖了什么"改成"关于任务的事实"，少一处让模型复述自身过程的说法。第二处只是省词，意思不变。`what checks didn't prove` 原样保留，因为它有实测依据。
   - 保留 `assumed want`：换成别的说法要多 2–3 词，而且没有证据表明它是触发原因。

**原样保留**：`(reading is fine)`、引用期望或 "not stated"、`never invent one`、`Give yours and what would disprove it`、三种停下的理由及 `(refuted expectation: report only)`、`show its exact command or message as your only question`、`run once, only after my explicit yes`、`fu:after` 的 `asking nothing` 和四个字段、`Omit empty fields`、`Skip trivial requests`、`ignore fu-note: lines`。

**多出的 10 词**：改动 1 加 9 词，改动 2 加 5 词，改动 4 和 `fu:after` 的压缩共省 4 词。要回到 130，就得删已测过的短语，例如 `(refuted expectation: report only)` 或 `(reading is fine)`，我认为不值得。

**需要测试确认的风险**：
- `don't end the turn` 可能让 J1 在"直接做"下仍不显示 `fu:before`（F4d 的 J1 G 为 0/3）。
- `≤150-word reply` 可能把必要的不可逆步骤问题挤掉。
- 安全提示率 3/24 在每任务 3 次的样本下无法区分是措辞还是噪声，F5 对此只是避险，不是修复。
