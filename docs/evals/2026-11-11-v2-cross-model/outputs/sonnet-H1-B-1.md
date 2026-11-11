I added `currency` to `Order`, defaulting to `"CNY"`, so existing callers still work. The four tests pass when run directly, because pytest isn't installed here. Nothing is committed.

Two things from the repo's docs and comments would have broken production, so I handled them:
- **Acme webhook:** `order_created_payload` builds its body from `asdict(order)`, so the new field would have gone to Acme. Their strict v1 schema rejects unknown fields and drops the delivery. I strip `currency` from the payload, and a test covers it. Sending it needs a v2 schema and 30 days' notice to Acme.
- **Cache:** I bumped `CACHE_SCHEMA` from 3 to 4 in `orders/cache.py`, as its comment requires. A stale pickle crashed every worker in the 2026-08-14 incident.

I also added `migrations/0007_orders_currency.sql`, which adds the column as nullable with no default. A NOT NULL default would lock the 40M-row `orders` table on Postgres 10, which last time meant 47 minutes of failed checkouts.

Before you take EUR orders:
1. **Backfill:** existing rows need `currency = 'CNY'` set in batches of 10k, then the NOT NULL constraint added. I didn't write that. Until then, rows loaded from the database will have a NULL currency.
2. **Revenue report:** `daily_revenue` in `orders/report.py` adds up `amount_cents` regardless of currency. Once EUR orders exist, the finance dashboard will silently add euro cents to CNY fen. I left it alone because the fix changes what the dashboard shows. Do you want it grouped by currency, or limited to CNY for now?
3. **Webhook:** Acme won't see the currency, so EUR orders will look like CNY amounts to them until v2 ships.