#!/usr/bin/env python3
"""The 6.0 lifecycle diagram in the 4.x style: before (one pause) → work → after → look-back.

Usage (from the repo root):
    python3 scripts/diagrams/lifecycle.py .
    python3 scripts/outline_cjk.py --fonts DIR --out assets/zh assets/zh/src/lifecycle.svg
The hero and quadrant diagrams were relabelled by one-off edits and have no generator here."""
from __future__ import annotations

import sys

from style import ACC, EDGE, GRN, INK, MONO, MUTE, ORG, PANEL, PINK, SAND, SANS, SUB, Fig

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
XS = (40, 326, 612, 898)
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
            T("Before non-trivial changes the assistant shows the map (fu:before) and waits for your reply "
              "(\"just do it\" skips the wait). Then it works, stops only for a scope change, a falsified "
              "premise that changes the task or an irreversible step, and shows what moved (fu:after). The look-back runs only "
              "when you ask. Nothing is written to disk.",
              "做非琐碎的改动之前，助手先列出地图（fu:before），等你回复（说“直接做”则不等）。之后开始执行，"
              "只在范围变化、前提失效以致任务改变或不可逆操作时停下，最后说明地图上的变化（fu:after）。回顾只在你要求时进行。"
              "不往磁盘写任何东西。"), zh)
    f.header(T("// HOW IT RUNS", "// 运行方式"),
             T("Map, your reply, then what moved", "先列地图，等你回复，再说明变化"),
             T("The always-on text runs the first three steps on every non-trivial request; the look-back runs only when you ask.",
               "常驻文字在每次非琐碎的请求中执行前三步；回顾只在你要求时进行。"))
    for x, label in zip(XS, T(["YOU · guess in the request", "YOU · reply: go, or answers",
                               "YOU · read what is not proved", "YOU · ask; fu-note: any time"],
                              ["你：在需求里写上猜测", "你：回复“继续”或给出答案",
                               "你：先看“没有证明的”", "你：主动要求；随时写 fu-note:"])):
        f.human(x, 150, 262, label)
        f.line(x + 131, 178, x + 131, TOP, INK, 1.5, "3 3")
    cols = [(T("BEFORE", "动手之前"), "fu:before", T("before any change", "改动之前"), ORG),
            (T("WORK", "执行"), "", T("after your reply", "你回复后"), GRN),
            (T("AFTER", "完成之后"), "fu:after", T("after the result", "给出结果后"), ORG),
            (T("LOOK-BACK", "回顾"), "/fu-lookback", T("when you ask", "你要求时"), SAND)]
    for i, ((name, cmd, when, color), x) in enumerate(zip(cols, XS)):
        f.topband(x, TOP, 262, BOTTOM - TOP, color)
        f.serif(x + 18, 232, name, 21)
        f.mono(x + 244, 232, when, 12, SUB, anchor="end")
        if cmd:
            f.mono(x + 18, 256, cmd, 13, ACC, "700")
        if i < 3:
            f.arrow(x + 264, 352, x + 284, 352, dash="4 4" if i == 2 else None)
    # before: the four quadrants
    x = XS[0]
    for k, (code, main, sub) in enumerate(T(
            [("KK", "Relying on", "each with its source; ✗ if wrong"), ("KU", "Open", "I find out, or you decide"),
             ("UK", "I assume you want", "a guess you can react to"), ("UU", "You did not ask", "but it matters; at most 3")],
            [("KK", "我依据的", "逐条注明来源；标出被推翻的"), ("KU", "待解决", "我去查，或由你定"),
             ("UK", "我猜你默认", "说出猜测，供你表态"), ("UU", "你没问但要紧", "最多三条")])):
        y = 270 + k * 50
        f.badge(x + 18, y, code, size=30, hot=code == "UU")
        f.text(x + 58, y + 13, main, 14, INK, SANS, "600")
        f.text(x + 58, y + 31, sub, 12, SUB, SANS)
    f.text(x + 18, 488, T("I expect …; wrong if …", "我的预期……；若……则我错了"), 13, ACC, SANS, "700")
    f.text(x + 18, 508, T("your expectation: quoted, or not stated", "你的预期：只引用原话，否则写“未说明”"), 12, SUB, SANS)
    # the pause, then the work
    x = XS[1]
    f.text(x + 18, 266, T("Waits for your reply", "先等你回复"), 14, ACC, SANS, "700")
    f.text(x + 18, 285, T("\"go\" accepts the recommendations", "回复“继续”即采纳建议答案"), 12, SUB, SANS)
    f.text(x + 18, 303, T("say \"just do it\" to skip the wait", "说“直接做”则不等待"), 12, SUB, SANS)
    f.text(x + 18, 326, T("Then stops only for:", "之后只在以下情况停下："), 14, INK, SANS, "600")
    y = 344
    for main, sub in T([("a scope change", ""), ("a falsified premise", "that changes the task"),
                        ("an irreversible step", "")],
                       [("范围变化", ""), ("前提失效以致任务改变", ""), ("不可逆操作", "")]):
        f.raw(f'<circle cx="{x + 24}" cy="{y - 5}" r="4" fill="{ORG}"/>')
        f.text(x + 36, y, main, 14, INK, SANS)
        if sub:
            y += 16
            f.text(x + 36, y, sub, 12, SUB, SANS)
        y += 20
    f.rect(x + 16, 410, 230, 64, "#FFFFFF", ORG, 1.2, 10)
    f.text(x + 30, 429, T("Irreversible step:", "不可逆操作："), 13, ACC, SANS, "700")
    f.text(x + 30, 446, T("exact command, your yes,", "给出确切命令，等你同意，"), 13, SUB, SANS)
    f.text(x + 30, 463, T("run once, never as a check", "只执行一次，绝不当检查跑"), 13, SUB, SANS)
    f.rect(x + 16, 480, 230, 46, "#FFFFFF", EDGE, 1, 10)
    f.text(x + 30, 498, T("Everything else:", "其余情况："), 13, GRN, SANS, "700")
    f.text(x + 30, 516, T("proceed; report in fu:after", "继续做，在 fu:after 中报告"), 12, SUB, SANS)
    # after
    rows(f, XS[2], T([("Expected → found", "a verdict; why only on a miss"), ("Now known", "with evidence"),
                      ("Not proved", "what each check leaves open"), ("Still unknown", "cheapest way to find out"),
                      ("Decided for you", "what you did not ask for")],
                     [("预期 → 实际", "给出结论；只在落空处写原因"), ("新知道的", "附证据"),
                      ("没有证明的", "每项检查留下了什么"), ("仍然未知", "附最省事的查法"),
                      ("替你定的", "你没要求的选择和改动")]), hot=(2,))
    f.text(XS[2] + 18, 516, T("then the turn ends", "然后这一轮结束"), 12, MUTE, MONO)
    # look-back
    rows(f, XS[3], T([("This session, or 7 days", "of transcripts, filtered"), ("Quotes, never rebuilds", "fu: blocks and fu-note: lines"),
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
