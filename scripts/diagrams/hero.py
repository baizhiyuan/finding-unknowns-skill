#!/usr/bin/env python3
"""The 6.0 hero banner in the 4.x style: name and tagline on the left, a terminal card on the
right showing fu:before, the reply "go", and fu:after for the README's /export example.

Usage (from the repo root):
    python3 scripts/diagrams/hero.py .
    python3 scripts/outline_cjk.py --fonts DIR --out assets/zh assets/zh/src/hero.svg"""
from __future__ import annotations

import sys

from style import ACC, EDGE, INK, MONO, MUTE, ORG, PANEL, PAPER, PINK, RED, SAND, SERIF, SANS, SUB, GRN, ZH, esc, tw

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
VERSION = "v6.0.0-rc.2"
W, H = 1200, 420
CARD_X, CARD_Y, CARD_W, CARD_H = 640, 34, 524, 352
LINE = 22

DEFS = """<defs>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#B1ADA1" opacity="0.28"/></pattern>
<filter id="fog" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="sh" x="-5%" y="-5%" width="110%" height="120%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#141413" flood-opacity="0.08"/></filter>
<clipPath id="frame"><rect width="1200" height="420" rx="18"/></clipPath>
</defs>"""

CONTOURS = """<g fill="none" stroke="#B1ADA1" stroke-opacity="0.45" stroke-width="1.2">
<path d="M560 380C640 320 720 350 800 318S960 360 1050 306S1160 276 1210 312"/>
<path d="M580 348C660 288 730 318 810 286S960 330 1040 276S1150 246 1210 282"/>
<path d="M600 316C680 258 740 286 820 254S960 298 1030 246S1140 216 1210 252"/>
<path d="M620 120C700 70 780 100 860 70S1000 96 1080 56S1170 40 1210 60"/>
<path d="M600 88C690 40 770 66 850 38S1000 62 1070 26S1160 12 1210 28"/>
</g>
<g filter="url(#fog)" fill="#F0EEE6">
<ellipse cx="640" cy="120" rx="110" ry="50" opacity="0.7"/><ellipse cx="620" cy="330" rx="100" ry="45" opacity="0.7"/>
</g>"""


def text(o, x, y, t, size, fill, family, weight=None, anchor=None, extra=""):
    if any("　" <= c <= "鿿" or "＀" <= c <= "￯" for c in t):
        family = ZH
    a = f' font-weight="{weight}"' if weight else ""
    a += f' text-anchor="{anchor}"' if anchor else ""
    o.append(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{fill}"{a}{extra}>{esc(t)}</text>')


def chip(o, x, y, label):
    w = round(tw(label, 14, mono=True) + 22)
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="12" fill="{PINK}" stroke="{ORG}"/>')
    text(o, x + w / 2, y + 19.9, label, 14, ACC, MONO, "700", "middle")
    return x + w + 10


def term_line(o, x, y, line, zh):
    """One line of terminal output; headers in accent, ✗ in red, the rest in ink."""
    if line.startswith("fu:"):
        text(o, x, y, line, 13, ACC, MONO, "700")
        return
    indent = len(line) - len(line.lstrip(" "))
    body = line.lstrip(" ")
    lead = x + indent * 7.8
    text(o, lead, y, "-", 13, MUTE, MONO)
    body = body[2:]
    bx = lead + 15.6
    if body.startswith("✗ "):
        text(o, bx, y, "✗", 13, RED, MONO, "700")
        bx += 15.6
        body = body[2:]
    fill = INK if indent else SUB
    weight = None if indent else "700"
    text(o, bx, y, body, 13 if not zh else 13, fill, MONO, weight)


def hero(zh: bool) -> str:
    T = (lambda en, cn: cn) if zh else (lambda en, cn: en)
    title = f"finding-unknowns {VERSION}"
    desc = T("Banner: finding-unknowns, keep your own map of what you know and do not know, and update it only on "
             "evidence. A terminal card shows fu:before for a bug fix (your quoted expectation, a premise marked ✗, a question that needs you, "
             "with a recommended answer), the reply \"go\", and fu:after (what the checks did not prove, what is "
             "still unknown).",
             "横幅：finding-unknowns，看清自己知道什么、不知道什么，只凭证据更新这张地图。终端卡片依次显示修复一个错误时的 "
             "fu:before（原话引用的预期，一条被推翻的前提，一个需要你定并附建议答案的问题）、你的回复“继续”，以及 fu:after"
             "（检查没有证明的、仍然未知的）。")
    o: list[str] = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
             f'aria-labelledby="t d">\n<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>')
    o.append(DEFS)
    o.append(f'<rect width="{W}" height="{H}" rx="18" fill="{PAPER}" stroke="{EDGE}"/>')
    o.append('<g clip-path="url(#frame)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#dots)"/>')
    o.append(CONTOURS)
    o.append("</g>")
    # left column
    text(o, 56, 84, T(f"{VERSION} · for Claude Code", f"{VERSION} · 用于 Claude Code"), 15, ACC, MONO, "700")
    text(o, 54, 166, "finding-unknowns", 64, INK, SERIF, "700")
    if zh:
        text(o, 56, 214, "看清自己知道什么、不知道什么，", 22, INK, ZH, "500")
        text(o, 56, 248, "只凭证据更新这张地图。", 20, SUB, ZH, "400")
    else:
        text(o, 56, 212, "Keep your own map of what you know and do not know,", 20, INK, SANS)
        text(o, 56, 240, "and update it only on evidence.", 20, SUB, SANS)
    x = 56
    for label in ("fu:before", "fu:after"):
        x = chip(o, x, 278, label)
    x = 56
    for label in ("/fu-interview", "/fu-lookback"):
        x = chip(o, x, 316, label)
    # terminal card
    o.append(f'<rect x="{CARD_X}" y="{CARD_Y}" width="{CARD_W}" height="{CARD_H}" rx="12" fill="#FFFFFF" '
             f'stroke="{EDGE}" stroke-width="1.5" filter="url(#sh)"/>')
    o.append(f'<path d="M{CARD_X} {CARD_Y + 12}a12 12 0 0 1 12 -12h{CARD_W - 24}a12 12 0 0 1 12 12v18H{CARD_X}z" fill="{PANEL}"/>')
    o.append(f'<path d="M{CARD_X} {CARD_Y + 30}H{CARD_X + CARD_W}" stroke="{EDGE}"/>')
    for k, c in enumerate((RED, SAND, GRN)):
        o.append(f'<circle cx="{CARD_X + 20 + 16 * k}" cy="{CARD_Y + 15}" r="4" fill="{c}"/>')
    text(o, CARD_X + CARD_W / 2, CARD_Y + 20, T("claude · ~/shop", "claude · ~/shop"), 12, MUTE, MONO, anchor="middle")
    tx = CARD_X + 22
    y = CARD_Y + 58
    before = T(["fu:before · fix the 500s on /export",
                "- You expect: \"…come from the new CSV encoder\"",
                "- KK · relying on",
                "  - ✗ the 500s began with the encoder change — logs: 3 Nov",
                "- KU · open",
                "  - drop empty fields? — needs you; I would pick \"no\""],
               ["fu:before · 修复 /export 的 500 错误",
                "- 你的预期：“……来自新的 CSV 编码器”",
                "- 已知的已知 · 我依据的",
                "  - ✗ 500 错误始于编码器改动 — 日志：11 月 3 日已出现",
                "- 已知的未知 · 待解决",
                "  - 空字段能否改为不输出？ — 需要你定；我建议不改"])
    for line in before:
        term_line(o, tx, y, line, zh)
        y += LINE
    # the reply (tight spacing leaves room for the You expect line)
    y -= 6
    pw = 92 if not zh else 104
    o.append(f'<rect x="{tx}" y="{y}" width="{pw}" height="28" rx="14" fill="{PINK}" stroke="{ORG}" stroke-width="1.2"/>')
    o.append(f'<circle cx="{tx + 17}" cy="{y + 10}" r="4.5" fill="{ORG}"/><path d="M{tx + 9} {y + 22}a8 7 0 0 1 16 0z" fill="{ORG}"/>')
    text(o, tx + 34, y + 19, T("go", "继续"), 13, INK, MONO, "700")
    text(o, tx + pw + 14, y + 19, T("you reply; \"go\" accepts the recommended \"no\"",
                                    "你的回复；“继续”即采纳建议答案"), 12, SUB, SANS)
    y += 28 + 24
    after = T(["fu:after · fix the 500s on /export",
               "- Not proved",
               "  - the new test covers NUL → leaves open other control chars",
               "- Still unknown",
               "  - a background job for export? — count exports > 10 s · you"],
              ["fu:after · 修复 /export 的 500 错误",
               "- 没有证明的",
               "  - 新测试覆盖了 NUL 字节 → 仍未说明其他控制字符",
               "- 仍然未知",
               "  - 导出是否应改为后台任务 — 统计超过 10 秒的导出 · 你"])
    for line in after:
        term_line(o, tx, y, line, zh)
        y += LINE
    o.append("</svg>\n")
    return "\n".join(o)


if __name__ == "__main__":
    open(f"{ROOT}/assets/hero.svg", "w", encoding="utf-8").write(hero(False))
    open(f"{ROOT}/assets/zh/src/hero.svg", "w", encoding="utf-8").write(hero(True))
    print("ok")
