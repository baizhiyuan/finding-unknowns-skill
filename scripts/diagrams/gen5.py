#!/usr/bin/env python3
"""5.0 diagrams in the 4.x style.

Usage: python3 scripts/diagrams/gen5.py .   (from the repo root), then outline the Chinese
sources: python3 scripts/outline_cjk.py --fonts DIR --out assets/zh assets/zh/src/*.svg
quadrants.svg and cartographer.svg are adapted from the 4.3.2 originals by text edits, not
generated here."""
from __future__ import annotations

import subprocess
import sys
from style import *  # noqa: F403

ROOT = sys.argv[1]


def L(zh):
    return lambda en, cn: cn if zh else en


# ---------------------------------------------------------------- hero ----------
def hero(zh):
    T = L(zh)
    old = subprocess.run(["git", "show", "v4.3.2:assets/hero.svg"], cwd=ROOT, capture_output=True, text=True, check=True).stdout  # 4.x map art
    art = old[old.index("<g clip-path=\"url(#frame)\">"): old.index("</g>\n<text x=\"56\" y=\"70\"") + 5]
    defs = old[old.index("<defs>"): old.index("</defs>") + 7]
    f = Fig(1200, 420, "finding-unknowns v5.0.0",
            T("Banner: a pin clearing fog on a dotted map. One task card per task: you predict first, the agent builds quietly, a fresh context grades what you both expected.",
              "横幅：地图上的定位针拨开迷雾。每个任务一张任务卡：你先预测，智能体安静执行，由新上下文评判双方的预期。"), zh)
    f.mono(56, 70, T("[ CLAUDE CODE PLUGIN · v5.0.0 ]", "[ CLAUDE CODE 插件 · v5.0.0 ]"), 15, ACC, "700", spacing="1.5" if not zh else None)
    f.text(54, 152, "finding-unknowns", 64, INK, SERIF, "700")
    f.text(56, 198, T("You predict first. The agent builds quietly.", "你先预测，智能体安静地执行。"), 20, INK, SANS)
    f.text(56, 226, T("A fresh context grades what you both expected.", "完成后，由新上下文评判你们双方的预期。"), 20, SUB, SANS)
    x = 56
    for t in T(["task card", "4 stop-points", "fresh-context debrief"], ["任务卡", "4 个打断点", "新上下文复盘"]):
        x = f.pill(x, 262, t, PINK, ORG, ACC, 14, 30) + 10
    x = 56
    for t in T(["3 agents", "+ structured mode", "+ theory → result"], ["3 个子代理", "+ 结构化模式", "+ 理论 → 实测"]):
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
    f = Fig(1200, 620, T("When finding-unknowns fires", "finding-unknowns 的使用时机"),
            T("Three moments around one task card: brief before the build, a quiet build, a debrief after; catch-up when you come back.",
              "围绕一张任务卡的三个时刻：动手前的简报、安静的执行、完成后的复盘；回来时先回顾。"), zh)
    f.header(T("// 01 · WHEN IT FIRES", "// 01 · 使用时机"), T("Three moments, one card", "三个时刻，一张任务卡"),
             T("You predict before the work, the agent builds quietly, and the debrief grades what you both expected.",
               "动手前你先预测，执行时智能体不打扰你，完成后复盘评判你们双方的预期。"))
    f.human(40, 150, 340, T("HUMAN · predict first + approve the Brief", "你：先预测，并确认简报"))
    f.human(612, 150, 548, T("HUMAN · irreversible step + confirm model changes", "你：执行不可逆操作，确认认知修正"))
    f.line(190, 178, 190, 192, INK, 1.5, "3 3")
    f.line(886, 178, 886, 192, INK, 1.5, "3 3")
    cols = [
        (T("BRIEF", "简报"), "/fu-brief", T("before the build", "动手前"),
         [("1", T("You predict first", "你先预测")), ("2", T("Territory before questions", "先查现场，再提问")),
          ("3", T("Then the agent predicts", "智能体随后预测")), ("4", T("Stop-points + contract", "打断点与验收标准")),
          ("5", T("Frozen on your yes", "你确认后冻结"))]),
        (T("BUILD", "安静执行"), "", T("quietly", "执行中"), None),
        (T("CATCH-UP", "回顾"), "/fu-catch-up", T("next session", "下次会话"),
         [("1", T("Recall questions first", "先问回忆性问题")), ("2", T("Only what changed", "只看新变化")),
          ("3", T("Next decision for you", "需要你做的决定"))]),
        (T("DEBRIEF", "复盘"), "/fu-debrief", T("after the work", "完成后"), None),
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
    for k, t in enumerate(T(["irreversible action", "scope change", "dead premise", "budget overrun"],
                            ["不可逆操作", "范围变化", "前提失效", "预算超支"])):
        f.raw(f'<circle cx="{x + 24}" cy="{288 + k * 26}" r="4" fill="{ORG}"/>')
        f.text(x + 36, 293 + k * 26, t, 14, INK, SANS)
    f.rect(x + 16, 404, 230, 92, "#FFFFFF", EDGE, 1, 10)
    f.text(x + 30, 428, T("Everything else:", "其余情况："), 13, GRN, SANS, "700")
    f.text(x + 30, 450, T("most reversible option,", "选最容易撤回的做法，"), 13, SUB, SANS)
    f.text(x + 30, 470, T("one delta line on the card", "在任务卡上记一行"), 13, SUB, SANS)
    f.mono(x + 30, 488, "D7 surprise: … → logs/r3", 11, MUTE)
    # debrief column
    x = 898
    f.rect(x + 16, 270, 230, 64, "#FFFFFF", ORG, 1.5, 10)
    f.mono(x + 30, 294, "mechanism-auditor", 13, INK, "700")
    f.text(x + 30, 318, T("fresh context, yours first", "新上下文评判，先评你的"), 13, SUB, SANS)
    for k, t in enumerate(T(["Evidence first", "Predictions quoted, graded", "Did NOT prove · not checked", "Model changes"],
                            ["证据在前", "原文引用并评判预测", "没有证明什么 · 未检查", "认知修正"])):
        f.raw(f'<circle cx="{x + 24}" cy="{360 + k * 32}" r="4" fill="{ORG}"/>')
        f.text(x + 38, 365 + k * 32, t, 14, INK, SANS)
    # card bar
    f.rect(40, 534, 1120, 56, "#F5DDD1", "#F5DDD1", 1, 10)
    f.raw(f'<rect x="40" y="534" width="5" height="56" rx="2.5" fill="{ORG}"/>')
    f.raw(f'<rect x="60" y="548" width="290" height="28" rx="14" fill="{ORG}"/>')
    f.mono(205, 567, ".finding-unknowns/tasks/{slug}.md", 13, INK, "700", "middle")
    f.text(370, 567, T("The card persists across sessions; committed, so the predictions' timing is provable.",
                       "任务卡跨会话保留；默认提交到 git，证明预测写在结果之前。"), 14, INK, SANS)
    return f.svg()


# ---------------------------------------------------------------- card ----------
def card(zh):
    T = L(zh)
    f = Fig(1200, 820, T("The task card", "任务卡"),
            T("Anatomy of a task card: header, frozen Brief, Amendments, Deltas, Model changes, Open and Debrief, with who writes each and when.",
              "任务卡的结构：页头、冻结的简报、修订、增量记录、认知修正、待办与复盘，以及各部分由谁、在何时写入。"), zh)
    f.header(T("// 04 · THE TASK CARD", "// 04 · 任务卡"), T("One file, two readers", "一个文件，两位读者"),
             T("You and the agent read the same card. It survives sessions; the frozen Brief is never edited.",
               "你和智能体读同一张卡。它跨会话保留；冻结后的简报不再修改。"))
    f.section(40, 158, ".finding-unknowns/tasks/{slug}.md")
    rows = [
        (T("Header", "页头"), 70, PANEL, MUTE, ["Goal · State · Next decision that needs you", "Last seen: D7 · Timing: commit 3f2a91c"] if not zh else ["目标 · 状态 · 需要你做的下一个决定", "上次查看：D7 · 时间：提交 3f2a91c"],
         T("Re-orients you", "帮你重新进入状态"), T("/fu-catch-up shows only what changed since Last seen.", "/fu-catch-up 只显示上次查看之后的变化。"), None),
        (T("Brief", "简报"), 150, "#FBEFEA", ORG, ["Approach: retry per batch, because …", "P1 (you, 70%): … · falsifier · should not change", "A1 (agent): … · falsifier · should not change", "Stop-points · budget 2× the estimate", "Contract: check | does NOT prove | lane"] if not zh else
         ["做法：按批次重试，因为……", "P1（你，70%）：…… · 反证条件 · 不应改变", "A1（智能体）：…… · 反证条件 · 不应改变", "打断点 · 预算上限为估计的 2 倍", "验收标准：检查 | 不能证明什么 | 可逆性分级"],
         T("Written at /fu-brief, frozen on your yes", "在 /fu-brief 中写成，经你确认后冻结"),
         T("Your prediction is recorded before you see the agent's.", "你的预测在看到智能体的预测之前就已记录。"), T("FROZEN", "已冻结")),
        (T("Amendments", "修订"), 56, PANEL, SAND, ["M1 11-12 premise died · why · decided-for-you"] if not zh else ["M1 11-12 前提失效 · 原因 · 代你决定"],
         T("Dated, append-only", "写明日期，只追加"), T("Explains a miss; never removes a prediction.", "用来解释预测落空，不会删掉任何预测。"), None),
        (T("Deltas", "增量记录"), 56, PANEL, SAND, ["D7 surprise: key holds session id → logs/r3"] if not zh else ["D7 意外：缓存键含会话 ID → logs/r3"],
         T("One line each", "每条一行"), T("Deviations, surprises, decisions made for you.", "偏离、意外、代你做的决定。"), None),
        (T("Model changes", "认知修正"), 56, PANEL, SAND, ["You expected X → it is Y, because Z"] if not zh else ["你原以为 X → 实际是 Y，因为 Z"],
         T("What changes in your picture", "你的认知需要哪些修正"), T("\"shown, not confirmed\" until you confirm.", "在你确认之前一直标为“已展示，未确认”。"), None),
        (T("Open", "待办"), 56, PANEL, SAND, ["run 4 of 5 pending · keep the v1 webhook?"] if not zh else ["第 4/5 次运行待完成 · 是否保留 v1 接口？"],
         T("Waiting for you", "等你处理"), T("Decisions and runs not yet done.", "尚未完成的决定和运行。"), None),
        (T("Debrief", "复盘"), 74, "#EEF1E8", GRN, ["| P1 | quoted | measured | partly | why [tier] |", "Evidence · did NOT prove · not checked"] if not zh else ["| P1 | 原文引用 | 实测 | 部分一致 | 机理［层级］|", "证据 · 检查没有证明什么 · 未检查"],
         T("Graded by a fresh context", "由新上下文评判"), T("Yours first; evidence before the bottom line.", "先评你的预测；证据在前，结论在后。"), None),
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
            f.mono(66, y + 46 + i * 20, l, 12, SUB)
        cy = y + h / 2
        f.line(574, cy, 618, cy, MUTE, 1, "3 4")
        f.card(624, cy - 30, 536, 60, accent=accent, fill=PANEL, stroke=EDGE, sw=1)
        f.text(644, cy - 6, ann1, 15, INK, SANS, "700")
        f.text(644, cy + 16, ann2, 13, SUB, SANS)
        y += h + 10
    f.text(40, 798, T("Committed by default (git add + commit --only on the card's paths); notes in logs/, the profile and the prediction log stay private.",
                      "默认只提交任务卡相关路径（git add + commit --only）；logs/、个人设置和预测记录不提交。"), 13, SUB, SANS)
    return f.svg()


# ---------------------------------------------------------------- stop-points ---
def stops(zh):
    T = L(zh)
    f = Fig(1200, 760, T("Four stop-points", "四个打断点"),
            T("During the build the agent stops for you only on four conditions checked against the card; everything else is logged and work continues. Lanes classify how reversible an action is.",
              "执行期间，智能体只在四种可对照任务卡核对的情况下停下来找你；其余情况记录在案，工作继续。可逆性分级决定一项操作有多难撤回。"), zh)
    f.header(T("// 05 · QUIET BUILD", "// 05 · 安静执行"), T("Four reasons to stop; everything else is a line", "只有四种情况会打断你"),
             T("Checked against the card, never against the agent's sense of what feels risky.", "对照任务卡核对，而不是由智能体凭感觉判断风险高低。"))
    rows = [
        ("1", T("Irreversible action", "不可逆操作"), T("data rewritten or deleted · production · money · publishing · promises", "改写或删除数据、生产环境、资金、对外发布、对他人的承诺"),
         T("Agent prepares the exact command;", "智能体准备好确切的命令；"), T("you run it, or say yes to that one command. Post-check before it closes.", "由你执行，或同意执行这一条命令；事后检查通过才算完成。")),
        ("2", T("Scope change", "范围变化"), T("outside the Brief's approach or contract", "超出简报中的做法或验收标准"),
         T("You decide whether the scope changes.", "由你决定是否改变范围。"), ""),
        ("3", T("Dead premise, no way back", "前提失效且无退路"), T("a premise or a falsifier fired; no reversible path", "前提或反证条件已触发，没有可逆的退路"),
         T("You confirm the Amendment.", "由你确认修订。"), T("The original prediction is still graded.", "原来的预测照样评判。")),
        ("4", T("Budget overrun", "预算超支"), T("past the multiple agreed in the Brief", "超过简报中约定的倍数"),
         T("You decide: continue, cut back or re-brief.", "由你决定：继续、收缩，还是重新做简报。"), ""),
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
    f.mono(304, y + 6, T("none of the four", "四项都不是"), 12, GRN, "700")
    f.card(40, y + 22, 1120, 66, accent=GRN, fill="#EEF1E8", stroke=GRN, sw=1.5)
    f.serif(64, y + 50, T("Keep going.", "继续执行。"), 18, GRN)
    f.text(64, y + 74, T("Most reversible option, one delta line on the card; questions that can wait go to Open.",
                         "选择最容易撤回的做法，在任务卡上记一行；可以等的问题放进待办。"), 14, INK, SANS)
    y += 116
    f.section(40, y, T("LANES · CLASSIFY UPWARD WHEN UNSURE", "可逆性分级 · 拿不准时往高处归"))
    f.raw(f'<rect x="40" y="{y + 14}" width="1120" height="16" rx="8" fill="url(#spec)"/>')
    for x, name, d, col in ((40, "reversible", T("contained, cheap to undo", "影响范围小，撤回成本低"), GRN),
                            (430, "wide", T("undoable, touches shared surface", "可以撤回，但涉及共享部分"), "#B07A4F"),
                            (820, "irreversible", T("downgrade only with your yes", "降级须经你同意"), RED)):
        f.mono(x, y + 54, name, 14, col, "700")
        f.text(x + tw(name, 14, True) + 12, y + 54, d, 13, SUB, SANS)
    return f.svg()


# ---------------------------------------------------------------- debrief -------
def debrief(zh):
    T = L(zh)
    f = Fig(1200, 740, T("Debrief", "复盘"),
            T("The slide from offloading to cognitive surrender, and the debrief that pushes back: evidence first, predictions quoted and graded by a fresh context, what the checks did not prove, model changes, bottom line last.",
              "从委托到放弃判断的滑坡，以及复盘如何拉回：证据在前，按原文引用预测并由新上下文评判，写明检查没有证明什么，列出认知修正，结论放在最后。"), zh)
    f.header(T("// 06 · DEBRIEF", "// 06 · 复盘"), T("Hand off the work, not the judgment", "交出工作，不交出判断"),
             T("Evidence first, bottom line last: the debrief makes checking cheap and surrender visible.", "证据在前，结论在后：复盘让核查变得容易，也让放弃判断无处藏身。"))
    # the slide (from 4.x)
    f.section(40, 158, T("THE SLIDE", "滑坡"))
    f.raw('<rect x="40" y="212" width="520" height="22" rx="11" fill="url(#spec)"/>')
    f.raw(f'<rect x="78.7" y="170" width="96" height="26" rx="13" fill="{ORG}"/>')
    f.mono(126.7, 187, T("stay here", "停在这里"), 13, INK, "700", "middle")
    f.raw(f'<path d="M126.7 198V210" stroke="{ORG}" stroke-width="2.5" marker-end="url(#ah)"/><circle cx="126.7" cy="223" r="11" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
    for x, name, col, l1, l2 in ((40, T("offloading", "委托"), GRN, T("delegate the work,", "把工作交出去，"), T("keep ownership", "自己仍负责")),
                                 (213, T("deferral", "依赖"), ACC, T("the output becomes", "产出直接成为"), T("the next input", "下一步的输入")),
                                 (387, T("cognitive surrender", "放弃判断"), RED, T("the output quietly becomes", "产出悄悄变成"), T("your own; no urge to check", "你自己的，不再想去核对"))):
        f.serif(x, 262, name, 17, col)
        f.text(x, 283, l1, 13, SUB, SANS)
        f.text(x, 300, l2, 13, SUB, SANS)
    f.line(205, 246, 205, 306)
    f.line(379, 246, 379, 306)
    # who grades
    f.section(40, 348, T("WHO GRADES", "由谁评判"))
    f.card(40, 362, 520, 92, accent=GRN, fill=PANEL, stroke=GRN)
    f.mono(64, 390, "mechanism-auditor", 14, INK, "700")
    f.text(64, 414, T("Gets the frozen card and the artifacts, not the transcript.", "只拿到冻结的任务卡和产出，不看执行过程。"), 13, SUB, SANS)
    f.text(64, 436, T("Fills Measured and Consistent?, your predictions first.", "填写“实测”和“是否一致”，先评你的预测。"), 13, SUB, SANS)
    f.card(40, 468, 520, 92, accent=ORG, fill=PANEL, stroke=EDGE)
    f.serif(64, 496, T("The builder writes only the Mechanism", "执行者只写机理"), 17)
    f.text(64, 520, T("with its tier: verified · supported · inferred · untested.", "并标明层级：已验证 · 有数据支持 · 推断 · 未检验。"), 13, SUB, SANS)
    f.text(64, 542, T("Explanation goes where a prediction missed.", "讲解放在预测落空的地方。"), 13, SUB, SANS)
    f.text(40, 600, T("Take the handoff where being wrong is cheap;", "出错代价低的地方，放心交出去；"), 17, ACC, SERIF, extra=' font-style="italic"' if not zh else "")
    f.text(40, 624, T("keep the reasoning where others bear the consequences.", "后果由别人承担的地方，判断留在自己手里。"), 17, ACC, SERIF, extra=' font-style="italic"' if not zh else "")
    f.text(40, 650, T("after Addy Osmani, Critical thinking when agents do the work; cognitive surrender: Shaw & Nave",
                      "参考 Addy Osmani《Critical thinking when agents do the work》；“放弃判断”一说出自 Shaw 与 Nave"), 12, SUB, SANS)
    # the debrief order
    f.section(620, 158, T("/fu-debrief · IN THIS ORDER", "/fu-debrief · 按此顺序"))
    items = [
        (T("Evidence", "证据"), T("commands actually run + their output, before any prose", "实际运行的命令及输出，先于任何说明"), "FIRST" if not zh else "最先", ACC),
        (T("Integrity", "完整性检查"), T("vs freeze commit · check files · unlogged deviations", "对照冻结提交 · 检查文件 · 未记录的偏离"), "fresh context" if not zh else "新上下文", BLUE),
        (T("Predictions, quoted and graded", "原文引用并评判预测"), T("yours first: consistent · partly · inconsistent · can't tell", "先评你的：一致 · 部分一致 · 不一致 · 无法判断"), "fresh context" if not zh else "新上下文", BLUE),
        (T("What the checks did NOT prove", "检查没有证明什么"), T("one line per check; same-context tests flagged", "每项检查一行；同一上下文写的测试要标出"), None, None),
        (T("Not checked", "未检查"), T("at least one thing nobody verified", "至少一项没人核对过的内容"), "never empty" if not zh else "不可为空", RED),
        (T("Model changes", "认知修正"), T("you expected X → it is Y, because Z", "你原以为 X → 实际是 Y，因为 Z"), "shown, not confirmed" if not zh else "已展示，未确认", SAND),
        (T("Bottom line · needs you", "结论 · 需要你决定的事"), T("one line; decisions stay with you", "一行；决定权留给你"), "LAST" if not zh else "最后", ACC),
    ]
    y = 172
    for i, (name, sub, tag, col) in enumerate(items):
        hot = i in (0, 6)
        f.rect(620, y, 540, 64, PINK if hot else PANEL, ORG if hot else EDGE, 1.5 if hot else 1, 12, True)
        f.badge(636, y + 17, str(i + 1), dark=not hot, size=30, hot=hot)
        f.text(680, y + 28, name, 15, INK, SANS, "700")
        f.text(680, y + 49, sub, 12, SUB, SANS)
        if tag:
            if hot:
                w = tw(tag, 12, True) + 22
                f.rect(1146 - w, y + 20, w, 24, ORG, ORG, 1, 12)
                f.mono(1146 - w / 2, y + 36.5, tag, 12, INK, "700", "middle")
            else:
                f.tag(1146, y + 20, tag, col)
        y += 72
    f.text(1160, y + 10, T("Structured mode: the full nine-section packet.", "结构化模式下使用完整的九段交付包。"), 13, SUB, SANS, anchor="end")
    return f.svg()


def write(name, fn):
    open(f"{ROOT}/assets/{name}.svg", "w").write(fn(False))
    open(f"{ROOT}/assets/zh/src/{name}.svg", "w").write(fn(True))


if __name__ == "__main__":
    for n, fn in (("hero", hero), ("lifecycle", lifecycle), ("card", card), ("stop-points", stops), ("debrief", debrief)):
        write(n, fn)
    print("ok")


# ---------------------------------------------------------------- framework -----
def framework(zh):
    T = L(zh)
    f = Fig(1200, 1130, T("Architecture", "架构"),
            T("Commands enter one skill; the skill loads references per phase and delegates to agents; everything lands on the task card. Structured mode is an optional layer.",
              "命令进入唯一的技能；技能按阶段加载参考文件并委托子代理；所有内容都落在任务卡上。结构化模式是可选的一层。"), zh)
    f.header(T("// 02 · ARCHITECTURE", "// 02 · 架构"), T("One plugin, one skill, one card", "一个插件，一个技能，一张任务卡"),
             T("Commands enter the skill; the skill loads what each moment needs; everything leaves a file you can audit.",
               "命令进入技能；技能按时刻加载所需内容；所有结果都留下可核查的文件。"))
    f.mono(40, 168, T("[ 01 ] ENTRY · SLASH COMMANDS", "[ 01 ] 入口 · 斜杠命令"), 13, ACC, "700", spacing="1.5" if not zh else None)
    cmds = [("$ /fu-brief", T("create + freeze the card", "建卡并冻结")), ("$ /fu-catch-up", T("recall, then what changed", "先回忆，再看变化")),
            ("$ /fu-debrief", T("grade the predictions", "评判预测")), ("$ /fu-cartographer", T("structured mode, high stakes", "结构化模式，高风险"))]
    xs = [40, 330, 620, 880]
    for (c, d), x in zip(cmds, xs):
        dashed = "cartographer" in c
        w = tw(c, 13, True) + 32
        f.rect(x, 186, w, 32, PINK if not dashed else PAPER, ORG, 1.2, 16, dash="5 4" if dashed else None)
        f.mono(x + w / 2, 207, c, 13, ACC, "700", "middle")
        f.text(x + w / 2, 240, d, 13, SUB, SANS, anchor="middle")
        f.arrow(x + w / 2, 250, x + w / 2, 272, MUTE, "ahc", 1.5)
    f.mono(40, 300, T("[ 02 ] THE SKILL · finding-unknowns", "[ 02 ] 技能 · finding-unknowns"), 13, ACC, "700", spacing="1.5" if not zh else None)
    f.rect(40, 314, 1120, 380, PANEL, ORG, 1.5, 14, True)
    f.raw(f'<path d="M40 326a12 12 0 0 1 12 -12h1096a12 12 0 0 1 12 12v0H40z" fill="{ORG}"/>')
    f.serif(64, 356, "SKILL.md", 22)
    f.mono(1136, 356, T("≤ 1,500 words · always loaded when invoked", "≤ 1,500 词 · 调用时加载"), 12, SUB, anchor="end")
    body = T(["the task card and its three operations", "four stop-points · lanes · the build rule", "territory first · absences cited · remote targets", "a check must be able to fail"],
             ["任务卡及其三个操作", "四个打断点 · 可逆性分级 · 执行规则", "先查现场 · 缺失须有搜索依据 · 远程目标", "检查必须有可能不通过"])
    for i, t in enumerate(body):
        f.raw(f'<circle cx="{70}" cy="{382 + i * 24}" r="4" fill="{ORG}"/>')
        f.text(84, 387 + i * 24, t, 14, INK, SANS)
    f.section(64, 496, T("REFERENCES · LOADED PER MOMENT", "参考文件 · 按需加载"))
    refs = [("card.md", T("template, commits", "模板与提交")), ("brief.md", T("discovery instruments", "探索工具")),
            ("debrief.md", T("grading, evidence", "评判与证据")), ("results.md", T("theory → measured", "理论 → 实测"))]
    for i, (n, d) in enumerate(refs):
        x = 64 + i * 270
        f.card(x, 510, 250, 64, accent=ORG, fill="#FFFFFF", stroke=EDGE, sw=1)
        f.mono(x + 22, 536, n, 14, INK, "700")
        f.text(x + 22, 558, d, 13, SUB, SANS)
    f.section(64, 604, T("STRUCTURED MODE · ONLY ON REQUEST", "结构化模式 · 仅在要求时加载"))
    srefs = [("structured.md", T("quadrants + 8 techniques", "四象限与八种方法")), ("cartographer.md", T("ledger, gate, spec", "台账、闸门、规格")),
             ("handoff-full.md", T("nine-section packet", "九段交付包"))]
    for i, (n, d) in enumerate(srefs):
        x = 64 + i * 360
        f.rect(x, 618, 340, 60, PAPER, SAND, 1.2, 10, dash="5 4")
        f.mono(x + 20, 643, n, 14, ACC, "700")
        f.text(x + 20, 664, d, 13, SUB, SANS)
    f.mono(40, 728, T("[ 03 ] AGENTS · DELEGATED WHEN IT PAYS", "[ 03 ] 子代理 · 值得时才委托"), 13, ACC, "700", spacing="1.5" if not zh else None)
    agents = [("blindspot-scout", "sonnet", T("read-only recon", "只读侦察"), T("Brief", "简报"), BLUE),
              ("mechanism-auditor", "inherit", T("fresh-context grader", "新上下文评判"), T("Debrief", "复盘"), GRN),
              ("quiz-master", "inherit", T("drafts recall questions", "起草回忆性问题"), T("Catch-up", "回顾"), ORG),
              ("ledger-keeper", "inherit", T("ledger + gate verdict", "台账与闸门结论"), T("structured", "结构化模式"), SAND),
              ("prototype-smith", "inherit", T("throwaway directions", "一次性原型"), T("Brief / structured", "简报 / 结构化"), SAND)]
    for i, (n, m, d, b, col) in enumerate(agents):
        x = 40 + i * 226
        f.card(x, 742, 212, 122, accent=col, fill=PANEL, stroke=EDGE, sw=1)
        f.mono(x + 22, 770, n, 14, INK, "700")
        f.pill(x + 22, 782, m, PINK if m == "inherit" else "#DCE8F3", None, ACC if m == "inherit" else BLUE, 11, 20)
        f.text(x + 22, 824, d, 13, SUB, SANS)
        f.text(x + 22, 848, b, 13, ACC, SANS, "700")
    f.mono(40, 898, T("[ 04 ] ARTIFACTS · .finding-unknowns/", "[ 04 ] 产出文件 · .finding-unknowns/"), 13, ACC, "700", spacing="1.5" if not zh else None)
    arts = [("tasks/{slug}.md", T("the card · committed", "任务卡 · 提交"), True), ("tasks/{slug}.deltas.md", T("every delta · committed", "全部增量 · 提交"), True),
            ("predictions/{slug}.md", T("claims, run tables · committed", "论断与运行记录 · 提交"), True), ("unknowns-ledger.md", T("structured mode", "结构化模式"), False),
            ("profile.md", T("ship | learn · private", "交付或学习 · 不提交"), False), ("predictions-log.md", T("your hit rate · private", "你的命中率 · 不提交"), False)]
    for i, (n, d, hot) in enumerate(arts):
        x = 40 + (i % 3) * 376
        y = 912 + (i // 3) * 72
        f.rect(x, y, 360, 60, PINK if hot else PANEL, ORG if hot else EDGE, 1.2 if hot else 1, 10)
        f.mono(x + 18, y + 26, n, 13, ACC, "700")
        f.text(x + 18, y + 47, d, 13, SUB, SANS)
    f.rect(40, 1068, 1120, 42, PINK, PINK, 1, 10)
    f.raw(f'<rect x="40" y="1068" width="5" height="42" rx="2.5" fill="{ORG}"/>')
    f.mono(60, 1094, T("PRINCIPLES", "原则"), 13, ACC, "700", spacing="1.5" if not zh else None)
    for x, t in ((180, T("you predict first", "你先预测")), (420, T("gate on blast radius, not confidence", "看影响范围，不看把握")),
                 (800, T("the builder never grades itself", "执行者不评判自己"))):
        f.raw(f'<circle cx="{x - 10}" cy="1089" r="3.5" fill="{ORG}"/>')
        f.text(x, 1094, t, 14, INK, SERIF, "700")
    return f.svg()


if __name__ == "__main__":
    write("framework", framework)
    print("framework ok")
