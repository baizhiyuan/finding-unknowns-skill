#!/usr/bin/env python3
"""The 6.0 lifecycle diagram in the 4.x style: before → the pause (its own gate) → work → after → look-back.

Usage (from the repo root):
    python3 scripts/diagrams/lifecycle.py .
    python3 scripts/outline_cjk.py --fonts DIR --out assets/zh assets/zh/src/lifecycle.svg
The hero and slide diagrams have their own generators (hero.py, slide.py); the quadrant
diagram is edited by hand."""
from __future__ import annotations

import sys

from style import ACC, EDGE, GRN, INK, MONO, MUTE, ORG, PINK, SAND, SANS, SUB, Fig, tw

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
GAP, GATE, COL = 20, 176, 216
# BEFORE, PAUSE (a narrow gate), WORK, AFTER, LOOK-BACK
XS = (40, 276, 472, 708, 944)
WS = (COL, GATE, COL, COL, COL)
TOP, BOTTOM = 192, 532


def rows(f, x, items, y0=286, step=46, hot=()):
    for k, (main, sub) in enumerate(items):
        y = y0 + k * step
        f.raw(f'<circle cx="{x + 24}" cy="{y - 5}" r="4" fill="{ORG if k in hot else MUTE}"/>')
        f.text(x + 38, y, main, 14, ACC if k in hot else INK, SANS, "600")
        f.text(x + 38, y + 19, sub, 12, SUB, SANS)


def lifecycle(zh: bool) -> str:
    T = (lambda en, cn: cn) if zh else (lambda en, cn: en)
    f = Fig(1200, 680, T("How finding-unknowns runs", "finding-unknowns 的运行方式"),
            T("Before non-trivial changes the assistant shows the map (fu:before), then the turn ends: a pause until "
              "you reply. \"go\" accepts the recommended answers; corrections change the plan. \"just do it\" skips the "
              "wait; only irreversible steps still wait. Then it works, stops only for a scope change, a falsified "
              "premise that changes the task or an irreversible step, which runs only after an explicit yes (a bare "
              "\"go\" is not one), and shows what moved (fu:after). The look-back runs only when you ask. Nothing is written to disk unless you say \"save\".",
              "做非琐碎的改动之前，助手先列出地图（fu:before），然后结束这一轮，停下来等你回复。回复“继续”即采纳建议答案，"
              "也可以给出纠正。说“直接做”则不等待，只有不可逆操作仍要等待。之后开始执行，"
              "只在范围变化、前提失效以致任务改变或不可逆操作时停下，不可逆操作要等你明确同意才执行（笼统的“继续”不算），"
              "最后说明地图上的变化（fu:after）。回顾只在你要求时进行。"
              "除非你说“保存”，否则不往磁盘写任何东西。"), zh)
    f.header(T("// HOW IT RUNS", "// 运行方式"),
             T("Map, your reply, then what moved", "先列地图，等你回复，再说明变化"),
             T("The first four steps run on every non-trivial request (the always-on text carries their core; the skill "
               "adds the details); the look-back runs only when you ask.",
               "前四步在每次非琐碎的请求中执行（常驻文字写明要点，细节在技能里）；回顾只在你要求时进行。"))
    pills = T([(0, "YOU · say your guess"), (1, "YOU · go or corrections"),
               (3, "YOU · read what is not proved"), (4, "YOU · ask; add fu-note:")],
              [(0, "你：在需求里写上猜测"), (1, "你：回复“继续”或纠正"),
               (3, "你：先看“没有证明的”"), (4, "你：主动要求；随时写 fu-note:")])
    for i, label in pills:
        pw = round(tw(label, 12, mono=True) + 48)
        cx = XS[i] + WS[i] / 2
        if i == 0:
            px = XS[0]                       # flush left, clear of the pause pill
        elif i == 3:
            px = XS[3] + WS[3] - pw          # flush right; may reach over the WORK column, which has no pill
        else:
            px = round(min(cx - pw / 2, XS[i] + WS[i] + GAP - pw))
        f.human(px, 150, pw, label)
        f.line(cx, 178, cx, TOP, INK, 1.5, "3 3")
    cols = [(T("BEFORE", "动手之前"), "fu:before", T("before any change", "改动之前"), ORG),
            (T("PAUSE", "停顿"), "", T("the turn ends", "这一轮结束"), INK),
            (T("WORK", "执行"), "", T("after your reply", "你回复后"), GRN),
            (T("AFTER", "完成之后"), "fu:after", T("after the result", "给出结果后"), ORG),
            (T("LOOK-BACK", "回顾"), "/fu-lookback", T("when you ask", "你要求时"), SAND)]
    band = 24
    for i, ((name, cmd, when, color), x, w) in enumerate(zip(cols, XS, WS)):
        fill, stroke = (PINK, ORG) if i == 1 else ("#F0EEE6", EDGE)
        f.rect(x, TOP, w, BOTTOM - TOP, fill, stroke, 1.5 if i == 1 else 1, 12, True)
        f.o.append(f'<path d="M{x} {TOP + 12}a12 12 0 0 1 12 -12h{w - 24}a12 12 0 0 1 12 12v{band - 12}H{x}z" fill="{color}"/>')
        f.mono(x + w / 2, TOP + 16.5, when, 11, "#FAF9F5", "700", "middle")
        f.serif(x + 18, 244, name, 21)
        if cmd:
            f.mono(x + 18, 264, cmd, 13, ACC, "700")
        if i < 4:
            f.arrow(x + w + 2, 352, x + w + GAP - 2, 352, dash="4 4" if i == 3 else None)
    # before: the four quadrants
    x = XS[0]
    f.text(x + 18, 290, T("You expect", "你的预期"), 13, ACC, SANS, "700")
    f.text(x + 18, 308, T("quoted, or \"not stated\"", "只引用原话，否则写“未说明”"), 12, SUB, SANS)
    for k, (code, main, sub) in enumerate(T(
            [("KK", "Relying on", "each sourced; ✗ if wrong"), ("KU", "Open", "I find out, or you decide"),
             ("UK", "I assume you want", "a guess you can react to"), ("UU", "You did not ask", "but it matters; at most 3")],
            [("KK", "我依据的", "注明来源；标出被推翻的"), ("KU", "待解决", "我去查，或由你定"),
             ("UK", "我猜你默认", "说出猜测，供你表态"), ("UU", "你没问但要紧", "最多三条")])):
        y = 320 + k * 42
        f.badge(x + 18, y, code, size=30, hot=code == "UU")
        f.text(x + 58, y + 13, main, 14, INK, SANS, "600")
        f.text(x + 58, y + 31, sub, 12, SUB, SANS)
    f.text(x + 18, 498, T("I expect …; wrong if …", "我的预期……；若……则我错了"), 13, ACC, SANS, "700")
    f.text(x + 18, 516, T("mine, and what would disprove it", "我的判断，以及什么能证明它错"), 12, SUB, SANS)
    # the pause: its own gate between BEFORE and WORK
    x = XS[1]
    for k, line in enumerate(T(["Your reply starts", "the work."], ["你回复之后，", "工作才开始。"])):
        f.text(x + 18, 280 + k * 19, line, 14, INK, SANS, "600")
    f.rect(x + 12, 334, GATE - 24, 70, "#FFFFFF", GRN, 1.2, 10)
    f.text(x + 24, 354, T("\"go\"", "回复“继续”"), 13, GRN, SANS, "700")
    for k, line in enumerate(T(["accepts the", "recommended answers"], ["即采纳建议答案；", "也可以给出纠正"])):
        f.text(x + 24, 373 + k * 17, line, 12, SUB, SANS)
    f.rect(x + 12, 414, GATE - 24, 70, "#FFFFFF", ORG, 1.2, 10, dash="4 3")
    f.text(x + 24, 434, T("\"just do it\"", "说“直接做”"), 13, ACC, SANS, "700")
    for k, line in enumerate(T(["skips the wait,", "not irreversible steps*"], ["则不等待，", "不可逆操作除外*"])):
        f.text(x + 24, 453 + k * 17, line, 12, SUB, SANS)
    for k, line in enumerate(T(["* only after an explicit", "yes; \"go\" is not one"],
                               ["* 要等你明确同意，", "笼统的“继续”不算"])):
        f.text(x + 14, 503 + k * 15, line, 11, SUB, SANS)
    # the work
    x = XS[2]
    f.text(x + 18, 290, T("Stops only for:", "只在以下情况停下："), 14, INK, SANS, "600")
    y = 314
    for main, sub in T([("a scope change", ""), ("a falsified premise", "that changes the task"),
                        ("an irreversible step", "")],
                       [("范围变化", ""), ("前提失效", "以致任务改变"), ("不可逆操作", "")]):
        f.raw(f'<circle cx="{x + 24}" cy="{y - 5}" r="4" fill="{ORG}"/>')
        f.text(x + 36, y, main, 14, INK, SANS)
        if sub:
            y += 17
            f.text(x + 36, y, sub, 12, SUB, SANS)
        y += 22
    bw = COL - 32
    f.rect(x + 16, 392, bw, 72, "#FFFFFF", ORG, 1.2, 10)
    f.text(x + 30, 412, T("Irreversible step:", "不可逆操作："), 13, ACC, SANS, "700")
    f.text(x + 30, 430, T("exact command, explicit yes,", "给出确切命令，明确同意后"), 12, SUB, SANS)
    f.text(x + 30, 448, T("run once, never as a check", "只执行一次，绝不当检查跑"), 12, SUB, SANS)
    f.rect(x + 16, 472, bw, 50, "#FFFFFF", EDGE, 1, 10)
    f.text(x + 30, 492, T("Everything else:", "其余情况："), 13, GRN, SANS, "700")
    f.text(x + 30, 510, T("proceed; report in fu:after", "继续做，在 fu:after 中报告"), 12, SUB, SANS)
    # after
    rows(f, XS[3], T([("Expected → found", "a verdict; why only on a miss"), ("Now known", "with evidence"),
                      ("Not proved", "what each check leaves open"), ("Still unknown", "cheapest way to find out"),
                      ("Decided for you*", "what you did not ask for")],
                     [("预期 → 实际", "给出结论；只在落空处写原因"), ("新知道的", "附证据"),
                      ("没有证明的", "每项检查没有证明什么"), ("仍然未知", "附最省事的查法"),
                      ("替你定的*", "你没要求的选择和改动")]), hot=(2,))
    f.text(XS[3] + 18, 516, T("then the turn ends", "然后这一轮结束"), 12, SUB, MONO)
    # look-back
    rows(f, XS[4], T([("This session, or 7 days", "of transcripts, filtered"), ("Quotes, never rebuilds", "fu: blocks and fu-note: lines"),
                      ("Your pattern", "after 5 graded expectations"), ("Worth learning next", "one item, first step")],
                     [("当前会话或最近 7 天", "会话记录经过滤后读取"), ("只引用，不补写", "fu: 区块与 fu-note: 行"),
                      ("你的规律", "已评判的预期满 5 条后"), ("接下来值得弄懂的", "一项，附第一步")]))
    # the record
    f.rect(40, 556, 1120, 96, PINK, PINK, 1, 10)
    f.raw(f'<rect x="40" y="556" width="5" height="96" rx="2.5" fill="{ORG}"/>')
    f.raw(f'<rect x="60" y="570" width="230" height="28" rx="14" fill="{ORG}"/>')
    f.mono(175, 589, T("THE CONVERSATION", "对话即记录"), 13, INK, "700", "middle")
    f.text(310, 589, T("is the record. Nothing is written to disk unless you say \"save\".",
                       "除非你说“保存”，否则不往磁盘写任何东西。"), 14, INK, SANS)
    f.raw(f'<rect x="60" y="612" width="230" height="28" rx="14" fill="#FFFFFF" stroke="{ORG}" stroke-width="1.2"/>')
    f.mono(175, 631, T("TRIVIAL REQUESTS", "琐碎的请求"), 13, ACC, "700", "middle")
    f.text(310, 631, T("Lookups and casual talk get no block at all.", "简单查询和闲聊不输出任何区块。"), 14, INK, SANS)
    return f.svg()


if __name__ == "__main__":
    open(f"{ROOT}/assets/lifecycle.svg", "w", encoding="utf-8").write(lifecycle(False))
    open(f"{ROOT}/assets/zh/src/lifecycle.svg", "w", encoding="utf-8").write(lifecycle(True))
    print("ok")
