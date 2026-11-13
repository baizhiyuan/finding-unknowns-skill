"""Shared drawing kit reproducing the 4.x diagram style (palette, fonts, components)."""
from __future__ import annotations

import html
import re

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SERIF = "Georgia, 'Times New Roman', serif"
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
ZH = "Noto Sans SC, 'PingFang SC', 'Microsoft YaHei', sans-serif"
CJK = re.compile(r"[　-〿一-鿿＀-￯]")

INK, SUB, ACC, ORG, PAPER, PANEL, EDGE = "#141413", "#5E5D59", "#C15F3C", "#D97757", "#FAF9F5", "#F0EEE6", "#E3DFD3"
PINK, GRN, SAND, RED, MUTE, BLUE = "#F5DDD1", "#788C5D", "#D4A27F", "#B5442E", "#B1ADA1", "#6A9BCC"
KICKER_H = 28  # the height the removed kicker line used to take above each title

DEFS = """<defs>
<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M1 1L9 5L1 9z" fill="#D97757"/></marker>
<marker id="ahc" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1L9 5L1 9z" fill="#B1ADA1"/></marker>
<marker id="ahg" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M1 1L9 5L1 9z" fill="#788C5D"/></marker>
<filter id="sh" x="-5%" y="-5%" width="110%" height="120%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#141413" flood-opacity="0.08"/></filter>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="#B1ADA1" opacity="0.35"/></pattern>
<linearGradient id="spec" x1="0" x2="1"><stop offset="0" stop-color="#788C5D"/><stop offset="0.5" stop-color="#D4A27F"/><stop offset="1" stop-color="#B5442E"/></linearGradient>
</defs>"""


def esc(t: str) -> str:
    return html.escape(t, quote=False)


def tw(text: str, size: float, mono: bool = False) -> float:
    """Rough rendered width."""
    w = 0.0
    for ch in text:
        if CJK.match(ch):
            w += size
        elif mono:
            w += size * 0.6
        else:
            w += size * (0.3 if ch in "ilI.,:;'|!" else 0.55)
    return w


class Fig:
    def __init__(self, w: int, h: int, title: str, desc: str, zh: bool):
        self.w, self.h, self.zh = w, h, zh
        self.title, self.desc = title, desc
        self.o: list[str] = []
        self.lift = 0

    # --- text -----------------------------------------------------------------
    def text(self, x, y, txt, size=15, fill=INK, family=SANS, weight=None, anchor=None, extra=""):
        if CJK.search(txt):
            family = ZH
        a = f' font-weight="{weight}"' if weight else ""
        a += f' text-anchor="{anchor}"' if anchor else ""
        self.o.append(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{fill}"{a}{extra}>{esc(txt)}</text>')

    def serif(self, x, y, t, size=22, fill=INK, weight="700", anchor=None):
        self.text(x, y, t, size, fill, SERIF, weight, anchor)

    def sans(self, x, y, t, size=14, fill=SUB, weight=None, anchor=None):
        self.text(x, y, t, size, fill, SANS, weight, anchor)

    def mono(self, x, y, t, size=13, fill=INK, weight=None, anchor=None, spacing=None):
        extra = f' letter-spacing="{spacing}"' if spacing else ""
        self.text(x, y, t, size, fill, MONO, weight, anchor, extra)

    # --- page furniture ---------------------------------------------------------
    def header(self, title, subtitle):
        """Title and subtitle. There is no kicker line; the content moves up by its height."""
        self.lift = KICKER_H
        self.text(40, 92 if not self.zh else 96, title, 32, INK, SERIF, "700")
        self.sans(40, 118 if not self.zh else 126, subtitle, 15, SUB)

    def section(self, x, y, label):
        self.mono(x, y, label, 13, SUB, "700", spacing="1.5" if not CJK.search(label) else None)

    # --- shapes ---------------------------------------------------------------
    def rect(self, x, y, w, h, fill=PANEL, stroke=EDGE, sw=1, rx=12, shadow=False, dash=None):
        f = ' filter="url(#sh)"' if shadow else ""
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{f}{d}/>')

    def card(self, x, y, w, h, accent=None, fill=PANEL, stroke=EDGE, sw=1.5):
        self.rect(x, y, w, h, fill, stroke, sw, 12, True)
        if accent:
            self.o.append(f'<rect x="{x}" y="{y + 10}" width="5" height="{h - 20}" rx="2.5" fill="{accent}"/>')

    def topband(self, x, y, w, h, color=ORG):
        self.rect(x, y, w, h, PANEL, EDGE, 1, 12, True)
        self.o.append(f'<path d="M{x} {y + 12}a12 12 0 0 1 12 -12h{w - 24}a12 12 0 0 1 12 12v0H{x}z" fill="{color}"/>')

    def pill(self, x, y, txt, fill=PINK, stroke=None, color=ACC, size=13, h=26):
        w = tw(txt, size, mono=True) + 24
        s = f' stroke="{stroke}"' if stroke else ""
        self.o.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{fill}"{s}/>')
        self.mono(round(x + w / 2, 1), round(y + h / 2 + size * 0.36, 1), txt, size, color, "700", "middle")
        return x + w

    def human(self, x, y, w, txt):
        self.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="14" fill="{PINK}" stroke="{ORG}" stroke-width="1.2"/>')
        self.o.append(f'<circle cx="{x + 17}" cy="{y + 10}" r="4.5" fill="{ORG}"/><path d="M{x + 9} {y + 22}a8 7 0 0 1 16 0z" fill="{ORG}"/>')
        self.mono(x + 34, y + 19, txt, 12, INK, "700")

    def badge(self, x, y, label, dark=False, size=30, hot=False):
        fill = INK if dark else (ORG if hot else PINK)
        col = "#FAF9F5" if (dark or hot) else ACC
        self.o.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="6" fill="{fill}"/>')
        self.mono(x + size / 2, y + size / 2 + 5, label, 13, col, "700", "middle")

    def tag(self, x, y, txt, color=ACC, fill="#FFFFFF"):
        w = tw(txt, 12, mono=True) + 22
        self.o.append(f'<rect x="{x - w}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="{fill}" stroke="{color}" stroke-width="1.2"/>')
        self.mono(round(x - w / 2, 1), y + 16.5, txt, 12, color, "700", "middle")

    def arrow(self, x1, y1, x2, y2, color=ORG, marker="ah", width=2.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.o.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="{width}" fill="none" marker-end="url(#{marker})"{d}/>')

    def line(self, x1, y1, x2, y2, color=EDGE, width=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.o.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="{width}" fill="none"{d}/>')

    def raw(self, s):
        self.o.append(s)

    def svg(self) -> str:
        h = self.h - self.lift
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{h}" viewBox="0 0 {self.w} {h}" '
                f'role="img" aria-labelledby="t d">\n<title id="t">{esc(self.title)}</title><desc id="d">{esc(self.desc)}</desc>\n'
                f'{DEFS}\n<rect x="0.5" y="0.5" width="{self.w - 1}" height="{h - 1}" rx="18" fill="{PAPER}" stroke="{EDGE}"/>\n'
                f'<rect x="0.5" y="0.5" width="{self.w - 1}" height="{h - 1}" rx="18" fill="url(#dots)" opacity="0.5"/>\n')
        body = "\n".join(self.o)
        if self.lift:
            body = f'<g transform="translate(0 -{self.lift})">\n{body}\n</g>'
        return head + body + "\n</svg>\n"
