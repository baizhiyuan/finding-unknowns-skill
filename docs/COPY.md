# Copy rules

For `README.md`, `README.zh.md`, `docs/` and diagram text. `CLAUDE.md`, `skills/` and `commands/` are out of scope.

**Before writing.** Name the reader and the next thing they do. A README reader decides whether to install; a diagram reader has ten seconds.

**Order of fixes:** the section's purpose → what belongs in `docs/` → repetition → names → sentences.

1. **One home per number.** A count appears in full once, in `docs/EVIDENCE.md` (`docs/EVIDENCE.zh.md` for the Chinese README). The README states the result in words and links to it.
2. **One job per appearance.** A claim may appear in the lead and in the evidence section. A third appearance is deleted.
3. **Reader or reviewer?** A sentence that defends a number against an objection moves to the evidence file.
4. **One name per thing,** from [GLOSSARY.md](GLOSSARY.md). No synonyms for variety. No internal labels (test arms, run ids) in reader-facing text.
5. **Neutral voice.** No "I", no "the owner", no author persona. Decisions are stated impersonally: "It was shipped as the release candidate anyway."
6. **Examples are real or marked.** Prefer a verbatim excerpt; mark an invented one "illustrative".
7. **Vary the shape.** At most one bold-label list per section.
8. **Add one, delete one.** After inserting a sentence, re-read its paragraph for what became redundant.
9. **Never soften a limit.** A failed test or an unmeasured claim stays visible, once, near the top.
10. **Compressing never strengthens a claim.** Keep qualifiers and the scope of each count; a dropped qualifier is a changed fact.

## Diagrams

- Every mark has a referent: one footnote per marked label; distinct notes use `*`, `†`, `‡`.
- A maintainer-only note may be deleted only if the README section the diagram illustrates already says it.
- A label is not repeated by its own tab. When space is short, delete words.

## 中文

- 术语以 [GLOSSARY.md](GLOSSARY.md) 的中文列为准，一个名字只指一件事。朗读整句检查术语；只在译文里成立的词，按术语表的问题处理，先改术语表。
- 先列出这一段要表达的命题，再用中文重写，不逐句翻译英文。
- 文风正式、自然，像工程师写的技术文档；标题直接给结论，不写口号。
- 不用破折号"——"。
- 命令、文件名、区块标题（如 `fu:before`）和 KK/KU/UK/UU 保留英文。
- 中立语气同样适用：不用"我"，也不用"作者"指代决策人。

## Checks

`python3 scripts/validate.py --copy` flags, in the READMEs, internal labels, the author persona and a fraction appearing more than twice (it counts repeated numbers, not claims); in SVGs, marks that do not pair one label with one footnote. Report a rewrite with the names chosen, what moved to `docs/`, word counts before and after, and the `--copy` output.

Several rules are adapted, reworded for this repo, from the `nature-shared` core files of [nature-skills](https://github.com/Yuan1z0825/nature-skills) (Apache-2.0).
