# 5 分钟教程

用一张任务卡走完全程：简报、一次打断、下一次会话中的回顾，以及复盘。[English](TUTORIAL.md)

> **这是示意，不是真实会话的记录。** 任务、数字和输出都是为说明结构而编写的。你得到的措辞会不同，需要核对的是结构。这套流程是否对人有帮助，目前尚未检验（见 [README](../README.zh.md)）。

代码块中的命令和输出保留英文原文，与英文版教程和任务卡模板一致；你也可以直接用中文提问。

## 1. 安装（1 分钟）

在 Claude Code 中逐条输入：

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
```

```
/plugin install finding-unknowns@finding-unknowns-skill
```

安装后有一个技能、三个子代理和三个命令：`/brief-me`、`/catch-up`、`/debrief`。其他安装方式见 [README](../README.zh.md)。

## 2. 简报（2 分钟）

任务：一个每晚运行的作业把 `orders` 表按每批 10,000 行导出为 CSV。作业崩溃后会从头重跑，你希望它能从中断处续跑。

```
/brief-me make the nightly order export resumable after a crash
```

在一个项目中第一次使用时，智能体只问一次：`ship` 还是 `learn`。这里选 `learn`。随后，在阅读任何代码之前，它先请你做预测：

```
Before I look: if the export crashes halfway and resumes, how long will the resumed
run take, compared with today's full run? Give a confidence, or say "no idea".
```

你回答：“完整跑一次大约 6 分钟，所以大约 3 分钟。把握 70 %。”这就是你的先验预期。此后智能体才去摸清代码现状，报告与你的预期相矛盾之处，再给出它自己的预测。你确认之后，任务卡被冻结并提交到 git。节选如下：

```
# Make the nightly order export resumable
Goal: a crashed export resumes where it stopped · State: building
Next decision that needs you: none
Mode: learn · Last seen by you: 2026-11-12, at the Brief
Timing: Brief frozen 2026-11-12, commit 3f9c2ab

## Brief (frozen 2026-11-12)
Approach: checkpoint the last exported (created_at, id) after each batch, because the
  job already writes in batches
Your predictions:  P1 resuming at the halfway point takes about half of today's 6 min
  (70 %) · falsifier: resume ≥ 6 min on the 5M-row fixture · should not change: an
  uninterrupted run's row count and checksum
Agent predictions: A1 created_at repeats across batch boundaries; the importer stamps
  a whole import with one time (importer.py:88) · falsifier: no repeat at any boundary
  in the fixture · should not change: rows with unique timestamps keep today's order
Stop-points: irreversible action · scope change · dead premise · budget > 2× 1 h
Contract:
| claim | check (can fail) | does NOT prove | lane |
| each row exported exactly once after a crash | tests/test_export_resume.py kills the
  job at 3 batch boundaries, compares ID sets with a full run | a crash between writing
  a batch and writing its checkpoint | reversible |
```

P1 预测的是智能体无法控制的事情：数据库的实际表现。“测试会通过”是智能体自己能让它成立的事，所以它写在验收标准（Contract）里，并注明它**不能**证明什么。每条预测都带有证伪条件（falsifier）和“不应改变”的一半。

## 3. 一次打断（30 秒）

构建过程默认安静进行：小的取舍都记成任务卡上的一行增量记录。会话快结束时，智能体停了下来：

```
Stopped: scope change, production (irreversible lane).
D4 surprise: resume from 50 % took 9 min 40 s on the fixture (3 runs, ±20 s)
  → logs/export-resumable-resume.txt
No index matches ORDER BY created_at, id. With that index on the fixture: 3 min 05 s.
The fix is an index on production, outside the Brief. Run this yourself, or say yes
to this exact command:
  CREATE INDEX CONCURRENTLY orders_created_at_id ON orders (created_at, id);
Post-check: EXPLAIN on the batch query shows an Index Scan.
```

这里同时触发了两个打断点：改动超出简报范围，并且涉及生产环境，属于不可逆一类。智能体只准备好确切的命令，由你亲自执行，或者对这条具体命令说“可以”。你暂时离开了。生产环境上什么都没有执行，任务卡的状态是 `waiting on you`。

## 4. 下一次会话：`/catch-up`（1 分钟）

```
/catch-up
```

在展示任务卡之前，先提回忆问题（learn 模式两到三个；ship 模式一个，可以跳过）：

```
1. What does the checkpoint store, and why not created_at alone?
2. Your P1 expected about 3 minutes; the resume took longer than a full run.
   Where would you look first?
```

也可以用两句话复述来代替回答。这里没有及格线。之后你只会看到上次查看以来的变化：增量记录 D1 到 D4，以及需要你做的下一个决定，也就是那个索引。你回复：“现在不做，我会在周四的维护窗口执行。”这一项进入 Open，没有执行，“Last seen” 更新到 D4。

## 5. `/debrief`（1 分钟）

```
/debrief
```

这一步是新上下文评判：`mechanism-auditor` 拿到冻结的任务卡和产物路径，而不是构建过程的对话记录。它先评判你的预测：

```
Evidence: `pytest tests/test_export_resume.py -q` → 3 passed · `bench/resume.sh` →
  9:41, 9:22, 9:58
Graded by: fresh context.

| ID | Prediction (quoted) | Measured | Consistent? | Mechanism [tier] |
|----|---------------------|----------|-------------|------------------|
| P1 | "resuming at the halfway point takes about half of today's 6 min" | 9 min 40 s, 3 runs ±20 s; full-run checksum unchanged | inconsistent; should-not-change half held | each batch is its own query and sorts the table [verified: with the index, 3 min 05 s] |
| A1 | "created_at repeats across batch boundaries" | at 37 of 499 boundaries | consistent | one timestamp per import [supported] |

Why P1 missed: today's job reads the table once, through one cursor. A resumable job
asks "rows after this key" for every batch; with no index matching the sort, each of
the 250 remaining queries scans and sorts all 5M rows. Resuming skips batches, but each
batch became far more expensive.

Did NOT prove: a crash between a batch write and its checkpoint; the resume test was
  written in the same context as the code
Not checked: the production row count and its existing indexes
Model changes: you expected resume ≈ half a full run → without the index it is slower
  than a full run, because each batch re-sorts the table [shown, not confirmed]
Bottom line: resume is correct (no duplicates or gaps in 3 kill tests) and slow until
  the index exists.
Needs you: the production index (Open)
```

表格按“理论预期 → 实测 → 是否一致 → 机理”的顺序读。P1 的结论是不一致，A1 是一致；机理分别标为已验证和有数据支持。P1 为什么没猜中：原来的作业用一个游标把整张表读一遍；可续跑的作业每一批都要单独查询“这个键之后的行”，而没有与排序匹配的索引时，剩下的 250 次查询每次都要扫描并排序全部 500 万行。续跑省掉了一半批次，但每一批都变贵了很多。

解释写在没猜中的那一行上，而不是事先讲一大段。每条被评判的预测都会在你个人的预测日志里追加一行，任务卡再次提交。用你自己的话复述这条模型变化（Model changes），它的状态就从 `shown, not confirmed` 变为 `confirmed`。

## 什么时候不用

改错字、一行改动，以及你本来就会直接做的事：不建任务卡，也不提问。没有任何可如实预测内容的任务，任务卡会写明 “No real prediction here; contract only”。

## 下一步

[README](../README.zh.md) · [术语表](GLOSSARY.md)（英文） · [架构](ARCHITECTURE.md)（英文） ·
[EXAMPLES.md](../EXAMPLES.md)（可复制的提示词，英文） · [5.0 设计](design/5.0.md)（英文）
