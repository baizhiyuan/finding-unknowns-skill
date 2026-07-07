<p align="center"><a href="README.md">English</a> | <a href="README.zh.md">简体中文</a> | <strong>日本語</strong> | <a href="README.ko.md">한국어</a></p>

<p align="center"><em>本書は英語版 README の翻訳です。内容に相違がある場合は英語版が優先されます。</em></p>

<p align="center">
  <img src="assets/hero.svg" alt="finding-unknowns — Claude Code スキル" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Skill-8A63D2" alt="Claude Code スキル">
  <img src="https://img.shields.io/badge/scope-global-5B8DEF" alt="グローバルスコープ">
  <img src="https://img.shields.io/badge/trigger-manual-F59E0B" alt="手動トリガー">
  <img src="https://img.shields.io/badge/covers-pre_%C2%B7_during_%C2%B7_post-2DD4BF" alt="ライフサイクル">
  <img src="https://img.shields.io/badge/license-MIT-22C55E" alt="MITライセンス">
</p>

<p align="center"><em>地図は領土ではない。長期にわたる作業の質は、自分の<strong>未知</strong>をどれだけ明確にできるかによって決まる。</em></p>

`finding-unknowns` は、実装の前・最中・後を通じて、あなたがまだ気づいていないことを浮かび上がらせる
ための Claude Code スキル・エージェントフレームワークです。曖昧さを、後になって高くつく手戻りでは
なく、早い段階での安価な質問によって解消することを目指します。単一のオーケストレーションスキルが
8つの発見手法と厳格なゲート付きモードを提供し、隔離・発散・独立した判断が効果を発揮する場面では、
4つの補助エージェントがこれらの手法を支えます。

> **謝辞(Attribution)。** 本スキルは、Thariq Shihipar 氏のエッセイ _"A Field Guide to Fable:
> Finding Your Unknowns"_ ([@trq212](https://x.com/trq212/status/2073100352921215386)) の内容を
> 蒸留したものです。背景にある考え方および各手法の名称に関する功績は原著者に帰属し、本リポジトリは
> それらをインストール可能な Claude Code スキルとしてパッケージ化したものです。

---

## 概要

**地図(map)** とは、あなたが Claude に与えるもの(プロンプト、コンテキスト、スキル)です。**領土
(territory)** とは、実際に作業が行われる場所(コードベースと現実世界)です。両者の間のギャップは
未知によって構成されており、未知が一つあるごとにモデルはあなたの意図を推測せざるを得なくなります。

本スキルは、タスクのライフサイクル全体でこうした未知を浮かび上がらせるための8つの具体的な手法に
加え、リスクの高い作業向けに任意で利用できる厳格モード(「Cartographer モード」)を提供します。

<p align="center">
  <img src="assets/lifecycle.svg" alt="未知を捉える3つの窓: 事前・最中・事後" width="92%">
</p>

## 機能

- **四象限フレーミング** — 行動する前に、ギャップを既知の未知か未知の未知として分類する。
- **ブラインドスポット・パス** — 自分でも気づいていなかった未知を、コンテキストに合わせて浮かび上
  がらせる。
- **ブレインストーミング&プロトタイピング** — コードを確定させる前に、複数の使い捨ての方向性に
  対して反応する。
- **インタビュー** — 一度に一つの質問で、アーキテクチャを変え得る回答を優先する。
- **リファレンス** — 既存のソースコードを、入手可能な最も豊富な仕様書として扱う。
- **実装計画** — 変わる可能性が最も高い意思決定から着手する。
- **実装メモ** — ビルド中に生じた逸脱を、後のレビューのために記録する。
- **ピッチ&クイズ** — 合意形成のためのレビュー成果物と、マージ前の理解度チェック。
- **Cartographer モード** — 永続的な台帳(ledger)に支えられた、曖昧さスコアリング・カバレッジ
  ゲート・後悔重み付けのプロトコルで、承認ゲート付きの実行ブリッジで終わる。
- **補助エージェント** — 深さが効果を発揮する場面でスキルが委譲する4人の専門家(`blindspot-scout`、
  `prototype-smith`、`ledger-keeper`、`quiz-master`)。

## アーキテクチャ

本フレームワークは層構造になっています — コマンドがディスパッチし、スキルが判断し、エージェントが
実行し、ドキュメントが永続化します。手順(プロシージャ)は唯一 `SKILL.md` にのみ存在し、他のすべて
の層はそこに入るか、そこからの契約を実行するかのいずれかです。すべての手法は単体でも機能します —
コマンドとエージェントは依存関係ではなく拡張です。設計の全体的なリファレンスについては
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) を参照してください。

| レイヤー | 内容 | 役割 |
|-------|----------|------|
| コマンド | `/finding-unknowns` `/blindspot` `/cartographer` `/change-quiz` | 薄いエントリーポイント。スキルのセクションを指定し、引数を渡す |
| スキル | `SKILL.md` | プロトコル本体: 四象限ルーティング、8つの手法、Cartographer モード、ガードレール |
| エージェント | 4人の専門家 | 明示的な入出力契約を持つ、独立した実行プロファイル |
| 成果物(Artifacts) | 台帳(ledger)、メモ、プロトタイプ、レポート | 永続化された状態。台帳が再開ポイントとなる |
| ワークフロー | `references/workflows.md` | ファンアウトの多い操作向けの、任意のダイナミックワークフロー・スクリプト。未導入時はプレーンなエージェントまたはインラインに縮退する |

<p align="center">
  <img src="assets/framework.svg" alt="フレームワーク: 1つのスキルが4人の専門エージェントをオーケストレーションする" width="96%">
</p>

| エージェント | モデル | 対応する手法 | 実行プロファイル |
|-------|-------|-------|-------------------|
| `blindspot-scout` | sonnet | ブラインドスポット・パス、リファレンス | 読み取り専用の偵察。自身のコンテキストウィンドウ内で探索し、構造上実装を開始できない |
| `prototype-smith` | inherit | ブレインストーミング&プロトタイピング、実装計画 | 新規の使い捨てファイルにサンドボックス化されている。1回のパスで真に発散したN個の方向性を生み出す |
| `ledger-keeper` | inherit | Cartographer モード | 未知の台帳を独立して管理する記帳係。後悔(regret)をスコアリングし、象限ごとの明瞭度を重み付き曖昧さスコアへと変換し、自らの作業を採点することなくカバレッジ+曖昧さの二重ゲートを判定する |
| `quiz-master` | inherit | クイズ、ピッチ&解説 | 変更を作成していない、先入観のない試験官。作成者が見落としがちな点を突く |

この分離は一つの原則に従っています。**発見・採点・検証は、実装を行うのと同じコンテキストで行っては
ならない。** ファイルを編集できないスカウトは、構築作業に踏み込みようがありません。インタビューを
行っていない記帳係は、ゲート判定を甘くすることがありません。差分を書いていない試験官は、より厳しい
質問を投げかけます。

## 四つの象限

未知がどこに存在するかを特定します。象限によって、使うべき手法が決まります。

<p align="center">
  <img src="assets/quadrants.svg" alt="未知の四象限" width="78%">
</p>

## 必要条件

- **Claude Code** — CLI、デスクトップアプリ、または IDE 拡張機能。スキルは Skill ツール(または
  `~/.claude/skills/`)経由で読み込まれます。スラッシュコマンドを使うにはプラグインまたは手動コピー
  が必要です。
- **ランタイム不要、依存関係なし。** スキル、エージェント、コマンドはすべて素の Markdown です。
  ファイルをコピーする以外に、コンパイルやインストールは一切必要ありません。
- **任意の拡張機能はすべて緩やかに縮退します:** 4つの補助エージェント(深さが効果を発揮する場面で
  委譲される)と、ダイナミックワークフロー・オーケストレーション用の Workflow ツール — どちらも
  導入していなくても、すべての手法は完全にインラインで動作します。
- **`bash`**: `install.sh`(オプションB)に必要。オプションA、C、Dはシェル不要です。

## インストール

**オプションA — プラグインマーケットプレイス(推奨):**

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
/plugin install finding-unknowns@finding-unknowns-skill
```

**オプションB — クローンしてインストール:**

```bash
git clone https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill
bash install.sh              # installs the skill and the four companion agents
```

**オプションC — パッシブなドロップイン(インストール不要):** [`CLAUDE.md`](CLAUDE.md) を
プロジェクトのルートにコピーするだけで、軽量かつ常時有効なガイダンスが得られます。

**オプションD — 手動コピー:**

```bash
mkdir -p ~/.claude/skills/finding-unknowns/references
cp skills/finding-unknowns/SKILL.md ~/.claude/skills/finding-unknowns/
cp skills/finding-unknowns/references/*.md ~/.claude/skills/finding-unknowns/references/
```

## アップデート

既存のインストールに最新リリース(現在 **v3.6.0**)を取り込むには、インストール方法に応じた手順を
使用してください。

**アップデート オプションA — プラグインマーケットプレイス:**

```
/plugin marketplace update finding-unknowns-skill
/plugin update finding-unknowns@finding-unknowns-skill
```

**アップデート オプションB — クローンしてインストール:** pull した後にインストーラーを再実行して
ください。`install.sh` はその場で上書きする(スキル、`references/`、4つのエージェント、スラッシュ
コマンド)ため、アップデーターとしても機能します。

```bash
cd finding-unknowns-skill
git pull origin main
bash install.sh              # re-copies skill + references + agents + commands
```

**アップデート オプションD — 手動コピー:** 同じファイルを上書きしてください(`references/` ディレ
クトリには Workflow オーケストレーションのテンプレートが含まれており、これも更新する必要があります)。

```bash
cd finding-unknowns-skill && git pull origin main
mkdir -p ~/.claude/skills/finding-unknowns/references
cp skills/finding-unknowns/SKILL.md ~/.claude/skills/finding-unknowns/
cp skills/finding-unknowns/references/*.md ~/.claude/skills/finding-unknowns/references/
cp agents/*.md   ~/.claude/agents/
cp commands/*.md ~/.claude/commands/
```

アップデート後は、インストールされたバージョンがリリースと一致していることを確認してください
(この grep はアップデート後の健全性チェックであり、`doctor` コマンドの簡易版に相当します):

```bash
grep '"version"' ~/.claude/plugins/*/finding-unknowns*/.claude-plugin/plugin.json 2>/dev/null \
  || grep -c 'Cross-validated execution bridge' ~/.claude/skills/finding-unknowns/SKILL.md
# expect: 3.6.0 (plugin) — or a non-zero match count confirming the v3.6.0 Phase E section
```

## 設定

本スキルは**設定不要(ゼロコンフィグ)**で動作します — 以下のすべての項目は任意であり、適切な
デフォルト値が設定されています。

**明瞭度しきい値(Cartographer モード)。** 重み付き曖昧さゲートのデフォルトは `0.25` です。
プロジェクト単位またはユーザー単位で `.claude/settings.json` により上書きできます(プロジェクト
設定がユーザー設定より優先されます):

```json
{
  "findingUnknowns": {
    "ambiguityThreshold": 0.25
  }
}
```

Cartographer は開始時に、確定したしきい値とその出所を通知するため、常にどの値が有効になっているか
を確認できます。

**深さのプリセット。** コマンドに付与するフラグは、設定値より優先されます:

| フラグ | しきい値 | 用途 |
|------|-----------|---------|
| `/cartographer --quick <task>` | 0.35 | 素早い状況把握、リスクの低い作業 |
| `/cartographer --standard <task>` | 0.25(デフォルト) | ほとんどのタスク |
| `/cartographer --deep <task>` | 0.15 | リスクが高く、後戻りしにくい作業 |

**その他のデフォルト値**(プロトタイプの方向性数、後悔(regret)の質問バー、クイズの規模とラウンド
数、Cartographer のラウンド上限、1ラウンドあたり最大3つの独立したインタビュー質問)は、
[`SKILL.md`](skills/finding-unknowns/SKILL.md) 内の **Defaults** テーブルに記載されており、平易な
言葉でスキルに伝えることで上書きできます。

**モデルルーティング。** OMC(判断には opus、実行には sonnet、幅広さには haiku)および Deep
Research(統合の中心には最強のモデル、ファンアウトには安価なモデル)にならい、判断・創造を担う
エージェント — `ledger-keeper`、`prototype-smith`、`quiz-master` — は `model: inherit` を使用
します。これらは、そのセッションが既に使用しているモデルで動作し、決して格下げされることはありません
(Fable なら Fable のまま、Opus なら Opus のまま)。`blindspot-scout` は `sonnet` のままです。これは
偵察が並列にファンアウトするためです。単一レンズで最大品質のパスを得たい場合は、そのエージェントの
frontmatter で `inherit` に設定してください。

## 使い方

曖昧なタスクや不慣れなタスクに着手する際は、まず Skill ツール経由で本スキルを呼び出してください:

```
finding-unknowns
```

プラグインをインストールしている場合、スラッシュコマンドが直接のエントリーポイントを提供します:

| コマンド | 開始位置 |
|---------|-----------|
| `/finding-unknowns <task>` | フェーズ0 — 四象限ルーティングの後、該当する手法へ |
| `/blindspot <goal or area>` | ブラインドスポット・パス(偵察のみ) |
| `/cartographer <task>` | Cartographer モード — 台帳、スコアゲート付きクリアリングループ、二重ゲート、実行ブリッジ |
| `/change-quiz [diff range]` | 変更レポート + 必須の理解度クイズ |

個々の手法は、平易な言葉でリクエストすることもできます。例えば _"do a blind-spot pass"_、
_"interview me"_、_"brainstorm four directions"_ のようにです。そのままコピー&ペーストできる
完全なプロンプトについては [`EXAMPLES.md`](EXAMPLES.md) を参照してください。

## 8つの手法

| フェーズ | 手法 | 用途 |
|--------|------------------------|--------------------------------------------------|
| 事前 | ブラインドスポット・パス | 新しいドメインやコードベースにおける未知の未知(unknown unknowns) |
| 事前 | ブレインストーミング&プロトタイピング | 未知の既知(unknown knowns) — 「見ればわかる」というもの |
| 事前 | インタビュー | ブレインストーミング後に残る曖昧さ |
| 事前 | リファレンス | 言葉で説明できないとき — コードを指し示す |
| 事前 | 実装計画 | リスクの高い意思決定を早期に洗い出す |
| 最中 | 実装メモ | 逸脱を強いるエッジケース |
| 事後 | ピッチ&解説 | 合意形成と承認 |
| 事後 | クイズ | マージ前の理解確認 |

各手法の完全なプロンプトは [`skills/finding-unknowns/SKILL.md`](skills/finding-unknowns/SKILL.md)
に記載されています。

## Cartographer モード

8つの手法は軽量な探りです。Cartographer モードは、リスクの高い作業のための厳格なエスカレーション
手段であり、問題空間が十分にマッピングされるまで実装を許可しないゲート付きインタビューです。これは
[oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) の Deep Interview スキルに
着想を得たものです。v3.6.0以降では、Deep Interview の透明性の仕組み — 設定可能なしきい値を持つ
重み付き曖昧さスコアへと集約される象限ごとの明瞭度スコア、ラウンド0のトポロジー確認、チャレンジ
モード — を*取り入れ*つつ、明瞭度スコアリングのインタビューだけでは対応できない軸を維持しています。

<p align="center">
  <img src="assets/cartographer.svg" alt="Cartographer モード: カバレッジゲート、未知の台帳、後悔重み付けターゲティング" width="96%">
</p>

| 軸 | Deep Interview | Cartographer モード |
|-------------------|-----------------------------------------|--------------------------------------------------------------------------|
| ゲート判定基準 | 曖昧さ ≤ しきい値(goal/constraint/criteria の各次元) | 二重: カバレッジ(4象限すべてを探索済み、ブラインドスポット・パス必須)AND 象限ごとの重み付き曖昧さ ≤ しきい値 |
| ブラインドスポット(UU) | モデル化されない | ファーストクラスの扱い。曖昧さ式の中で最も重い重み(0.30) |
| ライフサイクル | 仕様策定で終了 | 単一の台帳を事前にシードし、最中に追記し、事後にクローズする |
| 優先順位付け | 固定された次元の重み | 後悔(regret)= cost-if-wrong × P(wrong) で各行を順序付け。曖昧さは象限をスコアリングする |
| クリアリング手段 | ソクラテス式Q&Aのみ | 未知ごとにルートを型付け: interview / territory-verify / experiment / audit — このループはインタビューではなくルーターである |
| 実行への引き渡し | OMCパイプラインへブリッジする | 承認ゲート付きブリッジ: 独立したプランナー+レビューアーによる合意形成、またはタスクごとに反証形式の検証を伴う Workflow 実行 |

この仕組みの中核は、永続的な未知の台帳(`id · quadrant · cost-if-wrong · P(wrong) · regret · route ·
status · phase`)であり、そのヘッダーには明瞭度のしきい値、確定したトポロジー、そしてラウンドごとの
象限スコア履歴が記録されます。各ラウンドでは、最も後悔(regret)の大きい未クローズの行を、その行に
割り当てられたルートに沿ってクリアし、その後4象限すべてを再スコアリングして、ユーザーにスコア表を
提示します — `ambiguity = 1 − (KK×0.20 + KU×0.25 + UK×0.25 + UU×0.30)`、しきい値はデフォルトで
0.25です(`--quick` は0.35 / `--deep` は0.15)。いずれかの象限が未探索である間、`regret ≥ 1.0` の
未クローズ行が存在する間、あるいは曖昧さがしきい値を上回っている間は、実装を開始することはできま
せん。ゲートが PASS すると、承認待ちの仕様が確定し、それが相互検証された実行ブリッジへと引き渡され
ます。完全なスキーマとキックオフ用プロンプトは [`SKILL.md`](skills/finding-unknowns/SKILL.md) に
あります。

ホスト環境が Claude Code の**Workflow ツール**(ダイナミックワークフロー)を公開しており、ユーザーが
オーケストレーションを有効にしている場合、ファンアウトの多い操作は決定的なスクリプトとして実行され
ます — 所見ごとの敵対的検証を伴うマルチレンズ・スイープ(パイプライン化され、バリアなし)、コスト
≥ 4 の解決に対する3レンズ反証パネル、連続2ラウンドの「空振り」が出て初めて停止する UU 探索ループ、
そして各実装者に独立した反証形式の検証者を組み合わせる承認後の実行、です。テンプレートと段階的な
フォールバックの梯子は [`references/workflows.md`](skills/finding-unknowns/references/workflows.md)
にあります。

<p align="center">
  <img src="assets/workflows.svg" alt="ダイナミックワークフロー・オーケストレーション: マルチレンズ・スイープ、検証パネル、UUループ(空振りまで)、フォールバックの梯子" width="96%">
</p>

## 他のツールとの関係

`finding-unknowns` は、より重量級のワークフロースキルとは異なる高度で動作します。これは実行エンジン
ではなく、軽量な方向付けのレイヤーです。

| 性質 | finding-unknowns | Deep Interview([OMC](https://github.com/Yeachan-Heo/oh-my-claudecode)) | OMC execution(autopilot / ralph / team) | [Superpowers](https://github.com/obra/superpowers) |
|--------------|---------------------------|-------------------------|------------------------|------------------------|
| 高度 | メタ/方向付け | 単一フェーズ: 要件定義 | 実行と提供 | 規律のプリミティブ |
| ライフサイクル | 事前・最中・事後 | 事前のみ | 最中・事後 | ほぼ単一フェーズ |
| 厳密さ | 柔軟 | 曖昧さゲーティング | 検証ゲート付き | チェックリスト駆動 |
| 状態 | ステートレス | 永続化、再開可能 | 永続化、マルチエージェント | 様々 |
| 最適な場面 | 自分の未知がまだわかっていないとき | 検証済みの仕様が必要なとき | 仕様がすでに明確なとき | 一つの規律ある動きが必要なとき |

これらのツールは競合するものではなく、補完し合うものです。推奨されるパターンは、まず
`finding-unknowns` を使って未知の所在を特定し、その後、適切な専門ツールへとエスカレーションする
ことです:

```
finding-unknowns  (orient: which quadrant is this unknown in?)
        ├─ a light reframe is sufficient          → the eight techniques
        ├─ high-stakes, want a coverage gate       → Cartographer mode (this skill)
        ├─ want ambiguity gating + resumable state → OMC Deep Interview
        ├─ divergent option generation             → superpowers:brainstorming
        ├─ a rigorous written plan                 → superpowers:writing-plans / omc-plan
        └─ the specification is already concrete    → OMC autopilot / ralph / team
```

## プロジェクト構成

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

## コントリビューション

貢献を歓迎します。ガイドラインについては [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

## 謝辞

- 考え方および各手法の名称は、Thariq Shihipar 氏のエッセイ _"A Field Guide to Fable: Finding Your
  Unknowns"_ ([@trq212](https://x.com/trq212/status/2073100352921215386)) に由来します。
- Cartographer モードの比較は、[oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)
  の Deep Interview スキル、および [Superpowers](https://github.com/obra/superpowers) の
  プリミティブを参照しています。

## ライセンス

MIT ライセンスの下で公開されています。詳細は [LICENSE](LICENSE) を参照してください。

## 免責事項

これは独立したコミュニティプロジェクトです。Anthropic とは提携しておらず、その許可や支持を受けた
ものでもありません。
