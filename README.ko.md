<p align="center"><a href="README.md">English</a> | <a href="README.zh.md">简体中文</a> | <a href="README.ja.md">日本語</a> | <strong>한국어</strong></p>

<p align="center"><em>이 문서는 영어 README의 번역본입니다. 내용이 다를 경우 영어 버전이 우선합니다.</em></p>

<p align="center">
  <img src="assets/hero.svg" alt="finding-unknowns — Claude Code 스킬" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Skill-8A63D2" alt="Claude Code 스킬">
  <img src="https://img.shields.io/badge/scope-global-5B8DEF" alt="전역 범위">
  <img src="https://img.shields.io/badge/trigger-manual-F59E0B" alt="수동 트리거">
  <img src="https://img.shields.io/badge/covers-pre_%C2%B7_during_%C2%B7_post-2DD4BF" alt="생애주기 전 구간 커버">
  <img src="https://img.shields.io/badge/license-MIT-22C55E" alt="MIT 라이선스">
</p>

<p align="center"><em>지도는 영토가 아니다. 장기 과제의 결과물 품질은 당신이 자신의 <strong>미지수(unknowns)</strong>를 얼마나 잘 규명하느냐에 좌우된다.</em></p>

`finding-unknowns`는 구현 전, 구현 중, 구현 후에 걸쳐 아직 모르는 것을 드러내도록 도와주는
Claude Code 스킬 및 에이전트 프레임워크다. 그렇게 함으로써 모호함은 나중에 값비싼 재작업으로
이어지기 전에 저렴한 질문으로 미리 해소된다. 하나의 오케스트레이팅 스킬이 여덟 가지 발견
기법과 엄격한 게이트 모드를 제공하며, 격리·발산·독립적 판단이 값어치를 하는 지점에서는 네
개의 동반 에이전트가 이 기법들을 뒷받침한다.

> **저작권 표시(Attribution).** 이 스킬은 Thariq Shihipar의 에세이 _"A Field Guide to Fable:
> Finding Your Unknowns"_ ([@trq212](https://x.com/trq212/status/2073100352921215386))를
> 정제한 것이다. 기저 아이디어와 기법 이름에 대한 공로는 원저자에게 있으며, 이 저장소는 그것을
> 설치 가능한 Claude Code 스킬로 패키징한 것일 뿐이다.

---

## 개요

**지도(map)**란 당신이 Claude에게 주는 것(프롬프트, 컨텍스트, 스킬)이다. **영토(territory)**란
실제로 작업이 일어나는 곳(코드베이스와 실세계)이다. 이 둘 사이의 간극은 미지수로 이루어져
있으며, 모든 미지수는 모델이 당신의 의도를 추측하게 만든다.

이 스킬은 작업 생애주기 전반에 걸쳐 그런 미지수를 드러내기 위한 여덟 가지 구체적인 기법과,
고위험 작업을 위한 선택적인 엄격 모드("Cartographer 모드")를 제공한다.

<p align="center">
  <img src="assets/lifecycle.svg" alt="미지수를 포착하는 세 시점: 사전, 도중, 사후" width="92%">
</p>

## 특징

- **4분면 프레이밍** — 행동에 나서기 전에 간극을 기지(known) 또는 미지(unknown)의 미지수로
  분류한다.
- **블라인드 스팟 점검** — 당신 스스로 인지하지 못했던 미지수를, 당신의 맥락에 맞춰 드러낸다.
- **브레인스토밍과 프로토타이핑** — 코드를 확정하기 전에 여러 개의 버릴 수 있는 방향에
  반응해본다.
- **인터뷰** — 한 번에 한 질문씩, 아키텍처를 바꿀 만한 답변을 우선시한다.
- **레퍼런스** — 기존 소스 코드를 가장 풍부한 명세서로 취급한다.
- **구현 계획** — 바뀔 가능성이 가장 높은 결정을 먼저 다룬다.
- **구현 노트** — 빌드 도중 발생한 편차를 나중에 검토할 수 있도록 기록한다.
- **피치와 퀴즈** — 동의를 얻기 위한 리뷰 산출물, 그리고 머지 전 이해도 확인.
- **Cartographer 모드** — 지속되는 원장(ledger)이 뒷받침하는, 모호도 점수화·커버리지 게이트·
  후회 가중치 프로토콜로, 승인 게이트가 걸린 실행 브리지로 마무리된다.
- **동반 에이전트** — 깊이가 값어치를 할 때 스킬이 위임하는 네 명의 전문가
  (`blindspot-scout`, `prototype-smith`, `ledger-keeper`, `quiz-master`).

## 아키텍처

이 프레임워크는 계층화되어 있다 — 커맨드는 디스패치하고, 스킬은 결정하고, 에이전트는
실행하고, 문서는 상태를 보존한다. 절차는 정확히 한 곳(`SKILL.md`)에만 존재하며, 나머지
모든 계층은 그곳으로 진입하거나 그곳의 계약을 이행할 뿐이다. 모든 기법은 단독으로도
동작한다 — 커맨드와 에이전트는 의존 요소가 아니라 향상 요소다. 전체 설계 레퍼런스는
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)를 참고하라.

| 레이어 | 내용 | 역할 |
|-------|----------|------|
| 커맨드 | `/finding-unknowns` `/blindspot` `/cartographer` `/change-quiz` | 얇은 진입점; 스킬 섹션을 지정하고 인자를 전달 |
| 스킬 | `SKILL.md` | 프로토콜: 4분면 라우팅, 여덟 가지 기법, Cartographer 모드, 가드레일 |
| 에이전트 | 네 명의 전문가 | 명시적 입출력 계약을 갖춘 격리된 실행 프로필 |
| 산출물 | 원장, 노트, 프로토타입, 리포트 | 지속되는 상태; 원장이 재개 지점이 된다 |
| 워크플로 | `references/workflows.md` | 팬아웃이 심한 작업을 위한 선택적 동적 워크플로 스크립트; 일반 에이전트나 인라인 실행으로 저하(degrade) 가능 |

<p align="center">
  <img src="assets/framework.svg" alt="프레임워크: 하나의 스킬이 네 명의 전문 에이전트를 오케스트레이션" width="96%">
</p>

| 에이전트 | 모델 | 대응하는 기법 | 실행 프로필 |
|-------|-------|-------|-------------------|
| `blindspot-scout` | sonnet | 블라인드 스팟 점검, 레퍼런스 | 읽기 전용 정찰; 자체 컨텍스트 윈도우 안에서 탐색하며 구조적으로 구현에 착수할 수 없음 |
| `prototype-smith` | inherit | 브레인스토밍 & 프로토타이핑, 구현 계획 | 새로 만들어지는 버릴 수 있는 파일로만 샌드박스화됨; 한 번의 패스로 진짜로 발산하는 N개의 방향을 만들어냄 |
| `ledger-keeper` | inherit | Cartographer 모드 | 미지수 원장을 위한 독립 장부 담당자; 후회를 점수화하고, 분면별 명료도를 가중 모호도 수치로 점수화하며, 자신의 작업을 채점하지 않고 커버리지+모호도 이중 게이트를 판정 |
| `quiz-master` | inherit | 퀴즈, 피치 & 설명 | 변경을 작성하지 않은 신선한 시각의 검토자; 저자라면 대충 넘어갔을 부분을 캐묻는다 |

이 분리는 하나의 원칙을 따른다: **발견, 채점, 검증은 구현을 수행하는 것과 동일한 컨텍스트가
수행해서는 안 된다.** 파일을 편집할 수 없는 정찰병은 구현으로 흘러갈 수 없고, 인터뷰를
진행하지 않은 장부 담당자는 자신의 게이트 판정을 부풀리지 않으며, diff를 작성하지 않은
검토자는 더 날카로운 질문을 던진다.

## 네 개의 분면

미지수가 어디에 위치하는지 찾아라; 분면이 어떤 기법을 써야 할지 알려준다.

<p align="center">
  <img src="assets/quadrants.svg" alt="미지수의 네 분면" width="78%">
</p>

## 요구 사항

- **Claude Code** — CLI, 데스크톱 앱, 또는 IDE 확장. 스킬은 Skill 도구(또는
  `~/.claude/skills/`)를 통해 로드되며, 슬래시 커맨드는 플러그인이나 수동 복사가 필요하다.
- **런타임도, 의존성도 없음.** 스킬, 에이전트, 커맨드는 순수 마크다운이다. 파일을 복사하는
  것 외에 컴파일하거나 설치할 것이 없다.
- **선택적 기능 강화, 모두 우아하게 저하(degrade)됨:** 네 개의 동반 에이전트(깊이가
  값어치를 할 때 위임됨), 그리고 동적 워크플로 오케스트레이션을 위한 Workflow 도구 — 둘 다
  설치되지 않아도 모든 기법이 완전히 인라인으로 동작한다.
- **`bash`** — `install.sh`(옵션 B)에 필요. 옵션 A, C, D는 셸이 필요 없다.

## 설치

**옵션 A — 플러그인 마켓플레이스(권장):**

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
/plugin install finding-unknowns@finding-unknowns-skill
```

**옵션 B — 클론 후 설치:**

```bash
git clone https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill
bash install.sh              # installs the skill and the four companion agents
```

**옵션 C — 수동적 드롭인(설치 불필요):** [`CLAUDE.md`](CLAUDE.md)를 프로젝트 루트에 복사하면
가볍고 상시 작동하는 가이드가 된다.

**옵션 D — 수동 복사:**

```bash
mkdir -p ~/.claude/skills/finding-unknowns/references
cp skills/finding-unknowns/SKILL.md ~/.claude/skills/finding-unknowns/
cp skills/finding-unknowns/references/*.md ~/.claude/skills/finding-unknowns/references/
```

## 업데이트

기존 설치에 최신 릴리스(현재 **v3.6.0**)를 반영하려면, 설치했던 방식에 맞는 경로를 따르라.

**업데이트 옵션 A — 플러그인 마켓플레이스:**

```
/plugin marketplace update finding-unknowns-skill
/plugin update finding-unknowns@finding-unknowns-skill
```

**업데이트 옵션 B — 클론 후 설치:** pull 이후 설치 스크립트를 다시 실행하라. `install.sh`는
제자리에서 덮어쓰므로(스킬, `references/`, 네 개의 에이전트, 슬래시 커맨드) 업데이터 역할도
겸한다.

```bash
cd finding-unknowns-skill
git pull origin main
bash install.sh              # re-copies skill + references + agents + commands
```

**업데이트 옵션 D — 수동 복사:** 동일한 파일을 덮어쓴다(`references/` 디렉터리에는 Workflow
오케스트레이션 템플릿이 들어 있으므로 이것도 함께 업데이트해야 한다).

```bash
cd finding-unknowns-skill && git pull origin main
mkdir -p ~/.claude/skills/finding-unknowns/references
cp skills/finding-unknowns/SKILL.md ~/.claude/skills/finding-unknowns/
cp skills/finding-unknowns/references/*.md ~/.claude/skills/finding-unknowns/references/
cp agents/*.md   ~/.claude/agents/
cp commands/*.md ~/.claude/commands/
```

업데이트 후에는 설치된 버전이 릴리스와 일치하는지 확인하라(이 grep은 업데이트 후 정상성
점검용으로, `doctor` 커맨드의 경량 대체판이다):

```bash
grep '"version"' ~/.claude/plugins/*/finding-unknowns*/.claude-plugin/plugin.json 2>/dev/null \
  || grep -c 'Cross-validated execution bridge' ~/.claude/skills/finding-unknowns/SKILL.md
# expect: 3.6.0 (plugin) — or a non-zero match count confirming the v3.6.0 Phase E section
```

## 설정

이 스킬은 **설정 없이(zero configuration)** 동작한다 — 아래의 모든 옵션은 선택 사항이며
합리적인 기본값을 갖는다.

**명료도 임계값(Cartographer 모드).** 가중 모호도 게이트의 기본값은 `0.25`이다.
프로젝트별 또는 사용자별로 `.claude/settings.json`에서 이를 오버라이드할 수 있다(프로젝트
설정이 사용자 설정보다 우선):

```json
{
  "findingUnknowns": {
    "ambiguityThreshold": 0.25
  }
}
```

Cartographer는 진입 시 확정된 임계값과 그 출처를 알려주므로, 어떤 값이 적용되고 있는지
항상 확인할 수 있다.

**깊이 프리셋.** 커맨드에 붙는 플래그는 설정값보다 우선한다:

| 플래그 | 임계값 | 용도 |
|------|-----------|---------|
| `/cartographer --quick <task>` | 0.35 | 빠른 방향 탐색, 위험도가 낮은 작업 |
| `/cartographer --standard <task>` | 0.25 (기본값) | 대부분의 작업 |
| `/cartographer --deep <task>` | 0.15 | 고위험, 되돌리기 어려운 작업 |

**그 밖의 기본값**(프로토타입 방향 개수, 후회 질문 기준선, 퀴즈 크기와 라운드 수,
Cartographer 라운드 상한, 라운드당 최대 3개의 독립적인 인터뷰 질문)은
[`SKILL.md`](skills/finding-unknowns/SKILL.md) 안의 **Defaults** 표에 문서화되어 있으며,
자연어로 스킬에 지시하는 것만으로 오버라이드할 수 있다.

**모델 라우팅.** OMC(판단에는 opus, 실행에는 sonnet, 폭넓은 탐색에는 haiku)와 Deep
Research(합성의 중심에는 가장 강력한 모델을, 팬아웃에는 더 저렴한 모델을 쓰는 방식)를
따라, 판단·창작을 담당하는 에이전트 — `ledger-keeper`, `prototype-smith`, `quiz-master` —
는 `model: inherit`를 쓴다: 이들은 현재 세션이 이미 사용 중인 모델로 실행되며 절대
다운그레이드되지 않는다(Fable은 Fable로, Opus는 Opus로 남는다). `blindspot-scout`는
정찰이 병렬로 팬아웃되기 때문에 `sonnet`을 그대로 유지한다; 단일 렌즈 패스에서 최고
품질을 원한다면 에이전트 프론트매터에서 이를 `inherit`로 설정하라.

## 사용법

모호하거나 낯선 작업을 시작할 때, Skill 도구를 통해 스킬을 호출하라:

```
finding-unknowns
```

플러그인이 설치되어 있다면, 슬래시 커맨드가 직접적인 진입점을 제공한다:

| 커맨드 | 진입 지점 |
|---------|-----------|
| `/finding-unknowns <task>` | Phase 0 — 분면 라우팅, 이후 해당 기법으로 진입 |
| `/blindspot <goal or area>` | 블라인드 스팟 점검(정찰만 수행) |
| `/cartographer <task>` | Cartographer 모드 — 원장, 점수 게이트 클리어링 루프, 이중 게이트, 실행 브리지 |
| `/change-quiz [diff range]` | 변경 리포트 + 반드시 통과해야 하는 이해도 퀴즈 |

개별 기법은 평이한 언어로도 요청할 수 있다. 예를 들어 _"블라인드 스팟 점검을 해줘"_,
_"나를 인터뷰해줘"_, _"네 가지 방향으로 브레인스토밍해줘"_ 등이다. 그대로 복사해서 쓸 수
있는 프롬프트 전체는 [`EXAMPLES.md`](EXAMPLES.md)를 참고하라.

## 여덟 가지 기법

| 단계  | 기법              | 용도                                          |
|--------|------------------------|--------------------------------------------------|
| 사전    | 블라인드 스팟 점검        | 새로운 도메인이나 코드베이스에서의 미지의 미지수     |
| 사전    | 브레인스토밍 & 프로토타이핑 | 미지의 기지수(Unknown Knowns) — "보면 알 것 같다"     |
| 사전    | 인터뷰              | 브레인스토밍 이후에도 남아 있는 모호함           |
| 사전    | 레퍼런스             | 말로 설명할 수 없을 때 — 코드를 가리켜라      |
| 사전    | 구현 계획    | 위험한 결정을 조기에 드러내기               |
| 도중 | 구현 노트   | 편차를 강제하는 엣지 케이스                |
| 사후   | 피치 & 설명      | 동의와 승인                             |
| 사후   | 퀴즈                   | 머지 전 이해도 확인               |

각 기법에 대한 전체 프롬프트는
[`skills/finding-unknowns/SKILL.md`](skills/finding-unknowns/SKILL.md)에 문서화되어 있다.

## Cartographer 모드

여덟 가지 기법은 가벼운 탐침이다. Cartographer 모드는 고위험 작업을 위한 엄격한 에스컬레이션
단계로, 문제 공간이 충분히 지도화되기 전까지는 구현을 허용하지 않는 게이트가 걸린 인터뷰다.
이는 [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)의 Deep Interview
스킬에서 영감을 받았다: v3.6.0부터는 Deep Interview의 투명성 장치 — 분면별 명료도 점수를
가중 모호도 수치로 합산하는 방식, Round 0 토폴로지 확정, 챌린지 모드 — 를 *채택*하는 동시에,
명료도 점수화 인터뷰만으로는 다루지 못하는 축들은 그대로 유지한다.

<p align="center">
  <img src="assets/cartographer.svg" alt="Cartographer 모드: 커버리지 게이트, 미지수 원장, 후회 가중 타겟팅" width="96%">
</p>

| 축              | Deep Interview                          | Cartographer 모드                                                        |
|-------------------|-----------------------------------------|--------------------------------------------------------------------------|
| 게이트 기준    | 모호도 ≤ 임계값(목표/제약/기준 차원) | 이중 조건: 커버리지(네 분면 모두 탐침 완료, 블라인드 스팟 점검 필수) AND 분면별 가중 모호도 ≤ 임계값 |
| 블라인드 스팟(UU)  | 모델링되지 않음                            | 1급 항목; 모호도 공식에서 가장 높은 가중치(0.30)             |
| 생애주기      | 명세 단계에서 종료                | 하나의 원장, 사전에 시딩, 도중에 추가, 사후에 종료                                     |
| 우선순위 설정    | 고정된 차원 가중치                 | 후회(regret) = 오답 시 비용 × 오답 확률로 행의 순서를 정함; 모호도는 분면을 점수화 |
| 클리어링 수단 | 소크라테스식 Q&A만                     | 미지수별로 경로 유형화됨: 인터뷰 / 현장 검증 / 실험 / 감사 — 이 루프는 인터뷰가 아니라 라우터다 |
| 실행 인계 | OMC 파이프라인으로 연결              | 승인 게이트가 걸린 브리지: 독립적인 planner+reviewer 합의, 또는 태스크별 반증 지향 검증을 갖춘 Workflow 실행 |

그 메커니즘은 지속되는 미지수 원장(`id · quadrant · cost-if-wrong · P(wrong) ·
regret · route · status · phase`)으로, 헤더에는 명료도 임계값, 고정된 토폴로지, 라운드별
분면 점수 이력이 기록된다. 각 라운드는 자신의 경로에 따라 가장 후회가 큰 미해결 행을
클리어한 다음, 네 분면을 모두 다시 점수화하여 사용자에게 점수 표를 보여준다 —
`ambiguity = 1 − (KK×0.20 + KU×0.25 + UK×0.25 + UU×0.30)`, 기본 임계값은 0.25이다
(`--quick`은 0.35 / `--deep`은 0.15). 어느 분면이든 아직 탐침되지 않았거나, 미해결 행 중
하나라도 `regret ≥ 1.0`이거나, 모호도가 임계값을 초과하는 동안에는 구현을 시작할 수 없다;
게이트를 통과(PASS)하면 승인 대기 상태의 명세가 확정되어 교차 검증된 실행 브리지로
넘어간다. 전체 스키마와 착수 프롬프트는 [`SKILL.md`](skills/finding-unknowns/SKILL.md)에
있다.

호스트가 Claude Code의 **Workflow 도구**(동적 워크플로)를 노출하고 사용자가 오케스트레이션을
선택했다면, 팬아웃이 심한 작업은 결정론적 스크립트로 실행된다 — 발견마다 적대적 검증이
붙는(장벽 없이 파이프라인화된) 다중 렌즈 스윕, 비용 ≥ 4인 해소(resolution) 건을 위한 3렌즈 반증 패널,
연속 두 라운드가 소득 없이(dry) 끝나야만 멈추는 UU 탐침 루프, 그리고 모든 구현자에게
독립적인 반증 지향 검증자를 짝지어주는 승인 후 실행. 템플릿과 우아한 폴백 사다리는
[`references/workflows.md`](skills/finding-unknowns/references/workflows.md)에 있다.

<p align="center">
  <img src="assets/workflows.svg" alt="동적 워크플로 오케스트레이션: 다중 렌즈 스윕, 검증 패널, 소득 없을 때까지 도는 UU 루프, 폴백 사다리" width="96%">
</p>

## 다른 도구와의 관계

`finding-unknowns`는 더 무거운 워크플로 스킬들과는 다른 고도에서 작동한다. 이것은 실행
엔진이 아니라 가벼운 방향 설정 계층이다.

| 속성     | finding-unknowns          | Deep Interview ([OMC](https://github.com/Yeachan-Heo/oh-my-claudecode)) | OMC 실행 (autopilot / ralph / team) | [Superpowers](https://github.com/obra/superpowers) |
|--------------|---------------------------|-------------------------|------------------------|------------------------|
| 고도     | 메타 / 방향 설정          | 한 단계: 요구사항 | 실행 & 딜리버리   | 원칙 프리미티브  |
| 생애주기    | 사전 · 도중 · 사후       | 사전만                | 도중 · 사후    | 대부분 단일 단계    |
| 엄격도       | 유연함                  | 모호도 게이팅            | 검증 게이팅   | 체크리스트 기반        |
| 상태        | 상태 없음(stateless)                 | 지속·재개 가능    | 지속, 멀티 에이전트 | 다양함                 |
| 적합한 상황    | 자신의 미지수가 무엇인지도 아직 모를 때 | 검증된 명세가 필요할 때 | 명세가 이미 명확할 때 | 하나의 원칙적인 조치가 필요할 때 |

이 도구들은 경쟁 관계가 아니라 상호 보완적이다. 권장하는 패턴은 `finding-unknowns`로
미지수를 위치시킨 다음, 적절한 전문 도구로 에스컬레이션하는 것이다:

```
finding-unknowns  (orient: which quadrant is this unknown in?)
        ├─ a light reframe is sufficient          → the eight techniques
        ├─ high-stakes, want a coverage gate       → Cartographer mode (this skill)
        ├─ want ambiguity gating + resumable state → OMC Deep Interview
        ├─ divergent option generation             → superpowers:brainstorming
        ├─ a rigorous written plan                 → superpowers:writing-plans / omc-plan
        └─ the specification is already concrete    → OMC autopilot / ralph / team
```

## 프로젝트 구조

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

## 기여하기

기여를 환영한다. 가이드라인은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참고하라.

## 감사의 말

- 아이디어와 기법 이름은 Thariq Shihipar의 에세이 _"A Field Guide to Fable: Finding Your
  Unknowns"_ ([@trq212](https://x.com/trq212/status/2073100352921215386))에서 비롯되었다.
- Cartographer 모드 비교는 [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)의
  Deep Interview 스킬과 [Superpowers](https://github.com/obra/superpowers)의 원칙들을
  참조한다.

## 라이선스

MIT 라이선스로 배포된다. [LICENSE](LICENSE)를 참고하라.

## 면책 조항

이것은 독립적인 커뮤니티 프로젝트다. Anthropic과 제휴 관계가 없으며, Anthropic의 승인이나
보증을 받지 않았다.
