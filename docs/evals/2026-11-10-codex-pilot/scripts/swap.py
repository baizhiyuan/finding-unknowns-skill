"""Round 2: copy grade/T1-T5.md to grade-swap/ with outputs X and Y exchanged."""
import pathlib
src, dst = pathlib.Path("/tmp/fu-eval/grade"), pathlib.Path("/tmp/fu-eval/grade-swap")
dst.mkdir(exist_ok=True)
for t in ["T1", "T2", "T3", "T4", "T5"]:
    head, rest = (src / f"{t}.md").read_text(encoding="utf-8").split("\n## Output X\n", 1)
    x, y = rest.split("\n## Output Y\n", 1)
    (dst / f"{t}.md").write_text(head + "\n## Output X\n" + y.rstrip("\n") + "\n\n## Output Y\n" + x,
                                 encoding="utf-8")
