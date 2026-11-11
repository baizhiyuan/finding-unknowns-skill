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

<p align="center"><strong>智能体替你完成工作，你仍是这项工作的负责人：清楚正在做什么，事先预测会发生什么，事后看清结果在哪里偏离了预期。</strong></p>

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

也可以克隆仓库后运行 `install.sh`。它会安装技能及其参考文件、五个子代理和四个命令：

```bash
git clone https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill && bash install.sh
```

如果不想安装，也可以把 [`CLAUDE.md`](CLAUDE.md) 复制到项目根目录，使用一份始终生效的精简版。

**初次使用：**

```
/fu-brief "让导出任务支持断点续传"   # 你先预测，再查清现状，智能体随后预测；你确认后冻结
/fu-catch-up                        # 下次会话：看有哪些变化；学习模式（learn）下先回忆
/fu-debrief                         # 逐条评判预测，指出你的认知需要哪些修正
```

[5 分钟教程](docs/TUTORIAL.zh.md)以一张任务卡为例，从简报一直讲到复盘。

### 更新

下一个版本为 **v5.0.0**，是否发布取决于第 0 阶段评测的结果；当前发布的版本为 v4.3.2。按当初的安装方式更新即可：

```
/plugin marketplace update finding-unknowns-skill
```

```
/plugin update finding-unknowns@finding-unknowns-skill
```

<details>
<summary><b>克隆安装、从 4.x 升级与版本核对</b></summary>

`install.sh` 会直接覆盖已安装的文件，并删除它能确认属于本项目的 4.x 文件（Workflow 参考文件 `workflows.md`、独立的 keep-the-reasoning 和 theory-vs-result 技能以及旧命令）：

```bash
cd finding-unknowns-skill && git pull origin main && bash install.sh
```

4.x 仍可通过 `v4.3.2` 标签获取。各部分在 5.0 中的去向，见[设计文档第 11 节](docs/design/5.0.md#11-migration-for-4x-users)。

```bash
grep -h '"version"' ~/.claude/plugins/cache/finding-unknowns-skill/finding-unknowns/*/.claude-plugin/plugin.json 2>/dev/null \
  || ls ~/.claude/skills/finding-unknowns/references/card.md
# 预期：5.0.0（插件方式），或列出 card 参考文件
```

</details>

---

## 为什么选择 finding-unknowns？

把工作交给智能体以后，人很容易渐渐说不清究竟发生了什么：只扫了一眼的改动被批准了，长任务一点点偏离了原意，最后的结果归在你名下，里面却没有你的判断。Addy Osmani 把这一过程概括为**委托 → 依赖 → 放弃判断**。“放弃判断”（cognitive surrender）这一说法出自 Shaw 与 Nave 的 _Thinking—Fast, Slow, and Artificial_（SSRN 6097646）；与之相关的“认知债务”，见 Margaret-Anne Storey 的论述。

本插件为每个任务维护一张由你和智能体共用的**任务卡**：

- **动手之前：** 你先写下自己的预期；智能体随后查清代码和数据的现状，再给出它自己的预测。你的预测在你看到智能体的预测之前就已记录在案。
- **执行期间：** 智能体只在四个可以核对的打断点停下来找你。其余情况都记在任务卡上，你随时可以查看。
- **完成之后：** 由一个未参与执行的上下文逐条评判预测。你会看到哪些预测成立、各项检查没有证明什么，以及你需要做哪些认知修正。

任务卡是一个文件，会话结束后依然保留。这对长任务和科研尤其重要，因为这类工作的结果往往要过几天才陆续出来。

> **来源说明。** 发现未知项的方法出自 Thariq Shihipar 的文章 _"A Field Guide to Fable: Finding Your Unknowns"_（[@trq212](https://x.com/trq212/status/2073100352921215386)）。交付环节的做法，包括写明“检查没有证明什么”，出自 Addy Osmani 的 _"Critical thinking when agents do the work"_（[原文](https://x.com/addyosmani/status/2117512471930167377)）。“理论预期 → 实测 → 是否一致 → 机理”来自作者本人的科研实践。

### 评测结果

三次预注册的盲评评测（[docs/evals](docs/evals/)）检验了 4.x 技能能否让当前模型在单轮任务中发现更多预先埋设的陷阱。结果如下：

- **没有一项提升在复现中成立。** 基线本来就能发现 25 个陷阱中的 22 到 23 个。
- **成本可以测出：** 输入 token 或费用增加约 10 % 到 70 %，回答更长；Sonnet 还会多出一些细小的错误陈述。
- **只有一个范围很窄的效应，且仅见于 Sonnet：** 在合并问题上运行 keep-the-reasoning 时，Sonnet 在 5 次运行中有 4 次指出，“测试通过”只依赖一个会自行更新的快照测试；不运行该技能时，12 次中只有 1 次。这一点是事后才发现的，只能算线索，不能算结论。

5.0 围绕这些评测从未测量过的一面重新设计：**你**的理解和决策（[设计文档](docs/design/5.0.md)）。它对人是否有帮助，**目前尚未检验**。5.0 是否发布，由一项带预注册淘汰规则的模拟用户评测决定；之后还会有真人参与的研究。在此之前，请把它当作一种工作方式，而不是经过测量的改进。

---

## 工作原理

<p align="center"><img src="assets/zh/lifecycle.svg" alt="围绕一张任务卡的三个时刻：动手前的简报、安静的执行、完成后的复盘，以及回来时的回顾" width="100%"></p>

`/fu-brief` 冻结任务卡；执行期间只在四个打断点停下；`/fu-catch-up` 帮你在新会话中重新了解进展；`/fu-debrief` 评判冻结的预测。

### 架构

<p align="center"><img src="assets/zh/framework.svg" alt="命令、技能及其参考文件、五个子代理、磁盘上的文件与原则" width="100%"></p>

四个命令都进入同一个技能。`SKILL.md` 只包含每个时刻都要用到的内容（任务卡、打断点、常驻规则），其余内容放在参考文件中，到了对应时刻才加载。结构化模式是单独的一层，除非你明确要求，否则不会加载。

### 四类未知

<p align="center"><img src="assets/zh/quadrants.svg" alt="四类未知及各自对应的方法" width="100%"></p>

简报从你的预测开始。随后智能体判断缺口属于哪一类，因为每一类都需要不同的方法：

- **已知的已知**已经包含在你的需求里。风险在于它们始终没有明确写出，所以要先记下来。
- **已知的未知**是你能明确提出的问题。智能体会逐一提问，影响架构的问题优先；代码里已经有答案的，从不拿来问你。
- **未知的已知**是你看到就能判断、却说不清楚的偏好。几个真正不同的方向，或一份参考实现，可以把它转化为明确的标准。
- **未知的未知**是盲区。只读的盲区排查会找出潜在风险、隐含约束，以及行家会提出的问题。

### 任务卡

<p align="center"><img src="assets/zh/card.svg" alt="任务卡的结构：页头、冻结的简报、修订、增量记录、认知修正、待办、复盘" width="100%"></p>

任务卡保存在 `.finding-unknowns/tasks/{slug}.md`，默认提交到 git，这样提交记录就能证明预测写在结果出来之前。卡上包括：

- 页头：目标、当前状态、需要你做的下一个决定；
- **冻结的简报：** 做法及理由；你和智能体各自的预测，每条都附有反证条件和“不应改变的部分”；打断点；验收标准（每个检查项，以及它**不能**证明什么）；
- **修订：** 注明日期，只能追加。简报本身从不改动，每条原始预测仍照常评判；
- **增量记录：** 每一次偏离计划、每一处意外、每一个代你做出的决定，各记一行；
- **认知修正：** “你原以为 X，实际是 Y，因为 Z”；
- **待办**，最后是**复盘**。

预测针对的是智能体无法控制的事情：缺陷在哪里、会有多少调用方出错、基准测试得到什么数字。“测试会通过”属于验收标准中的检查项，不是预测。很多任务确实没有值得预测的内容，这时任务卡会如实写明。

### 四个打断点

<p align="center"><img src="assets/zh/stop-points.svg" alt="四个打断点及各自的处理方式；其余情况记录在案，工作继续" width="100%"></p>

只有出现以下情况之一，智能体才会停下来找你：

1. **不可逆操作：** 删除或改写数据，或涉及生产环境、资金、对外发布、对他人的承诺。智能体只准备好确切的命令，由你亲自执行，或由你明确同意执行这一条命令。
2. **范围变化。**
3. **前提失效**，而且已经没有可以撤回的退路。
4. **预算超支：** 超出事先约定的倍数。

其余情况下，智能体一律选择最容易撤回的做法，并记在任务卡上。

### 复盘

<p align="center"><img src="assets/zh/debrief.svg" alt="复盘：滑向放弃判断的过程、由谁评判，以及按顺序呈现的七个部分：证据在前，结论在后" width="100%"></p>

- **原文引用，不转述：** 每条预测都按编号从冻结的任务卡中原文引用。
- **新上下文评判：** `mechanism-auditor` 只看任务卡和产出文件，不看执行过程的对话记录，并且先评判你的预测。
- **在预测落空处讲解：** 讲解只写在预测落空的那几行。
- **证据在前：** 先列出实际运行的命令及其输出，再说明每项检查没有证明什么，以及哪些内容没有人检查过。
- **以结论收尾：** 最后一行写明 `Needs you: X (recommendation: Y)`（需要你：X，建议：Y），不提问；没有待决事项时写 `Needs you: nothing`。
- **默认控制在一屏之内**，需要时再展开细节。

### 实测结果

基准测试、回测、A/B 测试和模型训练的结果，按**理论预期 → 实测 → 是否一致 → 机理**呈现：

- **预测：** 在看到数据之前写好，附上停止规则；噪声底至少由三次重复运行测出。
- **运行记录表：** 几天内陆续得到的结果记入运行记录表；满足停止规则之前，不下结论。
- **两种结论：** 规则结论按事先约定的规则机械判定；这个方向是否还值得继续，由你来判断。

### 学习

- **你先预测：** 交付模式（`ship`）是默认模式，不会让你选择，只问一个可以跳过的问题；学习模式（`learn`）只在你提出时开启，最多问三个。
- **讲解围绕你的失误：** 讲解放在你预测落空的地方，而不是一开始先讲一大段。
- **仅在学习模式（`learn`）下，`/fu-catch-up` 先提回忆性问题：** 在你看到任务卡之前，提两到三个；交付模式（`ship`）不提问。不设及格线。
- **预测记录：** 你的命中率会持续记录下来，只供你本人查看，不提交到仓库。

### 结构化模式（可选）

<p align="center"><img src="assets/zh/cartographer.svg" alt="结构化模式：Cartographer，以未知项台账、六项开工条件和定稿规格组成的循环" width="100%"></p>

对于高风险任务，或者当你希望每一步都写明时（这可能对较小的模型有帮助），可以使用 `/fu-brief --structured` 或 `/fu-cartographer`，在任务卡之上叠加 4.x 的完整流程：

- **按象限选择方法**，以及八种编号方法（T1–T8）：盲区排查、方案原型、需求访谈、参考实现、实施计划、实施记录、变更说明、理解测验。
- **Cartographer 模式：** 每个未知项都成为未知项台账中的一个条目，带有预期、风险值（出错代价 × 出错概率）、处理方式和可逆性分级。每轮显示清晰度，便于你把握方向；六项开工条件决定何时可以开始实施；定稿规格中的验收标准成为任务卡上的验收标准。
- **完整交付报告：** 先做影响评估，共九个部分，证据在前。

任务卡、四个打断点和新上下文评判照常适用。

---

## 命令

| 命令 | 作用 |
|---|---|
| `/fu-brief <任务>` | 先记下你的预测，再查清现状，然后给出智能体的预测；约定打断点和验收标准；冻结任务卡并提交 |
| `/fu-catch-up [slug]` | 学习模式（`learn`）下先提回忆性问题，再只显示你上次查看之后的变化，以及需要你做的下一个决定 |
| `/fu-debrief [slug]` | 由新上下文评判每条冻结的预测；列出证据、各项检查没有证明什么，以及认知修正 |
| `/fu-cartographer <任务>` | 高风险任务的结构化模式：在任务卡之上运行 Cartographer 的未知项台账、开工条件和定稿规格 |

直接说“brief me”“catch me up”“where were we”或“did it match what we expected”也可以。改错字、一行改动这类小事不建任务卡，也不提问。在非交互的 `claude -p` 中，请使用完整名称（`/finding-unknowns:fu-brief`）。

| 子代理 | 职责 |
|---|---|
| `blindspot-scout` | 为简报做只读侦察：潜在风险、隐含背景、改写后的需求 |
| `mechanism-auditor` | 在复盘和实测结果中担任新上下文评判 |
| `quiz-master` | 可选：为 `/fu-catch-up` 起草回忆性问题，并标出没有任何增量记录能够解释的改动 |
| `ledger-keeper` | 结构化模式：维护 Cartographer 的未知项台账、评分和开工判定 |
| `prototype-smith` | 针对“看到才知道”的偏好，做出几个真正不同的一次性方案（用于简报和结构化模式） |

---

## 设计札记

- **为什么 5.0 是重新设计。** 三次评测把 4.x 技能当作提升模型输出的工具来衡量，没有发现可以复现的提升。作者的目标始终在人这一侧，所以 5.0 围绕人来组织。设计本身、两份顾问意见，以及 5.0 在哪些地方没有采纳这些意见，见 [docs/design/5.0.md](docs/design/5.0.md)。
- **哪些内容换了位置。** Cartographer 模式（风险值、清晰度显示、六项开工条件）、八种编号方法和九个部分的交付报告不再属于默认流程，而是作为**结构化模式**保留，只在你要求时加载。保留的理由是，较小的模型可能需要前沿模型用不着的明确步骤（这是一个尚在检验的假设）。Workflow 执行和必须通过的理解测验已删除。keep-the-reasoning 和 theory-vs-result 已并入现在唯一的技能。
- **基于设计判断保留的内容。** 不可逆操作确认规则；检查必须有可能失败，并写明它不能证明什么；先查清现状再提问；先预测再看数据；两种结论分开给出。目前还没有证据表明其中任何一项对人有帮助。
- **实际使用记录：** [docs/field-notes](docs/field-notes/)。

### 路线图

- **第 0 阶段：** 模拟用户评测，分三组：不装插件、在 `CLAUDE.md` 中写一段 60 个词的说明、安装插件。如果插件的效果不如这 60 个词，就改为发布这 60 个词。
- **较小的模型：** 用同一批模拟用户任务测试一个 27B 到 38B 的开放权重模型，对比不装插件、5.0 和结构化模式。
- **第 1 阶段：** 招募 8 到 12 名参与者，与未安装插件的 Claude Code 做交叉对照，并在 48 到 72 小时后测试他们的理解程度。
- **SessionStart 钩子**目前放在 [`extras/`](extras/session-start-hook/README.md) 中。只有第 0 阶段表明它能帮助新会话找到任务卡，才会正式发布。

---

## 文档

- **[5 分钟教程](docs/TUTORIAL.zh.md)：** 以一张任务卡为例，从简报到复盘
- **[术语表](docs/GLOSSARY.md)：** 任务卡、预测、验收标准、打断点、可逆性分级、两种结论
- **[架构](docs/ARCHITECTURE.md)：** 文件、子代理、数据流、设计原则
- **[5.0 设计](docs/design/5.0.md)：** 为什么这样设计、如何设计，以及评测计划
- **[SKILL.md](skills/finding-unknowns/SKILL.md)** 及其[参考文件](skills/finding-unknowns/references/card.md)
- **[示例](EXAMPLES.md)：** 可直接复制的提示词
- **[更新日志](CHANGELOG.md)** · **[AGENTS.md](AGENTS.md)** · **[贡献指南](CONTRIBUTING.md)**

---

## 环境要求

- **Claude Code：** 命令行、桌面应用或 IDE 扩展均可。这些 Markdown 文件在 Codex 中同样可用。
- **无运行时，无依赖。** 全部内容都是纯 Markdown。子代理是可选的；没有子代理时，评判在同一上下文中完成，并注明这种评判较弱。
- **git：** 用于提交任务卡（可选；没有 git 时，时间凭据改为自行记录）。
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

- 发现未知项的方法：Thariq Shihipar，_"A Field Guide to Fable: Finding Your Unknowns"_（[@trq212](https://x.com/trq212/status/2073100352921215386)）。
- “放弃判断”（cognitive surrender）：Shaw 与 Nave，_Thinking—Fast, Slow, and Artificial_（SSRN 6097646）；认知债务：Margaret-Anne Storey。
- 交付环节与验收标准：Addy Osmani，_"Critical thinking when agents do the work"_（[原文](https://x.com/addyosmani/status/2117512471930167377)）。
- 理论预期 → 实测 → 是否一致 → 机理：作者本人的实证研究实践。
- 5.0 的设计依据 Fable 5.2 的顾问意见，并参考了 GPT 6 Astra 的第二份意见（[意见原文](docs/design/5.0-advisors/fable.md)）。

**声明。** 本项目是独立的社区项目，与 Anthropic 无关联，未获其授权或认可。
