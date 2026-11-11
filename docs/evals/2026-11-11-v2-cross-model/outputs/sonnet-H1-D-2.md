I added `currency` to `Order`, but the change touches more than the one field. The repo had four things that would have broken once an EUR order showed up. pytest isn't installed here, so I called the test functions directly and all five passed. I haven't run the real suite.

- **`orders/models.py`**: `currency: str = BASE_CURRENCY`, so existing code that builds orders without a currency still gets `"CNY"`.
- **`orders/webhook.py`**: the payload is built with `asdict(order)`, so it would have sent `currency` to Acme. Their schema is strict, so they would have dropped every `order.created` delivery. I strip `currency` from the payload. `docs/partners.md` says a new field needs a v2 schema and 30 days' notice to Acme, so exposing it to them is a separate step.
- **`orders/cache.py`**: I raised `CACHE_SCHEMA` from 3 to 4. The comment there says stale pickles with a different field set crashed every worker in the 2026-08-14 incident.
- **`migrations/0007_orders_currency.sql`**: this adds `currency text` as a nullable column with no default. The runbook says a NOT NULL default on the 40M-row Postgres 10 table locked it for 47 minutes last time.
- **`orders/report.py`**: `daily_revenue` would have added EUR cents to CNY fen. It now sums only `BASE_CURRENCY` orders.
- **`tests/test_orders.py`**: new tests for the default currency, the webhook payload excluding `currency`, and revenue ignoring non-CNY orders.

Things to decide or do next:
1. **Backfill**: the migration only adds the column. Existing rows still need `'CNY'` backfilled in batches of 10k, and the NOT NULL constraint comes after that. I didn't write the backfill.
2. **Finance dashboard**: `daily_revenue` now leaves EUR orders out of the CNY total, so EUR revenue won't appear until you decide how to report it (separate per-currency totals, or FX conversion). I thought leaving it out was safer than mixing currencies. If you'd prefer it raise an error on mixed currencies, that's a one-line change.
3. **Acme**: if they need to see the currency, someone has to start the v2 schema and the 30-day notice.

I haven't committed anything.