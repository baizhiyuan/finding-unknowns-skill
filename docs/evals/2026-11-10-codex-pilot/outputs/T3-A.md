**Recommendation: don’t ship this as a demonstrated performance win yet.** The results are promising, but the benchmark setup cannot isolate the cache’s effect.

Team update:

The reported p50 change, **41.2 → 38.9 ms**, is a **5.6% reduction**. Across all recorded runs:

| Metric, averaged across runs | Baseline (5 runs) | LRU cache (3 runs) | Reduction |
|---|---:|---:|---:|
| p50 | 40.9 ms | 39.1 ms | 4.4% |
| p95 | 58.2 ms | 57.3 ms | 1.5% |

These are averages of each run’s percentiles, not pooled document percentiles. [Benchmark results](/tmp/fu-eval/runs/T3-A/tokbench/bench/results.csv)

The main limitation is that **every baseline run used `ci-runner-1` on November 3, while every cache run used `ci-runner-2` on November 8**. Machine and date differences could explain some or all of the improvement. Run ranges also overlap: baseline p50 spans 38.7–43.0 ms; cache p50 spans 37.6–40.8 ms.

The recorded cache statistics show **1,187 hits and 38,412 misses—a 3.0% hit rate**—for cache run 2 only. That corpus draws from a two-million-word vocabulary; its relevance to production traffic needs checking. A low hit rate doesn’t rule out a benefit, but it makes lookup overhead and memory cost worth measuring. [Cache statistics](/tmp/fu-eval/runs/T3-A/tokbench/bench/cache_stats.txt)

Before shipping on performance grounds, rerun both variants on the same machine with identical inputs, alternating their order over repeated trials. Measure cold and warm cache behavior on representative traffic, including p50, p95, hit rate, and memory use.

**Current conclusion: an observed improvement, with insufficient evidence to attribute it to the cache.**