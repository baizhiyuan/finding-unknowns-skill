<p align="center"><a href="README.md">English</a> | <strong>简体中文</strong></p>

<p align="center"><em>本文档是英文 README 的翻译；若有出入，以英文版为准。</em></p>

<p align="center">
  <img src="assets/hero.svg" alt="finding-unknowns — 一个 Claude Code 技能" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Skill-8A63D2" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/scope-global-5B8DEF" alt="全局作用域">
  <img src="https://img.shields.io/badge/trigger-manual-F59E0B" alt="手动触发">
  <img src="https://img.shields.io/badge/covers-pre_%C2%B7_during_%C2%B7_post-2DD4BF" alt="生命周期覆盖">
  <img src="https://img.shields.io/badge/license-MIT-22C55E" alt="MIT 许可证">
</p>

<p align="center"><em>地图不等于疆域。长周期工作的质量，取决于你把自己的<strong>未知（unknowns）</strong>厘清到什么程度。</em></p>

`finding-unknowns` 是一个 Claude Code 技能与代理（agent）框架，帮助你在实施之前、之中、之后
把自己尚未知晓的东西显露出来——从而用前期廉价的提问去化解歧义，而不是在后期付出昂贵的返工代价。
一个统筹调度的技能（skill）提供了八种发现技术，以及一套严谨的门控模式；四个配套代理在需要隔离、
发散或独立判断时为这些技术提供支撑。

> **来源说明。** 本技能提炼自 Thariq Shihipar 的文章《_A Field Guide to Fable:
> Finding Your Unknowns_》（[@trq212](https://x.com/trq212/status/2073100352921215386)）。
> 底层理念与技术名称的功劳归于原作者；本仓库将其打包为一个可安装的 Claude Code 技能。

---

## 概览

**地图（map）**是你交给 Claude 的东西（提示词、上下文和技能）。**疆域（territory）**是工作
真正发生的地方（代码库与现实世界）。二者之间的落差，正是由各种未知构成的，而每一个未知都会
迫使模型去猜测你的意图。

本技能提供了八种具体技术，用于在完整的任务生命周期中显露这些未知，此外还提供一个可选的严谨模式
（"Cartographer 模式"），用于高风险的工作。

<p align="center">
  <img src="assets/lifecycle.svg" alt="捕捉未知的三个窗口：事前、事中、事后" width="92%">
</p>

## 特性

- **四象限框架** — 在行动之前，先判断一个缺口属于已知未知还是未知未知。
- **盲点排查（Blind-spot pass）** — 显露出那些你自己都没意识到存在、且与你当前上下文相关的未知。
- **头脑风暴与原型（Brainstorm and prototype）** — 在提交代码之前，先对多个可丢弃的方向做出反应。
- **访谈（Interview）** — 一次只问一个问题，优先处理会改变架构的答案。
- **参考资料（References）** — 把现有源代码当作最丰富的可用规格说明来对待。
- **实施计划（Implementation plan）** — 优先摆出最可能发生变化的决策。
- **实施笔记（Implementation notes）** — 在构建过程中记录被迫做出的偏离，供事后复盘。
- **推介与测验（Pitch and quiz）** — 一个用于争取认可的评审产物，以及合并前的理解力检验。
- **Cartographer 模式** — 一套基于歧义评分、覆盖度门控、按遗憾值加权的协议，由一份持久化台账
  （ledger）支撑，最终以一个需审批门控的执行桥接收尾。
- **配套代理** — 四个专才代理（`blindspot-scout`、`prototype-smith`、
  `ledger-keeper`、`quiz-master`），技能在需要更大深度时会委派给它们。

## 架构

该框架是分层的——命令负责派发，技能负责决策，代理负责执行，文档负责持久化。流程只存在于唯一
一处（`SKILL.md`）；其余每一层要么进入这份流程，要么执行来自它的一份契约。每种技术都可独立运行——
命令与代理是增强项，而非依赖项。完整设计参考见
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

| 层级 | 内容 | 角色 |
|-------|----------|------|
| 命令 | `/finding-unknowns` `/blindspot` `/cartographer` `/change-quiz` | 薄入口点；指名一个技能小节，传递参数 |
| 技能 | `SKILL.md` | 协议本体：象限路由、八种技术、Cartographer 模式、护栏机制 |
| 代理 | 四个专才代理 | 具备明确输入/输出契约的隔离执行画像 |
| 产物 | 台账、笔记、原型、报告 | 持久化状态；台账是恢复执行的锚点 |
| 工作流 | `references/workflows.md` | 面向高扇出操作的可选动态工作流脚本；可降级为普通代理或内联执行 |

<p align="center">
  <img src="assets/framework.svg" alt="框架：一个技能统筹调度四个专才代理" width="96%">
</p>

| 代理 | 模型 | 支撑的技术 | 执行画像 |
|-------|-------|-------|-------------------|
| `blindspot-scout` | sonnet | 盲点排查、参考资料 | 只读侦察；在自己独立的上下文窗口中探索，结构上就不可能开始实施代码 |
| `prototype-smith` | inherit | 头脑风暴与原型、实施计划 | 被限制在新建的可丢弃文件中；一次性产出 N 个真正发散的方向 |
| `ledger-keeper` | inherit | Cartographer 模式 | 未知台账的独立记账者；负责给遗憾值打分、把各象限的清晰度打分汇总为加权歧义值，并在覆盖度+歧义度双重门控上做出裁决，且不给自己的工作打分 |
| `quiz-master` | inherit | 测验、推介与讲解 | 未参与撰写该改动的"新鲜视角"考官；专门追问作者本人容易一带而过的地方 |

这种分离遵循一条原则：**发现、评分与审查不应由负责实施的同一个上下文来完成。** 一个无法编辑
文件的侦察者，不会滑向去动手实现；一个未曾主持访谈的记账者，不会去粉饰自己的门控裁决；一个未曾
撰写该 diff 的考官，会提出更难回答的问题。

## 四个象限

先定位一个未知处在哪个象限；象限决定了该用哪种技术。

<p align="center">
  <img src="assets/quadrants.svg" alt="未知的四个象限" width="78%">
</p>

## 环境要求

- **Claude Code** — CLI、桌面应用，或某个 IDE 扩展。该技能通过 Skill 工具加载
  （或放在 `~/.claude/skills/` 下）；斜杠命令则需要插件或手动复制。
- **无运行时、无依赖。** 技能、代理与命令都是纯 Markdown 文件。除了复制文件之外，
  不需要编译或安装任何东西。
- **可选增强项，二者均可优雅降级：** 四个配套代理（在需要更大深度时使用），以及
  用于动态工作流编排的 Workflow 工具——即便二者都未安装，每种技术也都能完全以内联方式运行。
- **`bash`** 用于运行 `install.sh`（选项 B）。选项 A、C、D 都不需要 shell。

## 安装

**选项 A —— 插件市场（推荐）：**

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
/plugin install finding-unknowns@finding-unknowns-skill
```

**选项 B —— 克隆并安装：**

```bash
git clone https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill
bash install.sh              # installs the skill and the four companion agents
```

**选项 C —— 被动直接放入项目（无需安装）：** 将 [`CLAUDE.md`](CLAUDE.md) 复制到
项目根目录，即可获得轻量级、常驻生效的指引。

**选项 D —— 手动复制：**

```bash
mkdir -p ~/.claude/skills/finding-unknowns/references
cp skills/finding-unknowns/SKILL.md ~/.claude/skills/finding-unknowns/
cp skills/finding-unknowns/references/*.md ~/.claude/skills/finding-unknowns/references/
```

## 更新

要将现有安装更新到最新版本（**v3.7.0**），请遵循与最初安装方式相对应的流程。

**更新方式对应选项 A —— 插件市场：**

```
/plugin marketplace update finding-unknowns-skill
/plugin update finding-unknowns@finding-unknowns-skill
```

**更新方式对应选项 B —— 克隆并安装：** 拉取更新后重新运行安装脚本。`install.sh`
会原地覆盖（技能、`references/`、四个代理，以及斜杠命令），因此它同时也充当更新脚本。

```bash
cd finding-unknowns-skill
git pull origin main
bash install.sh              # re-copies skill + references + agents + commands
```

**更新方式对应选项 D —— 手动复制：** 覆盖同名文件（`references/` 目录承载着
Workflow 编排模板，也必须一并更新）。

```bash
cd finding-unknowns-skill && git pull origin main
mkdir -p ~/.claude/skills/finding-unknowns/references
cp skills/finding-unknowns/SKILL.md ~/.claude/skills/finding-unknowns/
cp skills/finding-unknowns/references/*.md ~/.claude/skills/finding-unknowns/references/
cp agents/*.md   ~/.claude/agents/
cp commands/*.md ~/.claude/commands/
```

更新完成后，请核实已安装的版本与发布版本一致：

```bash
grep '"version"' ~/.claude/plugins/*/finding-unknowns*/.claude-plugin/plugin.json 2>/dev/null \
  || grep -c '### Model routing' ~/.claude/skills/finding-unknowns/SKILL.md
# expect: 3.7.0 (plugin) — or a non-zero count confirming the v3.7.0 Model routing section
```

## 配置

该技能在**零配置**的情况下即可运行——下面每一个旋钮都是可选的，并且都有合理的默认值。

**清晰度阈值（Cartographer 模式）。** 加权歧义门控默认值为 `0.25`。
可以在 `.claude/settings.json` 中按项目或按用户覆盖此值（项目级配置优先于用户级配置）：

```json
{
  "findingUnknowns": {
    "ambiguityThreshold": 0.25
  }
}
```

进入时，Cartographer 会报告最终生效的阈值及其来源。

**深度预设。** 命令上的一个标志位会覆盖任何 settings 中的取值：

| 标志位 | 阈值 | 适用场景 |
|------|-----------|---------|
| `/cartographer --quick <task>` | 0.35 | 快速定向，风险较低的工作 |
| `/cartographer --standard <task>` | 0.25（默认） | 大多数任务 |
| `/cartographer --deep <task>` | 0.15 | 高风险、难以回退的工作 |

**其他默认值**（原型方向数量、遗憾值提问门槛、测验规模与轮次、Cartographer 的轮次上限、
每轮至多三个相互独立的访谈问题）记录在 [`SKILL.md`](skills/finding-unknowns/SKILL.md)
内的 **Defaults** 表中，也可以通过对技能下达自然语言指令来覆盖。

**模型路由。** 负责判断与创造性工作的代理——`ledger-keeper`、`prototype-smith`
以及 `quiz-master`——都以 `model: inherit` 声明，因此它们运行在当前会话所使用的模型上，
而非固定档位。`blindspot-scout` 被固定为 `sonnet`，因为侦察是以并行扇出方式运行的；
在单镜头式排查中，也可以在其 frontmatter 中将其设为 `inherit`。这一方案遵循了 OMC
（判断用最强模型、执行用中间档位、广度用最低档位）与 Deep Research（合成中枢用最强模型、
扇出环节用更便宜的模型）的基于角色的惯例。相关论证见
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

## 使用方法

在一项含糊或陌生的任务开始时，通过 Skill 工具调用该技能：

```
finding-unknowns
```

安装了插件之后，斜杠命令提供了直接的入口点：

| 命令 | 进入位置 |
|---------|-----------|
| `/finding-unknowns <task>` | 第 0 阶段——象限路由，随后进入匹配的技术 |
| `/blindspot <goal or area>` | 盲点排查（仅侦察） |
| `/cartographer <task>` | Cartographer 模式——台账、评分门控的清理循环、双重门控、执行桥接 |
| `/change-quiz [diff range]` | 变更报告 + 必须通过的理解力测验 |

也可以用自然语言直接请求单项技术，例如："做一次盲点排查""对我进行访谈"，或
"头脑风暴四个方向"。完整的、可直接复制粘贴的提示词见 [`EXAMPLES.md`](EXAMPLES.md)。

## 八种技术

| 阶段  | 技术              | 适用场景                                          |
|--------|------------------------|--------------------------------------------------|
| 事前   | 盲点排查        | 新领域或新代码库中的未知未知                    |
| 事前   | 头脑风暴与原型 | 未知已知——"我见到它就会知道"     |
| 事前   | 访谈              | 头脑风暴之后仍残留的歧义           |
| 事前   | 参考资料             | 当你无法描述它时——直接指向代码      |
| 事前   | 实施计划    | 提前显露风险最高的决策                |
| 事中 | 实施笔记   | 迫使做出偏离的边界情况                |
| 事后   | 推介与讲解      | 争取认可与审批                          |
| 事后   | 测验                   | 合并前确认理解无误               |

每种技术的完整提示词记录在
[`skills/finding-unknowns/SKILL.md`](skills/finding-unknowns/SKILL.md) 中。

## Cartographer 模式

上述八种技术是轻量级探针。Cartographer 模式则是面向高风险工作的严谨升级方案：一种门控式访谈，
在问题空间被充分绘制清楚之前，不允许开始实施。它的灵感来自
[oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) 中的 Deep Interview 技能：
自 v3.6.0 起，它*采纳*了 Deep Interview 的透明化机制——按象限打出清晰度分数、汇总为一个可配置
阈值的加权歧义值、第 0 轮的拓扑确认，以及挑战模式——同时保留了单纯的清晰度评分式访谈所无法覆盖的
那些维度。

<p align="center">
  <img src="assets/cartographer.svg" alt="Cartographer 模式：覆盖度门控、未知台账、按遗憾值加权的定位" width="96%">
</p>

| 维度              | Deep Interview                          | Cartographer 模式                                                        |
|-------------------|-----------------------------------------|--------------------------------------------------------------------------|
| 门控判据    | 歧义度 ≤ 阈值（目标/约束/标准三个维度） | 双重条件：覆盖度（四个象限均已排查，且必须完成盲点排查）且各象限加权歧义度 ≤ 阈值 |
| 盲点（UU）  | 未建模                            | 一等公民；在歧义度公式中权重最高（0.30）             |
| 生命周期         | 止步于规格说明                | 一份台账，事前生成、事中追加、事后关闭                      |
| 优先级排序    | 固定的维度权重                 | Regret = cost-if-wrong × P(wrong) 决定各行的排序优先级；歧义度则给各象限打分 |
| 清理手段 | 仅苏格拉底式问答                     | 按未知类型分派路由：访谈 / 现地核验 / 实验 / 审计——该循环是一个路由器，而非一场访谈 |
| 执行交接 | 桥接进入 OMC 的各条流水线              | 需审批门控的桥接：独立的规划者+评审者达成共识，或采用 Workflow 执行并对每个子任务做反驳式验证 |

其机制核心是一份持久化的未知台账（`id · quadrant · cost-if-wrong · P(wrong) ·
regret · route · status · phase`），其表头记录着清晰度阈值、已锁定的拓扑结构，以及逐轮的
各象限评分历史。每一轮都会按路由方式清理掉遗憾值最高的一条未关闭记录，然后重新为四个象限打分，
并向用户展示评分表——
`ambiguity = 1 − (KK×0.20 + KU×0.25 + UK×0.25 + UU×0.30)`，默认阈值为 0.25
（`--quick` 为 0.35 / `--deep` 为 0.15）。只要仍有象限未被排查、仍有未关闭记录的
`regret ≥ 1.0`，或歧义度高于阈值，就不得开始实施；门控 PASS 之后会固化出一份待审批的
规格说明，交由经交叉验证的执行桥接来处理。完整的字段结构与启动提示词见
[`SKILL.md`](skills/finding-unknowns/SKILL.md)。

当宿主环境暴露出 Claude Code 的 **Workflow 工具**（动态工作流）、且用户已选择启用编排时，
高扇出操作会以确定性脚本的形式运行——多镜头扫描并对每条发现做对抗式验证（流水线式，无阻塞点）、
针对代价 ≥ 4 的记录进行三镜头反驳评审、一个仅在连续两轮无收获时才停止的 UU 探测循环，以及
审批通过后的执行阶段（每个实施者都配有一名独立的、以反驳为导向的验证者）。相关模板与优雅降级
的兜底阶梯见 [`references/workflows.md`](skills/finding-unknowns/references/workflows.md)。

<p align="center">
  <img src="assets/workflows.svg" alt="动态工作流编排：多镜头扫描、验证评审、UU 循环直至无收获、兜底阶梯" width="96%">
</p>

## 与其他工具的关系

`finding-unknowns` 运行在与更重型的工作流技能不同的高度上。它是一个轻量级的定向层，
而不是一个执行引擎。

| 属性     | finding-unknowns          | Deep Interview（[OMC](https://github.com/Yeachan-Heo/oh-my-claudecode)） | OMC 执行（autopilot / ralph / team） | [Superpowers](https://github.com/obra/superpowers) |
|--------------|---------------------------|-------------------------|------------------------|------------------------|
| 高度     | 元层面 / 定向层            | 单一阶段：需求梳理 | 执行与交付   | 纪律性原语  |
| 生命周期    | 事前 · 事中 · 事后       | 仅事前                | 事中 · 事后                | 大多为单阶段      |
| 严谨度       | 灵活                  | 歧义度门控            | 验证门控   | 清单驱动        |
| 状态        | 无状态                 | 持久化，可恢复    | 持久化，多代理 | 视情况而定                 |
| 最佳适用场景    | 你还不知道自己有哪些未知 | 你需要一份经过验证的规格说明 | 规格说明已经明确 | 你需要一次有纪律的动作 |

这些工具是互补关系，而非彼此竞争。推荐的使用模式是：先用 `finding-unknowns` 定位一个未知，
再升级到合适的专项工具：

```
finding-unknowns  (orient: which quadrant is this unknown in?)
        ├─ a light reframe is sufficient          → the eight techniques
        ├─ high-stakes, want a coverage gate       → Cartographer mode (this skill)
        ├─ want ambiguity gating + resumable state → OMC Deep Interview
        ├─ divergent option generation             → superpowers:brainstorming
        ├─ a rigorous written plan                 → superpowers:writing-plans / omc-plan
        └─ the specification is already concrete    → OMC autopilot / ralph / team
```

## 项目结构

```
finding-unknowns-skill/
├── .claude-plugin/         Plugin and marketplace manifests (/plugin install)
├── commands/               Slash-command entry points (thin dispatchers)
│   ├── finding-unknowns.md   /finding-unknowns — Phase 0 routing
│   ├── blindspot.md          /blindspot — blind-spot pass
│   ├── cartographer.md       /cartographer — Cartographer mode
│   └── change-quiz.md        /change-quiz — report + merge quiz
├── skills/
│   └── finding-unknowns/
│       ├── SKILL.md        The protocol: routing, eight techniques, Cartographer mode
│       └── references/
│           └── workflows.md  Workflow-orchestration templates (multi-lens sweep, verify panel, UU loop)
├── agents/
│   ├── blindspot-scout.md  Read-only reconnaissance (sonnet)
│   ├── prototype-smith.md  Divergent throwaway prototyping (inherit)
│   ├── ledger-keeper.md    Regret scoring and coverage-gate verdicts (inherit)
│   └── quiz-master.md      Independent examiner (inherit)
├── docs/
│   └── ARCHITECTURE.md     Design reference: layers, contracts, principles
├── assets/                 README diagrams (SVG)
├── AGENTS.md               Repository guide for coding agents and contributors
├── EXAMPLES.md             Copy-paste, end-to-end prompts
├── CLAUDE.md               Passive single-file drop-in
├── install.sh              Installer (skill + references + agents + commands)
├── CONTRIBUTING.md         Contribution guidelines
├── CHANGELOG.md            Release history
├── LICENSE                 MIT
├── README.md               English (canonical)
└── README.zh.md            简体中文 translation
```

## 贡献

欢迎贡献。请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解相关指南。

## 致谢

- 相关理念与技术名称源自 Thariq Shihipar 的文章《_A Field Guide to
  Fable: Finding Your Unknowns_》（[@trq212](https://x.com/trq212/status/2073100352921215386)）。
- Cartographer 模式的对比部分参考了
  [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) 中的 Deep Interview 技能，
  以及 [Superpowers](https://github.com/obra/superpowers) 中的各项原语。

## 许可证

基于 MIT 许可证发布。详见 [LICENSE](LICENSE)。

## 免责声明

这是一个独立的社区项目，与 Anthropic 没有从属、授权或背书关系。
