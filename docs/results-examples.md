# Results: examples and anti-patterns

Companion to [`results.md`](../skills/finding-unknowns/references/results.md). Documentation only:
moved out of the skill in 5.2, so it is not loaded at runtime.

## Examples

```
Frozen rule (verbatim, approved before launch): "Ship if the conversion-lift 95% CI lower
bound > 0 and the refund-rate increase is < 0.3 pt."

Bottom line: rule verdict FAIL (lower bound −0.1 pt). Direction: alive-but-constrained.
The overall effect cannot be told apart from zero, but the lift is where the theory said
it would be (mobile) and absent where it said it would be absent (desktop).
Noise floor: last month's A/A test, ±0.4 pt on conversion.

| Question | Theory | Measured | Consistent? | Mechanism [tier] |
|---|---|---|---|---|
| Overall conversion lift? | Fewer fields → fewer abandons → about +1.0 pt | +0.5 pt [−0.1, +1.1], n = 48k per arm | can't tell: the CI spans both 0 and the predicted +1.0 | Diluted by desktop (next row) [supported] |
| Where does it show up? | Mobile about +1.5 pt (typing is costly); desktop ≈ 0 (a gain ≥ 1 pt would matter) | Mobile +1.3 [+0.4, +2.2]; desktop −0.1 [−0.9, +0.7] | consistent, including the predicted null | Typing cost on small screens [verified: abandon events fell only at the three typing-heavy fields and only on mobile; a design-wide or scroll-length effect would also have moved the non-typing fields, and it did not] |
| Refunds unchanged? | No mechanism links form length to refunds | +0.1 pt [−0.2, +0.4] | can't tell: upper bound crosses 0.3 | no mechanism named (no tier) |

Facts: mobile lift; desktop null; overall CI crosses 0.
Inferences: none beyond the tiers above.
To test: refund effect at a larger n.
Caveats: none of the fairness checks failed; the prediction card was saved before launch.
Not checked: novelty effect after week 2.
Next: pre-register a mobile-only test under the same rule. It uses fresh traffic and
needs your approval. This run's FAIL stands.
```
Why good: each prediction has a size and a location, including where the effect should
not appear. The overall row is `can't tell`, not "partly", because its interval holds both
0 and the prediction. The predicted null is judged against a stated size that matters. The
mechanism earns `verified` from a split that could have come out the other way. The rule
verdict stays FAIL while the direction stays alive, and the next step is a new
pre-registered test, not a reinterpretation of this one.

```
[R1] Does the read-through cache cut API p95?
Theory      : 80% of reads repeat within 60s → hit rate ~0.8 → p95 roughly halves.
              Writes should not change.
Measured    : read p95 −41 ms (412 → 371, −10%), 5 reruns, spread ±15 ms; hit rate 0.31;
              write p95 +2 ms ±8 (a regression ≥20 ms would matter).
Consistent? : partly — direction yes, magnitude no; writes flat as predicted.
Mechanism   : broken link = "a repeat is a cache hit". Reads do repeat, but the cache
              key includes the session ID, so repeats from different sessions miss
              [supported: the key format explains a 0.31 hit rate].
              Next check: replay one hour of logs with a session-free key; the predicted
              hit rate is ≥0.7.
```
Why good: the magnitude miss is traced to one link. The writes-flat half shows the
change did no damage. The next check is cheap and can fail.

```
New ranking model: NDCG 0.412 vs baseline 0.418. Doesn't pass, dropping this direction.
```
Why bad: no theory, no noise floor (is 0.006 within run-to-run spread?), no check that
the runs and query sets matched, no broken link named. A direction got discarded on one
confounded number.

```
It failed the pre-registered latency guard in one region, but that is clearly traffic
noise and the design is sound, so we treat it as passing.
```
Why bad: the rule verdict was rewritten by an untested environmental story. The correct
report is "rule verdict FAIL; direction alive-but-constrained because …; next
pre-registered test …".


## Anti-patterns

Recurring failures in empirical work. Each costs a decision when it goes unnoticed:

| Pattern | What it looks like | Instead |
|---------|-------------------|---------|
| Verdict without theory | "Didn't pass, dropping it" | Name the broken link and the next check |
| Story-fitting | A mechanism invented after the result, stated as fact | Tag it `inferred`; propose the discriminating test |
| Rescue by mechanism | "It failed, but the mechanism is sound, so it passes" | Rule verdict stands; direction can stay alive |
| Proxy drift | Average accuracy improves while the cases that drive the decision (top-ranked items, slowest requests) get worse | Report the decision-relevant metric first |
| Blunting to hit a cost metric | Delaying or averaging the output lowers a cost metric and also lowers accuracy and timeliness | Fix cost where it arises; don't degrade the core output |
| Unequal comparison | 3 runs vs 5; different date ranges; different populations | Match both sides, or say "can't tell" |
| Best-window reporting | The 3 good weeks out of 10; the best region | Report all of them |
| Pooled masking | The pooled result passes while the replication batch alone fails | Lead with the failed batch |
| Silent gate | A diagnostic gets used as a rejection line | Threshold gate: explain, get approval, apply going forward only |
| Retroactive rule | A new threshold re-judges old results | Rules apply from their approval onward |
| Blame the world | "Regime change" with no evidence | Walk pipeline → comparison → metric → theory first |
| Numeric failure as idea failure | A NaN-masked loss or an overflowed counter reported as "approach X doesn't work" | Mark the run `void`, fix the numerics, rerun on fresh data (or a re-read with approval) |
| Void-and-rerun rescue | A failed run is voided for a bug, rerun on the same holdout, and the new PASS reported as confirmation | A re-read is `not confirmatory`; audit passing runs for the same bug |
| Post-hoc as prediction | A theory written after seeing the result, reported as `consistent [supported]` | `post-hoc fit (not a test)`, tier ≤ `inferred`, plus a prediction card for a fresh run |
| Undefined terms | "Rare event", "accuracy", "return" used in shifting senses | Define each term before measuring |
