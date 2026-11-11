I added `currency` to `Order`. It wasn't quite the one-line change, because the repo has several traps around it. pytest isn't installed here, so I called the five test functions directly and they all pass. I haven't run the suite under pytest.

**What changed**
- **`orders/models.py`:** `currency: str = BASE_CURRENCY` is the last field, so existing constructors still work and default to CNY.
- **`migrations/0007_orders_currency.sql`:** adds a nullable column with no default. The runbook says a `NOT NULL DEFAULT` locks the 40M-row table for about 47 minutes on Postgres 10. I haven't run the migration. The backfill (batches of 10k) and the later constraint still need doing, and NULL is treated as CNY until then.
- **`orders/cache.py`:** `CACHE_SCHEMA` goes from 3 to 4. A stale pickle with a different field set crashed every worker in the 2026-08-14 incident.
- **`orders/webhook.py`:** `currency` is stripped from the `order.created` payload. `asdict(order)` would otherwise have added it. Acme's v1 schema rejects unknown fields and drops the delivery, and a v2 schema needs 30 days' notice to them.
- **`orders/report.py`:** `daily_revenue` now sums only CNY orders. It was adding every `amount_cents`, so a EUR order would have been counted as fen.
- **`tests/test_orders.py`:** new tests for the CNY default, the webhook payload without `currency`, and revenue excluding EUR.

**Decisions for you**
1. **Revenue:** EUR orders are now left out of the finance dashboard's revenue number until someone decides how to convert them. If you'd rather it raise an error or add a per-currency breakdown, tell me.
2. **Acme:** they won't see the currency, so EUR orders will reach them with a bare `amount_cents`. That's ambiguous on their side. You'll want to start the v2 schema and the 30-day notice before taking EUR orders.
3. **Order creation:** there's no code in this repo that creates orders or reads `orders` rows. If another service does either, it needs to set `currency` and handle the new column.

I haven't committed anything.