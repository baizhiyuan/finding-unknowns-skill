#!/usr/bin/env python3
"""Outline Chinese text in SVG diagrams so they render identically everywhere.

GitHub serves README images without web fonts, so CJK text falls back to whatever the
viewer has installed (often SimSun on Windows), which looks thin and uneven. This tool
converts every <text> whose font-family starts with "Noto Sans SC" into glyph outlines,
defining each glyph once in <defs> and placing it with <use>. Other text (Latin titles,
monospace identifiers) is left untouched.

Usage:
    python3 scripts/outline_cjk.py --fonts DIR SRC.svg [SRC.svg ...] --out OUT_DIR

DIR must contain NotoSansSC-Regular.otf, NotoSansSC-Medium.otf and NotoSansSC-Bold.otf
(SIL Open Font License), e.g. from
https://github.com/notofonts/noto-cjk/tree/main/Sans/SubsetOTF/SC
"""
from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
TARGET_FAMILY = "noto sans sc"
INHERITED = ("font-family", "font-size", "font-weight", "fill", "fill-opacity",
             "opacity", "text-anchor", "letter-spacing", "font-style")
WEIGHT_FILES = {400: "NotoSansSC-Regular.otf", 500: "NotoSansSC-Medium.otf",
                700: "NotoSansSC-Bold.otf"}

ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)


def q(tag: str) -> str:
    return f"{{{SVG_NS}}}{tag}"


@dataclass(frozen=True)
class Run:
    text: str
    attrs: dict


class Font:
    def __init__(self, path: Path, weight: int):
        self.font = TTFont(str(path))
        self.weight = weight
        self.cmap = self.font.getBestCmap()
        self.glyphs = self.font.getGlyphSet()
        self.hmtx = self.font["hmtx"]
        self.upm = self.font["head"].unitsPerEm
        self.paths: dict[str, str] = {}

    def glyph_id(self, ch: str) -> str:
        name = self.cmap.get(ord(ch))
        if name is None:
            raise KeyError(f"U+{ord(ch):04X} {ch!r} not in Noto Sans SC ({self.weight})")
        return name

    def advance(self, ch: str) -> float:
        return self.hmtx[self.glyph_id(ch)][0]

    def path_for(self, ch: str) -> tuple[str, str]:
        name = self.glyph_id(ch)
        ref = f"nsc{self.weight}-{re.sub(r'[^A-Za-z0-9]', '_', name)}"
        if ref not in self.paths:
            pen = SVGPathPen(self.glyphs, ntos=lambda v: f"{round(v)}")
            self.glyphs[name].draw(pen)
            self.paths[ref] = pen.getCommands()
        return ref, self.paths[ref]


def weight_of(value: str | None) -> int:
    raw = (value or "400").strip().lower()
    num = {"normal": 400, "bold": 700, "bolder": 700, "lighter": 400}.get(raw)
    num = num if num is not None else int(float(raw))
    return 700 if num >= 600 else 500 if num >= 500 else 400


def effective(el: ET.Element, parents: dict, own: dict | None = None) -> dict:
    chain, node = [], el
    while node is not None:
        chain.append(node)
        node = parents.get(node)
    attrs: dict = {}
    for node in reversed(chain):
        for key in INHERITED:
            if node.get(key) is not None:
                attrs[key] = node.get(key)
    return {**attrs, **(own or {})}


def runs_of(text_el: ET.Element, base: dict) -> list[Run]:
    runs = [Run(text_el.text or "", base)]
    for child in text_el:
        if child.tag != q("tspan"):
            raise ValueError("only <tspan> children are supported inside <text>")
        if any(child.get(k) for k in ("x", "y", "dx", "dy")):
            raise ValueError("positioned <tspan> is not supported; split into <text>")
        own = {k: child.get(k) for k in INHERITED if child.get(k) is not None}
        runs.append(Run(child.text or "", {**base, **own}))
        runs.append(Run(child.tail or "", base))
    collapsed = [Run(re.sub(r"\s+", " ", r.text), r.attrs) for r in runs]
    joined = "".join(r.text for r in collapsed)
    lead = len(joined) - len(joined.lstrip(" "))
    trail = len(joined) - len(joined.rstrip(" "))
    out, pos, end = [], 0, len(joined) - trail
    for r in collapsed:
        start, stop = max(pos, lead), min(pos + len(r.text), end)
        if stop > start:
            out.append(Run(joined[start:stop], r.attrs))
        pos += len(r.text)
    return out


def outline_text(text_el: ET.Element, parents: dict, fonts: dict[int, Font]) -> ET.Element:
    base = effective(text_el, parents)
    runs = runs_of(text_el, base)
    size = float(base.get("font-size", "16"))
    spacing = float(base.get("letter-spacing", "0") or 0)
    if spacing:
        raise ValueError(f"letter-spacing on CJK text is not allowed: {''.join(r.text for r in runs)!r}")
    placed, cursor = [], 0.0
    for r in runs:
        font = fonts[weight_of(r.attrs.get("font-weight"))]
        scale = size / font.upm
        for ch in r.text:
            if ch != " ":
                ref, _ = font.path_for(ch)
                placed.append((ref, cursor, scale, r.attrs))
            cursor += font.advance(ch) * scale
    width = cursor
    anchor = base.get("text-anchor", "start")
    x0 = float(text_el.get("x", "0")) - {"start": 0, "middle": width / 2, "end": width}[anchor]
    y0 = float(text_el.get("y", "0"))
    label = "".join(r.text for r in runs)
    group = ET.Element(q("g"), {"aria-label": label, "role": "img"})
    if text_el.get("transform"):
        group.set("transform", text_el.get("transform"))
    for key in ("fill", "fill-opacity", "opacity"):
        if base.get(key) is not None:
            group.set(key, base[key])
    for ref, dx, scale, attrs in placed:
        use = ET.SubElement(group, q("use"), {
            "href": f"#{ref}", f"{{{XLINK_NS}}}href": f"#{ref}",
            "transform": f"translate({x0 + dx:.2f} {y0:.2f}) scale({scale:.5f} {-scale:.5f})"})
        if attrs.get("fill") and attrs.get("fill") != base.get("fill"):
            use.set("fill", attrs["fill"])
    return group


def is_target(el: ET.Element, parents: dict) -> bool:
    family = (effective(el, parents).get("font-family") or "").lower()
    return family.replace("'", "").replace('"', "").strip().startswith(TARGET_FAMILY)


def outline_file(src: Path, out: Path, fonts: dict[int, Font]) -> tuple[int, int]:
    tree = ET.parse(src)
    root = tree.getroot()
    parents = {child: parent for parent in root.iter() for child in parent}
    for f in fonts.values():
        f.paths.clear()
    targets = [el for el in root.iter(q("text")) if is_target(el, parents)]
    for el in targets:
        group = outline_text(el, parents, fonts)
        parent = parents[el]
        idx = list(parent).index(el)
        parent.remove(el)
        parent.insert(idx, group)
    defs = ET.Element(q("defs"))
    for f in fonts.values():
        for ref, d in sorted(f.paths.items()):
            ET.SubElement(defs, q("path"), {"id": ref, "d": d})
    root.insert(0, defs)
    out.parent.mkdir(parents=True, exist_ok=True)
    tree.write(out, encoding="utf-8", xml_declaration=False)
    return len(targets), sum(len(f.paths) for f in fonts.values())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fonts", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("sources", nargs="+", type=Path)
    args = ap.parse_args()
    missing = [n for n in WEIGHT_FILES.values() if not (args.fonts / n).exists()]
    if missing:
        print(f"error: missing fonts in {args.fonts}: {', '.join(missing)}", file=sys.stderr)
        return 2
    fonts = {w: Font(args.fonts / n, w) for w, n in WEIGHT_FILES.items()}
    for src in args.sources:
        try:
            texts, glyphs = outline_file(src, args.out / src.name, fonts)
        except (KeyError, ValueError) as exc:
            print(f"error: {src}: {exc}", file=sys.stderr)
            return 1
        print(f"{src.name}: {texts} text elements outlined, {glyphs} unique glyphs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
