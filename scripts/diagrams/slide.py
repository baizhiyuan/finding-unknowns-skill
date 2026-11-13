#!/usr/bin/env python3
"""The slide (offloading → deferral → cognitive surrender, after Addy Osmani) in the 4.x style,
redrawn from the left half of 4.x's handoff.svg, with the map field or habit that interrupts
each step underneath.

Usage (from the repo root):
    python3 scripts/diagrams/slide.py .
    python3 scripts/outline_cjk.py --fonts DIR --out assets/zh assets/zh/src/slide.svg"""
from __future__ import annotations

import sys

from style import ACC, EDGE, GRN, INK, MONO, ORG, PINK, RED, SANS, SERIF, SUB, Fig, tw

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
X0, X1 = 40, 1160
GAP = 20
COLW = (X1 - X0 - 2 * GAP) / 3
BAR_Y = 214


def field_pill(f, x, y, txt):
    size = 12
    w = tw(txt, size, mono=True) + 20
    f.raw(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="{PINK}"/>')
    f.mono(round(x + w / 2, 1), y + 16.5, txt, size, ACC, "700", "middle")
    return x + w + 8


def slide(zh: bool) -> str:
    T = (lambda en, cn: cn) if zh else (lambda en, cn: en)
    f = Fig(1200, 560, T("The slide, and what is meant to interrupt it", "滑落的过程，以及用来打断它的环节"),
            T("Addy Osmani's slide across many handoffs: offloading (you delegate and keep ownership), deferral (the "
              "output becomes the next input), cognitive surrender (the output becomes your \"known\" without an update step). Under "
              "each step, the part of the map meant to interrupt it: the pause after fu:before keeps ownership with you; "
              "You expect records your prediction before the answer exists; Not proved and Still unknown keep a claim "
              "from entering the known beyond its evidence. This is why the fields exist; whether they slow the slide "
              "has not been measured.",
              "Addy Osmani 描述的多次交接中的滑落：委托（把工作交出去，责任仍在自己），依赖（直接拿输出当下一步的依据），"
              "放弃判断（输出没有经过更新地图这一步，就成了你的“已知”）。每一步下方是用来打断它的环节：fu:before 之后的停顿让决定仍由你来做；"
              "“你的预期”在答案出现之前记下你的预测；“没有证明的”和“仍然未知”让写进“已知”的内容不超出证据。"
              "这是设置这些栏目的理由；它们能否减缓滑落，尚未测量。"), zh)
    f.header(T("The slide, and what is meant to interrupt it", "滑落的过程，以及用来打断它的环节"),
             T("Across many handoffs, delegating slides into surrender. Under each step, the part of the map meant to stop it.",
               "交接多了，委托会一步步滑向放弃判断。每一步下方是用来拦住它的那部分地图。"))
    # the bar, with the marker at offloading
    f.raw(f'<rect x="{X0}" y="{BAR_Y}" width="{X1 - X0}" height="22" rx="11" fill="url(#spec)"/>')
    mx = X0 + COLW * 0.32
    label = T("stay here", "停在这里")
    pw = tw(label, 13, mono=True) + 28
    f.raw(f'<rect x="{mx - pw / 2:.1f}" y="166" width="{pw:.0f}" height="26" rx="13" fill="{ORG}"/>')
    f.mono(round(mx, 1), 183.5, label, 13, INK, "700", "middle")
    f.raw(f'<path d="M{mx:.1f} 194V210" stroke="{ORG}" stroke-width="2.5" marker-end="url(#ah)"/>')
    f.raw(f'<circle cx="{mx:.1f}" cy="{BAR_Y + 11}" r="11" fill="#FAF9F5" stroke="{INK}" stroke-width="3"/>')
    steps = T([("offloading", GRN, ["delegate the work,", "keep ownership"]),
               ("deferral", ACC, ["the output becomes", "the next input"]),
               ("cognitive surrender", RED, ["the output becomes your \"known\"", "without an update step"])],
              [("委托", GRN, ["把工作交出去，", "责任仍在自己"]),
               ("依赖", ACC, ["直接拿输出", "当下一步的依据"]),
               ("放弃判断", RED, ["输出没有经过更新地图这一步，", "就成了你的“已知”"])])
    for k, (name, color, lines) in enumerate(steps):
        x = round(X0 + k * (COLW + GAP))
        f.text(x, 268, name, 20, color, SERIF, "700")
        for j, line in enumerate(lines):
            f.sans(x, 291 + j * 18, line, 13)
        if k:
            f.line(x - GAP / 2, 250, x - GAP / 2, 322, EDGE)
    # what interrupts each step
    cards = T([
        ("The pause", ["fu:before → your reply"],
         ["You see the map and answer it before", "anything changes: the decision stays yours."], GRN),
        ("Predict before you look", ["You expect"],
         ["Your guess is quoted, or \"not stated\"; the", "output is checked against it before reuse."], ACC),
        ("Name what the evidence leaves open", ["Not proved", "Still unknown"],
         ["A claim enters \"known\" no further than its", "evidence; the open part stays on the map."], RED),
    ], [
        ("改动之前的停顿", ["fu:before → 你的回复"],
         ["你看过地图并作出回答之后，助手才动手：", "决定仍由你来做。"], GRN),
        ("先预测，再看答案", ["你的预期"],
         ["只引用你的原话，否则写“未说明”；", "输出先与它对照，再拿去当下一步的依据。"], ACC),
        ("说清证据没有覆盖的部分", ["没有证明的", "仍然未知"],
         ["证据支持到哪里，“已知”就写到哪里；", "没解决的部分留在地图上。"], RED),
    ])
    for k, (title, fields, lines, color) in enumerate(cards):
        x = round(X0 + k * (COLW + GAP))
        w = round(COLW)
        f.arrow(x + 24, 372, x + 24, 330, color=color, marker="ah" if color != GRN else "ahg", width=2)
        f.mono(x + 36, 356, T("keeps you here", "让你停在这里") if k == 0 else T("interrupts it", "打断这一步"), 12, SUB, "700")
        f.card(x, 376, w, 124, accent=color)
        f.text(x + 22, 402, title, 15 if not zh else 15, INK, SANS, "700")
        px = x + 22
        for fld in fields:
            px = field_pill(f, px, 412, fld)
        for j, line in enumerate(lines):
            f.sans(x + 22, 458 + j * 18, line, 13)
    # credit and honesty line
    f.text(X0, 530, T("after Addy Osmani's posts on critical thinking when agents do the work.",
                      "参考 Addy Osmani 关于智能体代劳时保持批判性思维的帖子。"), 12.5, SUB, SANS)
    f.text(X1, 530, T("Why these fields exist; whether they slow the slide is not measured.",
                      "这是设置这些栏目的理由；它们能否减缓滑落，尚未测量。"), 12.5, ACC, SANS, "600", "end")
    return f.svg()


if __name__ == "__main__":
    open(f"{ROOT}/assets/slide.svg", "w", encoding="utf-8").write(slide(False))
    open(f"{ROOT}/assets/zh/src/slide.svg", "w", encoding="utf-8").write(slide(True))
    print("ok")
