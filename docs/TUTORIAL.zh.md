# 5 分钟教程

本教程用一张任务卡走完全程：简报、一次打断、下一次会话中的回顾，以及完成报告。[English](TUTORIAL.md)

> **以下是示意，不是真实会话的记录。** 任务、数字和回复都是为说明结构而编写的，任务卡本身能通过 `fu lint`。你实际看到的措辞会有所不同，需要核对的是结构。这套流程对人是否有帮助，目前尚未检验（见 [README](../README.zh.md#评测结论56-个词有效插件没有胜出)）。如果你只想养成这个习惯，[`CLAUDE.md`](../CLAUDE.md) 中的 56 个词就是经过评测的配置，无需安装任何东西。

代码块中的命令和输出保留英文原文，以便与英文教程和任务卡模板对照；你也可以直接用中文提问。

## 1. 安装（1 分钟）

v5.2.0 发布之前，请从 `v5` 分支安装 5.2（插件市场目前提供的仍是 v4.3.2）：

```bash
git clone https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill && git checkout v5 && bash install.sh
```

正式发布后，也可以通过插件安装，这种方式会同时装上防护钩子：

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
```

```
/plugin install finding-unknowns@finding-unknowns-skill
```

安装后你会得到一个技能、一个子代理（`mechanism-auditor`）、fu 脚本和四个命令：`/fu-brief`、`/fu-catch-up`、`/fu-debrief` 和 `/fu-view`。脚本需要 `python3`。

## 2. 简报（2 分钟）

任务：一个每晚运行的作业把 `orders` 表导出为 CSV，每批 10,000 行。作业一旦崩溃就会从头重跑，你希望它能从中断处继续。

```
/fu-brief make the nightly order export resumable after a crash; I'd like to learn this part
```

智能体先静默阅读仓库，然后**只发一条**消息，最多三个问题。请你预测的那个问题不附任何参考答案，以免影响你的判断；只能由你决定的事则附上推荐答案，措辞让你回答“是”即可采纳：

```
1. If the export crashes halfway and resumes, how long will the resumed run take,
   compared with today's full run? Confidence: low, medium, high, or no idea.
2. Where should the checkpoint live? A local file next to the CSV, or a row in the
   database. Recommendation: the local file (easiest to undo). Yes?
```

你回答：“完整跑一次大约 6 分钟，所以续跑大约 3 分钟，把握中等。第二个问题同意。”你的原话会照录在任务卡上，第二个问题的答复写入 `.finding-unknowns/decisions.md`，以后不会再问。直到这时，智能体才写下它自己的预测。它把简报完整展示出来，最后只问一次是否同意（附上待定事项；因为你可能会中途离开再回来，还会顺带询问是否需要 HTML 视图）。你同意后，`fu freeze` 提交任务卡：

```
# export-resumable
Goal: a crashed nightly export resumes where it stopped · State: building
Needs you: nothing
Mode: learn · Last seen by you: never
Timing: Brief frozen 2026-11-12 09:10, commit 3f9c2ab

## Brief (frozen 2026-11-12 09:10)
Approach:
  - checkpoint the last exported (created_at, id) after each batch because the job already writes in batches
  - keep the checkpoint in a local file because you chose the most reversible place
P1 (you · medium) "a full run is about 6 minutes, so resuming from halfway takes roughly 3"
  - falsifier: resuming from halfway takes 6 min or more on the 5M-row fixture
  - should not change: an uninterrupted run's row count and checksum
A1 (agent · medium) "created_at repeats across batch boundaries, because the importer stamps a whole import with one time"
  - falsifier: no repeated created_at at any batch boundary in the fixture
  - should not change: rows with unique timestamps keep today's order
Stop-points: irreversible · scope · dead-premise · budget > 2× 1 h
C1 each row is exported exactly once after a crash
  - check: `pytest tests/test_export_resume.py -q` kills the job at 3 batch boundaries and compares ID sets with a full run
  - does NOT prove: a crash between writing a batch and writing its checkpoint
  - lane: reversible
Check files: tests/test_export_resume.py
```

P1 针对的是智能体无法控制的事情：数据库会怎样表现。“测试会通过”是智能体自己能做到的事，所以它属于验收标准（C1），并写明它不能证明什么。这份简报中没有不可逆操作，所以没有 `Irreversible:` 行；如果有，防护钩子会在那条确切命令执行前请你确认。

## 3. 一次打断（30 秒）

执行期间，智能体不会打扰你：每个小决定都在 `export-resumable.deltas.md` 中记一行，代你做出的决定还写明做错的代价。会话快结束时，智能体停了下来：

```
Stop (scope): resume from 50 % took 9 min 40 s on the fixture (D4); an index on
(created_at, id) brings it to 3 min 05 s, but that index is on production, outside the
Brief · `CREATE INDEX CONCURRENTLY orders_created_at_id ON orders (created_at, id);`
· recommend: run it in the next maintenance window
```

这个索引既超出了范围，又涉及生产环境，属于不可逆操作。它不在冻结的简报上，防护钩子没有可以匹配的行，所以智能体停下来，只有你在对话中明确同意这条命令，它才会执行。你回复：“现在不做，我周四维护窗口时自己跑。”这件事记入待办，没有执行。

## 4. 下一次会话：`/fu-catch-up`（30 秒）

```
/fu-catch-up
```

```
export-resumable · building
  - since you last looked: D1–D4 (checkpoint format, a lock retry, the fixture, the slow resume)
  - needs you: nothing; the production index is in Open for Thursday
```

你只会看到上次查看之后的变化，“上次查看”随之更新到 D4。除非你要求，不会有回忆性问题。

## 5. 完成报告即复盘（1 分钟）

工作完成时，完成报告就是复盘。你在确认简报时要求过由新上下文评判，所以由 `mechanism-auditor` 根据冻结的任务卡和产出文件评判；它看不到对话记录，也看不到执行者自己的判断。先列证据，再评你的预测：

```
Evidence:
  - `pytest tests/test_export_resume.py -q` → 3 passed
  - `bench/resume.sh` → 9:41, 9:22, 9:58
P1 (you · medium) "a full run is about 6 minutes, so resuming from halfway takes roughly 3"
  - measured: 9 min 40 s over 3 runs, ±20 s (logs/resume.txt)
  - consistent?: inconsistent
  - mechanism: each batch is a separate query that sorts the table, since no index matches the sort [verified]
A1 (agent · medium) "created_at repeats across batch boundaries, because the importer stamps a whole import with one time"
  - consistent?: consistent
Integrity:
  - Brief vs freeze: unchanged
  - Check files: unchanged
  - Unlogged hunks: none
Did NOT prove:
  - C1 kill tests → leaves open: a crash between a batch write and its checkpoint · still holds: no duplicates or gaps at 3 boundaries
Not checked:
  - the production row count and its existing indexes
Model changes:
  - You expected resuming from halfway to take half a full run → without an index it is slower than a full run, because each batch re-sorts the table [shown, not confirmed]
Bottom line:
  - holds: the checkpoint needs the id as well as created_at (A1)
  - did not hold: resuming from halfway is faster than a full run (P1)
  - stops at: the fixture; nothing ran on production
Needs you: the production index (recommendation: run it in Thursday's maintenance window; settles whether resume is fast in production)
```

一致的预测只占一行，解释只写在落空的预测上。因为你说过想学，落空的预测还附有简短的原因和一个例子：现在的作业通过一个游标把整张表读一遍，而可续传的作业对剩下 250 批中的每一批都要查询“这个键之后的行”；没有与排序匹配的索引，每次查询都要对全部 500 万行重新排序。

三行完整性检查由 `fu integrity` 生成；`fu log` 把每条评判过的预测写入你本地的预测记录；`fu freeze` 再次提交任务卡。你用自己的话复述这条认知修正后，它会标记为 `confirmed`。`/fu-view`（或你在简报时选择的 HTML 视图）会把同一张任务卡渲染成页面。

## 什么时候不用

改错字、一行改动不建任务卡，也不提问。确实没有什么可预测的任务，任务卡会如实写明；“这里没有值得预测的内容”本身就是有效的回答。

## 接下来

[README](../README.zh.md) · [术语表](GLOSSARY.md) · [架构](ARCHITECTURE.md) ·
[EXAMPLES.md](../EXAMPLES.md)（可复制的提示词） · [5.2 设计](design/5.2.md)
