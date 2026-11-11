`Order` now has a `currency` field that defaults to `"CNY"`, so existing callers keep working. pytest isn't installed here, so I didn't run the test suite. I only ran a manual check that the default is CNY, the webhook payload is unchanged and the cache schema is 4.

- **Model:** `currency` is in `orders/models.py`, with the default taken from `BASE_CURRENCY` in `orders/settings.py`.
- **Cache:** I bumped `CACHE_SCHEMA` from 3 to 4 in `orders/cache.py`, as its comment requires. Without that, workers would unpickle old Orders that lack the field, which is what caused the 2026-08-14 incident.
- **Webhook:** `order_created_payload` removes `currency` before sending. Acme's v1 schema rejects unknown fields and drops the delivery, and a new field needs a v2 schema plus 30 days' notice (`docs/partners.md`). So partners don't see the currency yet.
- **Migration:** `migrations/0007_orders_currency.sql` adds a nullable `currency` column with no default. A NOT NULL default would rewrite the 40M-row table on Postgres 10 and lock it (`docs/runbook.md`). The backfill and the NOT NULL constraint are still to do, as separate steps.
- **Tests:** I added two tests, one for the default and one that `currency` stays out of the payload.

**Before taking EUR orders:**
1. `daily_revenue` in `orders/report.py` adds up `amount_cents` across all orders. Once EUR orders exist, it will add EUR cents to CNY fen and give a wrong total. It needs a decision from you: report per currency, convert, or filter to CNY. I left it unchanged.
2. Acme needs the v2 schema and 30 days' notice before `currency` can go in the webhook.
3. The backfill and the NOT NULL constraint on the new column still need doing.

I haven't committed anything.