I added `currency` to `Order`. The three tests pass when called directly, but pytest isn't installed here, so I haven't run the suite itself. Nothing is committed.

**Changes**
- **`orders/models.py`:** `currency: str = "CNY"`. The default keeps existing call sites working.
- **`migrations/0007_orders_currency.sql`:** adds the column as nullable with no default. The runbook says a `NOT NULL DEFAULT` on Postgres 10 rewrites the 40M-row table and locks it, which caused a 47-minute outage last time. You still need to backfill `'CNY'` in batches of 10k and then add the constraint, as separate steps. I didn't write those.
- **`orders/cache.py`:** `CACHE_SCHEMA` bumped from 3 to 4. A field change without the bump crashed every worker in the 2026-08-14 incident.
- **`orders/webhook.py`:** `currency` is excluded from the `order.created` payload. The payload was built with `asdict(order)`, so the new field would have gone to Acme automatically. Their v1 schema rejects unknown fields and drops the delivery. I added a test for this.

**Before you take EUR orders**
- **Acme:** they need a v2 schema and 30 days' notice before `currency` can go in the webhook. Until then, Acme will get EUR amounts with no currency and will read them as CNY.
- **`report.daily_revenue`:** it sums `amount_cents` across all orders, so EUR and CNY amounts would be added together on the finance dashboard. I left it alone because the right behavior is your call: per-currency totals, conversion, or filtering. It needs fixing before the first EUR order.
- **NULL currency:** legacy rows will have NULL until the backfill runs. Any code that reads the column from the DB should treat NULL as CNY. I didn't find any such code in this repo.
- **`BASE_CURRENCY`:** `settings.py` says every order is CNY. Update that comment if it matters.