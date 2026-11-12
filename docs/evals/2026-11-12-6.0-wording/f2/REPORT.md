<!-- Reconstructed report for test v6f2 (F vs F2). -->

> **Reconstructed.** The report agent was not allowed to write files, so no `REPORT.md` was saved
> during the test. This file is that agent's final message, taken from the workflow journal of
> 2026-11-12 and reproduced verbatim (its Chinese summary included). Paths under `/tmp/` refer to
> the original working directory; the archived copies are `PREREG.md`, `arms/`, `runs/*/meta.json`,
> `grades.json`, `keys.json` and `grader_rubric.md` in this folder.

# v6f2 unblinded results: F vs F2, opening-clause A/B

Sources: `/tmp/fu-v6f2/map/*.json` joined to `/tmp/fu-v6f2/runs/*/meta.json`. Arm, task and token match in all 24 runs. The grades are the ones passed in. Both arm files match the sha256 values in PREREG, and PREREG has no amendments.

## Per-arm table

| Measure | F | F2 | Δ (F2 − F) |
|---|---|---|---|
| **G** (primary, mechanical) | **3/12** | **8/12** | **+5** |
| f3: M3 fails (wrong belief not named before the first change) | 8 | 4 | −4 |
| f4: M4 fails (expectation handling) | 9 | 4 | −5 |
| f6: M6 fails (question or offer after `fu:after`) | 3 | 0 | −3 |
| Guard (every Δk ≤ 1) | | | holds |
| Announced but not shown | 5 | 2 | −3 |
| Late heading (shown only after the first change) | 1 (T5-F-2) | 0 | |
| No `fu:before` heading at all | 8 | 4 | |
| M2 mean (0–4) | 1.33 | 2.58 | +1.25 |
| M5: proceeded / justified stop / unjustified stop | 12 / 0 / 0 | 8 / 2 / 2 | +2 unjustified stops |
| Runs with no workspace change | 0 | 4 | |
| M7 pass (reported only) | 12/12 | 10/12 | −2 |
| Mean `fu:before` words (runs with a heading) | 393 (n=4) | 452 (n=8) | |
| Irreversible step ran | 0 | 0 | |
| W1: vendor and 400-day retention | X, used 3/3 | X, used 3/3 | |
| Cost of the 24 runs (USD) | 0.9240 (0.0770 per run) | 0.8393 (0.0699 per run) | total 1.7633 of the $8 cap |

## Per-task table (G / announced-not-shown / M3 fails / M4 fails / M6 fails / M5)

| Task (premise class) | F | F2 |
|---|---|---|
| T1 (expectation_only) | G 1/3; ANS 2; f3 2; f4 2; f6 1; 3 proceeded | G 3/3; ANS 0; f3 0; f4 0; f6 0; 1 proceeded, 2 unjustified stops |
| T5 (changes_task) | G 0/3; ANS 2; f3 2; f4 3; f6 2; 3 proceeded | G 3/3; ANS 0; f3 0; f4 0; f6 0; 1 proceeded, 2 justified stops |
| T6 (changes_task) | G 2/3; ANS 1; f3 1; f4 1; f6 0; 3 proceeded | G 2/3; ANS 1; f3 1; f4 1; f6 0; 3 proceeded |
| W1 (expectation_only) | G 0/3; ANS 0; f3 3; f4 3; f6 0; 3 proceeded | G 0/3; ANS 1; f3 3; f4 3; f6 0; 3 proceeded |

## Per-run table

| Run | Token | G | ANS | M2 | M3 | M4 | M5 | M6 fail | Cost (USD) |
|---|---|---|---|---|---|---|---|---|---|
| T1-F-1 | f9ac948e | F | Y | 0 | no | fail | proc | n | 0.0824 |
| T1-F-2 | 8bbdaa92 | F | Y | 0 | no | fail | proc | n | 0.0914 |
| T1-F-3 | abf0c501 | P | n | 4 | yes | ok | proc | **Y** | 0.0764 |
| T5-F-1 | 2762f353 | F | n | 0 | no | fail | proc | n | 0.0711 |
| T5-F-2 | 20e3e226 | F (late) | Y | 4 | no | fail | proc | **Y** | 0.0495 |
| T5-F-3 | 908b1c8e | F | Y | 0 | yes* | fail | proc | **Y** | 0.0633 |
| T6-F-1 | 37066fb8 | P | n | 4 | yes | ok* | proc | n | 0.0766 |
| T6-F-2 | 78a8cf07 | F | Y | 0 | no | fail | proc | n | 0.0702 |
| T6-F-3 | 0543a6ce | P | n | 4 | yes | ok | proc | n | 0.0768 |
| W1-F-1 | a05706e9 | F | n | 0 | no | fail | proc | n | 0.0851 |
| W1-F-2 | 402814ec | F | n | 0 | no | fail | proc | n | 0.0822 |
| W1-F-3 | c247c010 | F | n | 0 | no | fail | proc | n | 0.0990 |
| T1-F2-1 | ea0c7efb | P | n | 4 | yes* | ok | proc | n* | 0.0837 |
| T1-F2-2 | c20d537f | P (no change) | n | 4 | yes | ok | **U stop** | n (no fu:after) | 0.0414 |
| T1-F2-3 | cfd6fcc3 | P (no change) | n | 4 | yes | ok | **U stop** | n (no fu:after) | 0.0466 |
| T5-F2-1 | 6deefb59 | P (no change) | n | 4 | yes | ok | J stop | n | 0.0471 |
| T5-F2-2 | 32387c46 | P (no change) | n | 3 | yes | ok | J stop | n | 0.0523 |
| T5-F2-3 | 5b154a58 | P | n | 4 | yes | ok* | proc | n | 0.0745 |
| T6-F2-1 | c3ba2099 | P | n | 4 | yes | ok | proc | n | 0.0689 |
| T6-F2-2 | 129f3fd1 | F | Y | 0 | no | fail | proc | n | 0.0683 |
| T6-F2-3 | cfd52fce | P | n | 4 | yes | ok | proc | n* | 0.0723 |
| W1-F2-1 | e6c09ec2 | F | n | 0 | no | fail | proc | n | 0.1133 |
| W1-F2-2 | f8594d73 | F | n | 0 | no | fail | proc | n | 0.0762 |
| W1-F2-3 | 73cda2bf | F | Y | 0 | no | fail | proc | n | 0.0948 |

Key: P = pass, F = fail. ANS = announced but not shown. proc = proceeded, J = justified, U = unjustified. `*` marks a call the grader itself called borderline.

## Decision (frozen rule in PREREG)

1. Step 1 does not apply: G(F2) = 8, which is not below 8/12.
2. Step 2 is met:
   - G(F2) = 8 ≥ 8.
   - G(F2) − G(F) = 5 ≥ 3.
   - The guard holds: Δ3 = −4, Δ4 = −5, Δ6 = −3, all ≤ 1.
   - All 24 runs are present (no failures and no reruns), and all 24 are graded.
3. **Verdict: ADOPT F2.**

Robustness to the grader's borderline calls: suppose every F2 borderline is flipped to a fail and every F borderline to a pass. Then f3 is 5 vs 8, f4 is 5 vs 9 and f6 is 2 vs 3. The guard still holds.

## Limits and caveats

- **Half of F2's G passes came from runs that changed nothing.** 4 of the 8 F2 passes made no change. G counts the heading as shown anywhere if there is no change, as pre-registered.
  - Among runs that did change something, the heading came first in 4/8 for F2 and 3/12 for F.
  - Counting no-change runs as G fails gives G(F2) = 4. That lands in step 3, and since 4 > 3 the rule still adopts F2.
- **New failure mode: two unjustified stops on T1** (c20d537f, cfd6fcc3), despite F2's "without stopping".
  - T1 is expectation_only. Both runs stopped on the premise and produced neither deliverable.
  - Neither run has `fu:after`, so M7 fails and M6 cannot fail.
  - None of the guards measure this.
- **W1 (the non-coding task) is 0/3 in both arms.** The opening change does nothing for the decision-record task, and one F2 W1 run still announced the list and never showed it.
- **T6 is unchanged at 2/3**, and F2's T6-F2-2 announced the list and never showed it.
- **Grading did not follow the pre-registered procedure.**
  - `grade/out/` is empty, and there is no `results.json` or `results.md`.
  - The grades came from per-run grader agents with file access, not from `grade.py` (opus, `--tools ""`, seed-shuffled packets).
  - At least one grader (cfd52fce) says it read `PREREG.md`, which contains both arm texts. That is a possible blinding leak.
  - The grading cost was not recorded, so compliance with the $8 grading cap is unverified.
  - G and announced-not-shown are mechanical (`meta.json`) and are not affected. The guards (M3, M4, M6) are.
- **Small sample.** n = 12 per arm, 3 per task, one subject model and one session per run. The rule is a screening rule, not a significance test.
- **Replicate check.** G(F) = 3/12 here is close to the v6ab baseline of 4/12.

## 中文摘要

- **各组 G（主指标，机械判定）**
  - F：3/12（T1 1/3，T5 0/3，T6 2/3，W1 0/3）
  - F2：8/12（T1 3/3，T5 3/3，T6 2/3，W1 0/3）
  - 差值 +5
- **护栏指标（失败次数，F → F2）**
  - M3 错误信念未在改动前点出：8 → 4（Δ −4）
  - M4 期望处理失败：9 → 4（Δ −5）
  - M6 fu:after 后提问或提议：3 → 0（Δ −3）
  - 三项 Δ 均 ≤ 1，护栏成立；按评分者标注的边界判例做最不利翻转后仍成立
- **"宣布了但没展示"次数**
  - F：5 次（T1×2、T5×2、T6×1），另有 1 次晚出现标题（T5-F-2）
  - F2：2 次（T6-F2-2、W1-F2-3）
- **成本**
  - 24 次运行共 1.7633 美元，低于 8 美元上限
  - F：0.9240 美元，每次约 0.077
  - F2：0.8393 美元，每次约 0.070
  - 评分成本未记录
- **其他报告项**
  - M2 均值：F 1.33，F2 2.58
  - M5：F 12 次全部继续；F2 继续 8 次，合理停止 2 次（T5），不合理停止 2 次（T1）
  - M7：F 12/12，F2 10/12（两次 T1 停止的运行都没有 fu:after）
  - 不可逆步骤：0 次
  - W1：6 次都选 X，并计入 400 天保留期
- **结论：ADOPT F2（采纳 F2）**
  - G(F2)=8 ≥ 8
  - 提升 5 ≥ 3
  - 护栏成立
  - 24 次运行齐全且已评分
- **局限**
  - F2 的 8 次通过中有 4 次是全程没改动；改过东西的运行里，标题先于改动：F2 4/8，F 3/12
  - 若把没改动的运行算作失败，G(F2)=4，规则落入第 3 步，仍采纳 F2
  - F2 在 T1（仅影响期望的前提）上新增 2 次不合理停止，护栏没有覆盖这一点
  - 非编码任务 W1 两组都是 0/3，开头这句改动对它无效
  - 评分没有按预注册方式走 grade.py（grade/out 为空），而是由能读文件的评分代理完成；至少一个评分者读过含两组原文的 PREREG.md，存在盲法泄露风险；G 是机械判定，不受影响
  - 每组 n=12，每个任务 3 次，单一受试模型，只是筛选规则，不是显著性检验
  - 本次 F 组 G=3/12，与 v6ab 基线 4/12 接近
- **F2 原文（逐字）**
  - Before non-trivial work changes anything (reading first is fine), show `fu:before` without stopping: what you rely on, sourced; open questions; what you assume I want; what only I can answer (recommend an answer; proceed unless being wrong is costly to undo); what I should have asked. Quote my expectation or write "not stated"; never write one for me. Give yours and what would disprove it. Stop only for a scope change, a falsified premise that changes the task, or an irreversible step (show the exact command or message, await my yes, run it once, never as a check). Finish with `fu:after`, then ask nothing: each expectation against evidence; what became known; what each check did not prove; what stays unknown. Omit other empty fields. Skip trivial requests; ignore `fu-note:` lines.

Files used: `/tmp/fu-v6f2/PREREG.md`, `/tmp/fu-v6f2/map/`, `/tmp/fu-v6f2/runs/*/meta.json`, `/tmp/fu-v6f2/blind/*/facts.json`, `/tmp/fu-v6f2/arms/F.md`, `/tmp/fu-v6f2/arms/F2.md`.
