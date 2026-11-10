The recorded p50 improvement is **5.6%, but the benchmark does not establish that caching caused it.**

Team write-up — retrospective shipping assessment:

1. **Evidence.** Recomputing [bench/results.csv](/tmp/fu-eval/runs/T3-B/tokbench/bench/results.csv) gives:

   | Median of per-run percentiles | Baseline, 5 runs | Cached, 3 runs | Change |
   |---|---:|---:|---:|
   | p50 | 41.2 ms | 38.9 ms | −2.3 ms / −5.6% |
   | p95 | 58.0 ms | 57.2 ms | −0.8 ms / −1.4% |

   These are summaries across runs, not pooled document percentiles. Baseline ran on `ci-runner-1` on November 3; cached ran on `ci-runner-2` on November 8.

2. **What this establishes.** Cached runs recorded lower central estimates. It does **not** isolate the cache’s effect: machine and date changed, run counts differ, and variability is substantial. Per-run p50 ranges were 38.7–43.0 ms versus 37.6–40.8 ms. Those ranges describe variability; they are not confidence intervals.

3. **Assumptions.** We interpret “performance win” as a repeatable benefit on the search service’s workload. Benchmark representativeness and end-to-end service impact are unverified.

4. **Theory → measured → consistency → mechanism.** Retrospectively, caching should save splitting work when words repeat before eviction. However, [cache_stats.txt](/tmp/fu-eval/runs/T3-B/tokbench/bench/cache_stats.txt) records only **1,187 hits and 38,412 misses: a 3.0% hit rate**, from cached run 2 alone. Whether caching explains the latency change is **undetermined**. Misses incur cache bookkeeping; the balance between that cost and avoided splitting remains unmeasured. This explanation is **inferred**, not verified. No pre-agreed shipping rule was found; the result remains descriptive.

5. **Strongest counterargument — same-context review, weaker.** A 3% hit rate could still help if hits avoid unusually expensive long-word splits. Production could also have more repetition. Low hit rate alone does not disprove the optimization.

6. **Potential blind spot.** The cache holds up to 4,096 entries, but entry count does not bound memory in bytes; retained words and token tuples vary in size.

7. **Not checked.** Correctness tests, memory overhead, concurrency, cold versus warm behavior, and production hit rates. No benchmark was rerun: the referenced corpus and benchmark harness are absent.

8. **Next evidence needed.** Alternate baseline and cached runs on the same machine with identical inputs and equal repetitions. Measure representative traffic plus low-repetition inputs, cold/warm latency, p95, hit rate, and memory. Before those fresh runs, agree on a worthwhile improvement and acceptable regressions.

9. **Recommendation: hold shipping as a performance win.** The cache remains a plausible optimization worth testing. Report this as an **observed, confounded improvement**, and make the shipping decision after a controlled comparison.