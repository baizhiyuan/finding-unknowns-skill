`Order` now has a `currency` field that defaults to `"CNY"`, but you can't safely take EUR orders yet. Two things are still open: what Acme gets for EUR orders, and how `daily_revenue` handles mixed currencies. The tests I ran pass (`test_currency_defaults_to_base`, `test_daily_revenue`, `test_payload_has_fields`, `test_webhook_v1_payload_excludes_currency`). pytest isn't installed here, so I called the test functions directly. Nothing is committed.

**What I changed**
- **Model:** `orders/models.py` adds `currency: str = BASE_CURRENCY`. Existing constructors keep working.
- **Cache:** `orders/cache.py` bumps `CACHE_SCHEMA` from 3 to 4. Its comment says a stale pickle crashed every worker in incident 2026-08-14.
- **Webhook:** `orders/webhook.py` removes `currency` from the payload. Acme's strict v1 schema would otherwise reject the delivery and drop it. A new field needs a v2 schema and 30 days' notice to Acme.
- **Migration:** `migrations/0007_orders_currency.sql` adds a nullable `currency` column with no default. I haven't run it. The runbook says a `NOT NULL DEFAULT` rewrites the 40M-row table on Postgres 10, which caused 47 minutes of failed checkouts last time.
- **Tests:** two new tests cover the default and the missing `currency` in the v1 payload.

**Decisions for you**
1. **Acme and EUR orders:** the v1 payload sends `amount_cents` with no currency. Acme will read a EUR order as CNY. Do you want to send them a v2 schema and start the 30-day notice? Until then, should EUR orders be left out of the `order.created` webhook?
2. **`daily_revenue`:** it adds all `amount_cents` together, so EUR and CNY would be summed as if they were the same unit. I left it alone because the fix depends on what finance wants. Options are grouping by currency, converting to CNY, or raising an error on mixed currencies. Which one?
3. **Rollout:** someone needs to run `0007`, then backfill `'CNY'` in batches of 10k, then add the constraint. I haven't written the backfill or run any of it. I'd keep EUR orders off until the backfill is done. Do you want me to write the backfill script?

I can't find where the repo writes orders to the database, since there's no ORM or insert code. Whatever does needs to start writing `currency` too.