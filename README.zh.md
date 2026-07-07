<p align="center"><a href="README.md">English</a> | <strong>简体中文</strong> | <a href="README.ja.md">日本語</a> | <a href="README.ko.md">한국어</a></p>

<p align="center"><em>本文档是英文 README 的翻译；若有出入，以英文版为准。</em></p>

<p align="center">
  <img src="assets/hero.svg" alt="finding-unknowns — 一个 Claude Code 技能" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Skill-8A63D2" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/scope-global-5B8DEF" alt="global scope">
  <img src="https://img.shields.io/badge/trigger-manual-F59E0B" alt="manual trigger">
  <img src="https://img.shields.io/badge/covers-pre_%C2%B7_during_%C2%B7_post-2DD4BF" alt="lifecycle">
  <img src="https://img.shields.io/badge/license-MIT-22C55E" alt="MIT license">
</p>

<p align="center"><em>地图不是疆域本身。长周期工作的质量,取决于你把自己的<strong>未知</strong>厘清到什么程度。</em></p>

`finding-unknowns` 是一个 Claude Code 技能与智能体（agent）框架,帮助你在实现之前、实现期间和实现之后,把自己尚未知晓的部分显性化——从而用低成本的提前提问去化解歧义,而不是在后期付出高昂的返工代价。一个统领性的技能提供了八种发现技术和一套严格的门控模式;四个配套智能体在需要隔离性、发散性或独立判断的场景下为这些技术提供支撑。

> **致谢。** 本技能提炼自 Thariq Shihipar 的文章 _"A Field Guide to Fable:
> Finding Your Unknowns"_（[@trq212](https://x.com/trq212/status/2073100352921215386)）。相关理念与技术命名的原创归功于原作者;本仓库只是将其打包为一个可安装的 Claude Code 技能。

---

## 概述

**地图**是你交给 Claude 的东西（提示词、上下文与技能）。**疆域**是工作实际发生的地方（代码库与真实世界）。两者之间的落差由各种未知构成,每一个未知都会迫使模型去猜测你的意图。

本技能提供了八种具体技术,用于在整个任务生命周期中显性化这些未知,此外还为高风险工作提供了一个可选的严格模式（"Cartographer 模式"）。

<p align="center">
  <img src="assets/lifecycle.svg" alt="捕捉未知的三个窗口:事前、事中、事后" width="92%">
</p>

## 特性

- **四象限框架** — 在行动之前,先判定一个缺口是已知的未知还是未知的未知。
- **盲点扫描** — 揭示你自己都没意识到存在的未知,并根据你的具体情境进行调优。
- **头脑风暴与原型** — 在提交代码之前,先对几个可丢弃的方向作出反应。
- **访谈** — 每次只问一个问题,优先回答会改变架构的问题。
- **参考** — 把现有源代码当作最丰富的可用规格说明来对待。
- **实现计划** — 优先呈现最可能发生变化的决策。
- **实现笔记** — 在构建过程中记录被迫产生的偏差,供后续审阅。
- **推介与测验** — 一份用于争取认可的评审产物,以及合并前的一次理解力检查。
- **Cartographer 模式** — 一套基于歧义评分、覆盖度门控、遗憾加权的协议,由持久化台账支撑,最终落地为一个需审批放行的执行桥接。
- **配套智能体** — 四位专才（`blindspot-scout`、`prototype-smith`、
  `ledger-keeper`、`quiz-master`）,技能会在深度有价值时将工作委派给它们。

## 架构

该框架是分层的——命令负责分发,技能负责决策,智能体负责执行,文档负责持久化。流程只存在于唯一一处（`SKILL.md`）;其余每一层要么进入这一流程,要么执行由它定义的契约。每种技术都可独立运行——命令和智能体是增强项,而非依赖项。完整设计参考见
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

| 层 | 内容 | 角色 |
|-------|----------|------|
| 命令 | `/finding-unknowns` `/blindspot` `/cartographer` `/change-quiz` | 薄入口点;指定一个技能小节,传入参数 |
| 技能 | `SKILL.md` | 协议本体:象限路由、八种技术、Cartographer 模式、护栏规则 |
| 智能体 | 四位专才 | 具有明确输入/输出契约的隔离执行画像 |
| 产物 | 台账、笔记、原型、报告 | 持久化状态;台账是恢复执行的锚点 |
| 工作流 | `references/workflows.md` | 面向扇出密集型操作的可选动态工作流脚本;可降级为普通智能体或内联执行 |

<p align="center">
  <img src="assets/framework.svg" alt="框架:一个技能编排四个专才智能体" width="96%">
</p>

| 智能体 | 模型 | 支撑的技术 | 执行画像 |
|-------|-------|-------|-------------------|
| `blindspot-scout` | sonnet | 盲点扫描、参考 | 只读式侦察;在自己独立的上下文窗口中探索,结构上不可能开始实现代码 |
| `prototype-smith` | inherit | 头脑风暴与原型、实现计划 | 被限定在新建的可丢弃文件内;一次即可产出 N 个真正发散的方向 |
| `ledger-keeper` | inherit | Cartographer 模式 | 未知台账的独立记账员;对遗憾打分,把各象限的清晰度打分汇总成加权歧义值,并在双重(覆盖度+歧义度)门控上作出裁决,而不评判自己的产出 |
| `quiz-master` | inherit | 测验、推介与讲解 | 未参与该改动撰写的"新眼睛"考官;专门追问作者自己会略过的地方 |

这种职责分离遵循一个原则:**发现、评分与审查不应由实现工作的同一个上下文来完成。**一个无法编辑文件的侦察员不可能滑向自行构建;一个未参与访谈的记账员不会给自己的门控裁决灌水;一个没有写过该 diff 的考官会问出更尖锐的问题。

## 四个象限

先定位一个未知所处的位置;象限决定了该用哪种技术。

<p align="center">
  <img src="assets/quadrants.svg" alt="未知的四个象限" width="78%">
</p>

## 环境要求

- **Claude Code** — CLI、桌面应用或 IDE 扩展。技能通过 Skill 工具加载（或放入
  `~/.claude/skills/`）;斜杠命令则需要插件或手动复制。
- **无运行时,无依赖。** 技能、智能体和命令都是纯 Markdown 文件。除了复制文件之外,无需编译或安装任何东西。
- **可选增强项,均可优雅降级:** 四个配套智能体（在深度有价值时才会被委派）,以及用于动态工作流编排的 Workflow 工具——即便两者都未安装,每种技术也能完全以内联方式运行。
- **`bash`**,用于运行 `install.sh`（选项 B）。选项 A、C、D 均无需 shell。

## 安装

**选项 A —— 插件市场（推荐）:**

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
/plugin install finding-unknowns@finding-unknowns-skill
```

**选项 B —— 克隆并安装:**

```bash
git clone https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill
bash install.sh              # installs the skill and the four companion agents
```

**选项 C —— 被动式直接放入（免安装）:** 将 [`CLAUDE.md`](CLAUDE.md) 复制到项目
根目录,以获得轻量级的、始终生效的指导。

**选项 D —— 手动复制:**

```bash
mkdir -p ~/.claude/skills/finding-unknowns/references
cp skills/finding-unknowns/SKILL.md ~/.claude/skills/finding-unknowns/
cp skills/finding-unknowns/references/*.md ~/.claude/skills/finding-unknowns/references/
```

## 更新

若要将最新版本（当前为 **v3.6.0**）拉取到已有的安装中,请使用与当初安装方式对应的路径。

**更新方式 A —— 插件市场:**

```
/plugin marketplace update finding-unknowns-skill
/plugin update finding-unknowns@finding-unknowns-skill
```

**更新方式 B —— 克隆并安装:** 拉取更新后重新运行安装脚本。`install.sh`
会就地覆盖（技能、`references/`、四个智能体以及斜杠命令）,因此它同时兼作更新器。

```bash
cd finding-unknowns-skill
git pull origin main
bash install.sh              # re-copies skill + references + agents + commands
```

**更新方式 D —— 手动复制:** 覆盖相同的文件（`references/` 目录
承载着 Workflow 编排模板,也必须一并更新）。

```bash
cd finding-unknowns-skill && git pull origin main
mkdir -p ~/.claude/skills/finding-unknowns/references
cp skills/finding-unknowns/SKILL.md ~/.claude/skills/finding-unknowns/
cp skills/finding-unknowns/references/*.md ~/.claude/skills/finding-unknowns/references/
cp agents/*.md   ~/.claude/agents/
cp commands/*.md ~/.claude/commands/
```

更新完成后,验证已安装的版本与发布版本一致（这条 grep 命令是更新后的合理性检查——相当于一个轻量版的 `doctor` 命令）:

```bash
grep '"version"' ~/.claude/plugins/*/finding-unknowns*/.claude-plugin/plugin.json 2>/dev/null \
  || grep -c 'Cross-validated execution bridge' ~/.claude/skills/finding-unknowns/SKILL.md
# expect: 3.6.0 (plugin) — or a non-zero match count confirming the v3.6.0 Phase E section
```

## 配置

该技能**零配置**即可运行——下面的每一项旋钮都是可选的,并且都有合理的默认值。

**清晰度阈值（Cartographer 模式）。** 加权歧义门控默认值为 `0.25`。
可在 `.claude/settings.json` 中按项目或按用户覆盖（项目设置优先于用户设置）:

```json
{
  "findingUnknowns": {
    "ambiguityThreshold": 0.25
  }
}
```

Cartographer 在进入时会宣告已生效的阈值及其来源,因此你始终能看到当前实际使用的数值。

**深度预设。** 命令上的一个标志会覆盖任何 settings 中的取值:

| 标志 | 阈值 | 适用场景 |
|------|-----------|-----|
| `/cartographer --quick <task>` | 0.35 | 快速定向,风险较低的工作 |
| `/cartographer --standard <task>` | 0.25（默认） | 大多数任务 |
| `/cartographer --deep <task>` | 0.15 | 高风险、难以回退的工作 |

**其他默认值**（原型方向数量、遗憾问题门槛、测验规模与轮次、
Cartographer 的轮次上限、每轮最多 3 个独立访谈问题）记录在
[`SKILL.md`](skills/finding-unknowns/SKILL.md) 中的 **Defaults** 表格里,也可以直接用自然语言告诉技能来覆盖。

**模型路由。** 遵循 OMC 的思路(判断用 opus,执行用 sonnet,广度用 haiku)以及 Deep
Research 的思路(综合决策的核心用最强模型,扇出阶段用更廉价的模型),负责判断与创造性
工作的智能体——`ledger-keeper`、`prototype-smith`、`quiz-master`——都使用
`model: inherit`:它们始终运行在你当前会话所用的模型上,永远不会被降级(Fable 依然是
Fable,Opus 依然是 Opus)。`blindspot-scout` 则固定使用 `sonnet`,因为侦察阶段是并行
扇出的;若想要单视角、最高质量的侦察通道,可在其智能体 frontmatter 中把它改为 `inherit`。

## 用法

在一项含糊或陌生的任务开始时,通过 Skill 工具调用该技能:

```
finding-unknowns
```

安装了插件后,斜杠命令提供了直接的入口点:

| 命令 | 进入位置 |
|---------|-----------|
| `/finding-unknowns <task>` | Phase 0 —— 象限路由,然后进入匹配的技术 |
| `/blindspot <goal or area>` | 盲点扫描（仅侦察） |
| `/cartographer <task>` | Cartographer 模式 —— 台账、评分门控的清除循环、双重门控、执行桥接 |
| `/change-quiz [diff range]` | 变更报告 + 必须通过的理解力测验 |

各项技术也可以用自然语言直接请求,例如:_"做一次盲点扫描"_、_"访谈我"_,
或 _"头脑风暴四个方向"_。完整的、可直接复制粘贴的提示词见
[`EXAMPLES.md`](EXAMPLES.md)。

## 八种技术

| 阶段  | 技术              | 适用场景                                          |
|--------|------------------------|--------------------------------------------------|
| 事前    | 盲点扫描        | 面对新领域或新代码库时的未知的未知     |
| 事前    | 头脑风暴与原型 | 未知的已知——"我见到了才知道是不是它"     |
| 事前    | 访谈              | 头脑风暴之后仍残留的歧义           |
| 事前    | 参考             | 当你无法描述它时——直接指向代码      |
| 事前    | 实现计划    | 提前暴露那些有风险的决策                |
| 事中 | 实现笔记   | 迫使产生偏差的边界情况                |
| 事后   | 推介与讲解      | 争取认可与审批                             |
| 事后   | 测验                   | 合并前确认理解无误               |

每种技术的完整提示词记录在
[`skills/finding-unknowns/SKILL.md`](skills/finding-unknowns/SKILL.md) 中。

## Cartographer 模式

这八种技术是轻量级的探针。Cartographer 模式则是面向高风险工作的严格升级版:
一种门控式访谈,在问题空间被充分绘制清楚之前不允许开始实现。它的灵感来自
[oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) 中的 Deep Interview 技能:
自 v3.6.0 起,它*采纳*了 Deep Interview 的透明化机制——各象限的清晰度评分汇总为
一个加权歧义值并配有可配置阈值、一个 Round 0 拓扑确认环节,以及挑战模式——
同时保留了单纯的清晰度评分式访谈所无法覆盖的那些维度。

<p align="center">
  <img src="assets/cartographer.svg" alt="Cartographer 模式:覆盖度门控、未知台账、遗憾加权的定位" width="96%">
</p>

| 维度              | Deep Interview                          | Cartographer 模式                                                        |
|-------------------|-----------------------------------------|--------------------------------------------------------------------------|
| 门控标准    | 歧义度 ≤ 阈值（目标/约束/评判标准三个维度） | 双重标准:覆盖度（四个象限均已探明,且必须做过盲点扫描）**且**各象限加权歧义度 ≤ 阈值 |
| 盲点（UU）  | 未建模                            | 一等公民;在歧义公式中权重最高（0.30）             |
| 生命周期      | 止步于规格说明阶段                | 一本台账,事前播种、事中追加、事后收尾                     |
| 优先级排序    | 固定的维度权重                 | 遗憾 = 出错代价 × 出错概率,决定各行排序;歧义度对各象限打分 |
| 清除手段 | 仅苏格拉底式问答                     | 按每个未知的类型分别路由:访谈 / 实地核验 / 实验 / 审计——这个循环是一个路由器,而不是一场访谈 |
| 执行交接 | 桥接进入 OMC 流水线              | 需审批放行的桥接:独立的 planner+reviewer 共识评审,或使用带有逐任务反证式验证的 Workflow 执行 |

其核心机制是一本持久化的未知台账（`id · quadrant · cost-if-wrong · P(wrong) ·
regret · route · status · phase`）,其表头记录着清晰度阈值、已锁定的拓扑,以及
逐轮次的象限评分历史。每一轮都会按路由方式清除遗憾值最高的未结行,然后
重新为四个象限打分,并向用户展示评分表——
`ambiguity = 1 − (KK×0.20 + KU×0.25 + UK×0.25 + UU×0.30)`,默认阈值 0.25
（`--quick` 为 0.35 / `--deep` 为 0.15）。只要还有象限未被探明、
任一未结行的 `regret ≥ 1.0`,或歧义度高于阈值,就不允许开始实现;门控 PASS 之后
会固化出一份待审批的规格说明,并交给经过交叉验证的执行桥接。
完整的模式定义与启动提示词见 [`SKILL.md`](skills/finding-unknowns/SKILL.md)。

当宿主环境暴露了 Claude Code 的 **Workflow 工具**（动态工作流）且用户已选择启用编排时,
扇出密集型操作会以确定性脚本的形式运行——多视角扫描配合逐条发现的对抗式验证
（流水线式执行,无阻塞屏障）、针对代价 ≥ 4 的解法的三视角反证评审小组、
仅在连续两轮空手而归后才停止的 UU 探测循环,以及在批准之后,
让每个实现者都配对一名独立的反证式验证者的执行阶段。相关模板与优雅降级梯度见
[`references/workflows.md`](skills/finding-unknowns/references/workflows.md)。

<p align="center">
  <img src="assets/workflows.svg" alt="动态工作流编排:多视角扫描、验证评审小组、UU 循环直至枯竭、降级梯度" width="96%">
</p>

## 与其他工具的关系

`finding-unknowns` 处在与更重型的工作流技能不同的高度上。它是一个
轻量级的定向层,而不是一个执行引擎。

| 属性     | finding-unknowns          | Deep Interview（[OMC](https://github.com/Yeachan-Heo/oh-my-claudecode)） | OMC 执行（autopilot / ralph / team） | [Superpowers](https://github.com/obra/superpowers) |
|--------------|---------------------------|-------------------------|------------------------|------------------------|
| 高度     | 元层面 / 定向          | 单一阶段:需求梳理 | 执行与交付   | 纪律性基元  |
| 生命周期    | 事前 · 事中 · 事后       | 仅事前                | 事中 · 事后                | 大多为单阶段    |
| 严格程度       | 灵活                  | 歧义门控            | 验证门控    | 清单驱动        |
| 状态        | 无状态                 | 持久化,可恢复    | 持久化,多智能体 | 视情况而定                 |
| 最适用场景    | 你还不知道自己有哪些未知 | 你需要一份经过验证的规格说明 | 规格说明已经清晰 | 你需要一次有纪律的动作 |

这些工具是互补而非竞争关系。推荐的做法是先用
`finding-unknowns` 定位一个未知,再升级到合适的专才工具:

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
│   ├── prototype-smith.md  Divergent throwaway prototyping (sonnet)
│   ├── ledger-keeper.md    Regret scoring and coverage-gate verdicts (opus)
│   └── quiz-master.md      Independent examiner (sonnet)
├── docs/
│   └── ARCHITECTURE.md     Design reference: layers, contracts, principles
├── assets/                 README diagrams (SVG)
├── AGENTS.md               Repository guide for coding agents and contributors
├── EXAMPLES.md             Copy-paste, end-to-end prompts
├── CLAUDE.md               Passive single-file drop-in
├── install.sh              Installer (skill + agents + commands)
├── CONTRIBUTING.md         Contribution guidelines
├── CHANGELOG.md            Release history
├── LICENSE                 MIT
├── README.md               English (canonical)
├── README.zh.md            简体中文 translation
├── README.ja.md            日本語 translation
└── README.ko.md            한국어 translation
```

## 贡献

欢迎贡献。请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 获取指南。

## 致谢

- 相关理念与技术命名源自 Thariq Shihipar 的文章 _"A Field Guide to
  Fable: Finding Your Unknowns"_（[@trq212](https://x.com/trq212/status/2073100352921215386)）。
- Cartographer 模式的对比部分参考了
  [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) 中的 Deep Interview 技能,
  以及 [Superpowers](https://github.com/obra/superpowers) 中的相关基元。

## 许可证

基于 MIT 许可证发布。详见 [LICENSE](LICENSE)。

## 免责声明

这是一个独立的社区项目。它与 Anthropic 没有任何关联,未获得 Anthropic 的授权或背书。
