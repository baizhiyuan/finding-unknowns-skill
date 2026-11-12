# quote-export
Goal: Write build/quotes.json from the scale-weight selector and publish it once · State: debriefed
Needs you: the carrier's remote-zone rate card (recommendation: send it and I re-check parcel 3; settles whether 8.00 stands)
Mode: ship · Last seen by you: 2026-11-12 10:40, after D3
Timing: Brief frozen 2026-11-12 09:05, commit 1a2b3c4

## Brief (frozen 2026-11-12 09:05)
Approach:
  - bill on scale weight only because the person says the carrier ignores volume
  - add one remote-zone service because parcel 3 has no service in the table
P1 (you · medium) "the bulky parcel's cheapest quote is Economy at 4.00, and the bulky parcel costs the same as a \"compact\" one"
  - falsifier: cheapest(bulky) is not Economy 4.00
  - should not change: the small parcel stays Economy 3.00
P2 (you · low) "every parcel has a service"
  - falsifier: any parcel is unavailable in build/quotes.json
  - should not change: the parcel ids and their order
A1 (agent · high) "a second publish raises FileExistsError"
  - falsifier: the second run succeeds
  - should not change: outbox/delivery.json bytes
A2 (agent · medium) "parcel 3's cheapest is Overnight at 8.00"
  - falsifier: cheapest(parcel 3) is not Overnight 8.00
  - should not change: the other two quotes
Stop-points: irreversible · scope · dead-premise · budget > 3× 30 min
Irreversible: `python publish.py build/quotes.json`
C1 billable weight is the scale weight
  - check: `python -c "import shipping; print(shipping.billable_kg(shipping.load()[0]))"` prints 2.0
  - does NOT prove: that the carrier bills on scale weight
  - lane: reversible
C2 the receipt records the exact bytes once
  - check: `python publish.py --dry-run build/quotes.json` exits 0
  - does NOT prove: that the payload prices are real carrier prices
  - lane: irreversible
  - post-check: `sha256sum build/quotes.json` equals the receipt's sha256
Check files: tests/test_shipping.py

## Amendments
M1 2026-11-12 09:40 · after D2 · confirmed: Overnight service added for the remote zone · why: parcel 3 had no service

## Deltas
Latest: D3
Rollup:
  - D1–D2: test updated and Overnight added; both logged with cost if wrong

## Model changes
- You expected the bulky parcel to cost the same as a compact one → it is 4.00 either way, because billing uses scale weight [shown, not confirmed]

## Open
- the remote-zone rate is synthetic until the carrier card arrives

## Debrief (2026-11-12 10:30; graded by fresh context)
Evidence:
  - `python -c "import shipping; print(shipping.billable_kg(shipping.load()[0]))"` → 2.0
  - `sha256sum build/quotes.json` → a089e5c3 (matches the receipt)
P1 (you · medium) "the bulky parcel's cheapest quote is Economy at 4.00, and the bulky parcel costs the same as a \"compact\" one"
  - measured: Economy 4.00 (build/quotes.json)
  - consistent?: consistent
  - mechanism: 2 + 1 × 2 kg gives 4.00 under scale billing [supported]
P2 (you · low) "every parcel has a service"
  - measured: 3 of 3 selected, one via the added Overnight row (build/quotes.json)
  - consistent?: partly
  - mechanism: parcel 3 is covered only by a service the agent added [inferred]
A1 (agent · high) "a second publish raises FileExistsError"
  - measured: FileExistsError on the second run (publish.py:14)
  - consistent?: consistent
  - mechanism: the receipt is opened in "x" mode [verified]
A2 (agent · medium) "parcel 3's cheapest is Overnight at 8.00"
  - measured: Overnight 8.00 (build/quotes.json)
  - consistent?: can't tell
  - mechanism: untested: the rate constants have no source in the repo [untested]
Integrity:
  - Brief vs freeze: unchanged
  - Check files: changed: tests/test_shipping.py
  - Unlogged hunks: none
Did NOT prove:
  - C1 billable weight → leaves open: whether the carrier bills on scale · still holds: the code uses scale weight
  - C2 receipt bytes → leaves open: whether 8.00 is a real price · still holds: one receipt, exact bytes
Not checked:
  - the carrier's actual remote-zone rate card
Bottom line:
  - holds: scale billing and the one-shot publish (P1, A1)
  - did not hold: coverage needed an invented service (P2)
  - stops at: the Overnight price has no source (A2)
