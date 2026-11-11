<p align="center">
  <img src="assets/zh/hero.svg" alt="finding-unknowns v5.0.0：每个任务一张任务卡。你先预测，智能体安静地执行，只在四种情况下打断你；完成后由新上下文评判预测。" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-D97757?style=for-the-badge&labelColor=F0EEE6" alt="Claude Code 插件">
  <img src="https://img.shields.io/badge/version-5.0.0-C15F3C?style=for-the-badge&labelColor=F0EEE6" alt="版本 5.0.0">
  <img src="https://img.shields.io/badge/skills-1-D4A27F?style=for-the-badge&labelColor=F0EEE6" alt="1 个技能">
  <img src="https://img.shields.io/badge/agents-5-C15F3C?style=for-the-badge&labelColor=F0EEE6" alt="5 个子代理">
  <img src="https://img.shields.io/badge/license-MIT-788C5D?style=for-the-badge&labelColor=F0EEE6" alt="MIT 许可证">
</p>

<p align="center"><strong>让智能体替你干活时，你仍是这项工作的主人：知道在做什么，预先判断会发生什么，看清现实在哪里偏离了预期。</strong></p>

<p align="center">
  <a href="#快速开始">快速开始</a> ·
  <a href="#工作原理">工作原理</a> ·
  <a href="#命令">命令</a> ·
  <a href="#文档">文档</a> ·
  <a href="README.md">English</a>
</p>

<p align="center"><em>本文是英文 README 的中文版；如有出入，以英文版为准。</em></p>

---

## 快速开始

通过插件市场安装。以下是 Claude Code 的斜杠命令，请**逐条**输入：

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
```

```
/plugin install finding-unknowns@finding-unknowns-skill
```

也可以克隆仓库后运行 `install.sh`，它会安装技能及其参考文件、三个子代理和三个命令：

```bash
git clone https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill && bash install.sh
```

不想安装？把 [`CLAUDE.md`](CLAUDE.md) 复制到项目根目录，即可使用常驻的精简版。

**初次使用：**

```
/fu-brief "让导出任务支持断点续传"   # 你先预测，再查现场，智能体随后预测；你确认后冻结
/fu-catch-up                        # 下次会话：先回忆，再看有哪些变化
/fu-debrief                         # 逐条评判预测，指出你的认知需要哪些修正
```

[5 分钟教程](docs/TUTORIAL.zh.md)用一张任务卡，从简报一直走到复盘。

### 更新

下一个版本为 **v5.0.0**，正式发布取决于第 0 阶段评测的结果；当前发布版本为 v4.3.2。用安装时的方式更新：

```
/plugin marketplace update finding-unknowns-skill
```

```
/plugin update finding-unknowns@finding-unknowns-skill
```

<details>
<summary><b>克隆安装、从 4.x 升级与版本核对</b></summary>

`install.sh` 会原地覆盖，并删除它能确认属于本项目的 4.x 文件（Cartographer、Workflow 模板、keep-the-reasoning、theory-vs-result、ledger-keeper、prototype-smith 以及旧命令）：

```bash
cd finding-unknowns-skill && git pull origin main && bash install.sh
```

4.x 仍可从 `v4.3.2` 标签获取。各部分在 5.0 中的去向见[设计文档第 11 节](docs/design/5.0.md#11-migration-for-4x-users)。

```bash
grep -h '"version"' ~/.claude/plugins/cache/finding-unknowns-skill/finding-unknowns/*/.claude-plugin/plugin.json 2>/dev/null \
  || ls ~/.claude/skills/finding-unknowns/references/card.md
# 预期：5.0.0（插件方式），或列出 card 参考文件
```

</details>

---

## 为什么选择 finding-unknowns？

工作交给智能体之后，人很容易不再清楚到底发生了什么：一份只扫了一眼的改动被批准，长任务慢慢偏离本意，结果成了你的，里面却没有你的判断。Addy Osmani 把这个过程称为**委托 → 依赖 → 放弃判断**。“放弃判断”（cognitive surrender）一说出自 Shaw 与 Nave 的 _Thinking—Fast, Slow, and Artificial_（SSRN 6097646）；另见 Margaret-Anne Storey 关于认知债务的论述。

本插件为每个任务维护一张由你和智能体共用的**任务卡**：

- **动手之前：** 你先写下自己的预期，智能体再摸清现场，然后才给出它的预测。你的预测在看到智能体的预测之前就记录下来。
- **执行期间：** 智能体只在四个可核对的打断点停下来，其余情况都记在任务卡上，你想看时再看。
- **完成之后：** 由未参与执行的上下文逐条评判预测。你会看到哪些预测成立、检查没有证明什么，以及你的认知需要哪些修正。

任务卡是一个文件，可以跨会话保留。这一点对长任务和科研最重要，因为结果往往要过好几天才陆续出来。

> **致谢。** 探索未知项的方法来自 Thariq Shihipar 的文章 _"A Field Guide to Fable: Finding Your Unknowns"_（[@trq212](https://x.com/trq212/status/2073100352921215386)）。交付复核，包括"检查没有证明什么"，来自 Addy Osmani 的 _"Critical thinking when agents do the work"_（[原文](https://x.com/addyosmani/status/2117512471930167377)）。理论预期 → 实测 → 是否一致 → 机理，来自作者本人的科研实践。

### 评测结果

三次预注册、盲评的评测（[docs/evals](docs/evals/)）检验了 4.x 技能能否让当前模型在单轮任务中发现更多预埋的陷阱：

- **没有经得起复现的提升。** 基线本来就能发现 25 个陷阱中的 22 到 23 个。
- **成本可测：** 输入 token 或费用约增加 10 % 到 70 %，回答更长；对 Sonnet 而言，细小的错误陈述也更多。
- **只有一个窄效应，且只见于 Sonnet：** 在合并问题上运行 keep-the-reasoning 技能时，Sonnet 在 5 次中有 4 次指出“测试通过”只依赖一个会自我更新的快照测试，未运行该技能时 12 次中只有 1 次。这是事后才发现的，只能算线索，不能算结论。

5.0 围绕这些评测从未测量过的一面重建：**你**的理解与决策（[设计文档](docs/design/5.0.md)）。它能否真正帮到人，**目前尚未验证**。下一步先做模拟用户评测，并预注册淘汰规则，由它决定 5.0 是否发布；之后再请真人参与研究。在此之前，请把它当作一种工作方式，而不是已被证实的改进。

---

## 工作原理

<p align="center"><img src="assets/zh/lifecycle.svg" alt="围绕一张任务卡的三个时刻：动手前的简报、安静的执行、完成后的复盘，以及回来时的回顾" width="100%"></p>

`/fu-brief` 冻结任务卡，执行期间只在四个打断点停下，`/fu-catch-up` 帮你在新会话里重新进入状态，`/fu-debrief` 评判冻结的预测。

### 架构

<p align="center"><img src="assets/zh/framework.svg" alt="命令、技能及其参考文件、五个子代理、磁盘上的文件与原则" width="100%"></p>

四个命令进入同一个技能。`SKILL.md` 只放每个时刻都需要的内容（任务卡、打断点、常驻规则），其余内容都是参考文件，到了对应时刻才加载。结构化模式是单独的一层，你不要求就不会加载。

### 四类未知

<p align="center"><img src="assets/zh/quadrants.svg" alt="四类未知及各自对应的方法" width="100%"></p>

简报先判断缺口属于哪一类，因为每一类需要不同的方法：

- **已知的已知**写在你的需求里，风险在于一直没写明，所以要先记下来。
- **已知的未知**是你能说出口的问题；智能体会先问影响架构的问题，代码里能查到的从不问你。
- **未知的已知**是你一看就知道、却说不清的偏好；几个真正不同的方向或一份参考实现，能把它变成明确的标准。
- **未知的未知**是盲区；只读的盲区排查会找出潜在风险、隐含约束，以及行家会问的问题。

### 任务卡

<p align="center"><img src="assets/zh/card.svg" alt="任务卡的结构：页头、冻结的简报、修订、增量记录、认知修正、待办、复盘" width="100%"></p>

任务卡位于 `.finding-unknowns/tasks/{slug}.md`，默认提交到 git，用提交记录证明预测写在结果之前。卡上包括：

- 页头：目标、当前状态、需要你做的下一个决定；
- **冻结的简报：** 做法及理由；你和智能体各自的预测，每条都带反证条件和“不应改变的部分”；打断点；验收标准（每项检查，以及它**不能**证明什么）；
- **修订：** 写明日期、只追加。简报本身从不修改，每条原始预测都照样评判；
- **增量记录：** 每条偏离、意外或代你做的决定各记一行；
- **认知修正：** “你原以为 X，实际是 Y，因为 Z”；
- **待办事项**，最后是**复盘**。

预测针对的是智能体控制不了的事：问题出在哪里、会影响多少调用方、基准测试的数字。“测试会通过”属于验收检查，不是预测。很多任务确实没有可预测的内容，任务卡会如实写明。

### 四个打断点

<p align="center"><img src="assets/zh/stop-points.svg" alt="四个打断点及各自的处理方式；其余情况记录在案，工作继续" width="100%"></p>

只有出现以下情况之一，智能体才会停下来找你：

1. **不可逆操作：** 删除或改写数据、生产环境、资金、对外发布、对他人的承诺。智能体准备好确切的命令，由你执行，或者你明确同意执行这一条命令。
2. **范围变化。**
3. **前提失效**，并且已经没有可逆的退路。
4. **预算超支：** 超出你们约定的倍数。

其余情况一律选择最容易撤回的做法，并记在任务卡上。

### 复盘

<p align="center"><img src="assets/zh/debrief.svg" alt="复盘：输入、新上下文评判的三个步骤，以及你在一屏内看到的内容" width="100%"></p>

- **引用而不复述：** 每条预测都按编号原文引用自冻结的任务卡。
- **由新上下文评判：** `mechanism-auditor` 只看任务卡和产出文件，不看执行过程，并且先评你的预测。
- **在出错处讲解：** 讲解放在预测落空的那几行。
- **证据在前：** 实际运行的命令及其输出、每项检查没有证明什么、哪些内容没有人检查过。
- **默认一屏**，需要时再展开细节。

### 实测结果

基准测试、回测、A/B 测试和模型训练使用**理论预期 → 实测 → 是否一致 → 机理**：

- **预测：** 在看数据之前写好，附停止规则，噪声底至少用三次重复运行测出。
- **运行记录表：** 几天内陆续出来的结果记入运行记录表，满足停止规则之前不下结论。
- **两种结论：** 规则结论按预先约定的规则机械判定；这个思路是否还值得继续，由你来判断。

### 学习

- **你先预测：** `ship` 模式下只问一个可以跳过的问题，`learn` 模式下最多三个。
- **讲解跟着你的失误走：** 讲解放在你预测落空的地方，而不是开头先上一堂课。
- **`/fu-catch-up` 里先回忆：** 在你看到任务卡之前，`ship` 模式问一个可以跳过的回忆性问题，`learn` 模式问两到三个，不设及格线。
- **预测记录：** 你的命中率会持续记录下来，只供你本人查看，不提交到仓库。

### 结构化模式（可选）

<p align="center"><img src="assets/zh/cartographer.svg" alt="结构化模式：Cartographer，带台账、六项闸门条件与规格的覆盖式循环" width="100%"></p>

对高风险任务，或者你希望每一步都写明（这可能对较小的模型有帮助），可以用 `/fu-brief --structured` 或 `/fu-cartographer`，在任务卡之上加上 4.x 的完整流程：

- **四象限路由**与八种编号方法（盲区排查、原型、访谈、参考、计划、实施记录、说明、测验）。
- **Cartographer：** 每个未知项都成为台账中的一条，带先验、风险值（代价 × 出错概率）、处理途径和可逆性分级。每轮显示清晰度，方便你掌控方向；六项闸门条件决定何时可以开工；带验收标准的规格成为任务卡的简报。
- **完整交付包：** 按风险分级，九个部分，证据在前。

任务卡、四个打断点和新上下文评判照常适用。

---

## 命令

| 命令 | 作用 |
|---|---|
| `/fu-brief <任务>` | 先记下你的预测，再摸清现场，然后给出智能体的预测；约定打断点和验收标准；冻结并提交任务卡 |
| `/fu-catch-up [slug]` | 先问回忆性问题，再只显示你上次查看之后的变化，以及需要你做的下一个决定 |
| `/fu-debrief [slug]` | 由新上下文评判每条冻结的预测；列出证据、检查没有证明什么、你的认知修正 |
| `/fu-cartographer <任务>` | 高风险任务的结构化模式：在任务卡之上运行 Cartographer 台账、闸门与规格 |

直接说“brief me”“catch me up”“where were we”或“did it match what we expected”也可以。在非交互的 `claude -p` 中请使用完整名称（`/finding-unknowns:fu-brief`）。改错字、一行改动之类的小事不会建任务卡，也不会提问。

| 子代理 | 职责 |
|---|---|
| `blindspot-scout` | 为简报做只读侦察：潜在风险、隐含背景、改写后的需求 |
| `mechanism-auditor` | 复盘和实测结果的新上下文评判者 |
| `quiz-master` | 可选：为 `/fu-catch-up` 起草回忆性问题，并标出没有任何增量记录能解释的改动 |
| `ledger-keeper` | 结构化模式：维护 Cartographer 台账、评分与闸门结论 |
| `prototype-smith` | 为“一看就知道”的偏好做几个真正不同的一次性方向（简报、结构化模式） |

---

## 设计札记

- **为什么 5.0 是一次重建。** 三次评测把 4.x 技能当作提升模型输出的工具来测，没有发现可复现的提升。作者的目标一直在人这一侧，所以 5.0 围绕它来组织。设计、两份顾问意见，以及 5.0 在哪些地方没有采纳顾问意见：[docs/design/5.0.md](docs/design/5.0.md)。
- **哪些内容挪了位置。** Cartographer（风险值、清晰度显示、六项闸门条件）、八种编号方法和九段交付包不再是默认流程，而是保留为**结构化模式**，只在你要求时加载。较小的模型可能需要前沿模型用不上的明确步骤（这一点仍在验证）。Workflow 执行和“必须通过”的测验已删除。keep-the-reasoning 和 theory-vs-result 并入了唯一的技能。
- **出于设计考虑保留了什么。** 不可逆底线；检查必须可能失败，并说明它不能证明什么；先查现场再提问；先预测再看数据；两种结论分开。这些都还没有证据表明对人有帮助。
- **实际使用中的现场记录：** [docs/field-notes](docs/field-notes/)。

### 路线图

- **第 0 阶段：** 模拟用户评测，分三组（不装插件、`CLAUDE.md` 里 60 个词的说明、完整插件）。如果插件比不过那 60 个词，就改为发布那 60 个词。
- **较小的模型：** 用同一批模拟用户任务测试 27B 到 38B 的开源模型，对比不装插件、5.0 默认流程和结构化模式。
- **第 1 阶段：** 8 到 12 名参与者，与未装插件的 Claude Code 交叉对照，48 到 72 小时后测试理解程度。
- **SessionStart 钩子**放在 [`extras/`](extras/session-start-hook/README.md) 中，只有第 0 阶段证明它能帮新会话找到任务卡，才会正式发布。

---

## 文档

- **[5 分钟教程](docs/TUTORIAL.zh.md)：** 一张任务卡，从简报到复盘
- **[术语表](docs/GLOSSARY.md)：** 任务卡、预测、验收标准、打断点、可逆性分级、两种结论
- **[架构](docs/ARCHITECTURE.md)：** 文件、子代理、数据流、设计原则
- **[5.0 设计](docs/design/5.0.md)：** 为什么这样设计、怎样设计，以及评测计划
- **[SKILL.md](skills/finding-unknowns/SKILL.md)** 及其[参考文件](skills/finding-unknowns/references/card.md)
- **[示例](EXAMPLES.md)：** 可直接复制的提示词
- **[更新日志](CHANGELOG.md)** · **[AGENTS.md](AGENTS.md)** · **[贡献指南](CONTRIBUTING.md)**

---

## 环境要求

- **Claude Code：** 命令行、桌面应用或 IDE 插件均可。这些 Markdown 在 Codex 中也能使用。
- **无运行时，无依赖。** 全部是纯 Markdown。子代理是可选的；没有子代理时，评判在同一上下文中完成，并标注为证据较弱。
- **git：** 用于提交任务卡（可选；没有 git 时，时间由智能体自行记录）。
- **`bash`：** 仅 `install.sh` 需要。

## 项目结构

<details>
<summary><b>仓库目录</b></summary>

```
finding-unknowns-skill/
├── .claude-plugin/          插件与插件市场清单
├── commands/                /fu-brief · /fu-catch-up · /fu-debrief · /fu-cartographer（只负责转发）
├── skills/finding-unknowns/
│   ├── SKILL.md             任务卡、三个操作、打断点、常驻规则
│   └── references/          card · brief · debrief · results · results-examples；结构化模式：structured · cartographer · handoff-full
├── agents/                  blindspot-scout（sonnet）· mechanism-auditor · quiz-master · ledger-keeper · prototype-smith
├── extras/session-start-hook/   尚未发布，等待第 0 阶段评测
├── docs/                    design/、evals/、field-notes/、ARCHITECTURE、GLOSSARY、TUTORIAL（含 .zh）
├── assets/                  八张示意图（SVG）；assets/zh/ 为中文版
├── CLAUDE.md                免安装的单文件精简版
├── install.sh               安装脚本；会删除能识别的 4.x 遗留文件
├── AGENTS.md · EXAMPLES.md · CONTRIBUTING.md · CHANGELOG.md · LICENSE（MIT）
└── README.md（英文，以此为准）· README.zh.md（简体中文）
```

</details>

## 许可与致谢

本项目以 [MIT 许可证](LICENSE)发布。

- 探索未知项的方法：Thariq Shihipar，_"A Field Guide to Fable: Finding Your Unknowns"_（[@trq212](https://x.com/trq212/status/2073100352921215386)）。
- “放弃判断”（cognitive surrender）：Shaw 与 Nave，_Thinking—Fast, Slow, and Artificial_（SSRN 6097646）；认知债务：Margaret-Anne Storey。
- 交付复核与验收标准：Addy Osmani，_"Critical thinking when agents do the work"_（[原文](https://x.com/addyosmani/status/2117512471930167377)）。
- 理论预期 → 实测 → 是否一致 → 机理：作者本人的科研实践。
- 5.0 的设计依据 Fable 5.2 的顾问意见，并参考了 GPT 6 Astra 的第二份意见（[原文](docs/design/5.0-advisors/fable.md)）。

**声明。** 本项目是独立的社区项目，与 Anthropic 无关联，未获其授权或认可。
