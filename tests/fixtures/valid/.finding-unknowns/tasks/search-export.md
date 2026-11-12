# search-export
Goal: 为图书馆目录添加前缀搜索导出，写入 build/search.json · State: building
Needs you: nothing
Mode: learn · Last seen by you: never
Timing: Brief frozen 2026-11-12 11:00, commit 9f8e7d6

## Brief (frozen 2026-11-12 11:00)
Approach:
  - reuse the existing tokenizer because it already folds case
P1 (you · high) "前缀搜索会比全文搜索快"
  - falsifier: the prefix query is slower on the 10k fixture
  - should not change: full-text results
A1 (agent · medium) "prefix search returns the same top 10 as full text for single-word queries"
  - falsifier: any single-word query differs in its top 10
  - should not change: multi-word query results
Stop-points: irreversible · scope · dead-premise · budget > 2× 1 h
C1 export writes valid JSON
  - check: `python -m json.tool build/search.json` exits 0
  - does NOT prove: that the ranking is right
  - lane: reversible
Check files: none

## Amendments

## Deltas
Latest: D1
Rollup:

## Model changes

## Open
