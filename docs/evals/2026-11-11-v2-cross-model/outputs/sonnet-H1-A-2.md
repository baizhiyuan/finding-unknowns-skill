I added `currency` to `Order`. pytest isn't installed here, so I called the four test functions directly and they all passed. The changes aren't committed.

- **Model:** `Order.currency: str = BASE_CURRENCY`, so it defaults to `"CNY"` and existing call sites still work.
- **Cache:** I bumped `CACHE_SCHEMA` from 3 to 4, as the comment in `cache.py` requires. Without the bump, workers would unpickle old Orders that have no `currency`.
- **Webhook:** `currency` is left out of the `order.created` payload. Acme's v1 schema rejects unknown fields and drops the delivery, and `asdict` would have added the field automatically. Sending it needs a v2 schema and 30 days' notice to Acme (`docs/partners.md`). The EUR orders won't carry their currency to Acme until then.
- **Migration:** `migrations/0007_orders_currency.sql` adds a nullable `currency text` column with no default. A NOT NULL default would lock the 40M-row table on Postgres 10 (`docs/runbook.md`).
- **Tests:** I added two, one for the default and one that checks the payload omits `currency`.

Still to do before EUR orders go live:
1. **Backfill and constraint:** Backfill existing rows to `'CNY'` in batches of 10k, then add the NOT NULL constraint. I didn't write that.
2. **`daily_revenue`:** It sums `amount_cents` across all orders, so EUR cents would be added to CNY fen and the finance number would be wrong. I left it alone because the fix is a finance decision: filter to CNY, group by currency, or convert.
3. **Acme:** Start the v2 schema and notice process if they need to receive currency.