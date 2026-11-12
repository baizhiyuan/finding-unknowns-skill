#!/usr/bin/env python3
"""5.2 diagrams in the 4.x style.

Usage: python3 scripts/diagrams/gen5.py .   (from the repo root), then outline the Chinese
sources: python3 scripts/outline_cjk.py --fonts DIR --out assets/zh assets/zh/src/*.svg
Six diagrams per language: hero, lifecycle, framework (four layers), card, stop-points,
debrief. The 4.x quadrant and Cartographer diagrams belong to branch v4."""
from __future__ import annotations

import subprocess
import sys
from style import *  # noqa: F403

ROOT = sys.argv[1]
VERSION = "v5.2.0"


def L(zh):
    return lambda en, cn: cn if zh else en


def spaced(zh):
    return None if zh else "1.5"


# ---------------------------------------------------------------- hero ----------
def hero(zh):
    T = L(zh)
    old = subprocess.run(["git", "show", "v4.3.2:assets/hero.svg"], cwd=ROOT, capture_output=True, text=True, check=True).stdout  # 4.x map art
    art = old[old.index("<g clip-path=\"url(#frame)\">"): old.index("</g>\n<text x=\"56\" y=\"70\"") + 5]
    defs = old[old.index("<defs>"): old.index("</defs>") + 7]
    f = Fig(1200, 420, f"finding-unknowns {VERSION}",
            T("Banner: a pin clearing fog on a dotted map. You predict first, the agent builds quietly and stops only at four points, and the completion report grades every prediction.",
              "横幅：地图上的定位针拨开迷雾。你先预测，智能体安静执行，只在四种情况下打断你，完成报告逐条评判每一条预测。"), zh)
    f.mono(56, 70, T(f"[ CLAUDE CODE PLUGIN · {VERSION} ]", f"[ CLAUDE CODE 插件 · {VERSION} ]"), 15, ACC, "700", spacing=spaced(zh))
    f.text(54, 152, "finding-unknowns", 64, INK, SERIF, "700")
    f.text(56, 198, T("You predict first. The agent builds quietly.", "你先预测，智能体再安静地执行。"), 20, INK, SANS)
    f.text(56, 226, T("The completion report grades every prediction.", "完成报告逐条评判每一条预测。"), 20, SUB, SANS)
    x = 56
    for t in T(["task card", "4 stop-points", "report = debrief"], ["任务卡", "4 个打断点", "完成报告即复盘"]):
        x = f.pill(x, 262, t, PINK, ORG, ACC, 14, 30) + 10
    x = 56
    for t in T(["guard hook", "fu script", "1 auditor"], ["防护钩子", "fu 脚本", "1 个评判子代理"]):
        x = f.pill(x, 300, t, PINK, ORG, ACC, 14, 30) + 10
    f.rect(56, 352, 520, 40, PANEL, EDGE, 1, 8)
    f.raw('<circle cx="76" cy="372" r="4" fill="#B5442E"/><circle cx="92" cy="372" r="4" fill="#D4A27F"/><circle cx="108" cy="372" r="4" fill="#788C5D"/>')
    f.mono(128, 377, "$", 14, ORG)
    f.mono(144, 377, '/fu-brief "make the export job resumable"', 14, INK)
    s = f.svg()
    s = s.replace(s[s.index("<defs>"): s.index("</defs>") + 7], defs)
    s = s.replace('<rect x="0.5" y="0.5" width="1199" height="419" rx="18" fill="url(#dots)" opacity="0.5"/>\n', art + "\n")
    return s


# ---------------------------------------------------------------- lifecycle -----
def lifecycle(zh):
    T = L(zh)
    f = Fig(1200, 660, T("How a carded task runs", "一张任务卡的流程"),
            T("A Brief before the build, a quiet build that stops only at four points, and a completion report that is the Debrief; a catch-up when you come back.",
              "动手前做简报，执行时只在四个打断点停下，完成报告即复盘；中途回来时先回顾。"), zh)
    f.header(T("// 01 · HOW A CARD RUNS", "// 01 · 任务卡的流程"), T("Predict before the build, grade in the report", "动手前先预测，完成报告里评判"),
             T("Both predictions are frozen before the work, so the completion report can grade them against what happened.",
               "双方的预测在动手前冻结，完成报告才能对照实际结果逐条评判。"))
    f.human(40, 150, 548, T("YOU · predict first, answer once, approve the Brief", "你：先预测，一次答完问题，确认简报"))
    f.human(612, 150, 548, T("YOU · answer at a stop, read the report", "你：在打断点作答，阅读完成报告"))
    for lx in (171, 457, 743, 1029):
        f.line(lx, 178, lx, 192, INK, 1.5, "3 3")
    cols = [
        (T("BRIEF", "简报"), "/fu-brief", T("before the build", "动手前"),
         [("1", T("You predict first", "你先预测")), ("2", T("What only you decide", "只问由你决定的事")),
          ("3", T("Then the agent predicts", "再由智能体预测")), ("4", T("Stop-points + contract", "打断点与验收标准")),
          ("5", T("One yes, then frozen", "确认一次后冻结"))]),
        (T("BUILD", "安静执行"), "", T("quietly", "执行中"), None),
        (T("CATCH-UP", "回顾"), "/fu-catch-up", T("next session", "下次会话"),
         [("1", T("Only what changed", "只看上次之后的变化")), ("2", T("What needs you", "需要你决定的事")),
          ("3", T("Recall only on request", "回忆性问题仅在要求时提"))]),
        (T("DEBRIEF", "复盘"), T("= the completion report", "= 完成报告"), T("after the work", "完成后"), None),
    ]
    xs = [40, 326, 612, 898]
    for i, ((name, cmd, when, items), x) in enumerate(zip(cols, xs)):
        f.topband(x, 192, 262, 320, ORG if i != 1 else GRN)
        f.serif(x + 18, 232, name, 21)
        f.mono(x + 244, 232, when, 12, SUB, anchor="end")
        if cmd:
            f.mono(x + 18, 256, cmd, 13, ACC, "700")
        if items:
            for k, (n, t) in enumerate(items):
                y = 274 + k * 42
                f.badge(x + 18, y, n, size=26)
                f.text(x + 56, y + 18, t, 14, INK, SANS, "600")
        if i < 3:
            f.arrow(x + 264, 352, x + 284, 352)
    # quiet build column
    x = 326
    f.text(x + 18, 266, T("Stops only for:", "只在以下情况打断你："), 14, INK, SANS, "600")
    for k, t in enumerate(T(["irreversible step", "scope change", "dead premise", "budget overrun"],
                            ["不可逆操作", "范围变化", "前提失效", "预算超支"])):
        f.raw(f'<circle cx="{x + 24}" cy="{288 + k * 26}" r="4" fill="{ORG}"/>')
        f.text(x + 36, 293 + k * 26, t, 14, INK, SANS)
    f.rect(x + 16, 404, 230, 92, "#FFFFFF", EDGE, 1, 10)
    f.text(x + 30, 428, T("Everything else:", "其余情况："), 13, GRN, SANS, "700")
    f.text(x + 30, 450, T("most reversible option,", "选最容易撤回的做法，"), 13, SUB, SANS)
    f.text(x + 30, 470, T("one line in the deltas file", "在增量记录中记一行"), 13, SUB, SANS)
    f.mono(x + 30, 488, "D4 surprise: … → logs/r3", 11, MUTE)
    # debrief column
    x = 898
    f.rect(x + 16, 270, 230, 64, "#FFFFFF", ORG, 1.5, 10)
    f.mono(x + 30, 294, "mechanism-auditor", 13, INK, "700")
    f.text(x + 30, 318, T("fresh context, used narrowly", "新上下文，只在少数场合使用"), 13, SUB, SANS)
    for k, t in enumerate(T(["Evidence first", "Graded, yours first", "Integrity · did NOT prove", "Bottom line · needs you"],
                            ["证据在前", "逐条评判，先评你的", "完整性 · 不能证明什么", "结论 · 需要你决定的事"])):
        f.raw(f'<circle cx="{x + 24}" cy="{360 + k * 32}" r="4" fill="{ORG}"/>')
        f.text(x + 38, 365 + k * 32, t, 14, INK, SANS)
    # card bar
    f.rect(40, 534, 1120, 96, "#F5DDD1", "#F5DDD1", 1, 10)
    f.raw(f'<rect x="40" y="534" width="5" height="96" rx="2.5" fill="{ORG}"/>')
    f.raw(f'<rect x="60" y="548" width="290" height="28" rx="14" fill="{ORG}"/>')
    f.mono(205, 567, ".finding-unknowns/tasks/{slug}.md", 13, INK, "700", "middle")
    f.text(370, 567, T("Persists across sessions; fu freeze commits it, so git shows the predictions came first.",
                       "任务卡跨会话保留，由 fu freeze 提交，提交记录可证明预测写在结果之前。"), 14, INK, SANS)
    f.raw(f'<rect x="60" y="590" width="290" height="28" rx="14" fill="#FFFFFF" stroke="{ORG}" stroke-width="1.2"/>')
    f.mono(205, 609, T("VIEWS", "视图"), 13, ACC, "700", "middle")
    f.text(370, 609, T("Terminal: nested lists, always. HTML view: offered for complex tasks, inside the Brief approval.",
                       "终端：始终是嵌套列表。HTML 视图：复杂任务在确认简报时附带询问。"), 14, INK, SANS)
    return f.svg()


# ---------------------------------------------------------------- framework -----
def framework(zh):
    T = L(zh)
    f = Fig(1200, 1110, T("Four layers", "四层结构"),
            T("Four layers: always-on text; the guard hook and the fu script; the card skill and its commands; one auditor. Every file lands under .finding-unknowns/.",
              "四层结构：常驻说明；防护钩子与 fu 脚本；任务卡技能及其命令；一个评判子代理。所有文件都在 .finding-unknowns/ 下。"), zh)
    f.header(T("// 02 · ARCHITECTURE", "// 02 · 架构"), T("Four thin layers, one always loaded", "四个薄层，只有一层始终加载"),
             T("Sized by what Stage 0 measured: words where they earned their cost, code where a rule can be checked.",
               "按第 0 阶段的测量结果确定分量：文字只用在值得的地方，能检查的规则交给代码。"))

    def layer(y, h, n, name, sub, accent):
        f.card(40, y, 1120, h, accent=accent, fill=PANEL, stroke=EDGE, sw=1.2)
        f.badge(62, y + 18, n, dark=True, size=30)
        f.serif(104, y + 40, name, 19)
        f.text(62, y + 70, sub, 13, SUB, SANS)

    # L1
    layer(156, 104, "1", T("Always-on text", "常驻说明"), T("about 75 tokens per session", "每个会话约 75 个 token"), ORG)
    f.rect(330, 172, 400, 72, PINK, ORG, 1.2, 10)
    f.mono(350, 200, T("CLAUDE.md · 56 words", "CLAUDE.md · 56 个词"), 14, INK, "700")
    f.text(350, 226, T("measured in Stage 0 · the recommended setup", "第 0 阶段测过 · 推荐配置"), 13, SUB, SANS)
    f.rect(746, 172, 394, 72, PAPER, SAND, 1.2, 10, dash="5 4")
    f.mono(766, 200, T("CLAUDE.next.md · 82 words", "CLAUDE.next.md · 82 个词"), 14, ACC, "700")
    f.text(766, 226, T("candidate · untested until Tier 1", "候选版本 · Tier 1 检验前未经检验"), 13, SUB, SANS)
    # L2
    layer(276, 214, "2", T("Guard hook + fu script", "防护钩子与 fu 脚本"), T("no model tokens to carry", "无需模型加载"), RED)
    f.rect(330, 292, 400, 182, "#FFFFFF", EDGE, 1, 10)
    f.mono(350, 318, "hooks/hooks.json → fu guard", 13, ACC, "700")
    for k, t in enumerate(T(["asks before a card-named", "irreversible command", "records the run; a second run asks again",
                             "advisory: never denies, fails open", "plugin install only"],
                            ["命令与任务卡上的不可逆操作", "相符时，请你确认", "记录每次执行；再次执行会重新确认",
                             "只作提醒：从不拒绝，出错时放行", "仅随插件安装"])):
        if k == 1:
            f.text(364, 342 + k * 24, t, 13, INK, SANS)
            continue
        f.raw(f'<circle cx="354" cy="{337 + k * 24}" r="3.5" fill="{ORG}"/>')
        f.text(364, 342 + k * 24, t, 13, INK, SANS)
    f.rect(746, 292, 394, 182, "#FFFFFF", EDGE, 1, 10)
    f.mono(766, 318, "scripts/fu.py", 13, ACC, "700")
    px, py = 766, 332
    for t in ("init", "lint", "freeze", "integrity", "log", "list", "render"):
        w = tw(t, 12, True) + 24
        if px + w > 1124:
            px, py = 766, py + 32
        px = f.pill(px, py, t, PINK, None, ACC, 12, 24) + 8
    f.text(766, 420, T("stdlib Python ≥ 3.8 · no network", "仅用 Python 标准库（≥ 3.8）· 不联网"), 13, SUB, SANS)
    f.text(766, 444, T("everything deterministic; never done by hand", "确定性的工作全部交给它，模型不手工处理"), 13, SUB, SANS)
    # L3
    layer(506, 236, "3", T("Card skill + commands", "任务卡技能与命令"), T("loaded when you start a card", "开始建卡时才加载"), SAND)
    cx = 330
    for c in ("/fu-brief", "/fu-catch-up", "/fu-debrief", "/fu-view"):
        w = tw(c, 13, True) + 28
        f.rect(cx, 522, w, 30, PINK, ORG, 1.2, 15)
        f.mono(cx + w / 2, 542, c, 13, ACC, "700", "middle")
        cx += w + 12
    f.text(cx + 4, 542, T("thin; /fu-brief holds the template", "命令很薄；模板在 /fu-brief 中"), 13, SUB, SANS)
    f.arrow(500, 556, 500, 572, MUTE, "ahc", 1.5)
    f.rect(330, 576, 810, 50, "#FFFFFF", ORG, 1.2, 10)
    f.serif(350, 607, "SKILL.md", 17)
    f.text(450, 607, T("≤ 700 words · the card, four stop-points, the always-on rules", "不超过 700 词 · 任务卡、四个打断点、常驻规则"), 13, SUB, SANS)
    refs = [("card.md", T("schema · lint", "格式规范")), ("brief.md", T("questions", "提问与预测")), ("debrief.md", T("grading", "评判")),
            ("results.md", T("measured", "实测结果")), ("view.md", T("HTML view", "HTML 视图"))]
    for i, (n, d) in enumerate(refs):
        x = 330 + i * 164
        f.card(x, 640, 152, 58, accent=SAND, fill="#FFFFFF", stroke=EDGE, sw=1)
        f.mono(x + 18, 664, n, 13, INK, "700")
        f.text(x + 18, 686, d, 12, SUB, SANS)
    f.text(330, 726, T("references load only in the phase that needs them", "参考文件只在需要它的阶段加载"), 12, SUB, SANS)
    # L4
    layer(758, 112, "4", T("One auditor", "一个评判子代理"), T("called narrowly", "只在少数场合调用"), GRN)
    f.rect(330, 774, 810, 80, "#FFFFFF", GRN, 1.2, 10)
    f.mono(350, 802, "mechanism-auditor", 14, INK, "700")
    f.text(520, 802, T("fresh context: frozen card + artifacts, never the builder's claims",
                       "新上下文：只看冻结的任务卡和产出文件，不看执行者的判断"), 13, SUB, SANS)
    f.text(350, 832, T("only for an irreversible-lane card, a measured result, or on request; else same-context — weaker",
                       "只用于含不可逆操作的任务卡、实测结果或应你要求；否则标明同一上下文评判，较弱"), 13, SUB, SANS)
    # artifacts
    f.mono(40, 904, T("[ FILES ] .finding-unknowns/", "[ 文件 ] .finding-unknowns/"), 13, ACC, "700", spacing=spaced(zh))
    arts = [("tasks/{slug}.md", T("the card · committed", "任务卡 · 提交"), True),
            ("tasks/{slug}.deltas.md", T("every delta · committed", "全部增量记录 · 提交"), True),
            ("decisions.md", T("your answers, never re-asked · committed", "你的答复，不再重复提问 · 提交"), True),
            ("profile.md", T("mode · strict · view · guard · local", "模式 · 严格 · 视图 · 防护 · 本地"), False),
            ("predictions-log.md", T("graded predictions · local", "已评判的预测 · 本地"), False),
            ("logs/ · view/", T("guard records, HTML · local", "防护记录、HTML · 本地"), False)]
    for i, (n, d, hot) in enumerate(arts):
        x = 40 + (i % 3) * 376
        y = 918 + (i // 3) * 68
        f.rect(x, y, 360, 58, PINK if hot else PANEL, ORG if hot else EDGE, 1.2 if hot else 1, 10)
        f.mono(x + 18, y + 25, n, 13, ACC, "700")
        f.text(x + 18, y + 46, d, 13, SUB, SANS)
    f.rect(40, 1054, 1120, 42, PINK, PINK, 1, 10)
    f.raw(f'<rect x="40" y="1054" width="5" height="42" rx="2.5" fill="{ORG}"/>')
    f.mono(60, 1080, T("PRINCIPLES", "原则"), 13, ACC, "700", spacing=spaced(zh))
    for x, t in ((190, T("you predict first", "你先预测")), (430, T("code enforces what code can", "能由代码保证的交给代码")),
                 (800, T("the evidence says where it stops", "证据写明止于何处"))):
        f.raw(f'<circle cx="{x - 10}" cy="1075" r="3.5" fill="{ORG}"/>')
        f.text(x, 1080, t, 14, INK, SERIF, "700")
    return f.svg()


# ---------------------------------------------------------------- card ----------
def card(zh):
    T = L(zh)
    f = Fig(1200, 910, T("The task card", "任务卡"),
            T("Anatomy of a task card: the header, frozen Brief, Amendments, the deltas rollup, Model changes, Open and Debrief, with who writes each and when.",
              "任务卡的结构：页头、冻结的简报、修订、增量记录汇总、认知修正、待办与复盘，以及各部分由谁、在何时写入。"), zh)
    f.header(T("// 03 · THE TASK CARD", "// 03 · 任务卡"), T("You and the agent work from one card", "你和智能体共用一张任务卡"),
             T("Nested lists with fixed keys, no tables. The frozen Brief is never edited, so no prediction is rewritten after the fact.",
               "固定的键，嵌套列表，不用表格。简报冻结后不再修改，预测无法事后改写。"))
    f.section(40, 158, ".finding-unknowns/tasks/{slug}.md")
    rows = [
        (T("Header", "页头"), 116, PANEL, MUTE,
         T(["Goal: … · State: building", "Needs you: nothing", "Mode: ship · Last seen by you: …, after D3", "Timing: Brief frozen …, commit 1a2b3c4"],
           ["Goal（目标）· State（状态）", "Needs you（需要你决定）：nothing", "Mode（模式）· Last seen（上次查看）：D3 之后", "Timing（时间凭据）：冻结于 …，提交 1a2b3c4"]),
         T("Re-orients you", "帮你接上进度"), T("Needs you lives here once; fu freeze owns State and Timing.", "需要你决定的事只在这里写一次；状态和时间凭据由 fu freeze 维护。"), None),
        (T("Brief", "简报"), 160, "#FBEFEA", ORG,
         ["Approach:", "  - {decision} because {why}", 'P1 (you · medium) "{your words}"', "  - falsifier · should not change",
          'A1 (agent · high) "…" · Stop-points · budget', "Irreversible: `…` · C1 check · does NOT prove · lane"],
         T("Written at /fu-brief, frozen on your yes", "在 /fu-brief 中写成，经你确认后冻结"),
         T("Your words, quoted; recorded before you see the agent's.", "你的原话照录，在你看到智能体的预测之前写下。"), T("FROZEN", "已冻结")),
        (T("Amendments", "修订"), 56, PANEL, SAND, ["M1 09:40 · after D2 · confirmed: … · why: …"],
         T("Dated, append-only", "写明日期，只追加"), T("Explains a miss; never removes a prediction.", "用于解释预测为何落空，不删除任何预测。"), None),
        (T("Deltas", "增量记录"), 56, PANEL, SAND, ["Latest: D3 · Rollup: at most three lines"],
         T("The lines live in {slug}.deltas.md", "明细在 {slug}.deltas.md 中"),
         T("Each decision made for you states its cost if wrong.", "代你做出的决定都写明做错的代价。"), None),
        (T("Model changes", "认知修正"), 56, PANEL, SAND, ["- You expected X → it is Y, because Z"],
         T("What changes in your picture", "你的认知需要哪些修正"), T("\"shown, not confirmed\" until you confirm.", "在你确认之前一直标为“已展示，未确认”。"), None),
        (T("Open", "待办"), 56, PANEL, SAND, ["- the remote-zone rate is synthetic"],
         T("Waiting for you", "等你处理"), T("Decisions and runs not yet done.", "尚未做出的决定和尚未完成的运行。"), None),
        (T("Debrief", "复盘"), 100, "#EEF1E8", GRN,
         ["Evidence · P1 measured · consistent? · mechanism [tier]", "Integrity · Did NOT prove · Not checked", "Bottom line: holds · did not hold · stops at"],
         T("The completion report", "即完成报告"), T("Yours first; evidence before the bottom line.", "先评你的预测；证据在前，结论在后。"), None),
    ]
    y = 176
    f.rect(36, y - 8, 548, sum(r[1] + 10 for r in rows) + 8, "#FFFFFF", EDGE, 1, 14, True)
    for name, h, fill, accent, lines, ann1, ann2, flag in rows:
        f.rect(48, y, 524, h, fill, EDGE, 1, 10)
        f.raw(f'<rect x="48" y="{y + 8}" width="5" height="{h - 16}" rx="2.5" fill="{accent}"/>')
        f.serif(66, y + 24, name, 17, ACC if flag else (GRN if accent == GRN else INK))
        if flag:
            f.tag(560, y + 9, flag, ACC, PINK)
        for i, l in enumerate(lines):
            f.mono(66, y + 46 + i * 20, l.replace("  ", "\u00a0\u00a0"), 12, SUB)
        cy = y + h / 2
        f.line(574, cy, 618, cy, MUTE, 1, "3 4")
        f.card(624, cy - 30, 536, 60, accent=accent, fill=PANEL, stroke=EDGE, sw=1)
        f.text(644, cy - 6, ann1, 15, INK, SANS, "700")
        f.text(644, cy + 16, ann2, 13, SUB, SANS)
        y += h + 10
    f.text(40, 886, T("fu freeze commits the card, its deltas file and decisions.md; profile.md, the prediction log, logs/ and view/ stay local.",
                      "fu freeze 提交任务卡、增量记录文件和 decisions.md；profile.md、预测记录、logs/ 和 view/ 只留在本地。"), 13, SUB, SANS)
    return f.svg()


# ---------------------------------------------------------------- stop-points ---
def stops(zh):
    T = L(zh)
    f = Fig(1200, 760, T("Four stop-points", "四个打断点"),
            T("During the build the agent stops for you only on four conditions checked against the card; everything else is logged and work continues. Lanes classify how reversible an action is.",
              "执行期间，智能体只在四种可对照任务卡核对的情况下停下来找你；其余情况记录在案，工作继续。可逆性分级表示一项操作撤回的难易程度。"), zh)
    f.header(T("// 04 · QUIET BUILD", "// 04 · 安静执行"), T("Four reasons to stop; everything else is a line", "只有四种情况会打断你，其余只记一行"),
             T("Checked against the card, never against the agent's sense of what feels risky.", "对照任务卡核对，而不是由智能体凭感觉判断风险高低。"))
    rows = [
        ("1", T("Irreversible step", "不可逆操作"), T("data rewritten or deleted · production · money · publishing · promises", "改写或删除数据、生产环境、资金、对外发布、对他人的承诺"),
         T("Exact command on an Irreversible: line; runs once.", "确切命令写在 Irreversible: 行上，只执行一次。"),
         T("Guard asks, or a chat yes to that exact command; dry-run checks.", "由防护钩子请你确认，无钩子时须你在对话中同意；检查只做试运行。")),
        ("2", T("Scope change", "范围变化"), T("outside the Brief", "超出简报约定的范围"),
         T("You decide whether the scope changes.", "由你决定是否改变范围。"), ""),
        ("3", T("Dead premise, no way back", "前提失效且无退路"), T("a premise died or a falsifier fired; no reversible path left", "简报前提不成立或反证条件已触发，且无可逆做法"),
         T("You confirm the Amendment.", "由你确认修订。"),
         T("Two failed fixes on one assumption: test it; a third failure stops.", "两次修复因同一假设失败：先检验它，第三次失败即停下。")),
        ("4", T("Budget overrun", "预算超支"), T("past the multiple agreed in the Brief", "超过简报中约定的倍数"),
         T("You decide: continue, cut back or re-brief.", "由你决定：继续、缩小范围，还是重新做简报。"), ""),
    ]
    y = 150
    for n, q, sub, a1, a2 in rows:
        f.card(40, y, 500, 84, accent=ORG, fill=PANEL, stroke=EDGE)
        f.badge(62, y + 16, n, dark=True, size=30)
        f.serif(106, y + 38, q, 19)
        f.text(106, y + 64, sub, 13, SUB, SANS)
        f.arrow(544, y + 42, 606, y + 42)
        f.mono(575, y + 34, T("STOP", "停下"), 11, ACC, "700", "middle")
        f.card(612, y, 548, 84, accent=None, fill=PINK, stroke=ORG, sw=1.5)
        f.text(632, y + (36 if a2 else 48), a1, 15, INK, SANS, "700")
        if a2:
            f.text(632, y + 60, a2, 13, SUB, SANS)
        y += 98
    f.arrow(290, y - 12, 290, y + 18, GRN, "ahg")
    f.mono(304, y + 6, T("none of the four", "不属于以上四种"), 12, GRN, "700")
    f.card(40, y + 22, 1120, 66, accent=GRN, fill="#EEF1E8", stroke=GRN, sw=1.5)
    f.serif(64, y + 50, T("Keep going.", "继续执行。"), 18, GRN)
    f.text(64, y + 74, T("Most reversible option, one line in the deltas file; a decision made for you states its cost if wrong.",
                         "选择最容易撤回的做法，在增量记录中记一行；代你做出的决定写明做错的代价。"), 14, INK, SANS)
    y += 116
    f.section(40, y, T("LANES · CLASSIFY UPWARD WHEN UNSURE", "可逆性分级 · 拿不准时归入更高一级"))
    f.raw(f'<rect x="40" y="{y + 14}" width="1120" height="16" rx="8" fill="url(#spec)"/>')
    for x, name, d, col in ((40, T("reversible", "可逆"), T("contained, cheap to undo", "影响范围小，撤回成本低"), GRN),
                            (430, T("wide", "影响面广"), T("undoable, touches shared surface", "可以撤回，但涉及共享部分"), "#B07A4F"),
                            (820, T("irreversible", "不可逆"), T("exact command, one run", "确切命令，只执行一次"), RED)):
        f.mono(x, y + 54, name, 14, col, "700")
        f.text(x + tw(name, 14, True) + 12, y + 54, d, 13, SUB, SANS)
    return f.svg()


# ---------------------------------------------------------------- debrief -------
def debrief(zh):
    T = L(zh)
    f = Fig(1200, 760, T("Debrief", "复盘"),
            T("The slide from offloading to cognitive surrender, and the completion report that pushes back: evidence first, every prediction graded with yours first, integrity, what the checks did not prove, bottom line and what needs you last.",
              "从委托到放弃判断的滑坡，以及完成报告如何拉回：证据在前，逐条评判预测并先评你的，完整性检查，写明检查没有证明什么，结论和需要你决定的事放在最后。"), zh)
    f.header(T("// 05 · COMPLETION REPORT = DEBRIEF", "// 05 · 完成报告即复盘"), T("Hand off the work, not the judgment", "交出工作，不交出判断"),
             T("Evidence first, bottom line last, so checking stays cheap and surrender shows.", "复盘先列证据、最后给结论，核查成本低，放弃判断也容易被发现。"))
    # the slide (from 4.x)
    f.section(40, 158, T("THE SLIDE", "滑坡"))
    f.raw('<rect x="40" y="212" width="520" height="22" rx="11" fill="url(#spec)"/>')
    f.raw(f'<rect x="78.7" y="170" width="96" height="26" rx="13" fill="{ORG}"/>')
    f.mono(126.7, 187, T("stay here", "停在这里"), 13, INK, "700", "middle")
    f.raw(f'<path d="M126.7 198V210" stroke="{ORG}" stroke-width="2.5" marker-end="url(#ah)"/><circle cx="126.7" cy="223" r="11" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
    for x, name, col, l1, l2 in ((40, T("offloading", "委托"), GRN, T("delegate the work,", "把工作交出去，"), T("keep ownership", "自己仍负责")),
                                 (213, T("deferral", "依赖"), ACC, T("the output becomes", "产出直接成为"), T("the next input", "下一步的输入")),
                                 (387, T("cognitive surrender", "放弃判断"), RED, T("the output quietly becomes", "产出悄悄成了"), T("your own; no urge to check", "你的结论，不再核对"))):
        f.serif(x, 262, name, 17, col)
        f.text(x, 283, l1, 13, SUB, SANS)
        f.text(x, 300, l2, 13, SUB, SANS)
    f.line(205, 246, 205, 306)
    f.line(379, 246, 379, 306)
    # who grades
    f.section(40, 348, T("WHO GRADES", "由谁评判"))
    f.card(40, 362, 520, 92, accent=GRN, fill=PANEL, stroke=GRN)
    f.mono(64, 390, "mechanism-auditor", 14, INK, "700")
    f.text(64, 414, T("Irreversible-lane card, measured result, or on request.", "含不可逆操作的任务卡、实测结果，或应你要求。"), 13, SUB, SANS)
    f.text(64, 436, T("Frozen card + artifacts; never the transcript or the claims.", "只看冻结的任务卡和产出文件，不看对话和执行者的判断。"), 13, SUB, SANS)
    f.card(40, 468, 520, 92, accent=ORG, fill=PANEL, stroke=EDGE)
    f.serif(64, 496, T("Otherwise: same-context — weaker", "其余情况：同一上下文评判，较弱"), 17)
    f.text(64, 520, T("The label stays on the report; it is never hidden.", "这个标注写在报告上，从不隐去。"), 13, SUB, SANS)
    f.text(64, 542, T("Explanation goes only where a prediction missed.", "只在预测落空处展开解释。"), 13, SUB, SANS)
    f.text(40, 610, T("Take the handoff where being wrong is cheap;", "出错代价低的地方，放心交出去；"), 17, ACC, SERIF, extra=' font-style="italic"' if not zh else "")
    f.text(40, 634, T("keep the reasoning where others bear the consequences.", "后果由别人承担的地方，判断留在自己手里。"), 17, ACC, SERIF, extra=' font-style="italic"' if not zh else "")
    f.text(40, 660, T("after Addy Osmani, Critical thinking when agents do the work; cognitive surrender: Shaw & Nave",
                      "参考 Addy Osmani《Critical thinking when agents do the work》；“放弃判断”出自 Shaw 与 Nave"), 12, SUB, SANS)
    # the report order
    f.section(620, 158, T("COMPLETION REPORT · IN THIS ORDER", "完成报告 · 按此顺序"))
    items = [
        (T("Evidence", "证据"), T("commands actually run + their output, before any prose", "实际运行的命令及输出，先于任何说明"), T("FIRST", "最先"), ACC),
        (T("Predictions, quoted and graded", "引用原文，评判预测"), T("yours first: consistent · partly · inconsistent · can't tell", "先评你的：一致 · 部分一致 · 不一致 · 无法判断"), T("yours first", "先评你的"), BLUE),
        (T("Integrity", "完整性检查"), T("Brief vs freeze · check files · unlogged hunks", "简报与冻结提交 · 检查文件 · 未记录的改动"), "fu integrity", BLUE),
        (T("What the checks did NOT prove", "检查不能证明什么"), T("check → leaves open · still holds", "检查项 → 留下的疑问 · 仍然成立的部分"), None, None),
        (T("Not checked", "未检查"), T("at least one thing nobody verified", "至少列出一项无人核对的内容"), T("never empty", "不可为空"), RED),
        (T("Model changes", "认知修正"), T("you expected X → it is Y, because Z", "你原以为 X → 实际是 Y，因为 Z"), T("shown, not confirmed", "已展示，未确认"), SAND),
        (T("Bottom line", "结论"), T("holds · did not hold · stops at", "成立 · 未成立 · 证据止于"), None, None),
        (T("Needs you", "需要你决定的事"), T("one decision and a recommendation; stated, not asked", "一项决定加一条推荐，直接陈述，不提问"), T("LAST", "最后"), ACC),
    ]
    y = 172
    for i, (name, sub, tag, col) in enumerate(items):
        hot = i in (0, 7)
        f.rect(620, y, 540, 58, PINK if hot else PANEL, ORG if hot else EDGE, 1.5 if hot else 1, 12, True)
        f.badge(636, y + 14, str(i + 1), dark=not hot, size=30, hot=hot)
        f.text(680, y + 25, name, 15, INK, SANS, "700")
        f.text(680, y + 46, sub, 12, SUB, SANS)
        if tag:
            if hot:
                w = tw(tag, 12, True) + 22
                f.rect(1146 - w, y + 17, w, 24, ORG, ORG, 1, 12)
                f.mono(1146 - w / 2, y + 33.5, tag, 12, INK, "700", "middle")
            else:
                f.tag(1146, y + 17, tag, col)
        y += 66
    f.text(1160, y + 12, T("/fu-debrief is for late results and re-grades.", "/fu-debrief 用于结果迟到或重新评判。"), 13, SUB, SANS, anchor="end")
    return f.svg()


def write(name, fn):
    open(f"{ROOT}/assets/{name}.svg", "w").write(fn(False))
    open(f"{ROOT}/assets/zh/src/{name}.svg", "w").write(fn(True))


if __name__ == "__main__":
    for n, fn in (("hero", hero), ("lifecycle", lifecycle), ("framework", framework), ("card", card),
                  ("stop-points", stops), ("debrief", debrief)):
        write(n, fn)
    print("ok")
